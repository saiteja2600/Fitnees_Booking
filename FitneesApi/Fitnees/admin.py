from django.contrib import admin
from .models import Register,avaliable_classes

# Register your models here.

class RegisterAdmin(admin.ModelAdmin):
    list_display = ('username','email','password')
    search_fields = ('username','email')
    list_filter = ('username','email')
class AvaliableClassAdmin(admin.ModelAdmin):
    list_display = ('client_name','client_email','slot_time','classes','trainer')
    search_fields = ('client_name','client_email')
    list_filter = ('client_name','client_email')
    
    
    
    
    
admin.site.register(Register,RegisterAdmin)
admin.site.register(avaliable_classes,AvaliableClassAdmin)
    
