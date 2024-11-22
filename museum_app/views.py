from django.shortcuts import render,redirect
from django.contrib import messages
from rest_framework import viewsets
from .models import Person, Exhibit, Visit, Item, Transaction, TransactionItem,PopularityReport
from .serializers import (
    PersonSerializer, ExhibitSerializer, VisitSerializer,
    ItemSerializer, TransactionSerializer, TransactionItemSerializer,
    PopularityReportSerializer
)
from .signals import update_popularity_report

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class ExhibitViewSet(viewsets.ModelViewSet):
    queryset = Exhibit.objects.all()
    serializer_class = ExhibitSerializer

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionItemViewSet(viewsets.ModelViewSet):
    queryset = TransactionItem.objects.all()
    serializer_class = TransactionItemSerializer

class PopularityReportViewSet(viewsets.ModelViewSet):
    queryset = PopularityReport.objects.all()
    serializer_class = PopularityReportSerializer

def popularity_report_list(request):
    """
    Display all the created popularity reports with their title, 
    start_date,end_date, rating and exhibit assoicated with it.
    """
    popreports = PopularityReport.objects.all()
    return render(request, 'museum_app/popularity_report.html',{'popularity_reports':popreports})

def generate_popularity_report(request):
    """
   Generate popularity report for each exhibit to be inserted in the popularity_report_list
    """
    if request.method == 'Post':
        visits = Visit.objets.all()
        for visit in visits:
            update_popularity_report(visit.id)
        messages.success(request,'Popularity Report has been generate successfully.')
    else:
        messages.error(request,'Invaild Method request')
    return redirect('popularity_report_list')
        