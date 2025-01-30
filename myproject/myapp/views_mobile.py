from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Genre,Sit_matrim,Contribuable
from .views import valider_cin_et_contact,GenererPRENIFetMdp,envoyer_email
from .serializers import GenreSerializer,FokontanyView
from .serializers import SitMatrimSerializer
from .serializers import FokontanyViewSerializer
from .serializers import ContribuableFormSerializer
from rest_framework.filters import SearchFilter
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import json
from django.http import JsonResponse
from django.db import connection
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination
from django.db import connection

class GenreListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)


class SitMatrimListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        sit_matrim = Sit_matrim.objects.all()  # Récupère toutes les situations matrimoniales
        serializer = SitMatrimSerializer(sit_matrim, many=True)  # Sérialise les données
        return Response(serializer.data)  # Retourne la réponse sérialisée

class FokontanyViewList(ListAPIView):
    queryset = FokontanyView.objects.all()
    serializer_class = FokontanyViewSerializer
    filter_backends = [SearchFilter]
    search_fields = ['fkt_desc', 'wereda_desc', 'locality_desc', 'city_name', 'parish_name']



from django.shortcuts import get_object_or_404

from django.db import connection  # Pour afficher les requêtes SQL exécutées

@csrf_exempt
def inscription(request):
    if request.method != 'POST':
        return JsonResponse({"message": "Méthode non autorisée. Utilisez POST."}, status=405)

    try:
        # Charger les données JSON envoyées
        data = json.loads(request.body)

        # Debug : Afficher les données reçues
        print("Données reçues:", data)

        # Valider les champs obligatoires
        champs_obligatoires = ['nom', 'dateNaissance', 'lieuNaissance', 'situationMatrimoniale', 'cin', 'dateDelivrance', 'lieuDelivrance', 'contact', 'email', 'id_fokontany']
        for champ in champs_obligatoires:
            if not data.get(champ):
                return JsonResponse({"message": f"Le champ '{champ}' est obligatoire."}, status=400)

        # Valider le CIN et le contact
        try:
            valider_cin_et_contact(data['cin'], data['contact'])
        except ValidationError as e:
            return JsonResponse({"message": str(e)}, status=400)

        # Récupérer les instances associées
        genre_instance = get_object_or_404(Genre, id=data['genre']) if data.get('genre') else None
        situation_matr_instance = get_object_or_404(Sit_matrim, id=data['situationMatrimoniale']) if data.get('situationMatrimoniale') else None

        # Créer une instance du modèle Contribuable
        contribuable = Contribuable(
            nom=data['nom'],
            prenom=data.get('prenom', ''),  # Le prénom est optionnel
            date_naissance=data['dateNaissance'],
            genre=genre_instance,  # Utiliser l'instance du genre ici
            situation_matrimoniale=situation_matr_instance,
            lieu_naissance=data['lieuNaissance'],
            lieu_delivrance=data['lieuDelivrance'],
            cin=data['cin'],
            date_delivrance=data['dateDelivrance'],
            contact=data['contact'],
            email=data['email'],
            fokontany=data['id_fokontany'],  # Assigner l'ID fokontany ici
        )
        contribuable.save()

        # Générer le PRENIF et le mot de passe
        prenif, mot_de_passe = GenererPRENIFetMdp(data['cin'])
        contribuable.propr_nif = prenif
        contribuable.mot_de_passe = mot_de_passe
        contribuable.save()

        # envoyer_email(data['email'], prenif, mot_de_passe)

        # Debug : Afficher les requêtes SQL exécutées
        for query in connection.queries:
            print(query)

        # Retourner une réponse JSON de succès
        return JsonResponse({"message": "Inscription réussie. Vérifiez votre email pour le PRENIF et le mot de passe."}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Format JSON invalide. Veuillez envoyer des données JSON correctes."}, status=400)

    except KeyError as e:
        return JsonResponse({"message": f"Champ manquant : {str(e)}"}, status=400)

    except Exception as e:
        # Gestion générique des erreurs inattendues
        return JsonResponse({"message": f"Erreur inattendue : {str(e)}"}, status=500)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            # Essayer de charger les données JSON
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Le corps de la requête n\'est pas un JSON valide'}, status=400)
            
            print('Données reçues:', data)  # Vérifier les données reçues

            prenif = data.get('prenif')
            password = data.get('password')

            # Vérifier si les données sont présentes
            if not prenif or not password:
                return JsonResponse({'error': 'Les champs prenif et password sont requis'}, status=400)

            # Rechercher l'utilisateur avec le prenif
            try:
                contribuable = Contribuable.objects.get(propr_nif=prenif)
            except Contribuable.DoesNotExist:
                return JsonResponse({'error': 'Utilisateur non trouvé'}, status=400)

            # Vérifier le mot de passe
            if contribuable.mot_de_passe == password:
                # Authentifier l'utilisateur
                request.session['contribuable_id'] = contribuable.id
                request.session['prenif'] = contribuable.propr_nif
                request.session['email'] = contribuable.email

                # Réponse JSON en cas de succès
                return JsonResponse({'message': 'Connexion réussie'}, status=200)

            else:
                return JsonResponse({'error': 'Mot de passe incorrect'}, status=400)

        except Exception as e:
            return JsonResponse({'error': f'Erreur inattendue: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

from django.http import JsonResponse
from django.db import connection

def api_profil(request):
    id_contribuable = request.session.get('contribuable_id')
    if not id_contribuable:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM myapp_contribuable WHERE id = %s", [id_contribuable])
        contribuable = cursor.fetchone()

    if contribuable:
        contribuable_info = {
            'name': contribuable[1],  # Exemple de mapping de données
            'contact': contribuable[8],
            'email': contribuable[10],
            'photo': contribuable[17],
            'cin': contribuable[6],
            'propr_nif': contribuable[18],
        }
        return JsonResponse(contribuable_info)
    else:
        return JsonResponse({'error': 'User not found'}, status=404)


from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from .models import Contribuable  # Assurez-vous d'importer votre modèle Contribuable
from django.contrib import messages

import json
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from .models import Contribuable  # Assurez-vous d'importer votre modèle Contribuable

from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
import json
from .models import Contribuable

@csrf_exempt
def modifier_mot_de_passe_api(request):
    if request.method == 'POST':
        # Récupérer l'ID du contribuable connecté depuis la session
        id_contribuable = request.session.get('contribuable_id')

        # Vérifier si l'utilisateur est connecté
        if not id_contribuable:
            return JsonResponse({'error': 'Utilisateur non authentifié'}, status=401)

        # Récupérer l'utilisateur connecté
        try:
            contribuable = Contribuable.objects.get(pk=id_contribuable)
        except Contribuable.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur introuvable'}, status=404)

        # Vérification pour hacher les mots de passe non hachés
        if not contribuable.mot_de_passe.startswith("pbkdf2_"):  # Vérifie si le mot de passe est déjà haché
            contribuable.mot_de_passe = make_password(contribuable.mot_de_passe)
            contribuable.save()

        # Récupérer les mots de passe depuis la requête JSON
        try:
            body = json.loads(request.body)  # Parser le corps de la requête JSON
            old_password = body.get('old_password')
            new_password = body.get('new_password')
            confirm_password = body.get('confirm_password')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données invalides'}, status=400)

        # Vérifier si le mot de passe actuel est correct
        if not check_password(old_password, contribuable.mot_de_passe):
            return JsonResponse({'error': 'Le mot de passe actuel est incorrect'}, status=400)

        # Vérifier si les nouveaux mots de passe correspondent
        if new_password != confirm_password:
            return JsonResponse({'error': 'Les nouveaux mots de passe ne correspondent pas'}, status=400)

        # Hacher et mettre à jour le mot de passe
        contribuable.mot_de_passe = make_password(new_password)
        contribuable.save()

        # Réponse de succès sous forme de JSON
        return JsonResponse({'success': 'Votre mot de passe a été modifié avec succès'}, status=200)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
import random

# views.py
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail



@csrf_exempt
def send_code(request):
    if request.method == 'POST':
        # Vérifier si le contribuable est connecté via la session
        contribuable_id = request.session.get('contribuable_id')
        if not contribuable_id:
            return JsonResponse({'error': 'Utilisateur non connecté'}, status=403)

        try:
            # Récupérer les informations du contribuable connecté
            contribuable = Contribuable.objects.get(id=contribuable_id)
            email = contribuable.email  # Supposons que le champ email existe dans le modèle

            # Générer un code OTP à 6 chiffres
            code = random.randint(100000, 999999)

            # Stocker le code OTP et son expiration dans la session
            request.session['auth_code'] = code
            expiration_time = datetime.now() + timedelta(minutes=5)  # Valide pour 5 minutes
            request.session['code_expiration'] = expiration_time.strftime("%Y-%m-%d %H:%M:%S")

            # Envoyer le code OTP par email
            send_mail(
                'Votre code de vérification',
                f'Votre code de vérification est : {code}',
                f"immatriculationenligne <{settings.DEFAULT_FROM_EMAIL}>",  # Adresse de l'expéditeur
                [email],  # Destinataire (email de l'utilisateur)
                fail_silently=False,
            )

            # Retourner une réponse JSON pour confirmer l'envoi du code
            return JsonResponse({'message': 'Code envoyé'}, status=200)

        except Contribuable.DoesNotExist:
            return JsonResponse({'error': 'Contribuable non trouvé'}, status=404)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@api_view(['POST'])
def validate_code(request):
    entered_code = request.data.get('code')

    # Récupérer le code et l'expiration depuis la session
    correct_code = request.session.get('auth_code')
    expiration_time = request.session.get('code_expiration')

    # Vérifier si le code existe dans la session
    if not correct_code or not expiration_time:
        return Response({"error": "Code non trouvé ou expiré. Veuillez demander un nouveau code."}, status=400)

    # Vérifier si le code a expiré
    if datetime.now() > datetime.strptime(expiration_time, "%Y-%m-%d %H:%M:%S"):
        return Response({"error": "Le code a expiré. Veuillez renvoyer un nouveau code."}, status=400)

    # Vérifier si le code est correct
    if int(entered_code) == correct_code:
        # Supprimer le code de la session après validation pour des raisons de sécurité
        del request.session['auth_code']
        del request.session['code_expiration']

        return Response({"message": "Code validé avec succès."}, status=200)
    else:
        return Response({"error": "Le code est incorrect. Veuillez réessayer."}, status=400)



class TransactionListAPI(APIView):
    class TransactionPagination(PageNumberPagination):
        page_size = 2  # Nombre de transactions par page
        page_size_query_param = 'page_size'
        max_page_size = 100

    def get(self, request, *args, **kwargs):
        # Récupérer l'ID du contribuable depuis la session
        id_contribuable = request.session.get('contribuable_id')

        # Vérifier si un contribuable est connecté
        if not id_contribuable:
            return JsonResponse({'error': 'Utilisateur non connecté'}, status=403)

        print(f"ID du contribuable: {id_contribuable}")  # Vérification de l'ID du contribuable

        # Requête SQL pour récupérer les transactions
        query = """
            SELECT n_quit, contribuable, total_payee, reste_ap
            FROM vue_transactions_par_quit_et_contribuable
            WHERE contribuable = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [id_contribuable])
            rows = cursor.fetchall()

        print(f"Résultats de la requête SQL: {rows}")  # Affiche les résultats de la requête

        if not rows:
            print("Aucune transaction trouvée pour ce contribuable.")  # Vérification de l'absence de résultats

        # Sérialiser les données
        transactions = [
            {
                'n_quit': row[0],
                'contribuable': row[1],
                'total_payee': row[2],
                'rest_payee': row[3],
            }
            for row in rows
        ]

        # Pagination
        paginator = self.TransactionPagination()
        paginated_transactions = paginator.paginate_queryset(transactions, request)

        # Retourner la réponse paginée
        return paginator.get_paginated_response(paginated_transactions)

def api_transaction_details(request, n_quit):
    id_contribuable = request.session.get('contribuable_id')

    if not id_contribuable:
        return JsonResponse({'error': 'Utilisateur non connecté'}, status=403)

    sql_query = """
        SELECT 
            contribuable, 
            n_quit, 
            date_paiement, 
            numrec,
            annee_de_paiement, 
            annee_recouvrement, 
            date_debut, 
            date_fin, 
            base, 
            mnt_ap, 
            nimp AS NIMP, 
            imp_detail, 
            numero, 
            impot, 
            sens, 
            logiciel,
            montant
        FROM 
            vue_detail_transactions_par_quit_et_contribuable 
        WHERE 
            contribuable = %s AND n_quit = %s;
    """

    with connection.cursor() as cursor:
        cursor.execute(sql_query, [id_contribuable, n_quit])
        rows = cursor.fetchall()

    if not rows:
        return JsonResponse({'error': 'Aucune transaction trouvée.'}, status=404)

    # Sérialiser les résultats en JSON
    transactions = [
        {
            'contribuable': row[0],
            'n_quit': row[1],
            'date_paiement': row[2],
            'numrec': row[3],
            'annee_de_paiement': row[4],
            'annee_recouvrement': row[5],
            'date_debut': row[6],
            'date_fin': row[7],
            'base': row[8],
            'mnt_ap': row[9],
            'nimp': row[10],
            'imp_detail': row[11],
            'numero': row[12],
            'impot': row[13],
            'sens': row[14],
            'logiciel': row[15],
            'montant': row[16],
        }
        for row in rows
    ]

    # Afficher les transactions dans la console
    print("Transactions récupérées :", transactions)

    return JsonResponse({'transactions': transactions}, status=200)


from rest_framework import status
@api_view(['PUT'])
def modifier_infos_personnelles(request):
    # Récupérer l'ID du contribuable depuis la session
    id_contribuable = request.session.get('contribuable_id')

    if not id_contribuable:
        return Response({"detail": "Utilisateur non authentifié"}, status=status.HTTP_401_UNAUTHORIZED)

    # Récupérer l'objet contribuable
    contribuable = Contribuable.objects.filter(id=id_contribuable).first()

    if not contribuable:
        return Response({"detail": "Contribuable introuvable"}, status=status.HTTP_404_NOT_FOUND)

    # Afficher les données du contribuable dans la console
    print("Contribuable récupéré:", contribuable)

    # Sérialiser les données
    if request.method == 'PUT':
        serializer = ContribuableFormSerializer(contribuable, data=request.data)

        # Afficher les données envoyées dans la requête PUT
        print("Données reçues dans la requête PUT:", request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Informations modifiées avec succès"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"detail": "Méthode non autorisée"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)    # def get(self, request, *args, **kwargs):



from django.core.files.storage import default_storage

@api_view(['POST'])
def modifier_photo_profil(request):
    # Vérifier si l'utilisateur est authentifié via la session
    id_contribuable = request.session.get('contribuable_id')
    if not id_contribuable:
        return Response({"detail": "Utilisateur non authentifié"}, status=status.HTTP_401_UNAUTHORIZED)

    # Charger le contribuable correspondant
    contribuable = Contribuable.objects.filter(id=id_contribuable).first()
    if not contribuable:
        return Response({"detail": "Contribuable introuvable"}, status=status.HTTP_404_NOT_FOUND)

    # Afficher les données du contribuable dans la console (utile pour le débogage)
    print("Contribuable récupéré:", contribuable)

    # Vérifier si un fichier a été envoyé
    if 'photo' not in request.FILES:
        return Response({'detail': 'Aucune photo fournie'}, status=status.HTTP_400_BAD_REQUEST)

    photo = request.FILES['photo']

    # Utiliser le gestionnaire de fichier du modèle pour sauvegarder l'image
    try:
        contribuable.photo = photo
        contribuable.save()
    except Exception as e:
        return Response({'detail': f"Erreur lors de l'enregistrement de la photo : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'detail': 'Photo de profil mise à jour avec succès.'}, status=status.HTTP_200_OK)
   #     id_contribuable = 20  # Utilisation d'un ID fixe pour le moment


def chart_api(request):
    # Récupérer l'ID du contribuable connecté depuis la session
    id_contribuable = request.session.get('contribuable_id')

    # Vérifier si l'utilisateur est connecté
    if not id_contribuable:
        return JsonResponse({'error': 'Utilisateur non connecté'}, status=401)

    # Récupérer les données depuis la base de données
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT annee, total_mnt_ver FROM vue_somme_par_contribuable_par_annee WHERE contribuable = %s",
            [id_contribuable]
        )
        rows = cursor.fetchall()

    # Préparer les données en format JSON
    data = [
        {'annee': row[0], 'total_mnt_ver': float(row[1])} for row in rows
    ]
    
    return JsonResponse({'data': data}, safe=False)

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.utils import timezone
from .models import Contribuable, Operateurs, Message
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Contribuable, Operateurs, Message
from django.utils import timezone

@api_view(['POST', 'GET'])
def discussion(request):
    contribuable_id = request.session.get('contribuable_id')
    
    # Vérifier si l'utilisateur existe dans la session
    if not contribuable_id:
        return Response({"error": "Contribuable non trouvé dans la session"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        contribuable = Contribuable.objects.get(id=contribuable_id)
    except Contribuable.DoesNotExist:
        return Response({"error": "Contribuable non trouvé"}, status=status.HTTP_404_NOT_FOUND)
    
    # Utiliser l'opérateur par défaut
    try:
        operateur = Operateurs.objects.get(id=1)  # Opérateur par défaut
    except Operateurs.DoesNotExist:
        return Response({"error": "Opérateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'POST':
        contenu = request.data.get('contenu')
        fichier_joint = request.FILES.get('fichier_joint')

        # Enregistrement du message dans la base de données
        message = Message.objects.create(
            contenu=contenu,
            fichier_joint=fichier_joint,
            id_contribuable_id=contribuable.id,
            id_operateur_id=operateur.id,
            type_message='contribuable',
            date_envoi=timezone.now()
        )

        return Response({"message": "Message envoyé avec succès"}, status=status.HTTP_201_CREATED)

    # Récupérer les messages non lus de l'opérateur
    messages_non_lus = Message.objects.filter(notifié=False, type_message='operateur')

    # Compter le nombre de messages non lus
    unread_count = messages_non_lus.count()

    # Récupérer tous les champs de chaque message dans la table
    messages_data = Message.objects.filter(id_contribuable=contribuable.id).order_by('date_envoi').values(
        'id', 'contenu', 'fichier_joint', 'date_envoi', 'type_message', 
        'id_contribuable_id', 'id_operateur_id', 'notifié'
    )

    # Sérialiser les données pour les renvoyer
    return Response({
        "messages": list(messages_data),
        "unread_count": unread_count  # Ajouter le comptage des messages non lus
    }, status=status.HTTP_200_OK)


def get_unread_message_count(request):
    # Récupérer l'ID du contribuable dans la session
    contribuable_id = request.session.get('contribuable_id')
    
    if not contribuable_id:
        return Response({"error": "Contribuable non trouvé dans la session"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Filtrer les messages non lus pour le contribuable
        messages_non_lus = Message.objects.filter(notifié=False, type_message='operateur', id_contribuable_id=contribuable_id)
        
        # Afficher les messages non lus dans la console Django
        print("Messages non lus pour le contribuable connecté :")
        for message in messages_non_lus:
            print(f"- ID: {message.id}, Contenu: {message.contenu}, Date: {message.date_envoi}")

        # Retourner le nombre de messages non lus
        unread_count = messages_non_lus.count()
        return JsonResponse({'unread_count': unread_count})

    except Exception as e:
        print(f"Erreur lors de la récupération des messages non lus : {e}")
        return JsonResponse({'error': 'Erreur serveur lors de la récupération des messages'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def mark_messages_as_read(request):
    # Récupérer l'ID du contribuable dans la session
    contribuable_id = request.session.get('contribuable_id')

    if not contribuable_id:
        return Response({"error": "Contribuable non trouvé dans la session"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Filtrer les messages non lus
        messages_non_lus = Message.objects.filter(notifié=False, type_message='operateur', id_contribuable_id=contribuable_id)

        # Mettre à jour les messages pour les marquer comme "lus"
        messages_non_lus.update(notifié=True)

        # Retourner une réponse de succès
        return JsonResponse({'success': True, 'updated_count': messages_non_lus.count()})

    except Exception as e:
        print(f"Erreur lors de la mise à jour des messages : {e}")
        return JsonResponse({'error': 'Erreur serveur lors de la mise à jour des messages'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)