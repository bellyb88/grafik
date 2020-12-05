from django.urls import path
from . import views

app_name = 'generator'
urlpatterns = [
    path('<int:month>/<int:year>', views.strona_glowna, name='strona_glowna'),
]