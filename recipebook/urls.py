from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from recipes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/add/', views.recipe_add, name='recipe_add'),
    path('recipes/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
]