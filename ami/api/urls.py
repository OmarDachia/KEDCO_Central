from django.urls import path

from .views import (
    DeviceCreateAPIView,
    DeviceListAPIView,
    DeviceDetailsAPIView,
    DeviceUpdateAPIView,
    DeviceDeleteAPIView,
    DeviceReadingCreateAPIView,
    DeviceReadingListAPIView,
    DeviceReadingDetailsAPIView,
)
urlpatterns = [
    path("device/create/", DeviceCreateAPIView.as_view()),
    path("device/list/", DeviceListAPIView.as_view()),
    path("device/details/<uid>/", DeviceDetailsAPIView.as_view()),
    path("device/update/<uid>/", DeviceUpdateAPIView.as_view()),
    path("device/delete/<uid>/", DeviceDeleteAPIView.as_view()),

    path("device/reading/create/", DeviceReadingCreateAPIView.as_view()),
    path("device/reading/list/", DeviceReadingListAPIView.as_view()),
    path("device/reading/details/<uid>/",
         DeviceReadingDetailsAPIView.as_view()),

]
