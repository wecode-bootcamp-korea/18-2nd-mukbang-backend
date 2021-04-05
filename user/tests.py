import json, unittest, bcrypt ,random, requests
from unittest.mock import patch, MagicMock, Mock

from django.test   import TestCase
from django.test   import Client
from django.http   import JsonResponse
from django.http   import response

from .views        import KakaoLoginView
from .models       import User


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


class SignUpTest(TestCase): 
    def setUp(self):
        User.objects.create(
            email    = 'testmail1@gmail.com',
            password = '12345689!'
        )
    
    def tearDown(sellf):
        User.objects.all().delete()

    def test_success_signup(self):
        client = Client()
        user   = {
            'email'   : 'testmail2@gmail.com',
            'password': '123456789!'
        }
        response = client.post("/user/signup", json.dumps(user), content_type ='application/json')
        self.assertEqual(response.json(),{'message':'SUCCESS_SIGNUP'})

    def test_fail_signup_email_exist(self):
        client = Client()
        user   = {
            'email':'testmail1@gmail.com',
            'password':'123456789!'
        }
        response = client.post("/user/signup", json.dumps(user), content_type ='application/json')
        self.assertEqual(response.json(),{'message': 'ERROR_EMAIL_EXISTS'})

    def test_fail_signup_email_form(self):
        client = Client()
        user   = {
            'email'   : 'testmailmail.com',
            'password': '123456789!'
        }
        response = client.post("/user/signup", json.dumps(user), content_type ='application/json')
        self.assertEqual(response.json(),{'message': 'ERROR_EMAIL_FORM'})

    def test_fail_signup_password_form(self):
        client = Client()
        user   = {
            'email'   : 'testmail3@gmail.com',
            'password': '123456789'
        }
        response = client.post("/user/signup", json.dumps(user), content_type ='application/json')
        self.assertEqual(response.json(),{'message': 'ERROR_PASSWORD_FORM'})
    
    def test_KEY_ERROR_signup(self):
        client = Client()
        user   = {
            ''        : 'testmail3@gmail.com',
            'password': '123456789!'
        }        
        response = client.post("/user/signup", json.dumps(user), content_type ='application/json')
        self.assertEqual(response.json(),{'message': 'KEY_ERROR'})

    def test_JSONDecodeError_signup(self):
        client = Client()
        user   = {
            'email'   : 'testmail3@gmail.com',
            'password': '123456789!'
        }
        response = client.post("/user/signup", user)
        self.assertEqual(response.json(),{'message': 'JSONDecodeError'})
        

class SignInTest(TestCase): 
    def setUp(self):
        User.objects.create(
            email    = 'logintest@gmail.com',
            password = bcrypt.hashpw('12345689!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
    
    def tearDown(self):
        User.objects.all().delete()

    def test_succecss_signin(self):
        user = {
            'email'   :'logintest@gmail.com',
            'password':'12345689!'
        }
        client   = Client()
        response = client.post("/user/signin", json.dumps(user), content_type ='application/json')
        self.assertEqual(response.json().get('message'),'SUCCESS_SIGNIN')


class CodeRequestTest(TestCase):
    @patch('requests.post')
    def test_success_code_requested(self, mocked_response):
        send_to         = {
            'auth_phone' : '0000000000'
        }
        client          = Client()
        res             = mocked_response.return_value
        res.status_code = 202
        response        = client.post("/user/smscoderequest", json.dumps(send_to), content_type ='application/json')
        self.assertEqual(response.json().get('message'),'SUCCESS_CODE_SENT')

    @patch('requests.post')
    def test_fail_code_not_requested(self, mocked_response):
        send_to          = {
            'auth_phone' : '0000000000'
        }
        client           = Client()
        res              = mocked_response.return_value
        res.status_code != 202
        response         = client.post("/user/smscoderequest", json.dumps(send_to), content_type ='application/json')
        self.assertEqual(response.json().get('message'), 'CODE_NOT_SENT')

    def test__JSONDecodeError_code__not_reqeusted(self):
        send_to  = {
            'auth_phone' : '0000000000'
        }
        client   = Client()
        response = client.post("/user/smscoderequest", send_to)
        self.assertEqual(response.json().get('message'), 'JSONDecodeError')


    def test_KeyError_code_not_requested(self):
        send_to  = {
            ''   :'0000000000'
        }
        client   = Client()
        response = client.post("/user/smscoderequest", json.dumps(send_to), content_type ='application/json')
        self.assertEqual(response.json().get('message'), 'KEY_ERROR')

        
class CodeCheckTest(TestCase):
    def test_success_auth_matched(self):
        random_code       = str(random.randint(1000, 9999))
        hased_random_code = bcrypt.hashpw(random_code.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        codes             = {
            "auth_code" : random_code,
            "hased_random_code" : hased_random_code
        }
        client   = Client()
        response = client.post("/user/smscodecheck", json.dumps(codes), content_type ='application/json')
        self.assertEqual(response.json().get('message'), 'SUCCESS_CODE_MATCHED')


    def test_fail_auth_not_matched(self):
        hased_random_code = bcrypt.hashpw("4321".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        codes             = {
            "auth_code" : "1234",
            "hased_random_code" : hased_random_code
        }
        client   = Client()
        response = client.post("/user/smscodecheck", json.dumps(codes), content_type ='application/json')
        self.assertEqual(response.json().get('message'), 'ERROR_CODE_NOT_MATCHED')

    def test_JSONDecodeError_code_check(self):
        random_code       = str(random.randint(1000, 9999))
        hased_random_code = bcrypt.hashpw(random_code.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        codes             = {
            "auth_code" : random_code,
            "hased_random_code" : hased_random_code
        }
        client   = Client()
        response = client.post("/user/smscodecheck", codes)
        self.assertEqual(response.json().get('message'), 'JSONDecodeError')

    def test_KeyError_code_check(self):
        random_code       = str(random.randint(1000, 9999))
        hased_random_code = bcrypt.hashpw(random_code.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        codes             = {
            "" : random_code,
            "hased_random_code" : hased_random_code
        }
        client   = Client()
        response = client.post("/user/smscodecheck", json.dumps(codes), content_type ='application/json')        
        self.assertEqual(response.json().get('message'), 'KEY_ERROR')