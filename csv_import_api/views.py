from rest_framework import generics
from csv_import.models import *
from .serializers import *
from rest_framework.response import Response
from csv_import.lib.csv_helper_funcs import *


class UploadsAPIView(generics.ListAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer


class UploadsAPICreateView(generics.CreateAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer


class UploadsAPIDeleteView(generics.DestroyAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer


class UploadsAPIRetrieveView(generics.RetrieveAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        file_ifo = None
        if UploadContentsFields.objects.filter(file=instance.pk).exists():
            file_info = get_file_column_info(file_pk=instance.pk)
        else:
            file_info = get_file_column_info_using_pandas(file_pk=instance.pk)
        resp = {
            "instance": serializer.data,
            "column_info": file_info,
        }
        return Response(resp)
