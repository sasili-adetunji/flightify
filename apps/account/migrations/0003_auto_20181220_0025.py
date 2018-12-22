# Generated by Django 2.1.3 on 2018-12-20 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_customuser_passport_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='contact_kin_mobile',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='contact_kin_email',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='NOK E-mail'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='contact_kin_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='NOK Name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='contact_kin_phone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='NOK Phone'),
        ),
    ]
