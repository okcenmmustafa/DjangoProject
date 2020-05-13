from django.contrib import admin

# Register your models here.
from home.models import Setting , ContactFormMessage , UserProfile


class SettingAdmin(admin.ModelAdmin):
    list_display = ['title','image_tag']
    readonly_fields = ('image_tag',)
class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name','email','subject','note','status']
    list_filter = ['status']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','phone','adress','city','country','image_tag']


admin.site.register(Setting,SettingAdmin)
admin.site.register(ContactFormMessage,ContactFormMessageAdmin)
admin.site.register(UserProfile,UserProfileAdmin)


