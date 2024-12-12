import logging
logger = logging.getLogger(__name__)
# from django.http import HttpResponse
from django.template.loader import render_to_string
# from weasyprint import HTML
from django.utils import timezone
# from django.http import HttpResponse
# from weasyprint import HTML
from django.core.paginator import Paginator
from firebase_admin.messaging import Message, Notification, send

import pdfkit
from pdfkit import configuration
from django.http import HttpResponse
# from django.template.loader import render_to_string
from firebase_admin import messaging


import json
from django.shortcuts import render, redirect,get_object_or_404
from .models import VueTransactionsParQuitEtContribuable  # Assurez-vous d'importer le modèle
from .models import VueSommeParContribuableParAnnee  # Assurez-vous d'importer le modèle
from .models import VueRecouvrementsEtPaiementsParAnnee
from django.core.mail import send_mail
from django.conf import settings
from .models import Message, Operateurs,Contribuable


import imaplib
import email
from email.header import decode_header


from django.http import JsonResponse
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db import connection
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from .models import TransactionDetail
from .models import Brochure
def acceuil(request):
    return render(request, 'acceuil/acceuil.html')  


from django.core.paginator import Paginator
from django.shortcuts import render

def acceuils(request):
    # Sélectionner les vidéos publiées
    videos_publiees = VideoPublicite.objects.filter(statut='publie').order_by('-date_publication')
    brochures = Brochure.objects.all()  # Récupère toutes les brochures

    # Configuration de la pagination
    paginator = Paginator(brochures, 5)  # 5 brochures par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Rendu du template d'accueil avec les vidéos publiées et les brochures paginées
    return render(request, 'acceuil/accueils.html', {
        'videos_publiees': videos_publiees,
        'page_obj': page_obj,  # Ajoutez l'objet de page à votre contexte
    })

from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Brochure

def get_brochures(request):
    page_number = request.GET.get('page', 1)  # Page actuelle
    brochures = Brochure.objects.all()  # Toutes les brochures
    paginator = Paginator(brochures, 5)  # Pagination à 5 brochures par page

    try:
        page_obj = paginator.get_page(page_number)
    except:
        return JsonResponse({'error': 'Page non valide'}, status=400)

    # Formatage des brochures pour la réponse JSON
    brochures_data = [
        {
            'titre': brochure.titre,
            'fichier_pdf': brochure.fichier_pdf.url,  # URL correcte
        }
        for brochure in page_obj.object_list
    ]

    return JsonResponse({
        'brochures': brochures_data,
        'has_next': page_obj.has_next(),  # Indique s'il y a une page suivante
        'has_previous': page_obj.has_previous(),  # Indique s'il y a une page précédente
        'current_page': page_obj.number,  # Page actuelle
    })


def acceuilCte(request):
    return render(request, 'acceuil/acceuilCte.html')  

def IS_calcul(request):
    return render(request, 'acceuil/IS_calcul.html')  



def IR_calcul(request):
    if request.method == 'POST':
        salaire_brut = float(request.POST.get('salaire_brut', 0))
        charges_sociales = float(request.POST.get('charges_sociales', 0))

        # Calcul des charges et du salaire net imposable
        charges = (salaire_brut * charges_sociales) / 100
        salaire_net_imposable = salaire_brut - charges
        irsa = salaire_net_imposable * 0.2  # Exemple : IRSA à 20%

        # Répartition des pourcentages
        sante = irsa * 0.1
        enseignement = irsa * 0.9

        return JsonResponse({
            'irsa': irsa,
            'details': {
                'sante': sante,
                'enseignement': enseignement
            }
        })
    return render(request, 'acceuil/IR_calcul.html')


def IRSA_calcul(request):
    return render(request, 'acceuil/IRSA_calcul.html')  


def home1(request):
    return render(request, 'myapp/home1.html')  


def notification(request):
    return render(request, 'acceuil/notification.html')  


