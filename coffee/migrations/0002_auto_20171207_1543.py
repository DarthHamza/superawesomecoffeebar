# Generated by Django 2.0 on 2017-12-07 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coffee',
            name='price',
            field=models.DecimalField(decimal_places=3, max_digits=20, null=True),
        ),
    ]
