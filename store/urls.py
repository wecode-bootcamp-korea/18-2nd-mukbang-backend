from django.urls import path

from .views import StoreView

urlpatterns = [
    path('', StoreView.as_view()),
]
