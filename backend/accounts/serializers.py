from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nom', 'email', 'role', 'specialite', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # Mot de passe en écriture seule
        }

    def create(self, validated_data):
        """
        Crée un utilisateur en utilisant le UserManager.
        """
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            nom=validated_data['nom'],
            role=validated_data['role'],
            specialite=validated_data['specialite']
        )
