from django.shortcuts import render,redirect
from .models import Product,Category
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm,UpdateUserForm
def update_user(request):
    if request.user.is_authenticated :
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request,current_user)
            messages.success(request,"Profile successfully updated")
            return redirect('home')
        return render(request,"update_user.html",{"user_form":user_form})
    else:
        messages.success(request,"You must be logged in to access this page")
        return redirect('home')

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})
def category(request,foo):
    foo = foo.replace('-'," ")
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request,'category.html',{'products': products, 'category' : category})
    except:
        messages.success(request,("This Category does not exist"))
        return redirect('home')
def category_summary(request):
    categories = Category.objects.all()
    return render(request,"category_summary.html",{'categories': categories})
def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products})
def about(request):
    return render(request,'about.html',{})
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("You have been logged in successfully"))
            return redirect('home')
        else:
            messages.success(request,("There was an error logging you in. Please Try Again"))
            return redirect('login')
    else:
        return render(request,'login.html',{})
def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out successfully"))
    return redirect('home')
def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("You have registered successfully"))
            return redirect('home')
        else:
            messages.success(request,("There was an error.Please Try Again"))
            return redirect('register')
    
    return render(request,'register.html',{'form':form})