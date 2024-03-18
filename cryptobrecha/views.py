from django.views.generic.base import View
from django.shortcuts import render
from .models import Bancos, Comerciante


def usuarios_registrados(request):
    usuarios = Comerciante.objects.all()
    bancos = Bancos.objects.all()

    return render(request,'pages/home/usuarios_registrados.html', {'usuarios': usuarios, 'bancos': bancos})


class ServicesDetailView(View):
    def get(self, request, *args, **kwargs):
        context={

        }
        return render(request,'dashboard/pages/servicios/dashboard.html', context)

