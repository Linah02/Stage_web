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
#  import requests

from django.core.exceptions import ValidationError
logger = logging.getLogger(__name__)
from .models import Genre
from django.contrib import messages
from django.http import JsonResponse
from .models import FokontanyView
from datetime import datetime, timedelta


def home(request):
    genres = Genre.objects.all()  # Récupère tous les genres
    situations = Sit_matrim.objects.all()  # Récupère toutes les situations matrimoniales

    if request.method == 'POST':
        nom = request.POST.get('nom')
        situation_matrimoniale = request.POST.get('situation_matrimoniale')
        prenom = request.POST.get('prenom')
        date_naissance = request.POST.get('date_naissance')
        genre = request.POST.get('genre')
        lieu_naissance = request.POST.get('lieu_naissance')

          # Stockage des données dans la session
        request.session['form_data'] = {
            'nom': nom,
            'situation_matrimoniale': situation_matrimoniale,
            'prenom': prenom,
            'date_naissance': date_naissance,
            'genre': genre,
            'lieu_naissance': lieu_naissance,
        }
        return redirect('form_part2')  # Redirige vers le formulaire 2

    # Remplir les champs avec les données de la session s'il y en a
    form_data = request.session.get('form_data', {})
    # Passer également les genres et situations dans le contexte
    return render(request, 'myapp/home.html', context={'genres': genres, 'situations': situations, **form_data})



def valider_cin_et_contact(cin, contact):
    cin = cin.strip()  # Supprimer les espaces inutiles au début et à la fin du CIN
    contact = contact.strip()  # Supprimer les espaces inutiles au début et à la fin du contact
    
    try:
        # Rechercher un opérateur avec le CIN donné
        operateur = Operateur.objects.get(cin=cin)
        
        # Vérifier si le contact correspond
        if operateur.contact != contact:
            # Lever une exception si le contact ne correspond pas
            raise ValidationError("Le contact ne correspond pas à ce CIN.")
    
    except Operateur.DoesNotExist:
        # Lever une exception si aucun opérateur avec ce CIN n'est trouvé
        raise ValidationError("Le CIN n'est pas valide.")
    
    # Si aucune exception n'a été levée, tout est correct
    return True




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
        email = request.POST['mail']
        password = request.POST['password']
        
        try:
            # Rechercher un utilisateur avec l'email et vérifier le mot de passe
            contribuable = Contribuable.objects.get(email=email)
            if contribuable.mot_de_passe == password:
                # Si l'email et le mot de passe correspondent, rediriger vers l'authentification à 2 facteurs
                request.session['contribuable_id'] = contribuable.id  # Stocker l'utilisateur pour la prochaine étape
                request.session['user_email'] = contribuable.email
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

def mdp_oubliee(request):
    return render(request, 'myapp/mdp_oubli.html')  # Rediriger vers la page d'accueil


def generate_code():
    return str(random.randint(100000, 999999))


def D_authentification(request):
    if request.method == 'POST':
        if 'send_code' in request.POST:
            # Récupérer l'email de l'utilisateur depuis la session
            email = request.session.get('user_email')  # Utilisez cet email pour renvoyer le code
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