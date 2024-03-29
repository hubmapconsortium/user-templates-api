"""user_templates_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("admin/", admin.site.urls),
    path("template_types/", views.TemplateTypeView.as_view(), name="template_types"),
    path(
        "templates/<str:template_type>/",
        views.TemplateView.as_view(),
        name="templates_by_template_type",
    ),
    path(
        "templates/<str:template_type>/<str:template_name>/",
        views.TemplateView.as_view(),
        name="template",
    ),
    path(
        "test_templates/<str:template_type>/<str:template_format>/",
        views.TestTemplateView.as_view(),
        name="test_template",
    ),
    path("status/", views.StatusView.as_view(), name="status"),
    path("tags/", views.TagsView.as_view(), name="tags"),
]
