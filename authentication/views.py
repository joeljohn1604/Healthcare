from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, AddressForm
from .models import User

def signup(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, request.FILES)
        address_form = AddressForm(request.POST)
        
        if user_form.is_valid() and address_form.is_valid():
            user = user_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()
            
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            return redirect('dashboard')
    else:
        user_form = UserRegistrationForm()
        address_form = AddressForm()
    
    return render(request, 'authentication/signup.html', {
        'user_form': user_form,
        'address_form': address_form
    })

def user_login(request):  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'authentication/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'authentication/login.html')

@login_required
def dashboard(request):
    user = request.user
    context = {
        'user': user,
        'address': user.address if hasattr(user, 'address') else None
    }
    
    if user.is_patient():
        return render(request, 'authentication/patient_dashboard.html', context)
    elif user.is_doctor():
        return render(request, 'authentication/doctor_dashboard.html', context)


def home(request):
    return render(request, 'authentication/home.html')