from rest_framework import serializers
from .models import Genre, Sit_matrim,Contribuable,FokontanyView

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'genre']

class SitMatrimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sit_matrim
        fields = ['id', 'situation']

class FokontanyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = FokontanyView
        fields = [
            'fkt_no',
            'fkt_desc', 
            'wereda_desc', 
            'locality_desc', 
            'city_name', 
            'parish_name', 
            'locality_desc_f', 
            'locality_desc_s', 
            'city_name_extra', 
            'country_name'
        ]




class ContribuableFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribuable
        fields = ['nom', 'contact', 'email']
    
    def validate_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError("Email invalide.")
        return value
class ContribuableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribuable
        fields = [
            'nom', 'prenom', 'date_naissance', 'genre', 'lieu_naissance', 
            'situation_matrimoniale', 'cin', 'date_delivrance', 'lieu_delivrance', 
            'contact', 'email', 'fokontany', 'photo'
        ]  # Inclure uniquement les champs nécessaires à l'inscription

    def create(self, validated_data):
        # Gérer les champs générés automatiquement (e.g., mot_de_passe, propr_nif)
        mot_de_passe = self.generate_password_from_cin(validated_data.get('cin'))
        validated_data['mot_de_passe'] = mot_de_passe
        validated_data['propr_nif'] = self.generate_nif()
        return super().create(validated_data)

    def generate_password_from_cin(self, cin):
        """Générer un mot de passe en additionnant deux par deux les chiffres du CIN"""
        if len(cin) != 12 or not cin.isdigit():
            raise serializers.ValidationError("Le CIN doit contenir 12 chiffres.")
        return ''.join(str(int(cin[i]) + int(cin[i + 1])) for i in range(0, len(cin), 2))

    def generate_nif(self):
        """Générer un numéro d'identification fiscale (NIF) aléatoire"""
        import uuid
        return f"NIF-{uuid.uuid4().hex[:8].upper()}"
    

class TransactionSerializer(serializers.Serializer):
    n_quit = serializers.CharField()  # Colonne dans vue_transactions_par_quit_et_contribuable
    contribuable = serializers.IntegerField()
    total_payee = serializers.FloatField()
    reste_ap = serializers.FloatField()
