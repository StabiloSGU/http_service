from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from csv_import.forms.upload_form import UploadForm
from django.urls import reverse, reverse_lazy
from csv_import.lib.csv_helper_funcs import *
from django.db import transaction

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
            file_info = self.get_file_info(obj.pk)
        except ObjectDoesNotExist:
            messages.add_message(self.request, messages.ERROR, "Invalid file id")
            raise Http404

        edit_view_objects = {
            'obj': obj,
            'file_info': file_info
        }
        return edit_view_objects

    def get_file_info(self, pk):
        obj = Upload.objects.get(pk=pk)
        if UploadContentsFields.objects.filter(file=obj.pk).exists():
            return get_file_column_info(file_pk=obj.pk)
        else:
            return get_file_column_info_using_pandas(file_pk=obj.pk)


def uploads_delete_view(request, pk):
    upload_to_delete = Upload.objects.get(pk=pk)
    upload_to_delete.delete()
    return HttpResponseRedirect(reverse('csv_import:uploads_list'))
    

class UploadsAddView(FormView):
    template_name = "csv_import/uploads_add.html"
    form_class = UploadForm
    success_url = reverse_lazy("csv_import:uploads_list")

    @transaction.atomic()
    def form_valid(self, form):
        obj = form.save()
        match int(form.cleaned_data['upload_choice']):
            case ImportSettings.DB:
                parse_csv_to_database(obj.pk)
            case ImportSettings.PANDAS:
                print('Selected pandas')
                pass
            case _:
                print('selected unaccounted import setting')
                print(form.cleaned_data['upload_choice'], type(form.cleaned_data['upload_choice']))
        return super().form_valid(form)


class UploadsDetailView(DetailView):
    model = Upload
    context_object_name = 'detail_view_data'
    template_name = "csv_import/uploads_detail.html"

    # что мне нужно? мне нужно вывести файл либо из датафрейма панд
    # либо из базы данных
    # я хочу получать get параметры, обязательно нужен pk
    # затем исходя из того, где лежит файл (в бд или на диске), собирать новый объект
    # можно собирать его всегда в датафрейм, чтобы упростить работу
    # получив датафрейм я хочу его вывести в виде таблицы на страницу
    # если помимо pk есть и другие параметры, надо применять их как фильтры к файлу

    # начнём с того, чтобы получать pk и выводить файл в виде таблицы
    def get_object(self, queryset=None):
        file = super().get_object(queryset)
        # фильтры применять тут
        obj = file
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # тут можно вернуть параметры фильтрации
        #data['param'] = self.request.GET.get('parameter')
        match determine_upload_method(data['object'].pk):
            case ImportSettings.DB:
                df = get_df_from_file_using_database(data['object'].pk)
                data['df'] = convert_df_to_dict(df)
            case ImportSettings.PANDAS:
                df = get_df_from_file_using_database(data['object'].pk)
                data['df'] = convert_df_to_dict(df)
            case _:
                print('Unaccounted import type')
        print('rows')
        for row in data['df']['rows']:
            print(list(row))
        return data
