# -*- coding: utf-8 -*-
"""
URL definitions for the api.
"""
from sme_imoveis import api_routers

from apps.home.urls import router as home_router
from sme_ofertaimoveis.imovel.urls import router as sme_imoveis_router

router = api_routers.DefaultRouter()
router.extend(home_router)
router.extend(sme_imoveis_router)
