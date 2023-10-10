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

    def get_object(self, queryset=None):
        file = super().get_object(queryset)
        return file

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        match determine_upload_method(data['object'].pk):
            case ImportSettings.DB:
                df = get_df_from_file_using_database(data['object'].pk)
            case ImportSettings.PANDAS:
                df = get_df_from_file_using_pandas(data['object'].pk)
            case _:
                df = pd.DataFrame()
                print('Unaccounted import type')
        data['filters_and_values'] = self.find_filters_and_values_in_request()
        if not df.empty and (data['filters_and_values']['search']\
                             or data['filters_and_values']['sorting']):
            df = self.filter_file(df, data['filters_and_values'])
        data['df'] = convert_df_to_dict(df)
        return data

    def find_filters_and_values_in_request(self) -> dict:
        filters = {}
        search = {}
        sorting = {}
        for keyword in self.request.GET:
            if keyword.startswith('search_'):
                search[keyword[7:]] = self.request.GET[keyword]
            if keyword.startswith('sorting_'):
                sorting[keyword[8:]] = self.request.GET[keyword]
        filters['search'] = search
        filters['sorting'] = sorting
        return filters

    def filter_file(self, file, filters):
        filtered_file = file
        for keyword, value in filters['search'].items():
            if value:
                filtered_file = filtered_file[filtered_file[keyword].astype(str).str.contains(value)]
        sorting_columns = []
        sorting_order = []
        for keyword, value in filters['sorting'].items():
            if value == 'asc' or value == 'desc':
                sorting_columns.append(keyword)
                sorting_order.append(True if value == 'asc' else False)
        filtered_file = filtered_file.sort_values(by=sorting_columns, ascending=sorting_order)
        return filtered_file
