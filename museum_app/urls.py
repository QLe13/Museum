from django.urls import path, include
from rest_framework import routers
from .views import (
    PersonViewSet, ExhibitViewSet, VisitViewSet,
    ItemViewSet, TransactionViewSet, TransactionItemViewSet,
    PopularityReportViewSet,popularity_report_list, generate_popularity_report,
    item_list, regenerate_cutoff_prices, total_revenue, total_visitors,
    home
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
    path('', home, name='home'),
    path('api/', include(router.urls)),
    path('popularityReportsList/',popularity_report_list,name = 'popularity_report_list'),
    path('generatePopularityReports/',generate_popularity_report, name = 'generate_popularity_report'),
    path('adv/revenue/exhibit', total_revenue, name = 'total_revenue'),
    path('adv/visitors/exhibit', total_visitors, name = 'total_visitors'),
    path('itemsList/', item_list, name='item_list'),  # Add your function-based views here
    path('regenerate-cutoff-prices/', regenerate_cutoff_prices, name='regenerate_cutoff_prices'),
]
