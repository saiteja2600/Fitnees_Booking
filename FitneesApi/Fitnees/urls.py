from django.urls import path
from Fitnees import views


urlpatterns = [
    path("Login/",views.user_login,name='user_login'),
    path("Logout/", views.user_logout, name='user_logout'),

    path("Register/",views.user_register,name='Register'),
    # Dashbord
    path("Dashbord/", views.index, name="Dashbord"),
    
    #Avaliable Class
     path('available_classes/', views.avaliableclasses, name='Available_Classes'),
    path('get_dates_by_class/', views.get_dates_by_class, name='get_dates_by_class'),
    path('get_trainers_and_times_by_class_and_date/', views.get_trainers_and_times_by_class_and_date, name='get_trainers_and_times_by_class_and_date'),
   #Schedule
   path("Schedule/",views.schedule,name='Schedule'),
   path("get-available-classes/", views.get_available_classes_events, name="get_available_classes"),


]