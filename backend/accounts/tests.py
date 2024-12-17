from .serializers import UserSerializer

data = {
    'nom': 'John Doe',
    'email': 'john@example.com',
    'password': 'securepassword123',
    'role': 'medecin',
    'specialite': 'cardiologue'
}

serializer = UserSerializer(data=data)
if serializer.is_valid():
    user = serializer.save()
    print(user)
else:
    print(serializer.errors)
