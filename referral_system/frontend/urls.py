from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import main, profile, signup, verification

app_name = 'frontend'


urlpatterns = [
    path('', main, name='main'),
    path('signup/', signup, name='signup'),
    path('verify/', verification, name='verification'),
    path('me/', profile, name='me'),
    path('logout/', LogoutView.as_view(), name='logout')
]
