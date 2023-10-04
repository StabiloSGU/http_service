from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from csv_import.views import *
app_name = "csv_import"

urlpatterns = [
        path("", UploadsListView.as_view(), name="uploads_list"),
        path("uploads/edit/<int:pk>", UploadsEditView.as_view(), name="uploads_edit"),
        path("uploads/delete/<int:pk>", uploads_delete_view, name="uploads_delete"),
        path("uploads/add", UploadsAddView.as_view(), name="uploads_add"),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
