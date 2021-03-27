from rest_framework import routers
from .views import UserPolicyHomeViewSet


router = routers.SimpleRouter()

router.register(r'home', UserPolicyHomeViewSet)

urlpatterns =  router.urls

