import json
import requests
import copy
import jwt

from django.test         import TestCase
from django.test         import Client
from rest_framework.test import APIClient
from django.http         import JsonResponse

from unittest.mock import patch, MagicMock, Mock

from .views import StoreView, StoreDetailView, ReviewDetail

from .models import (
                    Category, OpenStatus, Store,
                    Address, Menu, StoreImage,
                    MetroStation, MetroStationStore
                )
from user.models import User, Review

from mukbang.settings import SECRET_KEY, HASHING_ALGORITHM


TEST_DATA = {
    "data": {
        "category"                : "한식",
        "open_status"             : "오픈중",
        "store_name"              : "순남시래기",
        "one_line_introduction"   : "시래기와 막걸리가 맛있는 집!",
        "opening_time_description": "평일 09시 ~ 23시",
        "phone_number"            : "02-427-6626",
        "sns_url"                 : "https://www.instagram.com/soonnamsiraegi/",
        "menu_pamphlet_image_url" : "https://lh3.googleusercontent.com/proxy/2NvNh52wTbVf8_UATpmEQDlFZde5-eZbAySa0wxtdYYcmsUOk8_ALYk9SG0qX53FS-UfAvwW4K6h10dSlKzZ9gwmUZtI6ibteiwyHwvtUFd0fqv9npxfi2NIuI6PBJIUlHatKGu1PXahEV-zOIdRXJ65ibOyjlp5n1QCN3PraoZP9dg9bL5jAnvLdkejopLoz9f0aBMDSryzh8mo3VZ8EWLL-l2f_3K8WUVuONVRlieBfpUqbtRCxk3Cdk7hg8ZOlqu757LAjpoQpJ8x_ZDUR3bCM7WJykv-X3P0fMsSyHTzDjDg3WvlDBiWofrVy7I8HPDPhg",
        "is_reservation"          : 1,
        "is_wifi"                 : 1,
        "is_parking"              : 1,
        "store_image_urls"        : [
            "https://steemitimages.com/DQmf9fgCzGWsqj1gcoP9Z8YDCKykDGi1KRdanrZAdQtFLVE/20180221_190332.jpg",
            "https://s3-ap-northeast-1.amazonaws.com/dcreviewsresized/20200712094922_photo1_68d1c5bf458f.jpg",
            "https://s3-ap-northeast-1.amazonaws.com/dcreviewsresized/20200712094922_photo3_68d1c5bf458f.jpg"
        ],
        "road_address": {
            "address_name"      : "서울 강남구 강남대로66길 16",
            "building_name"     : "",
            "region_1depth_name": "서울",
            "region_2depth_name": "강남구",
            "region_3depth_name": "역삼동",
            "road_name"         : "강남대로66길",
            "x"               : "127.032166561787",
            "y"               : "37.4918939171295"
        },
        "menus": [
            {
                "name"     : "시래기 국밥",
                "price"    : 8000,
                "image_url": "https://s3-ap-northeast-1.amazonaws.com/dcreviewsresized/20200206030137603_photo_EnjdtHHZ6jYx.jpg"
            },
            {
                "name"     : "수육",
                "price"    : 13000,
                "image_url": "https://d2t7cq5f1ua57i.cloudfront.net/images/r_images/54372/58486/54372_58486_89_0_9602_2016112213118580.jpg"
            }
        ],
        "metros": [
            {
                "name": "선릉역",
                "line": "2호선",
                "x"   : "127.032166561787",
                "y"   : "37.4918939171295"
            },
            {
                "name": "선릉역",
                "line": "수인분당선",
                "x"   : "127.04870879368039",
                "y"   : "37.50516782598803"
            }
        ]
    }
}


