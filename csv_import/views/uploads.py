from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from csv_import.forms.upload_form import *
from django.urls import reverse

from csv_import.models import *


class UploadsListView(ListView):
    model = Upload
    context_object_name = 'uploads_list'
    template_name = 'csv_import/uploads_list.html'


class UploadsEditView(DetailView):
    model = Upload
    context_object_name = 'upload'
    template_name = "csv_import/uploads_edit.html"

    def get_object(self, queryset=None):
        try:
            obj = self.model.objects.get(pk=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            messages.add_message(self.request, messages.ERROR, "Invalid file id")
            raise Http404

        #upload = {
        #    'obj' : obj,
        #    'upload_form' : upload_form(model=self.model, fields='__all__', obj=obj)
        #    }
        
        return obj#upload

def uploads_delete_view(request, pk):
    #if request.method == 'GET':
        #messages.add_message(request, messages.ERROR, "Forgot to pass an upload id?")
        #return HttpResponseRedirect(reverse('csv_import:uploads_list',))
    upload_to_delete = Upload.objects.get(pk=pk)#request.POST.get('id'))
    upload_to_delete.delete()
    return HttpResponseRedirect(reverse('csv_import:uploads_list'))
    
