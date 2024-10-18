from django.db import models

class Genre(models.Model):
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.genre

class Sit_matrim(models.Model):
    situation = models.CharField(max_length=100)

    def __str__(self):
        return self.situation

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
    mot_de_passe = models.CharField(max_length=50, null=True)
    bank_acct_no = models.CharField(max_length=250, null=True)  # Numéro de compte bancaire
    passeport = models.CharField(max_length=20, null=True)  # Numéro de passeport
    dm_ref = models.CharField(max_length=15, null=True)  # Référence de la demande
    propr_nif = models.CharField(max_length=10, null=True)  # Numéro d'identification fiscale
    statistic_no = models.CharField(max_length=21, null=True)  # Numéro statistique
    statistic_date = models.DateField(null=True)  # Date d'enregistrement statistique
    photo = models.CharField(max_length=200, null=True)  # Photo du demandeur

    def __str__(self):
        return f'{self.nom} {self.prenom}'

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