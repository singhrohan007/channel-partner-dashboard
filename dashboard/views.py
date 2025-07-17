from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Lead

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
