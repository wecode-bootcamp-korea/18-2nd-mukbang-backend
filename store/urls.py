from django.urls import path

from .views import (
                    StoreView, StoreDetailView,
                    ReviewRegisterView, ReviewModifyView
                )

urlpatterns = [
    path('', StoreView.as_view()),
    path('/detail', StoreDetailView.as_view()),
    path('/<int:store_id>/review', ReviewRegisterView.as_view()),
    path('/<int:store_id>/review/<int:review_id>', ReviewModifyView.as_view()),
]
