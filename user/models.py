from django.db import models


class User(models.Model):
    email      = models.EmailField(max_length=128, null=True, unique=True)
    password   = models.CharField(max_length=200, null=True)
    kakao_id   = models.CharField(max_length=100, null=True, unique=True)
    google_id  = models.CharField(max_length=100, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        

class Review(models.Model):
    rating     = models.CharField(max_length=45)
    content    = models.CharField(max_length=500)
    image_url  = models.CharField(max_length=3000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user       = models.ForeignKey('User', on_delete=models.CASCADE)
    store      = models.ForeignKey('store.Store', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'


class WishList(models.Model):
    user  = models.ForeignKey('User', on_delete=models.CASCADE)
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE)

    class Meta:
        db_table        = 'wishlists'
        unique_together = ('user', 'store')
