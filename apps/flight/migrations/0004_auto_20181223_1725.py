# Generated by Django 2.1.3 on 2018-12-23 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0003_flight_reminder_notification_sent_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='reminder_notification_sent_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Reminder notification sent at'),
        ),
    ]