from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from rest_framework import viewsets
from .models import Person, Exhibit, Visit, Item, Transaction, TransactionItem, find_total_revenue, find_total_visitors, PopularityReport
from .serializers import (
    PersonSerializer, ExhibitSerializer, VisitSerializer,
    ItemSerializer, TransactionSerializer, TransactionItemSerializer,
    PopularityReportSerializer
)
from .signals import update_popularity_report
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
    elif table == 'transaction-item':
        return HttpResponse(loader.get_template("museum_app/addTransactionItem.html").render(request = request))
    else:
        return HttpResponseNotFound(loader.get_template("museum_app/notFound.html").render(request = request))



def read(request):
    return HttpResponse(loader.get_template("museum_app/read.html").render(request = request))

class PopularityReportViewSet(viewsets.ModelViewSet):
    queryset = PopularityReport.objects.all()
    serializer_class = PopularityReportSerializer

def popularity_report_list(request):
    """
    Display all the created popularity reports with their title, 
    start_date,end_date, rating and exhibit assoicated with it.
    """
    popularity_reports = PopularityReport.objects.all()
    return render(request, 'museum_app/popularity_report.html',{'popularity_reports':popularity_reports})

def generate_popularity_report(request):
    """
   Generate popularity report for each exhibit to be inserted in the popularity_report_list
    """
    if request.method == 'POST':
        visits = Visit.objects.all()
        for visit in visits:
            update_popularity_report(PopularityReport,visit,True)
        messages.success(request,'Popularity Report has been generate successfully.')
    else:
        messages.error(request,'Invaild Method request')
    return redirect('popularity_report_list')



def total_revenue(request):
    revenue_list = find_total_revenue()
    print(revenue_list)
    return render(request, 'museum_app/total_revenue.html', {'revenue_list':revenue_list})

def total_visitors(request):
    visitors_list = find_total_visitors()
    return render(request, 'museum_app/total_visitors.html', {'visitors_list': visitors_list})


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


def home(request):
    """
    Renders the main page with links to other pages.
    """
    return render(request, 'museum_app/home.html')
