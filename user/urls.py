from django.urls import path
from .views      import (
                        SMSCodeRequestView, SMSCodeCheckView,
                        KakaoLoginView, SignUpView, SignInView, 
                        ShowWishlist, AddWishlistView, DeleteWishlistView
                    )

urlpatterns = [
    path('/smscoderequest', SMSCodeRequestView.as_view()),
    path('/smscodecheck', SMSCodeCheckView.as_view()),
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/login/kakao', KakaoLoginView.as_view()),
    path('/wishlist/', AddWishlistView.as_view()),
    path('/addwishlist', AddWishlistView.as_view()),
    path('/deletewishlist/<int:wishlist_id>', DeleteWishlistView.as_view())
]
