from django.contrib import admin

# Register your models here.
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
    list_filter = ['status','category']
    inlines = [HouseImageInline]



class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','house','image_tag']
    readonly_fields = ('image_tag',)
    list_filter=['house']


admin.site.register(Category,CategoryAdmin)
admin.site.register(House,HouseAdmin)
admin.site.register(Images,ImagesAdmin)