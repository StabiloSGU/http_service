from django.urls import path

from csv_import.views import *
app_name = "csv_import"

urlpatterns = [
        path("", UploadsListView.as_view(), name="uploads_list"),
        path("uploads/edit/<int:pk>", UploadsEditView.as_view(), name="uploads_edit"),
        path("uploads/delete/<int:pk>", uploads_delete_view, name="uploads_delete"),
    ]
