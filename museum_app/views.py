from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from rest_framework import viewsets
from .models import Person, Exhibit, Visit, Item, Transaction, TransactionItem, find_total_revenue, find_total_visitors
from .serializers import (
    PersonSerializer, ExhibitSerializer, VisitSerializer,
    ItemSerializer, TransactionSerializer, TransactionItemSerializer
)
from .utils import update_cutoff_prices

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

def item_list(request):
    """
    Displays the list of items with their cut-off prices and a button to regenerate them.
    """
    items = Item.objects.all()
    return render(request, 'museum_app/item_list.html', {'items': items})

def regenerate_cutoff_prices(request):
    """
    Regenerates the cut-off prices for all exhibits and redirects back to the item list.
    """
    if request.method == 'POST':
        # Optionally, check user permissions here
        exhibits = Exhibit.objects.all()
        for exhibit in exhibits:
            update_cutoff_prices(exhibit.id)
        messages.success(request, 'Cut-off prices have been regenerated successfully.')
    else:
        messages.error(request, 'Invalid request method.')
    return redirect('item_list')

