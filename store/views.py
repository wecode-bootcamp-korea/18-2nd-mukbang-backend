import json
import geopy
import geopy.distance
from haversine import haversine
from json      import JSONDecodeError

from django.views           import View
from django.http            import JsonResponse
from django.db              import transaction
from django.db.utils        import DataError
from django.db.models       import Q, Avg, Count
from django.core.exceptions import ValidationError

from .models import (
                     Category, Store, StoreImage,
                     Address, Menu, MetroStation,
                     MetroStationStore, OpenStatus
                )
from user.models import Review

from utils.decorators import auth_check


DPI  = 200
INCH = 2.56

SCALE_LEVEL = {
                '1' : 20,
                '2' : 30,
                '3' : 50,
                '4' : 100,
                '5' : 250,
                '6' : 500,
                '7' : 1000,
                '8' : 2000,
                '9' : 4000,
                '10': 8000
            }


class ReviewDetail:
    @classmethod
    def get_review_ratings_avg(cls, store_obj):
        return store_obj.review_set.all().aggregate(Avg('rating')).get('rating__avg')
    
    @classmethod
    def get_review_count(cls, store_obj):
        return len(store_obj.review_set.all())


class StoreView(View):
    def get(self, request):
        """
        lng            : longitude
        lat            : latitude
        scale_level    : scale level
        pixel_width    : monitor width pixel
        pixel_height   : monitor width height
        category_filter: list of categories
        price_range    : [min_price, max_price]
        offset         : page number
        limit          : max elements
        """
        try:
            lng = float(request.GET['lng'])
            lat = float(request.GET['lat'])

            map_scale_level = request.GET['scale_level']
            map_scale_m     = SCALE_LEVEL.get(map_scale_level)

            if not map_scale_m:
                return JsonResponse({'message': 'SCALE_LEVEL_OUT_OF_RANGE'}, status=404)

            pixel_width  = float(request.GET['pixel_width'])
            pixel_height = float(request.GET['pixel_height'])

            lng_range, lat_range = self.get_boundary_range(lng, lat, map_scale_m, pixel_width, pixel_height)

            lng_min, lng_max = lng_range
            lat_min, lat_max = lat_range

            addresses_in_range_qs = Address.objects.filter(
                                                        Q(longitude__gte=lng_min) & Q(longitude__lte=lng_max)
                                                        & Q(latitude__gte=lat_min) & Q(latitude__lte=lat_max)
                                                    )

            store_ids = [address.store.id for address in addresses_in_range_qs]
            stores_qs = Store.objects.filter(id__in=store_ids)

            category_filter        = request.GET.getlist('category')
            price_range_filter     = request.GET.getlist('price_range')
            review_category_filter = request.GET.get('review_category')
            reverse                = request.GET.get('reverse')

            # 업종으로 필터링
            if category_filter:
                stores_qs = stores_qs.exclude(~Q(category__name__in=category_filter))

            # 가격범위로 필터링
            if price_range_filter:
                min_price, max_price = float(price_range_filter[0]), float(price_range_filter[1])

                stores_qs = stores_qs.exclude(~(Q(menu__price__gte=min_price) & Q(menu__price__lte=max_price)))

            # 리뷰평점으로 필터링
            if review_category_filter == 'rating_average':
                if reverse == '0':
                    stores_qs = stores_qs.annotate(rating_avg=Avg('review__rating')).order_by('-rating_avg')
                else:
                    stores_qs = stores_qs.annotate(rating_avg=Avg('review__rating')).order_by('rating_avg')

            # 리뷰건수로 필터링
            if review_category_filter == 'review_count':
                if reverse == '0':
                    stores_qs = stores_qs.annotate(review_count=Count('review__id')).order_by('-review_count')
                else:
                    stores_qs = stores_qs.annotate(review_count=Count('review__id')).order_by('review_count')

            offset = request.GET.get('offset')
            limit  = request.GET.get('limit')
            
            if limit == 0:
                return JsonResponse({'message': 'LIMIT_SHOULD_NOT_BE_ZERO'}, status=400)

            if offset and limit:
                offset = int(offset)
                limit  = int(limit)

                stores_qs = stores_qs[offset * limit:(offset + 1) * limit]\
                            .select_related('address', 'category', 'open_status')\
                            .prefetch_related('storeimage_set', 'review_set')
            else:
                stores_qs = stores_qs.select_related('address', 'category', 'open_status')\
                                     .prefetch_related('storeimage_set', 'review_set')

            results = [
                {   
                    'store_id'                : store.id,
                    'lat'                     : store.address.latitude,
                    'lng'                     : store.address.longitude,
                    'full_address'            : store.address.full_address,
                    'store_name'              : store.name,
                    'one_line_introduction'   : store.one_line_introduction,
                    'opening_time_description': store.opening_time_description,
                    'category'                : store.category.name,
                    'open_status'             : store.open_status.name,
                    'sns_url'                 : store.sns_url,
                    'store_images'            : [store_image.image_url for store_image in store.storeimage_set.all()],
                    'rating_average'          : ReviewDetail.get_review_ratings_avg(store),
                    'review_count'            : ReviewDetail.get_review_count(store)
                } for store in stores_qs
            ]

            return JsonResponse({'results': results}, status=200)

        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    def get_boundary_range(self, lng, lat, map_scale_m, pixel_width, pixel_height):
        width_cm  = pixel_width * INCH / DPI
        height_cm = pixel_height * INCH / DPI

        width_m  = width_cm * map_scale_m
        height_m = height_cm * map_scale_m

        start_point = geopy.Point(lat, lng)

        d_lng = geopy.distance.distance(meters=width_m / 2)
        d_lat = geopy.distance.distance(meters=height_m / 2)

        lng_range = (
                     d_lng.destination(point=start_point, bearing=270).longitude,
                     d_lng.destination(point=start_point, bearing=90).longitude
                )

        lat_range = (
                     d_lat.destination(point=start_point, bearing=180).latitude,
                     d_lat.destination(point=start_point, bearing=0).latitude
                )

        return lng_range, lat_range

    @transaction.atomic
    def post(self, request):
        try:
            data = json.loads(request.body)['data']

            category_name = data['category']
            category      = Category.objects.filter(name=category_name).first()
            if not category:
                return JsonResponse({'message': 'WRONG_CATEGORY'}, status=400)

            open_status_name = data['open_status']
            open_status      = OpenStatus.objects.filter(name=open_status_name).first()
            if not open_status:                
                return JsonResponse({'message': 'WRONG_OPEN_STATUS'}, status=400)
                
            store_name               = data['store_name']
            one_line_introduction    = data.get('one_line_introduction')
            opening_time_description = data.get('opening_time_description')
            phone_number             = data.get('phone_number')
            sns_url                  = data.get('sns_url')
            menu_pamphlet_image_url  = data.get('menu_pamphelt_image_url')
            is_reservation           = data['is_reservation']
            is_wifi                  = data['is_wifi']
            is_parking               = data['is_parking']

            store = Store.objects.create(
                                        name                     = store_name,
                                        one_line_introduction    = one_line_introduction,
                                        opening_time_description = opening_time_description,
                                        phone_number             = phone_number,
                                        sns_url                  = sns_url,
                                        menu_pamphlet_image_url  = menu_pamphlet_image_url,
                                        is_reservation           = is_reservation,
                                        is_wifi                  = is_wifi,
                                        is_parking               = is_parking,
                                        category                 = category,
                                        open_status              = open_status
                                    )

            store_image_urls = data['store_image_urls']
            for store_image_url in store_image_urls:
                StoreImage.objects.create(store=store, image_url=store_image_url)

            address = data['road_address']

            latitude           = address['y']
            longitude          = address['x']
            full_address       = address['address_name']
            region_1depth_name = address['region_1depth_name']
            region_2depth_name = address['region_2depth_name']
            region_3depth_name = address['region_3depth_name']
            road_name          = address['road_name']
            building_name      = address['building_name']

            if Address.objects.filter(full_address=full_address, store__name=store_name).exists():
                transaction.set_rollback(True)
                return JsonResponse({'message': 'DUPLICATE_STORE_NAME_AT_THE_SAME_LOCATION'}, status=400)

            Address.objects.create(
                                latitude           = latitude,
                                longitude          = longitude,
                                full_address       = full_address,
                                region_1depth_name = region_1depth_name,
                                region_2depth_name = region_2depth_name,
                                region_3depth_name = region_3depth_name,
                                road_name          = road_name,
                                building_name      = building_name,
                                store              = store
                                )
            
            menus = data['menus']
            for menu in menus:    
                menu_name      = menu['name']
                menu_price     = menu['price']
                menu_image_url = menu['image_url']

                Menu.objects.create(
                                    name           = menu_name,
                                    price          = menu_price,
                                    menu_image_url = menu_image_url,
                                    store          = store
                                    )

            metros = data['metros']
            for metro in metros: 
                metro_station_name      = metro['name']
                metro_station_line      = metro['line']
                metro_station_latitude  = metro['y']
                metro_station_longitude = metro['x']

                metro_station, _ = MetroStation.objects.get_or_create(
                                                                    name=metro_station_name,
                                                                    line=metro_station_line,
                                                                    defaults={
                                                                    'latitude':metro_station_latitude,
                                                                    'longitude':metro_station_longitude
                                                                    }
                                                                )       
                MetroStationStore.objects.create(store=store, metro_station=metro_station)
                return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            transaction.set_rollback(True)
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            transaction.set_rollback(True)
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except ValidationError:
            transaction.set_rollback(True)
            return JsonResponse({'message': 'DATA_VALIDATION_ERROR'}, status=400)
        except DataError:
            transaction.set_rollback(True)
            return JsonResponse({'message': 'DATA_ERROR'}, status=400)


