from django.contrib import admin
from django.urls import path
from main.views import order_view, all_order_view, details_view, delete_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', order_view, name="order"),
    path('all_orders/', all_order_view, name="all_orders"),
    path('exit/', LogoutView.as_view(next_page='order'), name="exit"),
    path('details/<order_id>/', details_view, name="details"),
    path('delete/<order_id>/', delete_view, name="delete")
]
