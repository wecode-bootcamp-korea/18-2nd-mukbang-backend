# Generated by Django 3.1.7 on 2021-03-31 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='openstatus',
            old_name='status_name',
            new_name='name',
        ),
    ]
