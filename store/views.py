import json
from json import JSONDecodeError
from enum import Enum

from django.views           import View
from django.http            import JsonResponse
from django.db              import transaction
from django.db.utils        import DataError
from django.core.exceptions import ValidationError

from .models import (
                     Category, Store, StoreImage,
                     Address, Menu, MetroStation,
                     MetroStationStore, OpenStatus
                )


class StoreView(View):
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

            latitude           = address['lat']
            longitude          = address['lon']
            full_address       = address['address_name']
            region_1depth_name = address['region_1depth_name']
            region_2depth_name = address['region_2depth_name']
            region_3depth_name = address['region_3depth_name']
            road_name          = address['road_name']
            building_name      = address['building_name']

            if Address.objects.filter(full_address=full_address).filter(store__name=store_name).exists():
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
                metro_station_latitude  = metro['lat']
                metro_station_longitude = metro['lon']

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
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except ValidationError:
            return JsonResponse({'message': 'DATA_VALIDATION_ERROR'})
        except DataError:
            return JsonResponse({'message': 'DATA_ERROR'})
