from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Token, Contribuable
import uuid
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, now

def generate_token(request, contribuable_id):
    """
    Génère un nouveau token pour un utilisateur spécifique.
    Désactive également les tokens expirés.
    """
    contribuable = get_object_or_404(Contribuable, id=contribuable_id)

    # Désactiver les tokens expirés pour ce contribuable
    Token.objects.filter(contribuable=contribuable, expires_at__lt=now(), is_active=True).update(is_active=False)

    # Générer un nouveau token unique
    new_token = str(uuid.uuid4())

    # Calculer la date d'expiration (1 heure après la génération)
    expires_at = make_aware(datetime.now() + timedelta(hours=1))

    # Créer et enregistrer le nouveau token
    token = Token.objects.create(
        contribuable=contribuable,
        token=new_token,
        expires_at=expires_at,
        is_active=True
    )

    return JsonResponse({
        "message": "Token généré avec succès",
        "token": token.token,
        "expires_at": token.expires_at.strftime('%Y-%m-%dT%H:%M:%S')
    })
