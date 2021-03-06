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
    path('plan_delete/<pk>', views.PlanDelete.as_view(), name = 'plan_delete'),

    path('regula_create/', views.RegulaCreate.as_view(), name='regula_create'),
    path('regula_update/<pk>', views.RegulaUpdate.as_view(), name='regula_update'),
    path('regula_delete/<pk>', views.RegulaDelete.as_view(), name='regula_delete'),

    path('pracownik_detail/<pk>', views.PracownikDetail.as_view(), name='pracownik_detail'),
    path('plan_update/<pk>/pracownik_create/', views.PracownikCreate.as_view(), name='pracownik_create'),
    path('pracownik_update/<pk>', views.PracownikUpdate.as_view(), name='pracownik_update'),
    path('pracownik_delete/<pk>', views.PracownikDelete.as_view(), name='pracownik_delete'),

    path('pracownik/<pk>/prosba_update/', views.ProsbaUpdate.as_view(), name='prosba_update'),
    path('pracownik/<pk>/urlop_update/', views.UrlopUpdate.as_view(), name='urlop_update'),

]