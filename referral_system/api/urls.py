from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet, authorization, invitation, verification

app_name = 'api'

router = DefaultRouter()
router.register(r'user', UsersViewSet, basename='users')

urlpatterns = [
    path('auth/', authorization),
    path('verify/', verification),
    path('user/invitation/', invitation),
    path('docs/', TemplateView.as_view(
        template_name='swagger.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    path('', include(router.urls)),
]
