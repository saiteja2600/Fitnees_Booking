from django.db import models


class Trainer(models.Model):
    T_id = models.AutoField(primary_key=True)
    T_name = models.CharField(max_length=50)
    T_email = models.EmailField()
    T_phone = models.CharField(max_length=10)
    
    def __str__(self):
        return self.T_name
    
class Classes(models.Model):
    CATEGORY_CHOICES = [
        ('Strength', 'Strength'),
        ('Yoga', 'Yoga'),
        ('HIIT', 'HIIT'),
        ('Cardio', 'Cardio'),
    ]
    C_id = models.AutoField(primary_key=True)
    C_name = models.CharField(max_length=50,choices=CATEGORY_CHOICES,default='Cardio')
    C_description = models.TextField()
    C_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE,default=True,null=False)
    C_date = models.DateField()
    C_start_time = models.TimeField()
    C_end_time = models.TimeField()
   
    def __str__(self):
        return f"{self.C_name} on {self.C_date} ({self.C_start_time}-{self.C_end_time}) with {self.C_trainer.T_name if self.C_trainer else 'N/A'}"