def chart(request):
    # Récupérer l'ID du contribuable connecté depuis la session
    id_contribuable = request.session.get('contribuable_id')
    messages_non_lus = Message.objects.filter(notifié=False,type_message='operateur')

    # Vérifier si l'utilisateur est connecté
    if not id_contribuable:
        return redirect('login')  # Redirige vers la page de login si non connecté

    # Récupérer les données depuis la base de données
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT contribuable, annee, total_mnt_ver FROM vue_somme_par_contribuable_par_annee WHERE contribuable = %s",
            [id_contribuable]
        )
        rows = cursor.fetchall()

    # Conversion des valeurs Decimal en float pour faciliter l'affichage JSON
    sommes = [{'contribuable': row[0], 'annee': row[1], 'total_mnt_ver': float(row[2])} for row in rows]
    
    # Rendu de la page avec les données JSON
    return render(request, 'acceuil/transaction_chart.html', {'sommes': json.dumps(sommes),'messages_non_lus':messages_non_lus})


def chart_line(request):
    messages_non_lus = Message.objects.filter(notifié=False,type_message='operateur')

    # Récupérer l'ID du contribuable connecté depuis la session
    id_contribuable = request.session.get('contribuable_id')

    # Vérifier si l'utilisateur est connecté
    if not id_contribuable:
        return redirect('login')  # Redirige vers la page de login si non connecté

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT contribuable, annee_recouvrement, total_recouvrement_annuel, total_paye_annuel
            FROM vue_recouvrements_et_paiements_par_annee
            WHERE contribuable = %s
            """,
            [id_contribuable]
        )
        rows = cursor.fetchall()

    # Structurer les données pour le graphique
    data_par_contribuable = {}
    for contribuable, annee, total_recouvrement, total_paye in rows:
        # Convertir les valeurs Decimal en float
        total_recouvrement = float(total_recouvrement) if total_recouvrement is not None else 0.0
        total_paye = float(total_paye) if total_paye is not None else 0.0

        if contribuable not in data_par_contribuable:
            data_par_contribuable[contribuable] = {
                'annees': [],
                'recouvrements': [],
                'paiements': []
            }
        data_par_contribuable[contribuable]['annees'].append(annee)
        data_par_contribuable[contribuable]['recouvrements'].append(total_recouvrement)
        data_par_contribuable[contribuable]['paiements'].append(total_paye)

    # Retourner les données sous forme JSON
    return render(request, 'acceuil/evolution_transaction.html', {
        'data': json.dumps(data_par_contribuable),
        'messages_non_lus': messages_non_lus
    })




def list_transaction(request):
    messages_non_lus = Message.objects.filter(notifié=False,type_message='operateur')

    # Récupérer l'ID du contribuable connecté depuis la session
    id_contribuable = request.session.get('contribuable_id')

    # Vérifier si l'utilisateur est connecté
    if not id_contribuable:
        return redirect('login')  # Redirige vers la page de login si non connecté

    # Créer la requête SQL pour obtenir les transactions du contribuable connecté
    query = """
        SELECT *
        FROM vue_transactions_par_quit_et_contribuable
        WHERE contribuable = %s;
    """
    
    # Exécuter la requête SQL
    with connection.cursor() as cursor:
        cursor.execute(query, [id_contribuable])
        transactions = cursor.fetchall()
    
    # Paginer les résultats avec 10 transactions par page
    paginator = Paginator(transactions, 2)  # 10 transactions par page
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)
    
    # Passer transactions au lieu de transactions dans le rendu
    return render(request, 'acceuil/liste_transaction.html', {'transactions': transactions,'messages_non_lus':messages_non_lus})


def filtre_list_transaction(request, min_montant=None, max_montant=None):
    # messages_non_lus = Message.objects.filter(notifié=False,type_message='operateur')

    # Récupérer l'ID du contribuable connecté depuis la session
    id_contribuable = request.session.get('contribuable_id')

    # Vérifier si l'utilisateur est connecté
    if not id_contribuable:
        return redirect('login')  # Redirige vers la page de login si non connecté

    # Récupérer les montants min et max à partir des paramètres GET, uniquement si fournis et valides
    try:
        if 'min' in request.GET and request.GET.get('min').strip():
            min_montant = float(request.GET['min'])
        if 'max' in request.GET and request.GET.get('max').strip():
            max_montant = float(request.GET['max'])
    except ValueError:
        logger.error("Valeur de min ou max non valide. Filtrage désactivé.")

    logger.debug(f"Filtrage avec min={min_montant} et max={max_montant}")

    # Construction de la requête SQL sécurisée avec des paramètres
    query = """
        SELECT *
        FROM vue_transactions_par_quit_et_contribuable
        WHERE contribuable = %s
    """
    params = [id_contribuable]

    if min_montant is not None and max_montant is not None:
        query += " AND mont_ap BETWEEN %s AND %s"
        params.extend([min_montant, max_montant])
    elif min_montant is not None:
        query += " AND mont_ap >= %s"
        params.append(min_montant)
    elif max_montant is not None:
        query += " AND mont_ap <= %s"
        params.append(max_montant)

    logger.debug(f"Requête SQL : {query}")

    # Exécuter la requête SQL
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        transactions = cursor.fetchall()

    # Passer la requête SQL dans le contexte pour l'afficher dans le template
    context = {
        'transactions': transactions,
    }

    # Retourner le rendu avec les transactions filtrées
    return render(request, 'acceuil/liste_transaction.html', context)


def profil(request):
    id_contribuable = request.session.get('contribuable_id')
    messages_non_lus = Message.objects.filter(notifié=False,type_message='operateur')

    # Vérifier si l'utilisateur est connecté
    if not id_contribuable:
        return redirect('login')  # Redirige vers la page de login si non connecté

    with connection.cursor() as cursor:
        # Exécutez une requête pour récupérer les informations du contribuable
        cursor.execute("SELECT * FROM myapp_contribuable WHERE id = %s", [id_contribuable])
        contribuable = cursor.fetchone()  # Récupérer la première ligne de résultats

    if contribuable:
        # Préparer les données pour le template
        contribuable_info = {
            'id': contribuable[0],  # Adaptez les indices selon votre structure de table
            'nom': contribuable[1],
            'prenom': contribuable[2],
            'email': contribuable[10],
            'contact': contribuable[8],
            'photo': contribuable[17],
            'propr_nif': contribuable[18],
            'cin':contribuable[6],
            'mot_de_passe': contribuable[13],
            # Ajoutez d'autres champs selon votre modèle
        }
    else:
        contribuable_info = {}  # Aucune information trouvée

    return render(request, 'myapp/profil.html', {'contribuable': contribuable_info,'messages_non_lus':messages_non_lus})

def get_transaction_details(request, n_quit, mnt_ap, reste_a_payer):
    messages_non_lus = Message.objects.filter(notifié=False,type_message='operateur')

    # Récupérer l'ID du contribuable à partir de la session utilisateur
    id_contribuable = request.session.get('contribuable_id')

    # Vérifier si l'utilisateur est connecté
    if not id_contribuable:
        return redirect('login')  # Redirige vers la page de login si non connecté


    # Préparation de la requête SQL
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

    # Exécuter la requête SQL
    with connection.cursor() as cursor:
        # Logger la requête
        logger.info("Exécution de la requête SQL : SELECT * FROM vue_detail_transactions_par_quit_et_contribuable WHERE contribuable = %d AND n_quit = '%s'", id_contribuable, n_quit)

        cursor.execute(sql_query, [id_contribuable, n_quit])  # Assurez-vous que n_quit est une chaîne
        
        # Récupérer tous les résultats
        transaction_details = cursor.fetchall()

    # Formater la requête pour l'afficher dans le template
    sql_query_formatted = f"SELECT contribuable, n_quit, date_paiement, annee_de_paiement, annee_recouvrement, date_debut, date_fin, base, mnt_ap, nimp AS NIMP, imp_detail, numero, impot, sens, logiciel FROM vue_detail_transactions_par_quit_et_contribuable WHERE contribuable = {id_contribuable} AND n_quit = '{n_quit}'"

    # Passer la requête et les résultats au template
    return render(request, 'acceuil/transaction_details.html', {
        'transaction_details': transaction_details,
        'sql_query': sql_query_formatted,
        'montant': mnt_ap,  # Montant passé dans l'URL
        'reste': reste_a_payer, 
        'n_quit':n_quit,'messages_non_lus':messages_non_lus  # Utilisation de la requête formatée
    })




def filtre_detail_transaction(request, n_quit):
    # Initialisation de variables pour les filtres
    min_montant = request.GET.get('min')
    max_montant = request.GET.get('max')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    
    # Créer la requête SQL avec les filtres
    query = """
        SELECT *
        FROM vue_detail_transactions_par_quit_et_contribuable
        WHERE n_quit = %s
    """
    params = [n_quit]
    
    # Ajouter des filtres pour le montant
    if min_montant:
        query += " AND montant >= %s"
        params.append(min_montant)
    if max_montant:
        query += " AND montant <= %s"
        params.append(max_montant)
    
    # Ajouter des filtres pour la date
    if date_min:
        query += " AND date_paiement >= %s"
        params.append(date_min)
    if date_max:
        query += " AND date_paiement <= %s"
        params.append(date_max)

    # Exécution de la requête SQL
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        transaction_details = cursor.fetchall()

    # Formater la requête pour affichage avec les valeurs réelles
    formatted_query = query % tuple(map(repr, params))  # Remplace les %s par les valeurs réelles
    
    # Passez les transaction_details sous le nom 'transaction_details' dans le contexte
    context = {
        'transaction_details': transaction_details,  # Assurez-vous que c'est 'transactions' et non 'transaction_details'
        'n_quit': n_quit,
        'query': formatted_query,  # Passer la requête formatée pour débogage
    }
    # Rendre la page avec les résultats filtrés
    return render(request, 'acceuil/transaction_details.html', context)


def export_transaction_pdf(request, n_quit):
    # Définir le contribuable pour la requête SQL
    id_contribuable = request.session.get('contribuable_id')

    # Vérifier si l'utilisateur est connecté
    if not id_contribuable:
        return redirect('login')  # Redirige vers la page de login si non connecté

    # Exécuter la requête SQL pour obtenir les détails de la transaction
    sql_query = """
        SELECT 
            contribuable, 
            n_quit, 
            date_paiement, 
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
        transaction_details = cursor.fetchall()  # Récupère les résultats sous forme de liste

    # Passer les résultats au template pour générer le HTML
    html_string = render_to_string('acceuil/pdf_template.html', {
        'transaction_details': transaction_details,
        'n_quit': n_quit,
    })

    # Configuration de pdfkit
    path_wkhtmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'  # Mettez le bon chemin ici
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    # Créer le PDF avec pdfkit
    pdf = pdfkit.from_string(html_string, False, configuration=config)

    # Retourner le PDF comme réponse
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="transaction_{n_quit}.pdf"'
    return response

