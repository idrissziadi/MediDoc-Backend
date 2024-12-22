from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import User
from rest_framework.permissions import AllowAny
from .permissions import IsMedecin, IsAdministratif


@api_view(['POST'])
@authentication_classes([])  # Désactive l'authentification pour la vue signup
@permission_classes([AllowAny])  # Permet l'accès à tous les utilisateurs
def signup(request):
    """
    Vue pour inscrire un utilisateur.
    Si le champ 'specialite' n'est pas fourni, le définir à 'other'.
    """
    if request.method == 'POST':
        # Vérifier si 'specialite' est présent dans les données, sinon définir à 'other'
        if 'specialite' not in request.data:
            request.data['specialite'] = 'other'
        
        # Créer un serializer avec les données mises à jour
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])  # Désactive l'authentification pour la vue login
@permission_classes([AllowAny])  # Permet l'accès à tous les utilisateurs
def login(request):
    """
    Vue pour connecter un utilisateur.
    Retourne les tokens JWT et les informations de l'utilisateur.
    """
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)

            # Sérialisation des données utilisateur
            user_data = UserSerializer(user).data

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data,  # Informations sur l'utilisateur
            })

        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET'])
@permission_classes([IsMedecin])  # Permet l'accès seulement aux médecins
def get_user(request, user_id):
    """
    Vue permettant à un médecin de rechercher un utilisateur par son ID.
    """
    try:
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([IsAdministratif])   
def get_medecins(request):
    
    medecins = User.objects.filter(role='medecin').values('id', 'nom', 'specialite')
    return Response(medecins, status=200)
