# -*- coding: utf-8 -*-
from rest_framework import viewsets
from ..models import (
    TypeBidders, Bidders, BiddersBuildings, BuildingsContacts,
    BiddersBuildingsDocsImages
)
from .serializers import (
    TypeBiddersSerializer, BiddersSerializer, BiddersBuildingsSerializer,
    BuildingsContactsSerializer, BiddersBuildingsDocsImagesSerializer
)


class TipoProponenteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TypeRegisters to be viewed or edited.
    """
    queryset = TypeBidders.objects.all().order_by('name')
    serializer_class = TypeBiddersSerializer
    # permission_classes = [permissions.IsAuthenticated]


class BiddersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Bidders to be viewed or edited.
    """
    queryset = Bidders.objects.all()
    serializer_class = BiddersSerializer
    # permission_classes = [permissions.IsAuthenticated]


class BiddersBuildingsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Store Buildings to be viewed or edited.
    """
    queryset = BiddersBuildings.objects.all()
    serializer_class = BiddersBuildingsSerializer
    # permission_classes = [permissions.IsAuthenticated]


class BuildingsContactsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Store Bidders Buildings Contacts to be viewed or edited.
    """
    queryset = BuildingsContacts.objects.all()
    serializer_class = BuildingsContactsSerializer
    # permission_classes = [permissions.IsAuthenticated]


class BiddersBuildingsDocsImagesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Store Bidders Buildings Images and Documents to be viewed or edited.
    """
    queryset = BiddersBuildingsDocsImages.objects.all()
    serializer_class = BiddersBuildingsDocsImagesSerializer
    # permission_classes = [permissions.IsAuthenticated]
