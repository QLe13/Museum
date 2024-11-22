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
    revenue_list = find_total_revenue()
    html = '''
    <html>
    <head>
        <title>Total Revenue for Each Exhibit</title>
    </head>
    <body>
        <h1 style="text-align: center;">Total Revenue for Each Exhibit</h1>
        <table style="border-collapse: collapse; width: 80%; margin: auto;">
            <tr style="background-color: #f2f2f2;">
                <th style="border: 1px solid #ddd; padding: 8px;">Exhibit Name</th>
                <th style="border: 1px solid #ddd; padding: 8px;">Total Revenue</th>
            </tr>
    '''

    for revenue in revenue_list:
        html += '''
            <tr>
                <td style="border: 1px solid #ddd; padding: 8px;">{exhibit_name}</td>
                <td style="border: 1px solid #ddd; padding: 8px;">${total_revenue:.2f}</td>
            </tr>
        '''.format(
            exhibit_name=revenue,
            total_revenue=revenue_list[revenue]
        )

    html += '''
        </table>
    </body>
    </html>
    '''

    return HttpResponse(html)

def total_visitors(request):
    visitors_list = find_total_visitors()
    html = '''
    <html>
    <head>
        <title>Total Number of Visitors for Each Exhibit</title>
    </head>
    <body>
        <h1 style="text-align: center;">Total Number of Visitors for Each Exhibit</h1>
        <table style="border-collapse: collapse; width: 80%; margin: auto;">
            <tr style="background-color: #f2f2f2;">
                <th style="border: 1px solid #ddd; padding: 8px;">Exhibit Name</th>
                <th style="border: 1px solid #ddd; padding: 8px;">Total Visitors</th>
            </tr>
    '''

    for visitor in visitors_list:
        html += '''
            <tr>
                <td style="border: 1px solid #ddd; padding: 8px;">{exhibit_name}</td>
                <td style="border: 1px solid #ddd; padding: 8px;">{total_visitors}</td>
            </tr>
        '''.format(
            exhibit_name=visitor,
            total_visitors=visitors_list[visitor]
        )

    html += '''
        </table>
    </body>
    </html>
    '''

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

