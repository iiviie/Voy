# Generated by Django 5.1.3 on 2024-11-28 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='total_passengers',
            field=models.IntegerField(default=0),
        ),
    ]
