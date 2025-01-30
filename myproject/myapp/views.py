from multiprocessing.connection import Client
from django.shortcuts import render, redirect,get_object_or_404 # type: ignore
from django.core.mail import send_mail # type: ignore
from django.conf import settings # type: ignore
from django.shortcuts import render, get_object_or_404 # type: ignore
from django.contrib.auth import authenticate, login # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from .models import Sit_matrim
from .models import Contribuable 
from .models import Operateur
import logging
import random
from django.contrib.auth.hashers import check_password, make_password # type: ignore

from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
import requests # type: ignore

from django import forms # type: ignore
import os
from datetime import datetime

from django.core.exceptions import ValidationError # type: ignore
logger = logging.getLogger(__name__)
from .models import Genre
from django.contrib import messages # type: ignore
from django.http import JsonResponse # type: ignore
from .models import FokontanyView
from .forms import ContribuableForm
from datetime import datetime, timedelta
# from rest_framework.views import APIView
# from rest_framework.response import Response
from rest_framework.exceptions import ValidationError # type: ignore

@api_view(['GET'])
def get_all_operateurs(request):
    # Récupérer tous les opérateurs
    operateurs = Operateur.objects.all()
    # Sérialiser les opérateurs en un format JSON
    data = [{"cin": operateur.cin, "contact": operateur.contact} for operateur in operateurs]
    return Response(data, status=status.HTTP_200_OK)



def valider_cin_et_contact(cin, contact):
    # URL de l'API où les opérateurs sont récupérés
    url = 'http://127.0.0.1:8000/get_all_operateurs/'  
    # Faire la requête à l'API pour récupérer tous les opérateurs
    response = requests.get(url)

    if response.status_code == 200:
        operateurs = response.json()
        
        for operateur in operateurs:
            if operateur['cin'] == cin and operateur['contact'] == contact:
                return True  # Si le CIN et le contact correspondent, on retourne True
        
        # Si aucun opérateur avec ce CIN et contact n'a été trouvé, lever une exception
        raise ValidationError("❌Le CIN ou le contact ne correspond pas.")
    else:
        raise ValidationError("Erreur lors de la validation avec l'API.")


def envoyer_email(email, prenif, mot_de_passe):
    """Envoie un email avec les informations d'inscription."""
    subject = 'Inscription réussie'
    message = (
        f"Vous êtes inscrit en tant que contribuable,\n"
        f"votre PRE N° d'Immatriculation Fiscale est : {prenif} "
        f"et votre mot de passe est : {mot_de_passe}.\n"
        "Merci d'utiliser ces informations pour vous connecter à votre compte."
    )
    
    send_mail(
        subject,
        message,
        f"immatriculationenligne <{settings.DEFAULT_FROM_EMAIL}>",
        [email],
        fail_silently=False,
    )



def envoyer_sms(contact, prenif, mot_de_passe):
    """Envoie un SMS avec les informations d'inscription."""
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message_body = (
        f"Félicitations, votre inscription est réussie !\n"
        f"Votre NIF est : {prenif}\n"
        f"Votre mot de passe est : {mot_de_passe}\n"
        f"Connectez-vous pour accéder à votre compte."
    )
    
    try:
        client.messages.create(
            body=message_body,
            from_=settings.TWILIO_PHONE_NUMBER,  # Numéro Twilio fourni par le service
            to=contact  # Numéro du bénéficiaire
        )
        return True
    except Exception as e:
        raise ValidationError(f"Échec de l'envoi du SMS : {str(e)}")


def login(request):
    if request.method == 'POST':
        prenif = request.POST['prenif']
        password = request.POST['password']
        
        try:
            # Rechercher un utilisateur avec l'email et vérifier le mot de passe
            contribuable = Contribuable.objects.get(propr_nif=prenif)
            if contribuable.mot_de_passe == password:
                # Si l'email et le mot de passe correspondent, rediriger vers l'authentification à 2 facteurs
                request.session['contribuable_id'] = contribuable.id  # Stocker l'utilisateur pour la prochaine étape
                request.session['prenif'] = contribuable.propr_nif
                request.session['email'] = contribuable.email
                return redirect('D_authentification')  # Redirigez vers la vue pour la confirmation 2FA
            else:
                # Si le mot de passe est incorrect, afficher une erreur
                return render(request, 'myapp/login.html', {'error': 'Mot de passe incorrect'})
        except Contribuable.DoesNotExist:
            # Si l'utilisateur n'existe pas, afficher une erreur
            return render(request, 'myapp/login.html', {'error': 'Email non trouvé'})
    return render(request, 'myapp/login.html')


