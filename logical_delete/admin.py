from django import forms
from django.contrib import admin
from django.forms import BooleanField
from django.http import HttpResponseRedirect

from logical_delete.models import LogicalDeleteModel


class LogicalDeleteModelInline(admin.TabularInline):
    exclude = ('deleted_at',)

    def get_queryset(self, request):
        # admin.ModelAdmin の定義を改変
        qs = self.model._default_manager.all_with_deleted()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    queryset = get_queryset


class LogicalDeleteAdminForm(forms.ModelForm):
    deleted = BooleanField(required=False)

    class Meta:
        model = LogicalDeleteModel
        exclude = ('deleted_at',)

    def __init__(self, *args, **kwargs):
        super(LogicalDeleteAdminForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.initial['deleted'] = instance.deleted

    def clean(self, *args, **kwargs):
        cleaned_data = super(LogicalDeleteAdminForm, self).clean(*args,
                                                                 **kwargs)
        if 'recover' in self.data:
            self.instance.deleted_set = False
            cleaned_data['deleted'] = False
        return cleaned_data

    def save(self, commit=True, *args, **kwargs):
        model = super(LogicalDeleteAdminForm, self).save(commit=False,
                                                         *args, **kwargs)
        model.deleted_set = self.cleaned_data['deleted']
        if commit:
            model.save()
        return model


class LogicalDeleteModelAdmin(admin.ModelAdmin):
    form = LogicalDeleteAdminForm
    list_display = ("id", "__str__",)
    list_display_links = ("id", "__str__",)
    list_filter = ()
    exclude = ('deleted_at',)
    actions = ['delete_selected', 'soft_recover']

    def delete_selected(self, request, queryset):
        queryset.delete()

    delete_selected.short_description = 'Soft delete selected objects'

    def soft_recover(self, request, queryset):
        queryset.recover()

    soft_recover.short_description = 'Recover selected objects'

    def response_change(self, request, obj, *args, **kwargs):
        if 'recover' in request.POST:
            return HttpResponseRedirect('../')
        return super(LogicalDeleteModelAdmin, self).response_change(request,
                                                                    obj,
                                                                    *args,
                                                                    **kwargs)

    def get_queryset(self, request):
        try:
            qs = self.model._default_manager.all_with_deleted()
        except Exception as ex:
            qs = self.model._default_manager.all()

        ordering = self.get_ordering(request) or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    queryset = get_queryset
