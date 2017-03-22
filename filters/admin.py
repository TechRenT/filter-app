from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Filter, Keyword, VRPage


class KeywordInline(admin.TabularInline):
    model = Keyword


class VRPageAdmin(admin.ModelAdmin):
    inlines = [KeywordInline]


class KeywordResource(resources.ModelResource):

    class Meta:
        model = Filter
        fields = ('id', 'order', 'keyword')


@admin.register(Filter)
class KeywordAdmin(ImportExportModelAdmin):
    resource_class = KeywordResource


admin.site.register(VRPage, VRPageAdmin)
