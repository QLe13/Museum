from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Person, Exhibit, Visit, Item, Transaction, TransactionItem, find_total_revenue, find_total_visitors
from .serializers import (
    PersonSerializer, ExhibitSerializer, VisitSerializer,
    ItemSerializer, TransactionSerializer, TransactionItemSerializer
)

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

def total_revenue(request):
    revenue = find_total_revenue()
    html = '<html><body>The total revenue for each exhibit is %s' % revenue
    return HttpResponse(html)

def total_visitors(request):
    visitors = find_total_visitors()
    html = '<html><body>The total number of visitors for each exhibit is %s' % visitors
    return HttpResponse(html)