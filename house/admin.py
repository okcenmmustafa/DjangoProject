from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin , DraggableMPTTAdmin

from house.models import Category, House, Images


class HouseImageInline(admin.TabularInline):
    model=Images
    extra=10


class CategoryAdmin(admin.ModelAdmin):
    list_display=['title','parent','status']
    list_filter=['status']


class HouseAdmin(admin.ModelAdmin):
    list_display = ['title','category','price','image_tag','status']
    readonly_fields = ('image_tag',)
    list_filter = ['status']
    inlines = [HouseImageInline]
    prepopulated_fields = {'slug': ('title' ,)}




class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','house','image_tag']
    readonly_fields = ('image_tag',)
    list_filter=['house']
    disable_fields=('title',)

class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count','id')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}


    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                House,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 House,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'
admin.site.register(Category,CategoryAdmin)
admin.site.register(House,HouseAdmin)
admin.site.register(Images,ImagesAdmin)