from django.urls import path
from main_app.views import ClientViewSet, MailingViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register('client', ClientViewSet)
router.register('mailing', MailingViewSet)

urlpatterns = router.urls
