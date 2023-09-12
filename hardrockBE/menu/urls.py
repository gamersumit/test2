from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.menu_list_create_view),
    path('<int:pk>', views.menu_detail_view),
    path('<int:pk>/update/', views.menu_update_view),
    path('list/', views.menu_list_view),
    path('create/', views.CreateMenuAPIView.as_view()),
    path('<int:pk>/delete/', views.DeleteMenuAPIView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

