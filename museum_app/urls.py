from django.urls import path, include
from rest_framework import routers
from .views import (
    PersonViewSet, ExhibitViewSet, VisitViewSet,
    ItemViewSet, TransactionViewSet, TransactionItemViewSet, total_revenue, total_visitors
)

router = routers.DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'exhibits', ExhibitViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'items', ItemViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'transaction-items', TransactionItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('adv/revenue/exhibit', total_revenue),
    path('adv/visitors/exhibit', total_visitors)
]