def view_message_contribuable(request, message_id):
    # Récupérer le message
    message = get_object_or_404(Message, id=message_id)
    
    # Marquer le message comme lu
    if not message.notifié:
        message.notifié = True
        message.save()

    # Rediriger vers la vue de réponse
    return redirect('discussion')


def discussion(request):
    contribuable_id = request.session.get('contribuable_id')
    contribuable = Contribuable.objects.get(id=contribuable_id)
    operateur = Operateurs.objects.get(id=1)  # Opérateur par défaut
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        fichier_joint = request.FILES.get('fichier_joint')
        # Enregistrement du message dans la base de données
        message = Message.objects.create(
            contenu=contenu,
            fichier_joint=fichier_joint,
            id_contribuable_id=contribuable_id,
            id_operateur_id=operateur.id,
            type_message='contribuable',
            date_envoi=timezone.now()
        )
        # Appel à la fonction d'envoi de notification après la création du message
        # send_notification_to_admin(message)

    # Récupérer les messages pour cet utilisateur, triés par date
    messages = Message.objects.filter(id_contribuable=contribuable_id).order_by('date_envoi')
    messages_non_lus = Message.objects.filter(notifié=False,type_message='operateur')
    
    return render(request, 'acceuil/message.html', {'messages': messages,'messages_non_lus':messages_non_lus})



