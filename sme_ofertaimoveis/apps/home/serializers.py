#-*- coding: utf-8 -*-
from rest_framework import serializers
from .models import (
    TypeRegisters, Bidders, BiddersBuildings, BiddersBuildingsContacts,
    BiddersBuildingsDocsImages
)


class TypeRegistersSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TypeRegisters
        fields = ['id', 'name']


class BiddersSerializer(serializers.HyperlinkedModelSerializer):
    # register_types = TypeRegistersSerializer(many=True)

    class Meta:
        model = Bidders
        fields = [
            'pk_bidders', 'fk_type_registers', 'name', 'email', 'telefone',
            'insert_date', 'update_date'
        ]


class BiddersBuildingsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BiddersBuildings
        fields = [
            'fk_bidders', 'cep', 'address', 'quarter', 'number',
            'complement', 'latitude', 'longitude', 'number_iptu',
            'insert_date', 'update_date',

        ]


class BiddersBuildingsContactsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BiddersBuildingsContacts
        fields = [
            'fk_bidders', 'cep', 'address', 'quarter', 'number',
            'complement', 'flag_default', 'insert_date', 'update_date',
        ]


class BiddersBuildingsDocsImagesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BiddersBuildingsDocsImages