class StoreRegistryTest(TestCase):
    def setUp(self):
        Category.objects.bulk_create(
                                [
                                Category(name='한식'),
                                Category(name='퓨전'),
                                Category(name='패스트푸드'),
                                Category(name='카페'),
                                Category(name='치킨'),
                                Category(name='중식'),
                                Category(name='주점'),
                                Category(name='일식'),
                                Category(name='양식'),
                                Category(name='분식'),
                                Category(name='베이커리')
                                ]
                            )

        OpenStatus.objects.bulk_create(
                                [
                                OpenStatus(name='영업종료'),
                                OpenStatus(name='오픈중'),
                                OpenStatus(name='브레이크타임')
                                ]
                            )

    def test_store_post_success(self):
        client   = Client()
        response = client.post('/store', json.dumps(TEST_DATA), content_type='application/json').json()
        
        self.assertEqual(response.get('message'), 'SUCCESS')

    def test_store_post_fail_with_wrong_category(self):
        TEMP_TEST_DATA = copy.deepcopy(TEST_DATA)
        TEMP_TEST_DATA['data']['category'] = 'wrong_category'

        client = Client()
        response = client.post('/store', json.dumps(TEMP_TEST_DATA), content_type='application/json').json()
        
        self.assertEqual(response.get('message'), 'WRONG_CATEGORY')

    def test_store_post_fail_with_wrong_open_status(self):
        TEMP_TEST_DATA = copy.deepcopy(TEST_DATA)
        TEMP_TEST_DATA['data']['open_status'] = 'wrong_open_status'

        client = Client()
        response = client.post('/store', json.dumps(TEMP_TEST_DATA), content_type='application/json').json()
        
        self.assertEqual(response.get('message'), 'WRONG_OPEN_STATUS')

    def test_store_post_fail_with_long_data(self):
        TEMP_TEST_DATA = copy.deepcopy(TEST_DATA)
        TEMP_TEST_DATA['data']['store_name'] = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

        client = Client()
        response = client.post('/store', json.dumps(TEMP_TEST_DATA), content_type='application/json').json()

        self.assertEqual(response.get('message'), 'DATA_ERROR')
    
    def test_store_post_fail_with_wrong_data_format(self):
        TEMP_TEST_DATA = copy.deepcopy(TEST_DATA)
        TEMP_TEST_DATA['data']['is_reservation'] = 'wrong_data_format'

        client = Client()
        response = client.post('/store', json.dumps(TEMP_TEST_DATA), content_type='application/json').json()

        self.assertEqual(response.get('message'), 'DATA_VALIDATION_ERROR')
    
    def test_store_post_fail_with_wrong_key(self):
        TEMP_TEST_DATA = copy.deepcopy(TEST_DATA)
        del TEMP_TEST_DATA['data']['store_name']

        client = Client()
        response = client.post('/store', json.dumps(TEMP_TEST_DATA), content_type='application/json').json()

        self.assertEqual(response.get('message'), 'KEY_ERROR')
    
    def test_store_post_fail_with_wrong_json_format(self):
        client = Client()
        response = client.post('/store', TEST_DATA).json()

        self.assertEqual(response.get('message'), 'JSON_DECODE_ERROR')

    
class StoreRegistryDuplicateTest(TestCase):
    def setUp(self):
        Category.objects.bulk_create(
                                [
                                Category(name='한식'),
                                Category(name='퓨전'),
                                Category(name='패스트푸드'),
                                Category(name='카페'),
                                Category(name='치킨'),
                                Category(name='중식'),
                                Category(name='주점'),
                                Category(name='일식'),
                                Category(name='양식'),
                                Category(name='분식'),
                                Category(name='베이커리')
                                ]
                            )

        OpenStatus.objects.bulk_create(
                                [
                                OpenStatus(name='영업종료'),
                                OpenStatus(name='오픈중'),
                                OpenStatus(name='브레이크타임')
                                ]
                            )
        
        client = Client()
        response = client.post('/store', json.dumps(TEST_DATA), content_type='application/json').json()

    def test_store_post_fail_with_duplicate_data(self):
        client   = Client()
        response = client.post('/store', json.dumps(TEST_DATA), content_type='application/json').json()

        self.assertEqual(response.get('message'), 'DUPLICATE_STORE_NAME_AT_THE_SAME_LOCATION')


class StoreBasicTest(TestCase):
    __test__ = False

    def setUp(self):
        category    = Category.objects.create(name='한식')
        open_status = OpenStatus.objects.create(name='오픈중')
        
        store = Store.objects.create(
                                        id                       = 1,
                                        name                     = '순남시래기',
                                        one_line_introduction    = 'The best siraegi you are going to taste',
                                        opening_time_description = '매일 09 - 22',
                                        phone_number             = '010-1234-5678',
                                        sns_url                  = 'instagram.com/siraegi',
                                        menu_pamphlet_image_url  = 'test_pamphlet_image_url',
                                        is_reservation           = 1,
                                        is_wifi                  = 1,
                                        is_parking               = 1,
                                        category                 = category,
                                        open_status              = open_status
                                    )

        StoreImage.objects.create(store=store, image_url='test_store_image_url')

        Address.objects.create(
                                latitude           = 37.4918939171295,
                                longitude          = 127.032166561787,
                                full_address       = '서울 강남구 강남대로66길 16',
                                region_1depth_name = '서울',
                                region_2depth_name = '강남구',
                                region_3depth_name = '역삼동',
                                road_name          = '강남대로66길',
                                building_name      = '',
                                store              = store
                                )

        Menu.objects.create(
                            name           = '시래기 국밥',
                            price          = 8000,
                            menu_image_url = 'test_menu_image_url',
                            store          = store
                        )

        metro_station = MetroStation.objects.create(
                                                    name='사당역',
                                                    line='2',
                                                    latitude=37.5045,
                                                    longitude=127.049
                                                )

        MetroStationStore.objects.create(store=store, metro_station=metro_station)

        user = User.objects.create(kakao_id='123456')

        Review.objects.create(rating=4, content='맛있어요', user=user, store=store, image_url='test_image_url')
        Review.objects.create(rating=5, content='맛있어요', user=user, store=store, image_url='test_image_url')


