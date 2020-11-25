# -*- coding: utf-8 -*-
from rest_framework import serializers
from ..models import (
    TypeBidders, Bidders, BiddersBuildings, BiddersBuildingsContacts,
    BiddersBuildingsDocsImages
)


class TypeBiddersSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TypeBidders
        fields = ['pk_type_bidders', 'name']


class BiddersSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Bidders
        fields = [
            'pk_bidders', 'fk_type_bidders_id', 'name', 'email', 'telefone',
            'insert_date', 'update_date'
        ]


class BiddersBuildingsSerializer(serializers.HyperlinkedModelSerializer):
    fk_bidders = serializers.StringRelatedField(many=True)

    class Meta:
        model = BiddersBuildings
        fields = [
            'fk_bidders', 'cep', 'address', 'quarter', 'number',
            'complement', 'latitude', 'longitude', 'number_iptu',
            'insert_date', 'update_date',

        ]


class BiddersBuildingsContactsSerializer(serializers.HyperlinkedModelSerializer):
    fk_bidders_buildings = serializers.StringRelatedField(many=True)

    class Meta:
        model = BiddersBuildingsContacts
        fields = [
            'fk_bidders_buildings', 'cep', 'address', 'quarter', 'number',
            'complement', 'flag_default', 'insert_date', 'update_date',
        ]


class BiddersBuildingsDocsImagesSerializer(serializers.HyperlinkedModelSerializer):
    fk_bidders_buildings_docs = serializers.StringRelatedField(many=True)

    class Meta:
        model = BiddersBuildingsDocsImages
        fields = [
            'fk_bidders_buildings_docs', 'document', 'flag_type_docs',
            'flag_type_file', 'insert_date', 'update_date',
        ]
