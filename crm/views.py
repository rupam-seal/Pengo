from multiprocessing import context
from django.shortcuts import render, redirect
from crm.decorators import admin_only, allowed_user, unauthenticated_user

from crm.forms import CreateUserForm, CustomerForm, OrderForm, UpdateCustomerForm, CreateProductForm

from .models import *
from .filters import ProductFilter, OrderFilter

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages

from django.contrib.auth.models import Group

# Create your views here.
# ---------- User authorization and authentication ---------- #
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')    
            messages.success(request, 'Account created for '+username)
            return redirect('dashboard')

    context = {
        'form':form,
    }

    return render(request, 'crm/authentication/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')    
        else:
            messages.info(request, 'Username Or Password is incorrect!')

    context = {}

    return render(request, 'crm/authentication/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

# ---------- Admin Access Pages ---------- #
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@admin_only
def dashboard(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    paid_orders = orders.filter(status='Paid').count()
    pending_orders = orders.filter(status='Pending').count()

    context = {
        'orders':orders,
        'customers':customers,
        'total_orders':total_orders,
        'paid_orders':paid_orders,
        'pending_orders':pending_orders,
    }

    return render(request, 'crm/admin/dashboard.html', context)

@login_required(login_url='login')
@allowed_user(allowed=['admin'])
def products(request):
    products = Product.objects.all()

    form = CreateProductForm()

    if request.method == "POST":
        form = CreateProductForm(request.POST, instance=Product)
        if form.is_valid():
            form.save()
            return redirect("products")
    
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs

    context = {
        'products':products,
        'filter':filter,
        'form':form,
    }

    return render(request, 'crm/admin/products.html', context)

@login_required(login_url='login')
@allowed_user(allowed=['admin'])
def viewCustomer(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()

    total_orders = orders.count()

    filter = OrderFilter(request.GET, queryset=orders)
    orders = filter.qs

    context = {
        'customer':customer,
        'orders':orders,
        'total_orders':total_orders,
        'filter':filter,
    }

    return render(request, 'crm/admin/viewCustomer.html', context)

@login_required(login_url='login')
@allowed_user(allowed=['admin'])
def updateCustomer(request, id):
    customer = Customer.objects.get(id=id)

    form = UpdateCustomerForm(instance=customer)

    if request.method == 'POST':
        form = UpdateCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {
        'form':form,
    }

    return render(request, 'crm/admin/updateCustomer.html', context)

@login_required(login_url='login')
@allowed_user(allowed=['admin'])
def createOrder(request, id):
    customer = Customer.objects.get(id=id)

    form = OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {
        'form':form
    }

    return render(request, 'crm/admin/orderForm.html', context)

@login_required(login_url='login')
@allowed_user(allowed=['admin'])
def createDashboardOrder(request):
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    
    context = {
        'form':form,
    }

    return render(request, 'crm/admin/orderForm.html', context)

@login_required(login_url='login')
@allowed_user(allowed=['admin'])
def updateOrder(request, id):
    orders = Order.objects.get(id=id)

    form = OrderForm(instance=orders)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=orders)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {
        'form':form,
    }
    return render(request, 'crm/admin/orderForm.html', context)

@login_required(login_url='login')
@allowed_user(allowed=['admin'])
def removeOrder(request, id):
    order = Order.objects.get(id=id)

    if request.method == 'POST':
        order.delete()
        return redirect('dashboard')

    context = {
        'order':order,
    }
    return render(request, 'crm/admin/removeOrder.html', context)

# --------- User Access Pages ---------- #
@login_required(login_url='login')
@allowed_user(allowed=['customer'])
def customerDashboard(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    paid_orders = orders.filter(status='Paid').count()
    pending_orders = orders.filter(status='Pending').count()

    context = {
        'orders':orders,
        'total_orders':total_orders,
        'paid_orders':paid_orders,
        'pending_orders':pending_orders,
    }

    return render(request, 'crm/customer/customerDashboard.html', context)

@login_required(login_url='login')
@allowed_user(allowed=['customer'])
def profile(request):
    customer = request.user.customer

    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            username = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            user = User.objects.get(id=request.user.id)
            user.username = username
            user.email = email
            user.save()
            form.save()

    context = {
        'form':form,
    }
    return render(request, 'crm/customer/profile.html', context)