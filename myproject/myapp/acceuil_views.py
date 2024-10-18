from django.shortcuts import render

def acceuil(request):
    return render(request, 'acceuil/acceuil.html')  # Rediriger vers la page d'accueil

def acceuilCte(request):
    return render(request, 'acceuil/acceuilCte.html')  # Rediriger vers la page d'accueil