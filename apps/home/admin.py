#-*- coding: utf-8 -*-
from django.contrib import admin
from .models import (
    TypeBidders, Bidders, BiddersBuildings, BiddersBuildingsContacts,
    BiddersBuildingsDocsImages
)


admin.register(TypeBidders)
admin.register(Bidders)
admin.register(BiddersBuildings)
admin.register(BiddersBuildingsContacts)
admin.register(BiddersBuildingsDocsImages)