class StoreShowTest(StoreBasicTest):
    def setUp(self):
        super(StoreShowTest, self).setUp()    

    def test_store_get_without_pagination_success(self):
        client = Client()
        params = {
            'lat'         : 37.491893917128,
            'lng'         : 127.032166561787,
            'scale_level' : 2,
            'pixel_width' : 300,
            'pixel_height': 300,
        }

        response   = client.get('/store', params).json()
        store_name = response['results'][0]['store_name']

        self.assertEqual(store_name, '순남시래기')

    def test_store_get_with_pagination_success(self):
        client = Client()
        params = {
            'lat'         : 37.491893917128,
            'lng'         : 127.032166561787,
            'scale_level' : 2,
            'pixel_width' : 300,
            'pixel_height': 300,
            'offset'      : 0,
            'limit'       : 1
        }

        response = client.get('/store', params).json()
        store_name = response['results'][0]['store_name']

        self.assertEqual(store_name, '순남시래기')
    
    def test_store_get_category_filter_success(self):
        client = Client()
        params = {
                'lat'         : 37.491893917128,
                'lng'         : 127.032166561787,
                'scale_level' : 2,
                'pixel_width' : 300,
                'pixel_height': 300,
                'offset'      : 0,
                'limit'       : 1,
                'category'    : ['한식', '중식']
            }
        
        response = client.get('/store', params).json()
        store_name = response['results'][0]['store_name']

        self.assertEqual(store_name, '순남시래기')
    
    def test_store_get_category_filter_not_found(self):
        client = Client()
        params = {
                'lat'         : 37.491893917128,
                'lng'         : 127.032166561787,
                'scale_level' : 2,
                'pixel_width' : 300,
                'pixel_height': 300,
                'offset'      : 0,
                'limit'       : 1,
                'category'    : ['중식']
            }
        
        response = client.get('/store', params).json()

        self.assertEqual(response.get('results'), [])
    
    def test_store_get_price_range_filter_success(self):
        client = Client()
        params = {
                'lat'         : 37.491893917128,
                'lng'         : 127.032166561787,
                'scale_level' : 2,
                'pixel_width' : 300,
                'pixel_height': 300,
                'offset'      : 0,
                'limit'       : 1,
                'price_range' : [5000, 10000]
            }
        
        response = client.get('/store', params).json()
        store_name = response['results'][0]['store_name']

        self.assertEqual(store_name, '순남시래기')
    
    def test_store_get_price_range_filter_not_found(self):
        client = Client()
        params = {
                'lat'         : 37.491893917128,
                'lng'         : 127.032166561787,
                'scale_level' : 2,
                'pixel_width' : 300,
                'pixel_height': 300,
                'offset'      : 0,
                'limit'       : 1,
                'price_range' : [9000, 10000]
            }
        
        response = client.get('/store', params).json()

        self.assertEqual(response.get('results'), [])
    
    def test_store_get_rating_avg_filter_with_reverse_success(self):
        client = Client()

        TEMP_TEST_DATA = copy.deepcopy(TEST_DATA)
        TEMP_TEST_DATA['data']['store_name'] = '담소사골국밥'

        client.post('/store', json.dumps(TEMP_TEST_DATA), content_type='application/json')
        
        params = {
                'lat'            : 37.491893917128,
                'lng'            : 127.032166561787,
                'scale_level'    : 2,
                'pixel_width'    : 300,
                'pixel_height'   : 300,
                'offset'         : 0,
                'limit'          : 2,
                'price_range'    : [2000, 10000],
                'review_category': 'rating_average',
                'reverse'        : 1
            }

        response = client.get('/store', params).json()
        
        first_store_name = response['results'][0]['store_name']

        self.assertEqual(first_store_name, '담소사골국밥')

    def test_store_get_review_count_filter_without_reverse_success(self):
        client = Client()

        TEMP_TEST_DATA = copy.deepcopy(TEST_DATA)
        TEMP_TEST_DATA['data']['store_name'] = '담소사골국밥'

        client.post('/store', json.dumps(TEMP_TEST_DATA), content_type='application/json')
        
        params = {
                'lat'            : 37.491893917128,
                'lng'            : 127.032166561787,
                'scale_level'    : 2,
                'pixel_width'    : 300,
                'pixel_height'   : 300,
                'offset'         : 0,
                'limit'          : 2,
                'price_range'    : [2000, 10000],
                'review_category': 'review_count',
                'reverse'        : 0
            }

        response = client.get('/store', params).json()
        
        first_store_name = response['results'][0]['store_name']

        self.assertEqual(first_store_name, '순남시래기')

    def test_store_get_fail_with_wrong_lat_lng(self):
        client = Client()
        params = {
                 'lat'         : 127.032166561787,
                 'lng'         : 37.491893917128,
                 'scale_level' : 2,
                 'pixel_width' : 300,
                 'pixel_height': 300,
               }
        
        response = client.get('/store', params).json()
        self.assertEqual(response.get('message'), 'VALUE_ERROR')

    def test_store_get_fail_with_key_error(self):
        client = Client()
        params = {
                 'lattt'         : 127.032166561787,
                 'lonnn'         : 37.491893917128,
                 'scale_level' : 2,
                 'pixel_width' : 300,
                 'pixel_height': 300,
               }

        response = client.get('/store', params).json()
        self.assertEqual(response.get('message'), 'KEY_ERROR')
    

