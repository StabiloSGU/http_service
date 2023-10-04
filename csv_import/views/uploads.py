from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from csv_import.forms.upload_form import UploadForm
from django.urls import reverse, reverse_lazy
from csv_import.lib.csv_helper_funcs import *

from csv_import.models import *


class UploadsListView(ListView):
    model = Upload
    context_object_name = 'uploads_list'
    template_name = 'csv_import/uploads_list.html'


class UploadsEditView(DetailView):
    model = Upload
    context_object_name = 'edit_view_objects'
    template_name = "csv_import/uploads_edit.html"

    def get_object(self, queryset=None):
        try:
            obj = self.model.objects.get(pk=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            messages.add_message(self.request, messages.ERROR, "Invalid file id")
            raise Http404
        edit_view_objects = {
            'obj': obj,
            'file_info': get_file_column_info(obj.pk)
        }
        return edit_view_objects


def uploads_delete_view(request, pk):
    upload_to_delete = Upload.objects.get(pk=pk)#request.POST.get('id'))
    upload_to_delete.delete()
    return HttpResponseRedirect(reverse('csv_import:uploads_list'))
    

class UploadsAddView(FormView):
    template_name = "csv_import/uploads_add.html"
    form_class = UploadForm
    success_url = reverse_lazy("csv_import:uploads_list")

    def form_valid(self, form):
        obj = form.save()
        parse_csv_to_database(obj.pk)
        return super().form_valid(form)