def search_province(request):
    query = request.GET.get('query', '')
    if query:
        data = FokontanyView.objects.filter(fkt_desc__icontains=query).values(
            'fkt_no', 'fkt_desc', 'wereda_desc', 'locality_desc', 
            'city_name', 'parish_name'
        )
        
        formatted_data = [
            {
                'label': f"{item['city_name']} => {item['parish_name']} => {item['locality_desc']} => {item['wereda_desc']} => {item['fkt_desc']}",
                'fkt_no': item['fkt_no'],
                'city_name': item['city_name'],
                'parish_name': item['parish_name'],
                'locality_desc': item['locality_desc'],
                'wereda_desc': item['wereda_desc'],
                'fkt_desc': item['fkt_desc']
            }
            for item in data
        ]
        
        return JsonResponse(formatted_data, safe=False)

def deconnexion(request):
    # Supprimez l'ID du contribuable de la session pour déconnecter l'utilisateur
    if 'id_contribuable' in request.session:
        del request.session['id_contribuable']
        
    # Redirigez vers la page de connexion (ou autre page de votre choix)
    return redirect('login')  # Remplacez 'login' par le nom de la vue de la page de connexion

def mdp_oubliee(request):
    return render(request, 'myapp/mdp_oubli.html')  # Rediriger vers la page d'accueil


def generate_code():
    return str(random.randint(100000, 999999))


def D_authentification(request):
    if request.method == 'POST':
        if 'send_code' in request.POST:
            # Récupérer l'email de l'utilisateur depuis la session
            email = request.session.get('email')  # Utilisez cet email pour renvoyer le code
            code = generate_code()
            request.session['auth_code'] = code  # Stocker le code dans la session
            request.session['code_expiration'] = (datetime.now() + timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S")
            # Envoyer le code par email à l'utilisateur
            send_mail(
                'Votre code de vérification',
                f'Votre code de vérification est : {code}',
                f"immatriculationenligne <{settings.DEFAULT_FROM_EMAIL}>",  # Adresse de l'expéditeur
                [email],  # Destinataire (email de l'utilisateur)
                fail_silently=False,
            )
            
            # Afficher le message après l'envoi du code et démarrer le compte à rebours
            return render(request, 'myapp/D_authentification.html', {
                'message': 'Code envoyé. Veuillez vérifier votre email.',
                'start_timer': True  # Indicateur pour démarrer le chronomètre
            })
        
        elif 'validate_code' in request.POST:
            entered_code = request.POST.get('code')
            correct_code = request.session.get('auth_code')
            expiration_time = request.session.get('code_expiration')
            
            # Vérifier si le code a expiré
            if datetime.now() > datetime.strptime(expiration_time, "%Y-%m-%d %H:%M:%S"):
                return render(request, 'myapp/D_authentification.html', {'error': 'Le code a expiré. Renvoyez un nouveau code.'})
            
            # Vérifier si le code entré est correct
            if entered_code == correct_code:
                return redirect('acceuil')  # Rediriger vers la page d'accueil
            else:
                return render(request, 'myapp/D_authentification.html', {'error': 'Le code est incorrect. Veuillez réessayer.'})

    return render(request, 'myapp/D_authentification.html')

def GenererPRENIFetMdp(cin):
    # Vérifiez que le CIN contient exactement 12 caractères
    if len(cin) != 12:
        raise ValueError("Le CIN doit contenir exactement 12 caractères pour générer le PRENIF et le mot de passe.")
    
    # Générer le PRENIF (Les 9 derniers chiffres du CIN et le premier est la somme des 3 premiers chiffres)
    derniere_partie_cin = cin[-9:]
    somme_trois_premiers = sum(int(digit) for digit in derniere_partie_cin[:3])

    # Si la somme est à deux chiffres, additionner encore
    while somme_trois_premiers >= 10:
        somme_trois_premiers = sum(int(digit) for digit in str(somme_trois_premiers))

    prenif = str(somme_trois_premiers) + derniere_partie_cin

    # Générer le mot de passe en additionnant 2 par 2 les chiffres du CIN (6 caractères au total)
    mot_de_passe = ''
    for i in range(0, 12, 2):  # Parcourir les chiffres du CIN par paires
        somme_pair = int(cin[i]) + int(cin[i + 1])
        # Ajouter le dernier chiffre de la somme à mot_de_passe
        mot_de_passe += str(somme_pair % 10)

    return prenif, mot_de_passe

