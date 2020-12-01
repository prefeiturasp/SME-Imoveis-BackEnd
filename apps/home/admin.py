#-*- coding: utf-8 -*-
from django.contrib import admin
from .models import (
    TypeBidders, Bidders, BiddersBuildings, BiddersBuildingsDocsImages
)


admin.site.register(TypeBidders)
admin.site.register(Bidders)
admin.site.register(BiddersBuildings)
admin.site.register(BiddersBuildingsDocsImages)
