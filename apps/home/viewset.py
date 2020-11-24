#-*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .models import (
    TypeRegisters, Bidders, BiddersBuildings, BiddersBuildingsContacts,
    BiddersBuildingsDocsImages
)
from .serializers import (
    TypeRegistersSerializer, BiddersSerializer, BiddersBuildingsSerializer,
    BiddersBuildingsContactsSerializer, BiddersBuildingsDocsImagesSerializer
)


class TypeRegisterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TypeRegisters to be viewed or edited.
    """
    queryset = TypeRegisters.objects.all().order_by('name')
    serializer_class = TypeRegistersSerializer
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


class BiddersBuildingsContactsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Store Bidders Buildings Contacts to be viewed or edited.
    """
    queryset = BiddersBuildingsContacts.objects.all()
    serializer_class = BiddersBuildingsContactsSerializer
    # permission_classes = [permissions.IsAuthenticated]


class BiddersBuildingsDocsImagesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Store Bidders Buildings Images and Documents to be viewed or edited.
    """
    queryset = BiddersBuildingsDocsImages.objects.all()
    serializer_class = BiddersBuildingsDocsImagesSerializer
    # permission_classes = [permissions.IsAuthenticated]
