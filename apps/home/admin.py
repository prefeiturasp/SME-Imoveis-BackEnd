#-*- coding: utf-8 -*-
from django.contrib import admin
from .models import (
    TypeRegisters, Bidders, BiddersBuildings, BiddersBuildingsContacts,
    BiddersBuildingsDocsImages
)


admin.register(TypeRegisters)
admin.register(Bidders)
admin.register(BiddersBuildings)
admin.register(BiddersBuildingsContacts)
admin.register(BiddersBuildingsDocsImages)
