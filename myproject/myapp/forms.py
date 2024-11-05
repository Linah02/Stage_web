from django import forms
from .models import Contribuable

class ContribuableForm(forms.ModelForm):
    class Meta:
        model = Contribuable
        fields = [
            'nom', 
            'prenom', 
            'email', 
            'contact', 
            'mot_de_passe', 
            'fokontany', 
            'photo',
            # Ajoutez d'autres champs nécessaires
        ]