class StoreDetailView(View):
    def get(self, request):
        try:
            store = Store.objects.select_related('category', 'address', 'open_status').\
                                  prefetch_related('menu_set', 'storeimage_set', 'metrostationstore_set', 'review_set').\
                                  get(id=request.GET['store_id'])

            review_ratings_avg = ReviewDetail.get_review_ratings_avg(store)
            review_count       = ReviewDetail.get_review_count(store)

            result = {
                    'region_1depth_name'      : store.address.region_1depth_name,
                    'region_2depth_name'      : store.address.region_2depth_name,
                    'region_3depth_name'      : store.address.region_3depth_name,
                    'store_id'                : store.id,
                    'lat'                     : store.address.latitude,
                    'lng'                     : store.address.longitude,
                    'full_address'            : store.address.full_address,
                    'store_name'              : store.name,
                    'one_line_introduction'   : store.one_line_introduction,
                    'opening_time_description': store.opening_time_description,
                    'phone_number'            : store.phone_number,
                    'sns_url'                 : store.sns_url,
                    'menu_pamphlet_image_url' : store.menu_pamphlet_image_url,
                    'is_reservation'          : 1 if store.is_reservation else 0,
                    'is_wifi'                 : 1 if store.is_wifi else 0,
                    'is_parking'              : 1 if store.is_parking else 0,
                    'category'                : store.category.name,
                    'open_status'             : store.open_status.name,
                    'menus'                   : [
                                                    {
                                                    'name'          : menu.name,
                                                    'price'         : menu.price,
                                                    'menu_image_url': menu.menu_image_url
                                                    } for menu in store.menu_set.all()
                                            ],
                    'store_images'  : [store_image.image_url for store_image in store.storeimage_set.all()],
                    'metro_stations': [
                                        {
                                        'name'                 : metro_station_store.metro_station.name,
                                        'line'                 : metro_station_store.metro_station.line,
                                        'lat'                  : metro_station_store.metro_station.latitude,
                                        'lng'                  : metro_station_store.metro_station.longitude,
                                        'distance_from_store_m': haversine(
                                            (store.address.longitude, store.address.latitude),
                                            (metro_station_store.metro_station.longitude, metro_station_store.metro_station.latitude),
                                            unit = 'm'
                                            )
                                        } for metro_station_store in store.metrostationstore_set.all()
                                    ],
                    'reviews': [
                                {
                                'review_id' : review.id,
                                'rating'    : review.rating,
                                'content'   : review.content,
                                'image_url' : review.image_url,
                                'updated_at': review.updated_at
                                }
                        for review in store.review_set.all()
                            ],
                    'visitor_photos': [review.image_url for review in store.review_set.all()],
                    'rating_average': review_ratings_avg,
                    'review_count'  : review_count
                    }
                    
            return JsonResponse({'result': result}, status=200)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Store.DoesNotExist:
            return JsonResponse({'message': 'STORE_DOES_NOT_EXIST'}, status=404)


