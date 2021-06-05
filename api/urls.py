from django.urls import path

from api.views import ItemViews, CreateItemViews, UpdateItemViews, DeleteAPIViews

urlpatterns = [
    path('items', ItemViews.as_view(), name='getItem'),
    path('item/create', CreateItemViews.as_view(), name='createItem'),
    path('item/update', UpdateItemViews.as_view(), name='updateItem'),
    path('item/delete/<str:key>', DeleteAPIViews.as_view(), name='deleteItem')
]