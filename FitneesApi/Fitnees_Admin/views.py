from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Trainer,Classes
from datetime import datetime,date
from django.http import JsonResponse
from Fitnees.models import avaliable_classes





# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if not username or not password:
                messages.error(request, 'Both username and password are required')
                return render(request, 'admin_panel/login.html')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_Dashbord') 
            else:
                messages.error(request, 'Invalid credentials or not an admin user')
                
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    return render(request, 'admin_panel/login.html')
def admin_logout(request):
    if 'admin_logged_in' in request.session:
        del request.session['admin_logged_in']  
    logout(request)
    return redirect('admin_login')


# Dashboard
@login_required(login_url='admin_login')
def index(request):
    total_trainers = Trainer.objects.count()
    total_classes = Classes.objects.count()
    total_bookings = avaliable_classes.objects.count()
    available_slots = total_classes - total_bookings  # Simple calculation
    
    trainers = Trainer.objects.all()
    classes = Classes.objects.all()
    bookings = avaliable_classes.objects.select_related('classes', 'trainer').all()
    
    return render(request, "admin_panel/index.html", {
        'trainers': trainers,
        'classes': classes,
        'bookings': bookings,
        'total_trainers': total_trainers,
        'total_classes': total_classes,
        'total_bookings': total_bookings,
        'available_slots': available_slots if available_slots > 0 else 0  # Ensure not negative
    })
# Classes
@login_required(login_url='admin_login')
def classes(request):
    if request.method == 'POST':
        C_name = request.POST.get('C_name')
        C_description = request.POST.get('C_description')
        C_date_str = request.POST.get('C_date')
        C_start_time_str = request.POST.get('C_start_time')
        C_end_time_str = request.POST.get('C_end_time')
        trainer_id = request.POST.get('C_trainer')

        try:
            C_date_obj = datetime.strptime(C_date_str, "%Y-%m-%d").date()
            start_time_obj = datetime.strptime(C_start_time_str, "%H:%M").time()
            end_time_obj = datetime.strptime(C_end_time_str, "%H:%M").time()

            selected_start_datetime = datetime.combine(C_date_obj, start_time_obj)

            if C_date_obj < date.today():
                messages.error(request, "Cannot schedule classes for past dates.")
                return redirect('Classes')
            
            if C_date_obj == date.today():
                current_datetime = datetime.now()
                if selected_start_datetime < current_datetime:
                    messages.error(request, "Cannot schedule a class with a start time in the past for today's date.")
                    return redirect('Classes')

            if end_time_obj <= start_time_obj:
                messages.error(request, "End time must be after start time.")
                return redirect('Classes')

            trainer = Trainer.objects.get(T_id=trainer_id)

            existing_classes = Classes.objects.filter(
                C_trainer=trainer,
                C_date=C_date_obj
            )

            for cls in existing_classes:
                if (start_time_obj < cls.C_end_time and end_time_obj > cls.C_start_time):
                    messages.error(request, f"{trainer.T_name} is already booked between {cls.C_start_time.strftime('%I:%M %p')} and {cls.C_end_time.strftime('%I:%M %p')} on {cls.C_date.strftime('%b %d, %Y')}.")
                    return redirect('Classes')

            if Classes.objects.filter(C_name=C_name, C_trainer=trainer, C_date=C_date_obj, C_start_time=start_time_obj, C_end_time=end_time_obj).exists():
                messages.error(request, 'Class with same details already exists.')
                return redirect('Classes')
            
            Classes.objects.create(
                C_name=C_name,
                C_description=C_description,
                C_trainer=trainer,
                C_date=C_date_obj,
                C_start_time=start_time_obj,
                C_end_time=end_time_obj,
            )
            messages.success(request, "Class has been added successfully.")

        except Trainer.DoesNotExist:
            messages.error(request, "Selected trainer does not exist.")
        except ValueError as e:
            messages.error(request, f"Invalid date or time format: {e}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

        return redirect('Classes')

    classes = Classes.objects.all().order_by('-C_id')
    trainers = Trainer.objects.all()
    category_choices = Classes.CATEGORY_CHOICES

    current_date_iso = date.today().isoformat()

    return render(request, "admin_panel/classes.html", {
        'classes': classes,
        'trainers': trainers,
        'category_choices': category_choices,
        'current_date_iso': current_date_iso
    })
def classes_Delete(request, C_id):
    try:
        classes = Classes.objects.get(C_id=C_id)  # Changed from id to C_id
        classes.delete()
        messages.success(request, 'Class has been deleted successfully.')
        
    except Classes.DoesNotExist:
        messages.error(request, 'Class not found.')
    return redirect('Classes')





# Traineer
@login_required(login_url='admin_login')
def trainer(request):
    if request.method == 'POST':
        T_name = request.POST.get('T_name')
        T_email = request.POST.get('T_email')
        T_phone = request.POST.get('T_phone')

        
        try:
            
            if Trainer.objects.filter( T_name=T_name,T_email=T_email, T_phone=T_phone).exists():
                messages.error(request, 'Trainer already exists.')
                return redirect('Trainers')
            elif Trainer.objects.filter(T_email=T_email).exists():
                messages.error(request, 'Email already exists.')
                return redirect('Trainers')
            elif Trainer.objects.filter(T_phone=T_phone).exists():
                messages.error(request, 'Phone number already exists.')
                return redirect('Trainers')

            else:
                
                Trainer.objects.create(
                T_name=T_name,
                T_email=T_email,
                T_phone=T_phone
            )
            messages.success(request, 'Trainer has been added successfully.')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('Trainers')

   
    trainers = Trainer.objects.all().order_by('-T_id')
    return render(request, 'admin_panel/traineer.html', {'trainers': trainers})        
                       
@login_required(login_url='admin_login')        
def trainer_Delete(request, T_id):
    try:
        trainer = Trainer.objects.get(T_id=T_id)  # Changed from id to T_id
        trainer.delete()
        messages.success(request, 'Trainer has been deleted successfully.')
    except Trainer.DoesNotExist:
        messages.error(request, 'Trainer not found.')
    return redirect('Trainers')



def get_available_classes(request):
    today = date.today()
    classes = Classes.objects.filter(C_date__gte=today).select_related('C_trainer')
    events = []
    for c in classes:
        events.append({
            "title": f"{c.C_name} - {c.C_trainer.T_name}",
            "start": f"{c.C_date}T{c.C_start_time}",
            "end": f"{c.C_date}T{c.C_end_time}",
            "description": c.C_description,
        })
    return JsonResponse(events, safe=False)
    
   