class ReviewRegisterView(View):
    @auth_check
    def post(self, request, store_id):
        try:
            data = json.loads(request.body)
            
            rating    = str(data['rating'])
            content   = data['content']
            image_url = data.get('image_url')

            if not Store.objects.filter(id=store_id).exists():
                return JsonResponse({'message': 'STORE_DOES_NOT_EXIST'})

            Review.objects.create(
                                 rating    = rating,
                                 content   = content,
                                 image_url = image_url,
                                 store_id  = store_id,
                                 user      = request.user
                                )
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
    

class ReviewModifyView(View):
    @auth_check
    def delete(self, request, store_id, review_id):
        try:
            if not Store.objects.filter(id=store_id).exists():
                return JsonResponse({'message': 'STORE_DOES_NOT_EXIST'})

            review = Review.objects.filter(id=review_id)
            if not review:
                return JsonResponse({'message': 'REVIEW_DOES_NOT_EXIST'}, status=404)

            review = review.filter(user=request.user)
            if not review:
                return JsonResponse({'message': 'PERMISSION_ERROR'}, status=403)
            
            review.delete()
            return JsonResponse({'message': 'SUCCESS'}, status=203)
        
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)  

            
class StoreSearchView(View):
    def get(self, request):
        keyword = request.GET.get('q')
        if not keyword:
            return JsonResponse({'message': 'NO_KEYWORD'}, status=400)

        stores_qs = Store.objects.filter(
                                        Q(name__contains=keyword) |
                                        Q(address__full_address__contains=keyword) |
                                        Q(metrostation__name__contains=keyword) |
                                        Q(category__name__contains=keyword)
                                        ).distinct()
        
        if not stores_qs:
            return JsonResponse({'message': 'RESULT_NOT_FOUND'}, status=404) 

        stores_qs = stores_qs.select_related('address', 'category').prefetch_related('metrostation_set')

        results = [
                    {   
                    'store_id'    : store.id,
                    'lat'         : store.address.latitude,
                    'lng'         : store.address.longitude,
                    'full_address': store.address.full_address,
                    'store_name'  : store.name,
                    'category'    : store.category.name,
                    'near_metro_stations': [metro_station.name for metro_station in store.metrostation_set.all()]
                    } for store in stores_qs
                ]

        return JsonResponse({'results': results}, status=200)
