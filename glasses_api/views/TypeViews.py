from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import OpticItem


class TypeList_View(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        types = OpticItem.objects.values_list('type', flat=True).distinct()
        return Response(types, status=status.HTTP_202_ACCEPTED)