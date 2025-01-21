from django.db import models
from datetime import datetime, timedelta
import uuid
 
class Genre(models.Model):
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.genre

class Sit_matrim(models.Model):
    situation = models.CharField(max_length=100)

    def __str__(self):
        return self.situation

# class User_token(models.Model):
#     id_contribuable = models.IntegerField()
#     tokenid

class Contribuable(models.Model):
    # Colonnes déjà présentes
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    lieu_naissance = models.CharField(max_length=120)
    situation_matrimoniale = models.ForeignKey(Sit_matrim, on_delete=models.SET_NULL, null=True)
    cin = models.CharField(max_length=15)
    date_delivrance = models.DateField()
    lieu_delivrance = models.CharField(max_length=120)
    contact = models.CharField(max_length=14)
    email = models.EmailField(unique=True)
    fokontany = models.IntegerField()
    mot_de_passe = models.CharField(max_length=128, null=True)
    bank_acct_no = models.CharField(max_length=250, null=True)  # Numéro de compte bancaire
    passeport = models.CharField(max_length=20, null=True)  # Numéro de passeport
    dm_ref = models.CharField(max_length=15, null=True)  # Référence de la demande
    propr_nif = models.CharField(max_length=10, null=True)  # Numéro d'identification fiscale
    statistic_no = models.CharField(max_length=21, null=True)  # Numéro statistique
    statistic_date = models.DateField(null=True)  # Date d'enregistrement statistique
    photo = models.ImageField(upload_to='images/faces/', blank=True, null=True)

    def __str__(self):
        return f'{self.nom} {self.prenom} {self.photo.name if self.photo else 'No Image'}'


class Token(models.Model):
    contribuable = models.ForeignKey(Contribuable, on_delete=models.CASCADE, related_name='tokens')  # Lien vers Contribuable
    token = models.CharField(max_length=255, unique=True)  # Token unique
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création du token
    expires_at = models.DateTimeField()  # Date d'expiration du token
    is_active = models.BooleanField(default=True)  # Statut actif/inactif du token

    def is_expired(self):
        """Vérifie si le token est expiré."""
        return datetime.utcnow() > self.expires_at

    def __str__(self):
        return f'Token for {self.contribuable.nom} {self.contribuable.prenom} (Active: {self.is_active})'
   
   
class Operateur(models.Model):
    cin = models.CharField(max_length=15)
    contact = models.CharField(max_length=14)

    def __str__(self):
        return f'{self.cin} {self.contact}'

class Country(models.Model):
    country_name = models.CharField(max_length=100)
    country_name_f = models.CharField(max_length=20, blank=True, null=True)
    country_name_s = models.CharField(max_length=20, blank=True, null=True)
    country_code = models.CharField(max_length=4)
    capital = models.CharField(max_length=100)

    def __str__(self):
        return self.country_name


class Parish(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    parish_name = models.CharField(max_length=35)
    parish_name_f = models.CharField(max_length=35, blank=True, null=True)
    parish_name_s = models.CharField(max_length=35, blank=True, null=True)
    parish_code = models.CharField(max_length=4)

    def __str__(self):
        return self.parish_name

class City(models.Model):
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=25)
    city_name_f = models.CharField(max_length=25, blank=True, null=True)
    city_name_s = models.CharField(max_length=25, blank=True, null=True)
    city_code = models.CharField(max_length=5)
    city_name_extra = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.city_name


class Locality(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    locality_desc = models.CharField(max_length=30)
    locality_desc_f = models.CharField(max_length=30, blank=True, null=True)
    locality_desc_s = models.CharField(max_length=30, blank=True, null=True)
    locality_code = models.CharField(max_length=6)

    def __str__(self):
        return self.locality_desc


class Wereda(models.Model):
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE)
    wereda_desc = models.CharField(max_length=50)
    wereda_code = models.IntegerField()

    def __str__(self):
        return self.wereda_desc

class Fokontany(models.Model):
    wereda = models.ForeignKey(Wereda, on_delete=models.CASCADE)
    fkt_desc = models.CharField(max_length=500)

    def __str__(self):
        return self.fkt_desc

class Logiciel(models.Model):
    logiciel = models.CharField(max_length=50)  # SURF/SIGTAS/HETRAONLINE

    def __str__(self):
        return self.logiciel

class ModePaiement(models.Model):
    sens = models.CharField(max_length=100)  # depot, declaration, espece, virement

    def __str__(self):
        return self.sens

class NumImpot(models.Model):
    impot = models.CharField(max_length=200)  # IRSA=5, IR=10, IS=15, AMENDE=43, PENALITE=44
    numero = models.IntegerField()

    def __str__(self):
        return f"{self.impot} ({self.numero})"

