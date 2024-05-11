"""central URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="KEDCO CENTRAL REPO API",
        default_version="v1",
        description="Central Repo API",
        terms_of_service="https://www.kedco.ng",
        contact=openapi.Contact(email="ahmad.shuaib@kedco.ng"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    # path("root/", admin.site.urls),
    # path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("accounts/api/", include(("accounts.api.urls", "accounts_api"), namespace="accounts_api")),
    path("apps/api/", include(("apps.api.urls", "apps_api"), namespace="apps_api")),
    # path('core/api/', include('core.api.urls')),
    path("location/api/", include("core.location.api.urls")),
    path("meters/api/", include("meters.api.urls")),
    path("gridx/api/", include("gridx.api.urls")),
    path("nmmp/api/", include("nmmp.api.urls")),
    path("api/", include("api.urls")),
    path("report/api/", include("report.api.urls")),
    path("md/api/", include("md.api.urls")),
    path("ami/api/", include("ami.api.urls")),
     # API documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=30),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
    path("", schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
]

# handler404 = "errorHandler.views.error_404"
# handler500 = "errorHandler.views.error_500"
# handler403 = "errorHandler.views.error_403"
# handler400 = "errorHandler.views.error_400"

handler404 = "errorHandler.api.views.error_404"
handler500 = "errorHandler.api.views.error_500"
handler403 = "errorHandler.api.views.error_403"
handler400 = "errorHandler.api.views.error_400"

# Serve static and media files from development server
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

# to make sure we capture media files before wildcard (useful in dev env only)
#urlpatterns += [path("", include(("core.urls", "core"), namespace="core"))]

admin.site.site_header = "KEDCO Central"
admin.site.index_title = "KEDCO Central Admin Interface"
admin.site.site_title = "KEDCO Central"
