from django.urls import path, include
from rest_framework import routers
from .views import (
    PersonViewSet, ExhibitViewSet, VisitViewSet,
    ItemViewSet, TransactionViewSet, TransactionItemViewSet,
    PopularityReportViewSet
)

router = routers.DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'exhibits', ExhibitViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'items', ItemViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'transaction-items', TransactionItemViewSet)
router.register(r'popularity-reports',PopularityReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
