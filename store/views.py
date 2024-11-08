from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserIntoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

# Tim kiem
def search(request):
    # Determine if they fill out the form
    if request.method == "POST":
        searched = request.POST['searched']
        # Query the products DB Models
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        # Test for null
        if not searched:
            messages.success(request, "Không tìm thấy sản phẩm, vui lòng thử lại")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})

# Cap nhat thong tin tai khoan
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id = request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id = request.user.id)
        form = UserIntoForm(request.POST or None, instance = current_user)

        shipping_form = ShippingForm(request.POST or None, instance= shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            # Save orginal form
            form.save()
            # Save shipping form
            shipping_form.save()
            messages.success(request, "Cập nhật thông tin tài khoản thành công")
            return redirect('home')
        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:  
        messages.success(request, "Cần đăng nhập để thực hiện")
        return redirect('home')

# Cap nhat mat khau
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did the fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Mật khẩu đã được cập nhật")
                #login(request, current_user)
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_user')
            # Do stuff
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, "Bạn cần đăng nhập trước")
        return redirect('home')

# Cap nhat thong tin user
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance = current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "Cập nhật tài khoản thành công")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:  
        messages.success(request, "Cần đăng nhập để thực hiện")
        return redirect('home')
    

# Gio hang
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})    

def category(request, foo):
    #Replace Hyphens with Spaces
    foo = foo.replace('-', ' ') 
    try:
        #Look up The Category 
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category })   
    except:
        messages.success(request, ("Category doesn't exist"))
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product' : product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products' : products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)

            # Do some shopping
            current_user = Profile.objects.get(user__id = request.user.id)
            # Get cart from DB
            saved_cart = current_user.old_cart
            # Convert db string to python dictionary   
            if saved_cart:
                converted_cart = json.loads(saved_cart)
            # Add load cart dictionary to session
            # Get the cart
                cart = Cart(request)

            for key, value in converted_cart.items():
                cart.db_add(product=key, quantity=value)


            messages.success(request, ("Log in success"))
            return redirect('home')
        else:
            messages.success(request, ("Log in is not success, please try again"))
            return redirect('login')
    else:
            return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been log out"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, ("Created Successfully - Please finish information"))
            return redirect('home')
        else:
            messages.success(request, ("There are problem, please try again"))
        return redirect('update_info')
    else:
        return render(request, 'register.html', {'form': form })
