from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import Gathering
from apps.accounts.api.serializers import GatheringSerializer, GatheringDetailSerializer


class GatheringViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = 'code'
    serializer_class_mapping = {
        'retrieve': GatheringDetailSerializer,
    }

    def get_queryset(self):
        return Gathering.objects.filter(members=self.request.user)

    def get_serializer_class(self):
        return self.serializer_class_mapping.get(self.action, GatheringSerializer)
    
    def perform_create(self, serializer):
        gathering = serializer.save(owner=self.request.user)
        gathering.members.add(self.request.user)

    @action(detail=True, methods=['post'])
    def join(self, request, code=None):
        gathering = get_object_or_404(Gathering, code=code)
        gathering.members.add(request.user)
        serializer = self.get_serializer(gathering)
        return Response(serializer.data)
