from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Lead
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Lead
from .forms import LeadForm
from django.http import JsonResponse
from django.contrib import messages

def is_admin(user):
    return user.is_superuser  

def is_superuser(user):
    return user.is_superuser  



def signup_view(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, email=username, password=password)
            return redirect('login')
    return render(request, 'dashboard/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'dashboard/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Lead

@login_required
def dashboard_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        college = request.POST['college']
        course = request.POST['course']
        

        Lead.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            college=college,
            course=course
            
        )
        return redirect('dashboard')

    tab = request.GET.get('tab', 'all')
    college_filter = request.GET.get('college')

    # Tab logic
    if tab == 'pending':
        leads = Lead.objects.filter(user=request.user, status='pending')
    elif tab == 'pushed':
        leads = Lead.objects.filter(user=request.user, status='pushed')  # Or leave empty to show message
    elif tab == 'college':
        if college_filter:
            leads = Lead.objects.filter(user=request.user, college=college_filter)
        else:
            leads = Lead.objects.filter(user=request.user)
        colleges = Lead.objects.filter(user=request.user).values_list('college', flat=True).distinct()
    else:
        leads = Lead.objects.filter(user=request.user)

    context = {
        "email": request.user.email,
        "leads": leads,
        "tab": tab,
    }

    if tab == 'college':
        context["colleges"] = colleges
        context["selected_college"] = college_filter

    return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url='login')
def dashboard(request):
    tab = request.GET.get('tab', 'pending')  # Default tab is 'pending'

    if tab == 'all':
        leads = Lead.objects.all()
    elif tab == 'pending':
        leads = Lead.objects.filter(status='pending')
    elif tab == 'pushed':
        leads = Lead.objects.filter(status='pushed')
    elif tab == 'college':
        leads = Lead.objects.order_by('college')  # Or apply filtering/grouping as needed
    else:
        leads = Lead.objects.none()

    return render(request, 'dashboard.html', {
        'leads': leads,
        'tab': tab,
    })





@user_passes_test(is_admin)
def admin_dashboard(request):
    leads = Lead.objects.all().order_by('-created_at')
    return render(request, 'dashboard/admin_dashboard.html', {'leads': leads})


@user_passes_test(is_superuser)
def update_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            print(form.errors)  # Add this to debug invalid form
    return JsonResponse({'success': False})

@user_passes_test(is_superuser)
def delete_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == 'POST':
        lead.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})



def admin_login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not authorized.')
            return redirect('admin_login')

    return render(request, 'dashboard/admin_login.html')