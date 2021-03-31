import jwt
import requests
import uuid

from django.shortcuts import redirect
from django.views     import View
from django.http      import JsonResponse

from .models import User

from my_settings import SECRET_KEY, HASHING_ALGORITHM, KAKAO_RESTAPI_KEY


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
