from django.shortcuts import render,redirect
from .models import Register,avaliable_classes
from Fitnees_Admin.models import Trainer,Classes
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date,datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMessage
from django.conf import settings








# Create your views here.
@login_required(login_url='user_login')
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Register.objects.get(email=email)

            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['email'] = user.email
                messages.success(request, 'Login Successful')
                return redirect('Dashbord')  # use 'Dashbord' if that's the correct URL name
            else:
                messages.error(request, 'Invalid password')
        except Register.DoesNotExist:
            messages.error(request, 'Invalid email')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'user_panel/login.html')

def user_logout(request):
    request.session.flush()  # Completely clears all session data
    messages.success(request, "Logged out successfully.")
    return redirect('user_login')  # Redirect to the login page


def user_register(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        conf_password = request.POST.get("conf_password")

        errors = {}

        if not username:
            errors['name'] = "Please enter your full username."

        if not email:
            errors['email'] = "Please enter your email."
        elif Register.objects.filter(email=email).exists():
            errors['email'] = "Email already exists."

        if not password:
            errors['password'] = "Please enter your password."

        if not conf_password:
            errors['conf_password'] = "Please confirm your password."
        elif password != conf_password:
            errors['conf_password'] = "Passwords do not match."

        if errors:
            context['errors'] = errors
            context['old'] = {
                'name': username,
                'email': email,
            }
            return render(request, 'user_panel/register.html', context)

        # Save user if no errors
        Register.objects.create(username=username, email=email, password=make_password(password))
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('Login')  # Ensure this name matches your URL pattern

    return render(request, 'user_panel/register.html')
@login_required(login_url='user_login')
def index(request):
    if 'user_id' not in request.session:
        return redirect('user_login')

    today = date.today()

    # Upcoming = today or future
    upcoming_classes = Classes.objects.filter(C_date__gte=today).order_by('C_date')

    # Scheduled = only today
    scheduled_classes = Classes.objects.filter(C_date=today).order_by('C_start_time')

    context = {
        'upcoming_classes': upcoming_classes,
        'scheduled_classes': scheduled_classes,
    }

    return render(request, "user_panel/index.html", context)

@login_required(login_url='user_login')
def avaliableclasses(request):
    if 'user_id' not in request.session:
        return redirect('user_login')
    
   
    
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        client_email = request.POST.get('client_email')
        classes_id = request.POST.get('classes') 

        try:
            selected_class_instance = Classes.objects.get(C_id=classes_id)
            
            if avaliable_classes.objects.filter(
                client_email=client_email, 
                classes=selected_class_instance
            ).exists():
                messages.error(request, 'You have already booked this specific class slot.')
                return redirect('Available_Classes')
                
            else:
                # Create the booking first
                booking = avaliable_classes.objects.create(
                    client_name=client_name,
                    client_email=client_email,
                    classes=selected_class_instance,
                    trainer=selected_class_instance.C_trainer 
                )
                
                # Prepare email content
                subject = "Slot Booking Confirmation - Fitness Studio"
                message = f"""
                <div style="font-family: Arial, sans-serif; font-size: 16px;">
                    <p>Hi {client_name},</p>
                    <p>Your booking is <strong>confirmed</strong>!</p>
                    <p><strong>Details:</strong></p>
                    <ul>
                        <li><strong>Class:</strong> {selected_class_instance.C_name}</li>
                        <li><strong>Trainer:</strong> {selected_class_instance.C_trainer.T_name}</li>
                        <li><strong>Date:</strong> {selected_class_instance.C_date.strftime('%A, %B %d, %Y')}</li>
                        <li><strong>Time:</strong> {selected_class_instance.C_start_time.strftime('%I:%M %p')} to {selected_class_instance.C_end_time.strftime('%I:%M %p')}</li>
                    </ul>
                    <p>Thank you for choosing <strong>Fitness Studio</strong>.</p>
                    <p>See you there!</p>
                </div>
                """
                
                try:
                    # Send email
                    email = EmailMessage(
                        subject=subject,
                        body=message,
                        from_email=settings.EMAIL_HOST_USER,
                        to=[client_email],  # Use the client_email from the form
                        reply_to=[settings.DEFAULT_FROM_EMAIL],
                    )
                    email.content_subtype = "html"  # Set content as HTML
                    email.send()
                    
                    messages.success(request, 'Slot booked successfully! Confirmation email sent.')
                except Exception as e:
                    # If email fails, still keep the booking but show warning
                    messages.warning(request, f'Slot booked but email could not be sent: {str(e)}')
                
                return redirect('Dashbord')
                
        except Classes.DoesNotExist:
            messages.error(request, "Selected class does not exist. Please try again.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
        
        return redirect('Available_Classes')
    
    classes = Classes.objects.values('C_name').distinct()
    return render(request, 'user_panel/available_classes.html', {'classes': classes})
@csrf_exempt
def get_trainers_by_class(request):
    class_name = request.GET.get('class_name')
    trainers = Trainer.objects.filter(classes__C_name=class_name).values('T_id', 'T_name')
    return JsonResponse(list(trainers), safe=False)

@csrf_exempt
def get_dates_by_class(request):
    class_name = request.GET.get('class_name')
    if class_name:
        dates = Classes.objects.filter(C_name=class_name).values('C_date').distinct().order_by('C_date')
        formatted_dates = [{'date': d['C_date'].strftime('%Y-%m-%d'), 'display': d['C_date'].strftime('%A, %B %d, %Y')} for d in dates]
        return JsonResponse(formatted_dates, safe=False)
    return JsonResponse([], safe=False)
@csrf_exempt
def get_trainers_and_times_by_class_and_date(request):
    class_name = request.GET.get('class_name')
    selected_date_str = request.GET.get('selected_date')
    
    if class_name and selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            class_instances = Classes.objects.filter(
                C_name=class_name,
                C_date=selected_date
            ).select_related('C_trainer').order_by('C_start_time')

            data = []
            for instance in class_instances:
                data.append({
                    'C_id': instance.C_id,
                    'T_id': instance.C_trainer.T_id,
                    'T_name': instance.C_trainer.T_name,
                    'C_start_time': instance.C_start_time.strftime('%I:%M %p'),
                    'C_end_time': instance.C_end_time.strftime('%I:%M %p'),
                    'C_description': instance.C_description
                })
            return JsonResponse(data, safe=False)
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)
    return JsonResponse([], safe=False)
@login_required(login_url='user_login')
def schedule(request):
    return render(request,'user_panel/schedule.html')


@csrf_exempt
def get_available_classes_events(request):
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
    