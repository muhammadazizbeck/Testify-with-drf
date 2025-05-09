from django.contrib import admin
from django.urls import path,include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
   openapi.Info(
      title="Tester Mobile API",
      default_version='v1',
      description="tester descriptiom",
      terms_of_service="default terms of services",
      contact=openapi.Contact(email="aa2004bek@gmail.com"),
      license=openapi.License(name="default lisence"),
   ),
   public=True,
   permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/',include('users.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
