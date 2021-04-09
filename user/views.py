import jwt, time, random
import requests, hashlib, hmac
import json, bcrypt, re
import datetime, base64
from json import JSONDecodeError

from django.views     import View
from django.http      import JsonResponse

from .models import User, Review

from my_settings import (
                         SMS_SERVICE_ID, SMS_SECRET_KEY,
                         SMS_ACCESS_KEY, HASHING_ALGORITHM,
                         SECRET_KEY, EMAIL_REGEX,
                         PASSWORD_REGEX, KAKAO_RESTAPI_KEY
                    )

from utils.decorators import auth_check, validator


KAKAO_USERINFO_REQUEST_URL = 'https://kapi.kakao.com/v2/user/me'


class KakaoLoginView(View):
    def get(self, request):
        try:
            access_token = request.GET.get('access_token')
            if not access_token:
                return JsonResponse({'message': 'ACCESS_TOKEN_DOES_NOT_EXIST'}, status=400)

            headers  = {'Authorization': 'Bearer {}'.format(access_token)}
            response = requests.get(KAKAO_USERINFO_REQUEST_URL, headers=headers).json()
            
            res_code = response.get('code')
            if res_code == -401:
                return JsonResponse({'message': 'code -401 : {}'.format(response.get('msg'))}, status=400)

            kakao_user_id = response.get('id')

            if kakao_user_id:
                kakao_user_nickname = response['properties']['nickname']

                user, _   = User.objects.get_or_create(kakao_id=kakao_user_id)
                jwt_token = jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm=HASHING_ALGORITHM)

                user_info = {'token': jwt_token, 'nickname': kakao_user_nickname}
                return JsonResponse(user_info, status=200)
            else:
                return JsonResponse({'message': 'INVALID_ACCESS_TOKEN'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class SignUpView(View):
    @validator
    def post(self, request):
        try:
            data          = json.loads(request.body)
            email         = data['email']
            password      = data['password']
            email_check   = User.objects.filter(email=email).exists()

            if email_check:
                return JsonResponse({'message': 'ERROR_EMAIL_EXISTS'}, status=401)
            
            if not EMAIL_REGEX.match(email):
                return JsonResponse({'message': 'ERROR_EMAIL_FORM'}, status=401)
            
            if not PASSWORD_REGEX.match(password):
                return JsonResponse({'message': 'ERROR_PASSWORD_FORM'}, status=401)

            decoded_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            User.objects.create(email=email, password=decoded_password)
            return JsonResponse({'message':'SUCCESS_SIGNUP'}, status = 201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)            

        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)

class SMSCodeRequestView(View):
    
        def make_signature(self):
            timestamp  = str(int(time.time() * 1000))
            secret_key = bytes(SMS_SECRET_KEY, 'UTF-8')
            method     = "POST"
            uri        = '/sms/v2/services/{}/messages'.format(SMS_SERVICE_ID)
            message    = method + " " + uri + "\n" + timestamp + "\n" + SMS_ACCESS_KEY
            message    = bytes(message, 'UTF-8')
            signature  = base64.b64encode(hmac.new(secret_key, message, digestmod  = hashlib.sha256).digest())
            return signature   
        
        def post(self, request):
            try:
                data              = json.loads(request.body)
                auth_phone        = data['auth_phone']
                random_code       = str(random.randint(1000, 9999))
                hased_random_code = bcrypt.hashpw(random_code.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                timestamp         = str(int(time.time() * 1000))
                
                headers = {
                    'Content-Type':'application/json; charset=UTF-8',
                    'x-ncp-apigw-timestamp':timestamp,
                    'x-ncp-iam-access-key': SMS_ACCESS_KEY,
                    'x-ncp-apigw-signature-v2':self.make_signature()
                } 
                
                body = {
                    "type": "sms",
                    "countryCode": "82",
                    "from": "01032974510",
                    "content": "Authentication Code.\n{}".format(random_code),
                    "messages":[
                        {
                            "to": "{}".format(auth_phone)
                        }
                    ]
                }

                sms_service_url   = 'https://sens.apigw.ntruss.com/sms/v2/services/{}/messages'.format(SMS_SERVICE_ID)
                response          = requests.post(sms_service_url, headers=headers, data=json.dumps(body), timeout_seconds=5)

                if response.status_code == 202:
                    return JsonResponse({'message': 'SUCCESS_CODE_SENT', 'hased_random_code':hased_random_code})      
                return JsonResponse({'message': 'CODE_NOT_SENT'})


            except KeyError:
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)            
                
            except JSONDecodeError:
                return JsonResponse({'message': 'JSONDecodeError'}, status=400)

class SMSCodeCheckView(View):
    def post(self, request):
        try:
            data              = json.loads(request.body)
            auth_code         = data['auth_code']
            hased_random_code = data['hased_random_code']
            auth_token        = jwt.encode({'exp':datetime.datetime.utcnow() + datetime.timedelta(seconds=100)}, SECRET_KEY, HASHING_ALGORITHM)
            
            if not bcrypt.checkpw(auth_code.encode('utf-8'), hased_random_code.encode('utf-8')):
                return JsonResponse({'message': 'ERROR_CODE_NOT_MATCHED'}, status=401)
            return JsonResponse({'message': 'SUCCESS_CODE_MATCHED','auth_token':auth_token}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)            

        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            email         = data['email']
            password      = data['password']
            
            email_check      = User.objects.get(email=email)
            decoded_password = email_check.password

            if not email_check:
                return JsonResponse({'message': 'ERROR_NO_EMAIL'}, status=401)

            if not bcrypt.checkpw(password.encode('utf-8'), decoded_password.encode('utf-8')):
                return JsonResponse({'message': 'ERROR_PASSWORD_NOT_MATCHED'}, status=401)

            return JsonResponse({'message':'SUCCESS_SIGNIN'}, status = 201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)            

        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)


