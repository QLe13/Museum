from django.urls import path, include
from rest_framework import routers
from .views import (
    PersonViewSet, ExhibitViewSet, VisitViewSet,
    ItemViewSet, TransactionViewSet, TransactionItemViewSet,
    PopularityReportViewSet,popularity_report_list, generate_popularity_report,
    item_list, regenerate_cutoff_prices, total_revenue, total_visitors,
    home, crud, delete_object, edit_object, add_object
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView



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
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    #Basic funtionality URLS
    path('add/<str:model>/', add_object, name='add_object'),
    path('edit/<str:model>/<int:pk>/', edit_object, name='edit_object'),
    path('delete/<str:model>/<int:pk>/', delete_object, name='delete_object'),
    path('viewData/',crud, name = 'crud'),

    #Intermediate functionality URL
    path('itemsList/', item_list, name='item_list'),
    path('adv/revenue/exhibit', total_revenue, name = 'total_revenue'),
    path('adv/visitors/exhibit', total_visitors, name = 'total_visitors'),

    #Advance Functionality URL
    path('popularityReportsList/',popularity_report_list,name = 'popularity_report_list'),
    path('generatePopularityReports/',generate_popularity_report, name = 'generate_popularity_report'),
    path('regenerate-cutoff-prices/', regenerate_cutoff_prices, name='regenerate_cutoff_prices'),
]
