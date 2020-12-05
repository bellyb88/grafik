from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'front'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # alternative way to include authentication views
    # path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),

    path('plan_create/', views.PlanCreate.as_view(), name = 'plan_create'),
    path('plan_update/<pk>', views.PlanUpdate.as_view(), name = 'plan_update'),
]