from django.db import models
from Fitnees_Admin.models import Classes, Trainer
from datetime import datetime,time


class Register(models.Model):
    username = models.CharField(max_length=300)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    conf_password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.email
class avaliable_classes(models.Model):
    user = models.ForeignKey(Register,on_delete=models.CASCADE,default=True,null=False)
    client_name = models.CharField(max_length=300)
    client_email = models.EmailField()
    slot_time = models.DateTimeField(null=True,blank=True)
    classes = models.ForeignKey(Classes,on_delete=models.CASCADE,default=True,null=False)
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE,default = True,null=False)
    
    def save(self, *args, **kwargs):
        
        if self.classes and not self.slot_time:
            combined_datetime = datetime.combine(self.classes.C_date, self.classes.C_start_time)
            self.slot_time =combined_datetime
        if self.classes and not self.trainer_id:
            self.trainer = self.classes.C_trainer
        super().save(*args, **kwargs)
            
    def __str__(self):
        return f"{self.client_email} booked {self.classes.C_name} on {self.classes.C_date}"

    


