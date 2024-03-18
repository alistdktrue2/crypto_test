from django.urls import path
from .views import usuarios_registrados,ServicesDetailView

app_name="cryptobrecha"

urlpatterns = [
    # Otras rutas aquí...
    path('usuarios-registrados/', usuarios_registrados, name='usuarios_registrados'),
    path('', ServicesDetailView.as_view(), name='dashboard'),
    

]