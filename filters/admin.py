from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Filter, Keyword, VRPage, LinkedinProfile


class KeywordInline(admin.TabularInline):
    model = Keyword


class VRPageAdmin(admin.ModelAdmin):
    inlines = [KeywordInline]

# So we can be able to import and export data for Filter class
class KeywordResource(resources.ModelResource):

    class Meta:
        model = Filter
        fields = ('id', 'order', 'keyword')


@admin.register(Filter)
class KeywordAdmin(ImportExportModelAdmin):
    resource_class = KeywordResource

# So we can be able to import and export data for LinkedinProfile class
class LinkedinResource(resources.ModelResource):

    class Meta:
        model = LinkedinProfile
        fields = ('id', 'profile_link')


@admin.register(LinkedinProfile)
class LinkedinProfileAdmin(ImportExportModelAdmin):
    resource_class = LinkedinResource


admin.site.register(VRPage, VRPageAdmin)
