import json
import requests
import copy

from django.test import TestCase
from django.test import Client
from django.http import JsonResponse

from unittest.mock import patch, MagicMock, Mock

from .views import StoreView

from .models import Store, OpenStatus, Category


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
            "x"                 : "127.032166561787",
            "y"                 : "37.4918939171295"
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
        client = Client()
        response = client.post('/store', json.dumps(TEST_DATA), content_type='application/json').json()

        self.assertEqual(response.get('message'), 'DUPLICATE_STORE_NAME_AT_THE_SAME_LOCATION')
