from django.contrib import admin
from .models import Trainer,Classes

class TraineerAdmin(admin.ModelAdmin):
    list_display = ('T_id','T_name', 'T_email', 'T_phone')
    search_fields = ('T_name', 'T_email')
    list_filter = ('T_name','T_email')

class ClassesAdmin(admin.ModelAdmin):
    list_display = ('C_id','C_name', 'C_trainer', 'C_date', 'C_start_time', 'C_end_time')
    search_fields = ('C_name', 'C_trainer__T_name')
    list_filter = ('C_date', 'C_trainer')
    date_hierarchy = 'C_date'

admin.site.register(Trainer, TraineerAdmin)
admin.site.register(Classes, ClassesAdmin)

