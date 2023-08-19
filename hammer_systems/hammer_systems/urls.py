from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from referral_system.views import (UsersViewSet, authorization, invitation,
                                   verification)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', authorization),
    path('api/verify/', verification),
    path('api/users/<slug:code>/invitation/', invitation),
    path('swagger/', TemplateView.as_view(
        template_name='swagger.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    path('api/', include(router.urls)),
]
