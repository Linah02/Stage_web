from django.shortcuts import render, redirect,get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .models import Sit_matrim
from .models import Contribuable 
from .models import Operateur
import logging
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests

from django import forms
import os
from datetime import datetime

from django.core.exceptions import ValidationError
logger = logging.getLogger(__name__)
from .models import Genre
from django.contrib import messages
from django.http import JsonResponse
from .models import FokontanyView
from .forms import ContribuableForm
from datetime import datetime, timedelta
# from rest_framework.views import APIView
# from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

# def home(request):
#     genres = Genre.objects.all()  # Récupère tous les genres
#     situations = Sit_matrim.objects.all()  # Récupère toutes les situations matrimoniales

#     if request.method == 'POST':
#         nom = request.POST.get('nom')
#         situation_matrimoniale = request.POST.get('situation_matrimoniale')
#         prenom = request.POST.get('prenom')
#         date_naissance = request.POST.get('date_naissance')
#         genre = request.POST.get('genre')
#         lieu_naissance = request.POST.get('lieu_naissance')

#           # Stockage des données dans la session
#         request.session['form_data'] = {
#             'nom': nom,
#             'situation_matrimoniale': situation_matrimoniale,
#             'prenom': prenom,
#             'date_naissance': date_naissance,
#             'genre': genre,
#             'lieu_naissance': lieu_naissance,
#         }
#         return redirect('form_part2')  # Redirige vers le formulaire 2

#     # Remplir les champs avec les données de la session s'il y en a
#     form_data = request.session.get('form_data', {})
#     # Passer également les genres et situations dans le contexte
#     return render(request, 'myapp/home.html', context={'genres': genres, 'situations': situations, **form_data})

def home(request):
    genres = Genre.objects.all()
    situations = Sit_matrim.objects.all()
    error_message = None

    if request.method == 'POST':
        nom = request.POST.get('nom')
        situation_matrimoniale = request.POST.get('situation_matrimoniale')
        prenom = request.POST.get('prenom')
        date_naissance = request.POST.get('date_naissance')
        genre = request.POST.get('genre')
        lieu_naissance = request.POST.get('lieu_naissance')

        # Vérification de l'âge
        try:
            date_naissance_dt = datetime.strptime(date_naissance, '%Y-%m-%d')
            age = (datetime.now() - date_naissance_dt).days // 365
            if age < 18:
                error_message = "Vous devez avoir un CIN !"
            else:
                # Stockage des données dans la session si l'âge est valide
                request.session['form_data'] = {
                    'nom': nom,
                    'situation_matrimoniale': situation_matrimoniale,
                    'prenom': prenom,
                    'date_naissance': date_naissance,
                    'genre': genre,
                    'lieu_naissance': lieu_naissance,
                }
                return redirect('form_part2')
        except ValueError:
            error_message = "Date de naissance invalide."

    # Remplir les champs avec les données de la session s'il y en a
    form_data = request.session.get('form_data', {})
    context = {'genres': genres, 'situations': situations, 'error_message': error_message, **form_data}
    return render(request, 'myapp/home.html', context=context)



# def valider_cin_et_contact(cin, contact):
#     url = 'http://votre_api_url/valider_cin/'
#     response = requests.post(url, json={'cin': cin, 'contact': contact})
    
#     if response.status_code == 200:
#         # Validation réussie
#         return True
#     elif response.status_code == 400:
#         # Si l'API renvoie une erreur de validation
#         raise ValidationError(response.json().get('message', 'Erreur de validation inconnue'))
#     else:
#         # Erreur de communication avec l'API
#         raise ValidationError("Impossible de valider les informations, veuillez réessayer.")


@api_view(['GET'])
def get_all_operateurs(request):
    # Récupérer tous les opérateurs
    operateurs = Operateur.objects.all()
    # Sérialiser les opérateurs en un format JSON
    data = [{"cin": operateur.cin, "contact": operateur.contact} for operateur in operateurs]
    return Response(data, status=status.HTTP_200_OK)



# def valider_cin_et_contact(cin, contact):
#     cin = cin.strip()  # Supprimer les espaces inutiles au début et à la fin du CIN
#     contact = contact.strip()  # Supprimer les espaces inutiles au début et à la fin du contact
    
#     try:
#         # Rechercher un opérateur avec le CIN donné
#         operateur = Operateur.objects.get(cin=cin)
        
#         # Vérifier si le contact correspond
#         if operateur.contact != contact:
#             # Lever une exception si le contact ne correspond pas
#             raise ValidationError("Le contact ne correspond pas à ce CIN.")
    
#     except Operateur.DoesNotExist:
#         # Lever une exception si aucun opérateur avec ce CIN n'est trouvé
#         raise ValidationError("Le CIN n'est pas valide.")
    
#     # Si aucune exception n'a été levée, tout est correct
#     return True



