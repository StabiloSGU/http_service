from django.urls import path
from .views import *

app_name = "csv_import_api"

urlpatterns = [
    path('uploads_list/', UploadsAPIView.as_view(), name="uploads_list"),
    path('uploads_list/create/', UploadsAPICreateView.as_view(), name="create_upload"),
    path('uploads_list/delete/<int:pk>', UploadsAPIDeleteView.as_view(), name="delete_upload"),
    path('uploads_list/view/<int:pk>', UploadsAPIRetrieveView.as_view(), name="retrieve_upload")
]