def reponse_admin(request,id_contribuable):
    # Récupérer l'id_contribuable depuis les paramètres GET de l'URL
    # contribuable_id = 6

    try:
        contribuable_id = Contribuable.objects.get(id=id_contribuable)
    except Contribuable.DoesNotExist:
        return render(request, 'admin/message.html', {'error': 'Contribuable non trouvé'})

    # # Vérifier si l'id_contribuable est fourni et est valide
    # if not contribuable_id:
    #     return render(request, 'error.html', {'message': "L'ID du contribuable est requis."})
    
    # # Récupérer le contribuable ou retourner une erreur 404 s'il n'existe pas
    # contribuable = get_object_or_404(Contribuable, id=contribuable_id)
    
    # Récupérer l'opérateur par défaut
    operateur = Operateurs.objects.get(id=1)  # Remplacer si l'opérateur par défaut doit être déterminé dynamiquement

    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        fichier_joint = request.FILES.get('fichier_joint')
        
        # Enregistrement du message dans la base de données
        message = Message.objects.create(
            contenu=contenu,
            fichier_joint=fichier_joint,
           id_contribuable_id=contribuable_id.id,
            id_operateur_id=operateur.id,
            type_message='operateur',
            date_envoi=timezone.now()
        )
        
        # Appel à la fonction d'envoi de notification après la création du message
        # send_notification_to_admin(message)

    # Récupérer les messages pour cet utilisateur, triés par date
    messages_non_lus = Message.objects.filter(id_operateur=1, notifié=False)
    messages = Message.objects.filter(id_contribuable=contribuable_id).order_by('date_envoi')

    return render(request, 'admin/reponse_admin.html', {
        'messages': messages,
        'messages_non_lus': messages_non_lus
    })



