
from django.contrib import admin
from django.urls import path
from app.views import About
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', About, name='about')
]
