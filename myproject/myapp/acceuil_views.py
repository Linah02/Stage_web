import logging
logger = logging.getLogger(__name__)
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import json
from django.shortcuts import render, redirect,get_object_or_404
from .models import VueTransactionsParQuitEtContribuable  # Assurez-vous d'importer le modèle
from .models import VueSommeParContribuableParAnnee  # Assurez-vous d'importer le modèle
from .models import VueRecouvrementsEtPaiementsParAnnee
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db import connection
from django.contrib.auth.decorators import login_required
from .models import TransactionDetail
def acceuil(request):
    return render(request, 'acceuil/acceuil.html')  

def acceuilCte(request):
    return render(request, 'acceuil/acceuilCte.html')  

def test_acceuil(request):
    return render(request, 'acceuil/test.html')  


def home1(request):
    return render(request, 'myapp/home1.html')  

def discussion(request):
    return render(request, 'acceuil/message.html')  

def notification(request):
    return render(request, 'acceuil/notification.html')  


# def chart(request):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT contribuable, annee, total_mnt_ver FROM vue_somme_par_contribuable_par_annee")
#         rows = cursor.fetchall()

#     # Conversion des valeurs Decimal en float
#     sommes = [{'contribuable': row[0], 'annee': row[1], 'total_mnt_ver': float(row[2])} for row in rows]
    
#     return render(request, 'acceuil/transaction_chart.html', {'sommes': json.dumps(sommes)})

# def chart_line(request):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT contribuable, annee_recouvrement, total_recouvrement_annuel, total_paye_annuel FROM vue_recouvrements_et_paiements_par_annee")
#         rows = cursor.fetchall()

#     # Structurer les données pour le graphique
#     data_par_contribuable = {}
#     for contribuable, annee, total_recouvrement, total_paye in rows:
#         # Convertir les valeurs Decimal en float
#         total_recouvrement = float(total_recouvrement) if total_recouvrement is not None else 0.0
#         total_paye = float(total_paye) if total_paye is not None else 0.0
        
#         if contribuable not in data_par_contribuable:
#             data_par_contribuable[contribuable] = {'annees': [], 'recouvrements': [], 'paiements': []}
#         data_par_contribuable[contribuable]['annees'].append(annee)
#         data_par_contribuable[contribuable]['recouvrements'].append(total_recouvrement)
#         data_par_contribuable[contribuable]['paiements'].append(total_paye)

#     # Retourner les données sous forme JSON
#     return render(request, 'acceuil/evolution_transaction.html', {'data': json.dumps(data_par_contribuable)})


def chart(request):
    # Vérifiez si l'utilisateur est connecté
    # if request.session.get('id_contribuable'):
        # id_contribuable = request.session['id_contribuable']  # Récupérer l'ID du contribuable de la session
    id_contribuable = 6  # Récupérer l'ID du contribuable de la session
    with connection.cursor() as cursor:
        cursor.execute("SELECT contribuable, annee, total_mnt_ver FROM vue_somme_par_contribuable_par_annee WHERE contribuable = %s", [id_contribuable])
        rows = cursor.fetchall()

    # Conversion des valeurs Decimal en float
    sommes = [{'contribuable': row[0], 'annee': row[1], 'total_mnt_ver': float(row[2])} for row in rows]
    # else:
    #     sommes = []  # Pas de données si l'utilisateur n'est pas connecté
    return render(request, 'acceuil/transaction_chart.html', {'sommes': json.dumps(sommes)})


def chart_line(request):
    # Vérifiez si l'utilisateur est connecté
    # if request.session.get('id_contribuable'):
    id_contribuable = 6  # Récupérer l'ID du contribuable de la session
    # id_contribuable = request.session['id_contribuable']  # Récupérer l'ID du contribuable de la session
    with connection.cursor() as cursor:
        cursor.execute("SELECT contribuable, annee_recouvrement, total_recouvrement_annuel, total_paye_annuel FROM vue_recouvrements_et_paiements_par_annee WHERE contribuable = %s", [id_contribuable])
        rows = cursor.fetchall()

        # Structurer les données pour le graphique
    data_par_contribuable = {}
    for contribuable, annee, total_recouvrement, total_paye in rows:
        # Convertir les valeurs Decimal en float
        total_recouvrement = float(total_recouvrement) if total_recouvrement is not None else 0.0
        total_paye = float(total_paye) if total_paye is not None else 0.0
        
        if contribuable not in data_par_contribuable:
            data_par_contribuable[contribuable] = {'annees': [], 'recouvrements': [], 'paiements': []}
        data_par_contribuable[contribuable]['annees'].append(annee)
        data_par_contribuable[contribuable]['recouvrements'].append(total_recouvrement)
        data_par_contribuable[contribuable]['paiements'].append(total_paye)

    # Retourner les données sous forme JSON
    return render(request, 'acceuil/evolution_transaction.html', {'data': json.dumps(data_par_contribuable)})
    # else:
    #     # Gérer le cas où l'utilisateur n'est pas connecté
    #     return render(request, 'acceuil/evolution_transaction.html', {'data': json.dumps({})})