def discussion_admin(request):
    try:
        operator = Operateurs.objects.get(id=1)  # Utiliser l'ID 1 par défaut
    except Operateurs.DoesNotExist:
        return render(request, 'admin/message.html', {'error': 'Opérateur non trouvé'})
    messages_non_lus = Message.objects.filter(id_operateur=1, notifié=False)
    
    # messages_non_lus = Message.objects.filter(id_operateur=operator, notifié=False).order_by('date_envoi')
    return render(request, 'admin/message.html', {'messages_non_lus': messages_non_lus})


def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # Marquer le message comme lu
    if not message.notifié:
        message.notifié = True
        message.save()

    return redirect('reponse_admin', message.id_contribuable.id)




def notifier_message_cont(request):
    contribuable_id = request.session.get('contribuable_id')

    # Récupérer les messages non lus pour l'opérateur connecté
    # operator = request.user.operateur
    messages_non_lus = Message.objects.filter(id_contribuable_id=contribuable_id, notifié=False)
    
    # Passer les messages au template
    return render(request, 'layout/navbar_admin.html', {'messages_non_lus': messages_non_lus})



# @login_required
def dashboard(request):
    # Récupérer les messages non lus pour l'opérateur connecté
    # operator = request.user.operateur
    messages_non_lus = Message.objects.filter(id_operateur=1, notifié=False)
    
    # Passer les messages au template
    return render(request, 'layout/navbar_admin.html', {'messages_non_lus': messages_non_lus})



# def dashboard(request):
#     # Récupérer les informations de session
#     contribuable_id = request.session.get('contribuable_id')
#     prenif = request.session.get('prenif')
#     email = request.session.get('email')

#     return render(request, 'acceuil/dashboard.html', {
#         'contribuable_id': contribuable_id,
#         'prenif': prenif,
#         'email': email
#     })


from django.shortcuts import render
from .models import VideoPublicite

