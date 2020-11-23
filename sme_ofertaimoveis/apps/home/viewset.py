#-*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .models import (
    TypeRegisters, Bidders, BiddersBuildings, BiddersBuildingsContacts,
    BiddersBuildingsDocsImages
)
from .serializers import (
    TypeRegistersSerializer, SMEContactsSerializer, RegisterSerializer
)


class TypeRegisterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TypeRegisters to be viewed or edited.
    """
    queryset = TypeRegisters.objects.all().order_by('name')
    serializer_class = TypeRegistersSerializer
    permission_classes = [permissions.IsAuthenticated]


class SMEContactsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SMEContacts to be viewed or edited.
    """
    queryset = SMEContacts.objects.all()
    serializer_class = SMEContactsSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Registers to be viewed or edited.
    """
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]
