from django.shortcuts import render

def acceuil(request):
    return render(request, 'acceuil/acceuil.html')  # Rediriger vers la page d'accueil

def acceuilCte(request):
    return render(request, 'acceuil/acceuilCte.html')  # Rediriger vers la page d'accueil

def test_acceuil(request):
    return render(request, 'acceuil/test.html')  # Rediriger vers la page d'accueil


def home1(request):
    return render(request, 'myapp/home1.html')  # Rediriger vers la page d'accueil


def chart(request):
    return render(request, 'acceuil/transaction_chart.html')  # Rediriger vers la page d'accueil

def list_transaction(request):
    return render(request, 'acceuil/liste_transaction.html')  # Rediriger vers la page d'accueil


def profil(request):
    return render(request, 'myapp/profil.html')  # Rediriger vers la page d'accueil
