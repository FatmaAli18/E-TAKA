from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Order
from .forms import ProductForm
from .forms import OrderForm
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    orders_count = orders.count()
    products_count = products.count()
    generators_count = User.objects.all().count()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()
    context = {
        'orders': orders,
        'form': form,
        'products': products,
        'orders_count': orders_count,
        'generators_count': generators_count,
        'products_count': products_count,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
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


@login_required
def staff_detail(request, pk):
    generators = User.objects.get(id=pk)
    context = {
        'generators': generators,
    }

    return render(request, 'dashboard/staff_detail.html', context)


@login_required
def product1(request):
    items = Product.objects.all()  # Using ORM
    product_count = items.count()
    generators_count = User.objects.all().count()
    orders_count = Order.objects.all().count()

    if request.method == 'POST':
        form = ProductForm(request.POST)
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
        return redirect('product')
    context = {
        'item': item
    }
    return render(request, 'dashboard/product-delete', context)


@login_required
def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('user-product')
    else:
        form = ProductForm(instance=item)

    context = {
        'form': form
    }
    return render(request, 'dashboard/product-update', context)


def home(request):
    return render(request, 'users/home.html')


def about(request):
    return render(request, 'users/about.html')


@login_required
def order(request):
    orders = Order.objects.all()
    orders_count = orders.count()
    generators_count = User.objects.all().count()
    product_count = Product.objects.all().count()
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=item)
        if form.is_valid():
            form.save()

    else:
        form = OrderForm()
        context = {
            'orders': orders,
            'generators_count': generators_count,
            'orders_count': orders_count,
            'product_count': product_count,
            'form': form,
        }

    return render(request, 'dashboard/order.html', context)


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


def profile(request):
    return render(request, 'users/profile.html')


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
