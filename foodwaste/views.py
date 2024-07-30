from django.http import JsonResponse
from .models import foodmart
from geopy.distance import great_circle
from django.shortcuts import render, redirect
from .forms import SignUpForm,LoginForm
from .models import foodmart
from geopy.geocoders import Nominatim
from .forms import SearchFoodMartForm,FoodmartForm
import geopy.distance
from django.contrib.auth import authenticate, login as auth_login,logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
import geopy.distance
from django.db.models import Sum, IntegerField
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404

def home(request):
    total_quantity = foodmart.objects.filter(
        is_delivered=True
    ).annotate(
        quantity_int=Cast('quantity', IntegerField())
    ).aggregate(total_quantity=Sum('quantity_int'))['total_quantity'] or 0
    foodmarts = foodmart.objects.all()
    return render(request, 'home.html', {'total_quantity': total_quantity,'foodmarts':foodmarts})


def find_foodmarts(request):
    if request.method == 'GET':
        user_lat = request.GET.get('latitude')
        user_lon = request.GET.get('longitude')

        if user_lat is None or user_lon is None:
            return render(request, 'foodmarts_list.html', {'error': 'Coordinates not provided'})

        try:
            user_lat = float(user_lat)
            user_lon = float(user_lon)
        except ValueError:
            return render(request, 'foodmarts_list.html', {'error': 'Invalid coordinates'})

        user_coords = (user_lat, user_lon)

        foodmarts = []
        for fm in foodmart.objects.all():
            fm_coords = (fm.lat, fm.lon)
            distance = geopy.distance.great_circle(user_coords, fm_coords).kilometers
            foodmarts.append({
                'name': fm.name,
                'distance': distance,
                'description':fm.description
            })

        foodmarts.sort(key=lambda x: x['distance'])

        return render(request, 'sortedfoodmartlist.html', {'foodmarts': foodmarts})

    return render(request, 'home.html', {'error': 'Invalid request method'})


def register_view(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Store user information in session
                request.session['username'] = username
                request.session['user_id'] = user.id
                if user.is_admin:
                    return redirect('foodmart_list') 
                else:
                    return redirect('') 
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})

@login_required
def user_foodmart_list(request):
    foodmarts = foodmart.objects.filter(created_by=request.user)
    return render(request, 'foodmart_list.html', {'foodmarts': foodmarts})

@login_required
def foodmart_add(request):
    if request.method == 'POST':
        form = FoodmartForm(request.POST)
        if form.is_valid():
            foodmart_instance = form.save(commit=False)
            foodmart_instance.created_by = request.user
            foodmart_instance.save()
            return redirect('foodmart_list')
    else:
        form = FoodmartForm()
    
    return render(request, 'foodmart_form.html', {'form': form})


def map(request):
    foodmarts = foodmart.objects.all()
    return render(request,'map.html',{'foodmarts' : foodmarts})

def about(request):
    return render(request,'about.html')


def foodmart_edit(request):
    foodmart_instance = foodmart.objects.filter(created_by=request.user).first()

    if not foodmart_instance:
        return redirect('foodmart_list')

    if request.method == 'POST':
        form = FoodmartForm(request.POST, instance=foodmart_instance)
        if form.is_valid():
            form.save()
            return redirect('foodmart_list')
    else:
        form = FoodmartForm(instance=foodmart_instance)
    
    return render(request, 'foodmart_form.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return render(request,'logout.html') 
    return redirect('home') 

def get_foodmarts(request):
    return render(request,'get_foodmarts.html')

def sortedfoodmart(request):
    return render(request,'sortedfoodmartlist.html')

@login_required
def markdelivered(request):
    foodmart_instance = foodmart.objects.filter(created_by=request.user, is_delivered=False).first()
    
    if not foodmart_instance:
        return redirect('home') 

    if request.method == 'POST':
        if not foodmart_instance.is_delivered:
            foodmart_instance.is_delivered = True
            foodmart_instance.save()
        return redirect('foodmart_list')
    return render(request, 'confirm_delivery.html', {'foodmart': foodmart_instance})

