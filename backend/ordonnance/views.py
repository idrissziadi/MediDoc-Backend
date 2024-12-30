from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DPI, Ordonnance
from .serializers import OrdonnanceDetailSerializer
from DPI.permissions import IsPatientOrMedecin
from rest_framework.decorators import permission_classes

 

@api_view(['GET'])
@permission_classes([IsPatientOrMedecin])
def get_ordonnances(request):
   
    nss = request.query_params.get('nss')
    date = request.query_params.get('date')

    if not nss:
        return Response({'detail': 'Le champ NSS est obligatoire.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Récupérer le DPI
        dpi = DPI.objects.get(nss=nss)
    except DPI.DoesNotExist:
        return Response({'detail': 'DPI non trouvé avec ce NSS.'}, status=status.HTTP_404_NOT_FOUND)

    # Filtrer les ordonnances par NSS et éventuellement par date
    ordonnances = Ordonnance.objects.filter(
        consultation__dpi=dpi
    ).select_related('consultation__medecin')

    if date:
        ordonnances = ordonnances.filter(consultation__date__gt=date)

    # Sérialiser les données
    serializer = OrdonnanceDetailSerializer(ordonnances, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

