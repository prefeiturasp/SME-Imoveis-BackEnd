# -*- coding: utf-8 -*-
from rest_framework import serializers
from ..models import (
    TypeBidders, Bidders, BiddersBuildings, BiddersBuildingsDocsImages
)


class TypeBiddersSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeBidders
        fields = ['pk_type_bidders', 'name']


class BiddersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bidders
        fields = [
            'pk_bidders', 'fk_type_bidders', 'name', 'email', 'phone',
            'cel', 'insert_date', 'update_date'
        ]


class BiddersBuildingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BiddersBuildings
        fields = [
            'fk_bidders', 'cep', 'address', 'quarter', 'number',
            'complement', 'latitude', 'longitude', 'number_iptu',
            'insert_date', 'update_date'
        ]


class BiddersBuildingsDocsImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = BiddersBuildingsDocsImages
        fields = [
            'fk_bidders_buildings', 'document', 'flag_type_docs',
            'flag_type_file', 'insert_date', 'update_date',
        ]
