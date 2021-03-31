import json
import requests

from django.test import TestCase
from django.test import Client
from django.http import JsonResponse

from unittest.mock import patch, MagicMock, Mock

from .views import KakaoLoginView


class KakaoLoginTest(TestCase):
    def test_kakaologin_get_success(self):
        mock_content  = {'id': '12345678', 'properties': {'nickname': 'test_nickname'}}

        mock_response          = requests.Response()
        mock_response._content = bytes(json.dumps(mock_content), 'utf-8')

        with patch('requests.get', return_value=mock_response):
            client = Client()
            params = {'access_token': 'test_access_token'}
            response = client.get('/user/login/kakao', data=params, content_type='application/json').json()

            self.assertEqual(response.get('nickname'), 'test_nickname')
            self.assertTrue(response.get('token'), True)

    def test_kakaologin_get_fail_access_token_not_exist(self):
        client = Client()
        params = {'access_token': ''}
        response = client.get('/user/login/kakao', data=params, content_type='application/json').json()

        self.assertEqual(response.get('message'), 'ACCESS_TOKEN_DOES_NOT_EXIST')

    def test_kakaologin_get_fail_with_error_code(self):
        mock_content  = {'code': -401}

        mock_response          = requests.Response()
        mock_response._content = bytes(json.dumps(mock_content), 'utf-8')

        with patch('requests.get', return_value=mock_response):
            client = Client()
            params = {'access_token': 'test_access_token'}
            response = client.get('/user/login/kakao', data=params, content_type='application/json').json()

        self.assertIn('code -401', response.get('message'))

    def test_kakaologin_get_fail_with_invalid_token(self):
        mock_content  = {'id': ''}

        mock_response          = requests.Response()
        mock_response._content = bytes(json.dumps(mock_content), 'utf-8')

        with patch('requests.get', return_value=mock_response):
            client = Client()
            params = {'access_token': 'test_access_token'}
            response = client.get('/user/login/kakao', data=params, content_type='application/json').json()

        self.assertEqual(response.get('message'), 'INVALID_ACCESS_TOKEN')

    def test_kakaologin_get_fail_with_key_error(self):
        mock_content  = {'id': '12345678'}

        mock_response          = requests.Response()
        mock_response._content = bytes(json.dumps(mock_content), 'utf-8')

        with patch('requests.get', return_value=mock_response):
            client = Client()
            params = {'access_token': 'test_access_token'}
            response = client.get('/user/login/kakao', data=params, content_type='application/json').json()

        self.assertEqual(response.get('message'), 'KEY_ERROR')
