from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Menu
from .serializers import MenuSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import serializers

class MenuListCreateAPIView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('description') or None
        if content is None:
            content = title
        serializer.save(description=content)


menu_list_create_view = MenuListCreateAPIView.as_view()


class MenuDetailAPIView(generics.RetrieveAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        obj = get_object_or_404(Menu, pk=self.kwargs.get('pk'))
        return obj


menu_detail_view = MenuDetailAPIView.as_view()


class MenuListAPIView(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


menu_list_view = MenuListAPIView.as_view()


class DeleteMenuAPIView(generics.DestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_object(self):
        obj = get_object_or_404(Menu, pk=self.kwargs.get('pk'))
        return obj


class CreateMenuAPIView(generics.CreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuUpdateAPIView(generics.UpdateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance:
            raise serializers.ValidationError("Error occurred during update")


menu_update_view = MenuUpdateAPIView.as_view()