class StoreDetailShowTest(StoreBasicTest):
    def setUp(self):
        super(StoreDetailShowTest, self).setUp()
    
    def test_store_detail_get_success(self):
        client = Client()
        params = {
            'store_id': 1
        }

        response = client.get('/store/detail', params).json()
        store_name = response['result']['store_name']

        self.assertEqual(store_name, '순남시래기')
    
    def test_store_review_ratings_avg_get_success(self):
        store              = Store.objects.get(id=1)
        review_ratings_avg = ReviewDetail.get_review_ratings_avg(store)

        self.assertEqual(review_ratings_avg, 4.5)
    
    def test_store_review_count_get_success(self):
        store        = Store.objects.get(id=1)
        review_count = ReviewDetail.get_review_count(store)

        self.assertEqual(review_count, 2)

    def test_store_detail_get_fail_with_key_error(self):
        client = Client()
        params = {
            'store_idddddd': 1
        }

        response = client.get('/store/detail', params).json()

        self.assertEqual(response.get('message'), 'KEY_ERROR')
    
    def test_store_detail_get_fail_with_store_not_found(self):
        Store.objects.filter(id=1).delete()

        client = Client()
        params = {
            'store_id': 1
        }

        response = client.get('/store/detail', params).json()

        self.assertEqual(response.get('message'), 'STORE_DOES_NOT_EXIST')


class ReviewRegisterTest(TestCase):
    def setUp(self):
        Category.objects.bulk_create(
                                [
                                Category(name='한식'),
                                Category(name='퓨전'),
                                Category(name='패스트푸드'),
                                Category(name='카페'),
                                Category(name='치킨'),
                                Category(name='중식'),
                                Category(name='주점'),
                                Category(name='일식'),
                                Category(name='양식'),
                                Category(name='분식'),
                                Category(name='베이커리')
                                ]
                            )

        OpenStatus.objects.bulk_create(
                                [
                                OpenStatus(name='영업종료'),
                                OpenStatus(name='오픈중'),
                                OpenStatus(name='브레이크타임')
                                ]
                            )
        
        client = Client()
        response = client.post('/store', json.dumps(TEST_DATA), content_type='application/json').json()

        user           = User.objects.create(kakao_id='test_kakao_id')
        self.jwt_token = jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm=HASHING_ALGORITHM)

    def test_review_register_success(self):
        client = APIClient()

        store_id = Store.objects.all().first().id
        user_id  = User.objects.all().first().id

        review_content = {
                        'rating'   : '4.5',
                        'content'  : 'good',
                        'image_url': 'test_image_url'
                    }

        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)
        response = client.post('/store/{}/review'.format(store_id), json.dumps(review_content), content_type='application/json')
        
        self.assertEqual(response.json().get('message'), 'SUCCESS')
    
    def test_review_register_fail_with_decode_error(self):
        client = APIClient()

        store_id = Store.objects.all().first().id
        user_id  = User.objects.all().first().id

        review_content = {
                        'rating'   : '4.5',
                        'content'  : 'good',
                        'image_url': 'test_image_url'
                    }

        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)
        response = client.post('/store/{}/review'.format(store_id), review_content, content_type='application/json')
        
        self.assertEqual(response.json().get('message'), 'JSON_DECODE_ERROR')
    
    def test_review_register_fail_with_key_error(self):
        client = APIClient()

        store_id = Store.objects.all().first().id
        user_id  = User.objects.all().first().id

        review_content = {
                        'ratinasdfasdfg'  : '4.5',
                        'contenasdfsadt'  : 'good',
                        'image_urasfsdafl': 'test_image_url'
                    }

        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)
        response = client.post('/store/{}/review'.format(store_id), json.dumps(review_content), content_type='application/json')
        
        self.assertEqual(response.json().get('message'), 'KEY_ERROR')

    def test_review_register_fail_with_store_not_found(self):
        client = APIClient()

        store_id = Store.objects.all().first().id
        user_id  = User.objects.all().first().id

        review_content = {
                        'rating'   : '4.5',
                        'content'  : 'good',
                        'image_url': 'test_image_url'
                    }

        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)
        response = client.post('/store/1000000/review', json.dumps(review_content), content_type='application/json')
        
        self.assertEqual(response.json().get('message'), 'STORE_DOES_NOT_EXIST')
    

