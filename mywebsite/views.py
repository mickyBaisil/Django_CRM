from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout 
from django.contrib import messages
from .forms import SignUpForm , AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()
    # check to see if logging in 
    if request.method == "POST":
        Username = request.POST["username"] # from home.html name = "username"
        Password = request.POST["password"] # from home.html name = "password"
        # Authenticate
        User = authenticate(request, username = Username , password = Password)
        if User:
            login(request,User)
            messages.success(request, "YOU ARE LOGGED IN")
            return redirect("home")
        else:
            messages.success(request, "ERROR! PLEASE TRY AGAIN")
            return redirect("home")
    else:
        return render(request, 'home.html', {'records':records})


def logout_user(request):
    logout(request)
    messages.success(request, "YOU ARE LOGGED OUT")
    return redirect("home")

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username= username, password = password)
            login(request, user)
            messages.success(request, "Successfully Registered")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        # look up the record
        customer_record = Record.objects.get(id = pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "MUST LOGIN TO VIEW THE RECORDS PAGE")
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        record_to_delete = Record.objects.get(id = pk)
        record_to_delete.delete()
        messages.success(request, "CUSTOMER RECORD DELETED SUCCESSFULLY")
        return redirect('home')
    else:
        messages.success(request, "MUST LOGIN TO VIEW THE RECORDS PAGE")
        return redirect('home')
    
def add_record(request):
    if request.user.is_authenticated:
        form = AddRecordForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                add_customer = form.save()
                messages.success(request, "CUSTOMER RECORD ADDED SUCCESSFULLY")
                return redirect('home')
    else:
        messages.success(request, "MUST LOGIN TO VIEW THE RECORDS PAGE")
        return redirect('home')
    
    return render(request, 'add_record.html', {'form':form})

def update_record(request, pk):
    if request.user.is_authenticated:
        record_to_update = Record.objects.get(id = pk)
        form = AddRecordForm(request.POST or None, instance = record_to_update)
        if form.is_valid():
            form.save()
            messages.success(request, "RECORD UPDATED SUCCESSFULLY")
            return redirect('home')
    else:
        messages.success(request, "MUST LOGIN TO VIEW THE RECORDS PAGE")
        return redirect('home')
    
    return render(request, 'update_record.html', {'form':form})