from django.urls import path
from Fitnees_Admin import views

urlpatterns = [
    path("Admin-Login/", views.admin_login, name="admin_login"),
    path("Admin-Logout/", views.admin_logout, name="admin_logout"),
    path("Admin-Dashbord/", views.index, name="admin_Dashbord"),
    # Classes
    path("Classes/", views.classes, name="Classes"),
    path("classes_Delete/<int:C_id>/", views.classes_Delete, name="classes_Delete"),
    path("get-available-classes/", views.get_available_classes, name="get_available_classes"),
    # Traineer
    path("Trainers/", views.trainer, name="Trainers"),
    path("trainer_Delete/<int:T_id>/", views.trainer_Delete, name="trainer_Delete"),
]