class ReviewModifyTest(ReviewRegisterTest):
    def setUp(self):
        super(ReviewModifyTest, self).setUp()

        client = APIClient()

        store_id = Store.objects.all().first().id

        review_content = {
                        'rating'   : '4.5',
                        'content'  : 'good',
                        'image_url': 'test_image_url'
                    }

        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)
        client.post('/store/{}/review'.format(store_id), json.dumps(review_content), content_type='application/json')
        
        self.review_id = Review.objects.all().first().id

    def test_review_delete_success(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)

        store_id = Store.objects.all().first().id

        response = client.delete('/store/{}/review/{}'.format(store_id, self.review_id))

        self.assertEqual(response.json().get('message'), 'SUCCESS')
    
    def test_review_delete_fail_with_wrong_store_id(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)

        store_id = Store.objects.all().first().id

        response = client.delete('/store/{}/review/{}'.format(10000, self.review_id))

        self.assertEqual(response.json().get('message'), 'STORE_DOES_NOT_EXIST')
    
    def test_review_delete_fail_with_wrong_review_id(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.jwt_token)

        store_id = Store.objects.all().first().id

        response = client.delete('/store/{}/review/{}'.format(store_id, 10000))

        self.assertEqual(response.json().get('message'), 'REVIEW_DOES_NOT_EXIST')
    
    def test_review_delete_fail_with_permission_error(self):
        user = User.objects.create(kakao_id='test_kakao_id_wrong_user')

        wrong_user_jwt_token = jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm=HASHING_ALGORITHM)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=wrong_user_jwt_token)

        store_id = Store.objects.all().first().id

        response = client.delete('/store/{}/review/{}'.format(store_id, self.review_id))

        self.assertEqual(response.json().get('message'), 'PERMISSION_ERROR')

        
class StoreSearchTest(StoreBasicTest):    
    def setUp(self):
        super(StoreSearchTest, self).setUp()
    
    def test_store_search_get_success_with_category(self):
        client = Client()

        params = {
            'q': '한'
        }

        response = client.get('/store/search', params)
        result   = response.json().get('results')[0]

        category = result.get('category')

        self.assertEqual(category, '한식')
    
    def test_store_search_get_success_with_store_name(self):
        client = Client()

        params = {
            'q': '순남'
        }

        response = client.get('/store/search', params)
        result   = response.json().get('results')[0]

        store_name = result.get('store_name')

        self.assertEqual(store_name, '순남시래기')

    def test_store_search_get_success_with_address(self):
        client = Client()

        params = {
            'q': '강남'
        }

        response = client.get('/store/search', params)
        result   = response.json().get('results')[0]

        full_address = result.get('full_address')

        self.assertEqual(full_address, '서울 강남구 강남대로66길 16')

    def test_store_search_get_success_with_metro_station(self):
        client = Client()

        params = {
            'q': '사당'
        }

        response = client.get('/store/search', params)
        result   = response.json().get('results')[0]

        near_metro_stations = result.get('near_metro_stations')

        self.assertEqual(near_metro_stations, ['사당역'])

    def test_store_search_get_fail_with_no_keyword(self):
        client = Client()

        params = {
            'q': ''
        }

        response = client.get('/store/search', params).json()

        self.assertEqual(response.get('message'), 'NO_KEYWORD')
    
    def test_store_search_get_fail_with_result_not_found(self):
        client = Client()

        params = {
            'q': 'test_keyword_with_no_result'
        }

        response = client.get('/store/search', params).json()

        self.assertEqual(response.get('message'), 'RESULT_NOT_FOUND')