class CentralRecette(models.Model):
    id_contribuable = models.ForeignKey("Contribuable", on_delete=models.CASCADE)
    id_centre_recette = models.CharField(max_length=200)  # NIF+QUIT+CENTRE
    regisseur = models.CharField(max_length=50, null=True, blank=True, default=None)
    logiciel = models.ForeignKey(Logiciel, on_delete=models.CASCADE, null=True, blank=True)
    ref_trans = models.CharField(max_length=60, null=True, blank=True)
    ref_reglement = models.CharField(max_length=60, null=True, blank=True)
    daty = models.DateField(null=True, blank=True)
    mouvement = models.CharField(max_length=1, default='0')
    moyen_paiement = models.CharField(max_length=2, null=True, blank=True, default=None)
    rib = models.CharField(max_length=30, null=True, blank=True)
    raison_sociale = models.CharField(max_length=250, null=True, blank=True)
    nimp = models.ForeignKey(NumImpot, on_delete=models.CASCADE, null=True, blank=True)  # N° impôts
    libelle = models.CharField(max_length=20, null=True, blank=True)
    flag = models.CharField(max_length=1, default='N')
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    periode = models.IntegerField(default=1)  # Période d’impôts (1 ou 2)
    periode2 = models.CharField(max_length=10, null=True, blank=True)
    mnt_ap = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)  # Montant à payer
    base = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)  # Base de calcul
    imp_detail = models.CharField(max_length=200, null=True, blank=True)  # Nature des impôts
    da = models.IntegerField(default=0)  # Début d’activité (1/0)
    banque = models.CharField(max_length=75, null=True, blank=True)
    annee_recouvrement = models.IntegerField(null=True, blank=True)  # Date de recouvrement
    code_bureau = models.CharField(max_length=250, null=True, blank=True)  # Code unité opérationnelle
    libelle_bureau = models.CharField(max_length=250, null=True, blank=True)  # Centre fiscal

    def __str__(self):
        return f"Transaction {self.id_transaction} - Contribuable {self.id_contribuable}"


class Paiement(models.Model):
    id_contribuable = models.ForeignKey("Contribuable", on_delete=models.CASCADE)
    central_recette = models.ForeignKey(CentralRecette, on_delete=models.CASCADE)
    mode_paiement = models.ForeignKey(ModePaiement, on_delete=models.CASCADE)
    n_quit = models.CharField(max_length=50)  # Numéro quittance de paiement
    numrec = models.IntegerField(null=True, blank=True,default=0)  # N° de créance
    montant = models.DecimalField(max_digits=20, decimal_places=2)  # Montant à payer
    date_paiement = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Paiement {self.n_quit} - Contribuable {self.id_contribuable}"


