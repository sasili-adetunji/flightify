from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

class OptionalSlashRouter(SimpleRouter):
    def __init__(self, trailing_slash='/?'):
        self.trailing_slash = trailing_slash
        super(SimpleRouter, self).__init__()


router = OptionalSlashRouter()


urlpatterns = []

router = DefaultRouter()
router.register(r'tickets', views.TicketViewSet, basename='tickets')
urlpatterns += router.urls
