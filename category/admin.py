from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name','slug','cat_image')
    list_display_links = ('category_name','cat_image')
    read_only_fields = ('slug')
    ordering = ('category_name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
# Register your models here.
admin.site.register(Category,CategoryAdmin)