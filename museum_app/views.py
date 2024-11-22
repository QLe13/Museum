from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from rest_framework import viewsets
from .models import Person, Exhibit, Visit, Item, Transaction, TransactionItem
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

def v1(request):
    return HttpResponse(loader.get_template("museum_app/v1.html").render(request = request))

def index(request):
    return HttpResponse(loader.get_template("museum_app/index.html").render(request = request))

def add(request):
    return HttpResponse(loader.get_template("museum_app/add.html").render(request = request))

def addResponse(request):
    table = request.GET['table'].lower()
    if table.lower() == 'person':
        return HttpResponse(loader.get_template("museum_app/addPerson.html").render(request = request))
    elif table == 'exhibit':
        return HttpResponse(loader.get_template("museum_app/addExhibit.html").render(request = request))
    elif table == 'visit':
        return HttpResponse(loader.get_template("museum_app/addVisit.html").render(request = request))
    elif table == 'item':
        return HttpResponse(loader.get_template("museum_app/addItem.html").render(request = request))
    elif table == 'transaction':
        return HttpResponse(loader.get_template("museum_app/addTransaction.html").render(request = request))
    elif table == 'transaction_item':
        return HttpResponse(loader.get_template("museum_app/addTransactionItem.html").render(request = request))
    else:
        return HttpResponseNotFound(loader.get_template("museum_app/notFound.html").render(request = request))
