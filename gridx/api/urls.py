from django.urls import path
from .views import (
    FeederListAPIView,
    FeederSearchAPIView,
    FeederDetailsAPIView,
    TransformerListAPIView,
    TransformerSearchAPIView,
    TransformerDetailsAPIView,
)

urlpatterns = [
    path("feeder/list/", FeederListAPIView.as_view()),
    path("feeder/search/", FeederSearchAPIView.as_view()),
    path("feeder/details/<pk>/", FeederDetailsAPIView.as_view()),
    # path("feeder/delete/<pk>/", FeederDeleteAPIView.as_view()),

    path("transformer/list/", TransformerListAPIView.as_view()),
    path("transformer/search/", TransformerSearchAPIView.as_view()),
    path("transformer/details/<pk>/", TransformerDetailsAPIView.as_view()),
    # path("transformer/delete/<pk>/", UserProfileDeleteAPIView.as_view()),
]