class Operateurs(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    def __str__(self):
        return f'Operateurs {self.nom} {self.email}'

class Message(models.Model):
    contenu = models.TextField(blank=True, null=True)  # Le texte du message (optionnel si fichier joint)
    fichier_joint = models.FileField(upload_to='messages_fichiers/', blank=True, null=True)  # Fichier attaché, ex. PDF, Excel
    date_envoi = models.DateTimeField(auto_now_add=True)
    id_contribuable = models.ForeignKey(Contribuable, on_delete=models.CASCADE)
    id_operateur = models.ForeignKey(Operateurs, on_delete=models.SET_NULL, null=True, blank=True)
    type_message = models.CharField(max_length=20, choices=[('contribuable', 'Contribuable'), ('operateur', 'Opérateur')])
    notifié = models.BooleanField(default=False)
    def __str__(self):
        return f"Message de {self.type_message} le {self.date_envoi}"


class FokontanyView(models.Model):
    fkt_no = models.IntegerField(primary_key=True)
    fkt_desc = models.CharField(max_length=255)
    wereda_no = models.IntegerField()
    wereda_desc = models.CharField(max_length=255)
    wereda_code = models.CharField(max_length=10)
    locality_no = models.IntegerField()
    locality_desc = models.CharField(max_length=255)
    locality_desc_f = models.CharField(max_length=255, blank=True, null=True)
    locality_desc_s = models.CharField(max_length=255, blank=True, null=True)
    locality_code = models.CharField(max_length=10)
    city_no = models.IntegerField()
    city_name = models.CharField(max_length=255)
    city_name_f = models.CharField(max_length=255)
    city_name_s = models.CharField(max_length=255)
    city_code = models.CharField(max_length=10)
    city_name_extra = models.CharField(max_length=255, blank=True, null=True)
    parish_no = models.IntegerField()
    parish_name = models.CharField(max_length=255)
    parish_name_f = models.CharField(max_length=255)
    parish_name_s = models.CharField(max_length=255)
    parish_code = models.CharField(max_length=10)
    country_no = models.IntegerField()
    country_name = models.CharField(max_length=255)
    country_name_f = models.CharField(max_length=255)
    country_name_s = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    capital = models.CharField(max_length=255)

    class Meta:
        managed = False  # Indique à Django de ne pas essayer de créer ou de modifier cette table
        db_table = 'v_getfokontany'

class VueTransactionsParQuitEtContribuable(models.Model):
    contribuable = models.IntegerField()  # Changez cela si c'est juste un ID
    n_quit = models.CharField(max_length=50, primary_key=True)  # Numéro quittance comme clé primaire
    mont_ap = models.DecimalField(max_digits=20, decimal_places=2)  # Montant à payer
    total_payee = models.DecimalField(max_digits=20, decimal_places=2)  # Total payé
    reste_ap = models.DecimalField(max_digits=20, decimal_places=2)  # Reste à payer
    code_bureau = models.CharField(max_length=50)
    libelle_bureau = models.CharField(max_length=50)
    imp_detail = models.CharField(max_length=50)
    numero = models.CharField(max_length=50)
    impot =models.CharField(max_length=50)
    sens=models.CharField(max_length=50)
    logiciel=models.CharField(max_length=50)

    class Meta:
        managed = False  # Indique que ce modèle ne gère pas les migrations
        db_table = 'vue_transactions_par_quit_et_contribuable' 


class VueSommeParContribuableParAnnee(models.Model):
    contribuable = models.IntegerField()
    annee = models.IntegerField()
    total_mnt_ver = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False  # Indique que Django ne doit pas gérer les migrations pour ce modèle
        db_table = 'vue_somme_par_contribuable_par_annee'  # Nom de votre vue dans la base de données
        unique_together = (('contribuable', 'annee'),)  # Si vous voulez traiter ce couple comme unique




class VueRecouvrementsEtPaiementsParAnnee(models.Model):
    contribuable = models.IntegerField()  # Utilisez IntegerField pour l'ID du contribuable
    annee_recouvrement = models.IntegerField()  # Pour l'année de recouvrement
    total_recouvrement_annuel = models.DecimalField(max_digits=10, decimal_places=2)  # Montant total des recouvrements
    total_paye_annuel = models.DecimalField(max_digits=10, decimal_places=2)  # Montant total payé

    class Meta:
        managed = False  # Indique que Django ne gère pas ce modèle (pas de migrations)
        db_table = 'vue_recouvrements_et_paiements_par_annee'  # Nom de la vue dans la base de données



class TransactionDetail(models.Model):
    contribuable = models.IntegerField()  # Utilisez IntegerField pour l'ID du contribuable
    n_quit = models.CharField(max_length=50)
    date_paiement = models.DateField()
    numrec = models.IntegerField(null=True, blank=True,default=0)  # N° de créance
    annee_de_paiement = models.IntegerField()
    annee_recouvrement = models.IntegerField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    base = models.DecimalField(max_digits=15, decimal_places=2)
    mnt_ap = models.DecimalField(max_digits=15, decimal_places=2)
    nimp = models.IntegerField()
    imp_detail = models.CharField(max_length=200)
    numero = models.CharField(max_length=50)
    impot = models.CharField(max_length=50)
    sens = models.CharField(max_length=50)
    logiciel = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=15, decimal_places=2)


    class Meta:
        managed = False  # Indique que Django ne doit pas essayer de créer ou modifier cette table
        db_table = 'vue_detail_transactions_par_quit_et_contribuable'  # Nom de la vue dans la base de données
        verbose_name = 'Transaction Detail'
        verbose_name_plural = 'Transaction Details'

    def __str__(self):
        return f"Contribuable {self.contribuable} - Quittance {self.n_quit}"


from django.db import models

class VideoPublicite(models.Model):
    titre = models.CharField(max_length=255, help_text="Titre de la vidéo publicitaire")
    description = models.TextField(blank=True, help_text="Description ou contenu de la vidéo")
    video = models.FileField(upload_to='videos/', blank=True, null=True, help_text="Fichier vidéo local")
    lien_video = models.URLField(blank=True, null=True, help_text="Lien externe pour la vidéo")
    date_publication = models.DateTimeField(auto_now_add=True, help_text="Date de publication")
    duree = models.DurationField(blank=True, null=True, help_text="Durée de la vidéo (HH:MM:SS)")
    categorie = models.CharField(max_length=100, blank=True, help_text="Catégorie de la publicité")
    langue = models.CharField(max_length=50, blank=True, help_text="Langue principale de la vidéo")
    statut = models.CharField(
        max_length=20,
        choices=[
            ('brouillon', 'Brouillon'),
            ('publie', 'Publié'),
            ('archive', 'Archivé')
        ],
        default='brouillon',
        help_text="Statut de la vidéo"
    )
    tags = models.CharField(max_length=255, blank=True, help_text="Tags ou mots-clés pour la recherche")
    nombre_vues = models.PositiveIntegerField(default=0, help_text="Nombre de vues de la vidéo")
    auteur = models.CharField(max_length=255, blank=True, help_text="Auteur de la vidéo")
    miniature = models.ImageField(upload_to='thumbnails/', blank=True, null=True, help_text="Miniature pour la vidéo")
    date_modification = models.DateTimeField(auto_now=True, help_text="Date de dernière modification")

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "Vidéo Publicitaire"
        verbose_name_plural = "Vidéos Publicitaires"
        ordering = ['-date_publication']


class Brochure(models.Model):
    titre = models.CharField(max_length=200)  # Titre de la brochure
    description = models.TextField()  # Description de la brochure
    fichier_pdf = models.FileField(upload_to='brochurespdfs/')  # Fichier PDF
    date_publication = models.DateField(auto_now_add=True)  # Date de publication de la brochure

    def __str__(self):
        return self.titre