class WishlistView(View):
    @auth_check
    def get(self, request):
        wishlist_qs = WishList.objects.filter(user=request.user)\
                                      .select_related('store__address', 'store__category')\
                                      .prefetch_related('store__review_set')

        stores = [
                {
                'store_id'             : wishlist.store.id,
                'store_name'           : wishlist.store.name,
                'full_address'         : wishlist.store.address.full_address,
                'one_line_introduction': wishlist.store.one_line_introduction,
                'category'             : wishlist.store.category.name,
                'rating'               : ReviewDetail.get_review_ratings_avg(wishlist.store),
                'counting'             : ReviewDetail.get_review_count(wishlist.store),
                'image_url'            : wishlist.store.storeimage_set.all().first().image_url
            } for wishlist in wishlist_qs]
        return JsonResponse({'results':stores}, status=200)

    @auth_check
    def post(self, request):
        try:
            store_id = request.GET.get('store_id')
            if not store_id:
                return JsonResponse({'message' : 'STORE_ID_PARAMETER_MISSING'}, status=400)

            store_id = int(store_id)

            if not Store.objects.filter(id=store_id).exists():
                return JsonResponse({'message' : 'ERROR_STORE_UNKOWN'}, status=404)
            if WishList.objects.filter(store_id=store_id, user=request.user).exists():
                return JsonResponse({'message' : 'ERROR_STORE_ALREADY_LIKED'}, status=404)
            WishList.objects.create(
                user=request.user, store_id=store_id
            )
            return JsonResponse({'message':'SUCCESS_STORE_ADDED'}, status=201)

        except IntegrityError:
            return JsonResponse({'message':'INTEGRITY_ERROR'}, status=400)


class DeleteWishlistView(View):   
    @auth_check
    def delete(self, request, store_id):    
        if not Store.objects.filter(id=store_id).exists():
            return JsonResponse({'message':'STORE_DOES_NOT_EXIST'})

        if not WishList.object.filter(store_id=store_id, user=request.user).exists():
            return JsonResponse({'message':'ERROR_STORE_NOT_LISTED'})

        WishList.object.delete(store_id=store_id, user=request.user)
        return JsonResponse({'message':'SUCCESS_STROE_DELDTED'}, status=201)
