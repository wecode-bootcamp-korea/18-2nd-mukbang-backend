from django.urls import path

from .views import (
                    StoreView, StoreDetailView,
                    ReviewRegisterView, ReviewModifyView,
                    StoreSearchView
                )


urlpatterns = [
    path('', StoreView.as_view()),
    path('/detail', StoreDetailView.as_view()),
    path('/<int:store_id>/review', ReviewRegisterView.as_view()),
    path('/<int:store_id>/review/<int:review_id>', ReviewModifyView.as_view()),
    path('/search', StoreSearchView.as_view()),
]
