"""images_processing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .apps.jobs.views import JobsListAPIView, job_start, JobsRetrieveUpdateAPIView
from .apps.logs.views import LogsListAPIView, LogsRetrieveAPIView

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('job/', job_start, name='job'),
    path('job/<int:id>', JobsRetrieveUpdateAPIView.as_view(), name='jobs'),
    path('jobs/', JobsListAPIView.as_view(), name='jobs'),
    path('logs/', LogsListAPIView.as_view(), name='logs'),
    path('logs/<int:id>/', LogsRetrieveAPIView.as_view(), name='log'),
]
