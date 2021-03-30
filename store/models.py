from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'categories'


class OpenStatus(models.Model):
    name = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table ='open_status'


class Store(models.Model):
    name                     = models.CharField(max_length=30)
    one_line_introduction    = models.CharField(max_length=100, null=True)
    opening_time_description = models.CharField(max_length=100, null=True)
    phone_number             = models.CharField(max_length=15, null=True)
    sns_url                  = models.CharField(max_length=500, null=True)
    menu_pamphlet_image_url  = models.CharField(max_length=3000, null=True)
    is_reservation           = models.BooleanField(default=True)
    is_wifi                  = models.BooleanField(default=True)
    is_parking               = models.BooleanField(default=False)
    category                 = models.ForeignKey('Category', on_delete=models.CASCADE)
    open_status              = models.ForeignKey('OpenStatus', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'stores'


class Address(models.Model):
    latitude           = models.DecimalField(max_digits=25, decimal_places=22)
    longitude          = models.DecimalField(max_digits=25, decimal_places=22)
    full_address       = models.CharField(max_length=200)
    region_1depth_name = models.CharField(max_length=30)
    region_2depth_name = models.CharField(max_length=30)
    region_3depth_name = models.CharField(max_length=30)
    road_name          = models.CharField(max_length=30)
    building_name      = models.CharField(max_length=30)
    store              = models.OneToOneField('Store', on_delete=models.CASCADE)

    class Meta:
        db_table = 'addresses'


class Menu(models.Model): 
    name           = models.CharField(max_length=30)
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    menu_image_url = models.CharField(max_length=3000, null=True)
    store          = models.ForeignKey('Store', on_delete=models.CASCADE)

    class Meta:
        db_table = 'menus'
        unique_together = ('store', 'name')


class StoreImage(models.Model):
    image_url = models.CharField(max_length=3000)
    store     = models.ForeignKey('Store', on_delete=models.CASCADE)

    class Meta:
        db_table = 'store_images'


class MetroStation(models.Model):
    name       = models.CharField(max_length=30)
    line       = models.IntegerField()
    latitude   = models.DecimalField(max_digits=25, decimal_places=22)
    longitude  = models.DecimalField(max_digits=25, decimal_places=22)
    near_store = models.ManyToManyField('Store', through='MetroStationStore')

    class Meta:
        db_table        = 'metro_stations'
        unique_together = ('name', 'line')


class MetroStationStore(models.Model):
    store         = models.ForeignKey('Store', on_delete=models.CASCADE)
    metro_station = models.ForeignKey('MetroStation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'metro_stations_stores'
