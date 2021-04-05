from django.urls import path

from .views import StoreView, StoreDetailView


urlpatterns = [
    path('', StoreView.as_view()),
    path('/detail', StoreDetailView.as_view()),
]
