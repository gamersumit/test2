from django.contrib import admin
from django.urls import path, include
from authentication.views import MyTokenObtainPairView, MyTokenRefreshView, MyTokenBlacklistView, ChangePasswordView
from authentication import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('signin/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signout/', MyTokenBlacklistView.as_view(), name='logout_token'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('user/', include('authentication.urls')),
    path('user/', include('djoser.urls.jwt')),
    path('signup/', views.user_create_view, name='signup'),
    path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('changepassword/', ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/', PasswordResetView.as_view()),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
# router = DefaultRouter()
# router.register(r"user", views.UserViewSet, basename="user")
# urlpatterns += router.urls
