import json
import jwt
from jwt.exceptions import InvalidSignatureError, DecodeError

from django.http import JsonResponse

from user.models import User

from mukbang.settings import SECRET_KEY, HASHING_ALGORITHM


# auth check with blocking access
def auth_check(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return JsonResponse({'message': 'TOKEN_DOES_NOT_EXIST'}, status=400)
            
            decoded_auth_token = jwt.decode(token, SECRET_KEY, algorithms=HASHING_ALGORITHM)

            user_id = decoded_auth_token['user_id']
            user    = User.objects.get(id=user_id)

            request.user = user
            return func(self, request, *args, **kwargs)

        except InvalidSignatureError:
            return JsonResponse({'message': 'SIGNATURE_VERIFICATION_FAILED'}, status=400)
        except DecodeError:
            return JsonResponse({'message': 'DECODE_ERROR'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status=404)
    return wrapper


# user check without blocking access
def user_check(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            if not token:
                request.user = None
                return func(self, request, *args, **kwargs)

            decoded_auth_token = jwt.decode(token, SECRET_KEY, algorithms=HASHING_ALGORITHM)
            
            user_id = decoded_auth_token['user_id']
            user    = User.objects.get(id=user_id)

            request.user = user
            return func(self, request, *args, **kwargs)

        except InvalidSignatureError:
            return JsonResponse({'message': 'SIGNATURE_VERIFICATION_FAILED'}, status=400)
        except DecodeError:
            return JsonResponse({'message': 'DECODE_ERROR'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, stauts=404)
    return wrapper

#for SMS authorization
def Validator(func):
    def Wrapper(self, request, *args, **kwargs):
        encoded_token = request.headers.get('Authorization')
        try:
            if encoded_token:
                decoded_token = jwt.decode(encoded_token, SECRET_KEY, HASHING_ALGORITHM)
            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status=401)
    return Wrapper
