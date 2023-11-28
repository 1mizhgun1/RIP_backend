from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from ..models import OpticItem

@api_view(['Get'])
def getTypeList(request, format=None):
    types = OpticItem.objects.values_list('type', flat=True).distinct()
    return Response(types, status=status.HTTP_202_ACCEPTED)