def list_transaction(request):
    # Vérifiez si l'utilisateur est connecté
    # if request.session.get('id_contribuable'):
        # id_contribuable = request.session['id_contribuable']  # Récupérer l'ID du contribuable de la session
    id_contribuable = 6 # Récupérer l'ID du contribuable de la session
    transactions = VueTransactionsParQuitEtContribuable.objects.filter(contribuable=id_contribuable)  # Filtrer les transactions
    return render(request, 'acceuil/liste_transaction.html', {'transactions': transactions})  # Passer les données au template

    # else:
    #     transactions = []  # Pas de transactions si l'utilisateur n'est pas connecté



def profil(request):
    # Vérifiez si l'utilisateur est connecté
    # if 'id_contribuable' in request.session:
    id_contribuable = 6  # Récupérer l'ID du contribuable de la session
    # id_contribuable = request.session['id_contribuable']  # Récupérer l'ID du contribuable de la session

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
            'propr_nif': contribuable[6],
            'mot_de_passe': contribuable[13],
            # Ajoutez d'autres champs selon votre modèle
        }
    else:
        contribuable_info = {}  # Aucune information trouvée

    return render(request, 'myapp/profil.html', {'contribuable': contribuable_info})
    # else:
    #     # Gérer le cas où l'utilisateur n'est pas connecté
    #     return render(request, 'myapp/profil.html', {'error': 'Utilisateur non connecté.'})


# @login_required
# def get_transaction_details(request, n_quit):
#     # Récupérer l'ID du contribuable à partir de la session utilisateur
#     id_contribuable = 6
#     # id_contribuable = request.session.get('id_contribuable')

#     # Vérifier que l'ID du contribuable est défini
#     # if id_contribuable is None:
#     #     return render(request, 'myapp/error.html', {'message': 'Contribuable non connecté ou session invalide'})

#     # Préparation de la requête SQL
#     sql_query = """
#         SELECT 
#             contribuable, 
#             n_quit, 
#             date_paiement, 
#             annee_de_paiement, 
#             annee_recouvrement, 
#             date_debut, 
#             date_fin, 
#             base, 
#             mnt_ap, 
#             nimp AS NIMP, 
#             imp_detail, 
#             numero, 
#             impot, 
#             sens, 
#             logiciel 
#         FROM 
#             vue_detail_transactions_par_quit_et_contribuable 
#         WHERE 
#             contribuable = %s AND n_quit = %s
#     """

#     # Exécuter la requête SQL
#     with connection.cursor() as cursor:
#         logger.info("Exécution de la requête SQL : %s", sql_query % (id_contribuable, n_quit))  # Afficher la requête
#         cursor.execute(sql_query, [id_contribuable, n_quit])
        
#         # Récupérer tous les résultats
#         transaction_details = cursor.fetchall()

#     # Passer les résultats à votre template
#     return render(request, 'acceuil/transaction_details.html', {'transaction_details': transaction_details})


def get_transaction_details(request, n_quit):
    # Récupérer l'ID du contribuable à partir de la session utilisateur
    id_contribuable = 6

    # Préparation de la requête SQL
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
        'sql_query': sql_query_formatted  # Utilisation de la requête formatée
    })


def export_transaction_pdf(request, n_quit):
    # Récupérer l'ID du contribuable à partir de la session utilisateur
    id_contribuable = 6

    # Préparation de la requête SQL
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

    # Exécuter la requête SQL
    with connection.cursor() as cursor:
        logger.info("Exécution de la requête SQL : SELECT * FROM vue_detail_transactions_par_quit_et_contribuable WHERE contribuable = %d AND n_quit = '%s'", id_contribuable, n_quit)
        cursor.execute(sql_query, [id_contribuable, n_quit])  # Assurez-vous que n_quit est une chaîne
        transaction_details = cursor.fetchall()

    # Si aucune transaction n'est trouvée, vous pouvez gérer cela ici
    if not transaction_details:
        return HttpResponse("Aucune transaction trouvée.", status=404)

    # Passer les résultats au template
    html_string = render_to_string('acceuil/pdf_template.html', {
        'transaction_details': transaction_details,
        'n_quit': n_quit,
    })
    
    # Créer le PDF
    pdf = HTML(string=html_string).write_pdf()

    # Retourner le PDF comme réponse
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="transaction_{n_quit}.pdf"'
    return response