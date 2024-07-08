from django.urls                    import path, include
from django.contrib                 import admin
from rest_framework                 import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg                       import openapi
from drf_yasg.views                 import get_schema_view



schema_view = get_schema_view(
    openapi.Info(
        title="b2tech API",
        default_version='v1',
        description="API documentation for b2tech",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/locations/', include('locations.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/groups/', include('groups.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
