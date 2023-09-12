
from . import views
from rest_framework import routers
from rest_framework_nested import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register('', views.CartViewSet,basename='carts')
cart_router=routers.NestedDefaultRouter(router,'',lookup='cart')
cart_router.register('items',views.CartItemViewSet, basename='cart-items')
urlpatterns = [
    path('',include(router.urls)),
    path('',include(cart_router.urls)),
    path('', views.auth_view, name='auth'),
]
