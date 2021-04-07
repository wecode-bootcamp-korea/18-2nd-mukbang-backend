from django.urls import path
from .views      import (
                        SMSCodeRequestView, SMSCodeCheckView,
                        SignUpView, SignInView,
                        KakaoLoginView
                    )

urlpatterns = [
    path('/login/kakao', KakaoLoginView.as_view()),
    path('/smscoderequest', SMSCodeRequestView.as_view()),
    path('/smscodecheck', SMSCodeCheckView.as_view()),
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/login/kakao', KakaoLoginView.as_view()),
    ]
