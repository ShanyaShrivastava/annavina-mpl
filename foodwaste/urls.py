from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('find_foodmarts/',views.find_foodmarts,name=''),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login_view'),
    path('logout',views.logout_view,name='logout'),
    path('foodmart/', views.user_foodmart_list, name='foodmart_list'),
    path('foodmart_add/', views.foodmart_add, name='foodmart_add'),
    path('foodmart/edit/',views.foodmart_edit, name='foodmart_edit'),
    path('map', views.map, name='map'),
    path('about/',views.about,name='about'),
    path('getf/',views.get_foodmarts,name='getfoodmart'),
    path('foodmart/',views.sortedfoodmart,name='foodmart'),
    path('markdelivered/',views.markdelivered,name='markdelivered'),
    # path('user_foodmarts/', views.user_foodmart, name='user_foodmart_list'),
]
