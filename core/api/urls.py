from django.urls import path
from .views import (
    UserNotificationList,
    UserNotificationDetailsAPIView,
    UserNotificationDeleteAPIView,
    UserNotificationUpdateAPIView,
    DocumentList,
    DocumentDetailsAPIView,
    DocumentDownloadAPIView,
    DocumentUpdateAPIView,
    DocumentDeleteAPIView,
)


urlpatterns = [
    path("user/notification/list/", UserNotificationList.as_view()),
    path("user/notification/details/<pk>/", UserNotificationDetailsAPIView.as_view()),
    path("user/notification/update/<pk>/", UserNotificationUpdateAPIView.as_view()),
    path("user/notification/delete/<pk>/", UserNotificationDeleteAPIView.as_view()),
    #
    path("documents/list/", DocumentList.as_view()),
    path("documents/details/<pk>/", DocumentDetailsAPIView.as_view()),
    path("documents/download/<uid>/", DocumentDownloadAPIView.as_view(), name="document-download"),
    path("documents/update/<pk>/", DocumentUpdateAPIView.as_view()),
    path("documents/delete/<pk>/", DocumentDeleteAPIView.as_view()),

]
