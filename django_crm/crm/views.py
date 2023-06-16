from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import Signup_form, RecordForm
from .models import Record


# Create your views here.
def index(request):
    records = Record.objects.all()
    # Check if the user is logged in
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # auth
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in")
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect("index")
    else:
        return render(request, "index.html", {"records": records})


def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out")
    return redirect("index")


def register(request):
    if request.method == "POST":
        form = Signup_form(request.POST)
        if form.is_valid():
            form.save()
            # authenticate and log in
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered")
            return redirect("index")
    else:
        form = Signup_form()
    return render(request, "register.html", {"form": form})

def record(request, pk):
    if request.user.is_authenticated:
        # lookup for record
        customer_record = Record.objects.get(id=pk)
        return render(request, "record.html", {"customer_record": customer_record})
    else:
        messages.info(request, "You must be logged in to view this record")
        return redirect("index")
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_by_customer = Record.objects.get(id=pk)
        delete_by_customer.delete()
        messages.success(request, "Record deleted successfully")
        return redirect("index")
    
    else:
        messages.info(request, "You must be logged in to delete this record")
        return redirect("index")
    
def add_record(request):
    form = RecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Record added')
                return redirect('index')
        return render(request, "add.html", { 'form': form } )
    else:
        messages.info(request, "You must be logged in to add this record")
        return redirect("index")
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = RecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated successfully')
            return redirect('index')
        return render(request, "update.html", { 'form': form } )
    else:
        messages.info(request, "You must be logged in to add this record")
        return redirect("index")



    