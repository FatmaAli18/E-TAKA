from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
import json
from .models import Product, Order, Profile
from .forms import ProductForm
from .forms import OrderForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator



# Create your views here.

def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    orders_count = orders.count()
    products_count = products.count()
    generators_count = User.objects.all().count()
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page', 1)
    orders = paginator.get_page(page_number)

    context = {
        'orders': orders,
        'products': products,
        'orders_count': orders_count,
        'generators_count': generators_count,
        'products_count': products_count,
    }
    return render(request, 'dashboard/index.html', context)


@login_required(login_url='login')
def staff(request):
    generators = User.objects.all()
    generators_count = generators.count()
    order_count = Order.objects.all()
    product_count = Product.objects.all().count()
    context = {
        'generators': generators,
        'generators_count': generators_count,
        'order_count': order_count,
        'product_count': product_count

    }
    return render(request, 'dashboard/staff.html', context)


@login_required(login_url='login')
def staff_detail(request, pk):
    generators = User.objects.get(id=pk)
    context = {
        'generators': generators,
    }

    return render(request, 'dashboard/staff_detail.html', context)


@login_required(login_url='login')
def product1(request):
    items = Product.objects.all()  # Using ORM
    product_count = items.count()
    generators_count = User.objects.all().count()
    orders_count = Order.objects.all().count()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
            return redirect('dashboard-product')

    else:
        form = ProductForm()
    context = {
        'items': items,
        'form': form,
        'generators_count': generators_count,
        'orders_count': orders_count,
        'product_count': product_count,

    }
    return render(request, 'dashboard/product.html', context)


@login_required
def product_delete(request, pk):
    from .models import Product
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')
    context = {
        'item': item
    }
    return render(request, 'dashboard/product-delete.html', context)



@login_required(login_url='login')
def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=item)

    context = {
        'form': form
    }
    return render(request, 'dashboard/product-update.html', context)


def home(request):
    return render(request, 'users/home.html')


def about(request):
    return render(request, 'users/about.html')


@login_required(login_url='login')
def order(request):
    orders = Order.objects.all().order_by('-date')
    orders_count = orders.count()
    generators_count = User.objects.all().count()
    product_count = Product.objects.all().count()
    total = sum([i.name.price * i.order_quantity  for i in orders])
    
    products = Product.objects.filter(quantity__gte=1)
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page', 1)
    products = paginator.get_page(page_number)

    
    if request.user.is_authenticated:
        customer = request.user
    profile = Profile.objects.get(staff=customer)
    phone_number = profile.phone
    
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.staff = customer
            amount = order.order_quantity * order.name.price
            print(amount)
            mpesa = requests.post("http://127.0.0.1:8000/mpesa/submit/", data={"phone_number": phone_number,"amount": amount})  
            messages.success(request, "Check Your Phone and Input your Mpesa PIN to make payment.")
            order.save()
            product = Product.objects.get(id=order.name.id)
            product.quantity =  product.quantity - order.order_quantity
            product.save()

    else:
        form = OrderForm()
    context = {
            'orders': orders,
            'products': products,
            'generators_count': generators_count,
            'orders_count': orders_count,
            'product_count': product_count,
            'total': total,
            'form': form,
    }

    return render(request, 'dashboard/order.html', context)

def confirm_order(request, pk):
    order = Order.objects.filter(id=pk)
    order.status = 'Delivered'
    
    for item in order:
        item.status = 'Delivered'
        item.save()
        messages.success(request, "Order Updated Successfully")
        
    return redirect('user-profile')


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {username} . Continue to Log In')
            return redirect('login')
    else:
        form = CreateUserForm()
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


def login(request):
    return render(request, 'users/login.html')


def logout_request(request):
    messages.success(request, "You have successfully logged out.")
    return redirect("login")

@login_required(login_url='login')
def profile(request):
    customer = request.user
    orders = Order.objects.filter(staff=customer)
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page', 1)
    orders = paginator.get_page(page_number)
    return render(request, 'users/profile.html', {'orders':orders})


@login_required(login_url='login')
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form: ProfileUpdateForm = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        user_form.save()
        profile_form.save()
        return redirect('user-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/profile_update.html', context)