def valider_cin_et_contact(cin, contact):
    # URL de l'API où les opérateurs sont récupérés
    url = 'http://127.0.0.1:8000/get_all_operateurs/'  # Remplacez par l'URL correcte
    
    # Faire la requête à l'API pour récupérer tous les opérateurs
    response = requests.get(url)

    if response.status_code == 200:
        operateurs = response.json()
        
        # Vérifier si le CIN existe dans la liste et si le contact correspond
        for operateur in operateurs:
            if operateur['cin'] == cin and operateur['contact'] == contact:
                return True  # Si le CIN et le contact correspondent, on retourne True
        
        # Si aucun opérateur avec ce CIN et contact n'a été trouvé, lever une exception
        raise ValidationError("Le CIN ou le contact ne correspond pas.")
    else:
        raise ValidationError("Erreur lors de la validation avec l'API.")





# def valider_cin_et_contact_api(cin, contact):
#     cin = cin.strip()  # Supprimer les espaces
#     contact = contact.strip()
    
#     try:
#         # Appel à l'API pour obtenir l'opérateur
#         response = requests.get(f"https://api.exemple.com/operateurs?cin={cin}")
        
#         if response.status_code == 200:
#             data = response.json()  # Récupérer les données JSON
            
#             # Vérifier si le contact correspond
#             if 'contact' not in data or data['contact'] != contact:
#                 raise ValidationError("Le contact ne correspond pas à ce CIN.")
#         else:
#             raise ValidationError("Le CIN n'est pas valide.")
        
#     except requests.exceptions.RequestException:
#         raise ValidationError("Erreur lors de l'accès à l'API.")
    
#     return True

def form_part2(request):
    show_modal = False  # Pour contrôler l'affichage du modal de succès
    success_message = ""
    error_message = ""  # Pour stocker les messages d'erreur

    if request.method == 'POST':
        lieu_delivrance = request.POST.get('lieu_delivrance')
        cin = request.POST.get('cin')
        date_delivrance = request.POST.get('date_delivrance')
        contact = request.POST.get('contact')
        fokontany = request.POST.get('fkt_no')
        email = request.POST.get('email')

        form_data = request.session.get('form_data', {})

        try:
            # Appel de la fonction de validation pour CIN et contact
            valider_cin_et_contact(cin, contact)

            # Si validation réussie, continuer le traitement
            genre_instance = get_object_or_404(Genre, genre=form_data['genre'])
            situation_matrimoniale_instance = get_object_or_404(Sit_matrim, id=form_data['situation_matrimoniale'])

            contribuable = Contribuable(
                nom=form_data['nom'],
                prenom=form_data['prenom'],
                date_naissance=form_data['date_naissance'],
                genre=genre_instance,
                situation_matrimoniale=situation_matrimoniale_instance,
                lieu_naissance=form_data['lieu_naissance'],
                lieu_delivrance=lieu_delivrance,
                cin=cin,
                date_delivrance=date_delivrance,
                contact=contact,
                fokontany=fokontany,
                email=email,
            )
            contribuable.save()

            prenif, mot_de_passe = GenererPRENIFetMdp(cin)

            contribuable.propr_nif = prenif
            contribuable.mot_de_passe = mot_de_passe
            contribuable.save()

            envoyer_email(email, prenif, mot_de_passe)

            success_message = "Votre inscription a été réalisée avec succès. Veuillez vérifier votre email."
            show_modal = True  # Afficher le modal de succès

        except ValidationError as e:
            # Récupérer le message d'erreur de validation
            error_message = str(e)
            show_modal = False

    return render(request, 'myapp/inscription_part2.html', {
        'success_message': success_message,
        'error_message': error_message,  # Envoyer le message d'erreur au template
        'show_modal': show_modal,
    })


def envoyer_email(email, prenif, mot_de_passe):
    """Envoie un email avec les informations d'inscription."""
    subject = 'Inscription réussie'
    message = (
        f"Vous êtes inscrit en tant que membre,\n"
        f"votre n° d'immatriculation fiscale est : {prenif} "
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
                settings.DEFAULT_FROM_EMAIL,  # Adresse de l'expéditeur
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


def modifier_contribuable(request):
    # Récupérer l'ID du contribuable connecté depuis la session
    id_contribuable = request.session.get('contribuable_id')

    # Vérifier si l'utilisateur est authentifié
    if not id_contribuable:
        return redirect('login')  # Redirige vers la page de login si non connecté

    # Charger le contribuable avec l'ID récupéré
    contribuable = get_object_or_404(Contribuable, id=id_contribuable)

    if request.method == 'POST':
        form = ContribuableForm(request.POST, request.FILES, instance=contribuable)
        if  form.is_valid():
            form.save()
            messages.success(request, 'Profil modifié avec succès.')
            return redirect('profil')  # Redirection après la sauvegarde
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erreur dans {field}: {error}")

    else:
        form = ContribuableForm(instance=contribuable)
    
    return render(request, 'myapp/profil.html', {
        'form': form,
        'contribuable': contribuable,
        'MEDIA_URL': settings.MEDIA_URL
    })


class ContribuableForm(forms.ModelForm):
    class Meta:
        model = Contribuable
        fields = ['nom', 'prenom', 'email', 'contact', 'mot_de_passe', 'fokontany', 'photo']  # Assurez-vous que les champs sont corrects

    # Rendre 'mot_de_passe' et 'photo' optionnels
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mot_de_passe'].required = False
        self.fields['fokontany'].required = False
        self.fields['photo'].required = False

def deconnexion(request):
    request.session.flush()
    return redirect('login')  # Redirige vers la page d'accueil