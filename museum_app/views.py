import datetime

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
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
    data = {'exhibits': Exhibit.objects.all()}
    if table.lower() == 'person':
        return HttpResponse(loader.get_template("museum_app/addPerson.html").render(request = request))
    elif table == 'exhibit':
        return HttpResponse(loader.get_template("museum_app/addExhibit.html").render(request = request))
    elif table == 'visit':
        return HttpResponse(loader.get_template("museum_app/addVisit.html").render(request = request, context=data))
    elif table == 'item':
        return HttpResponse(loader.get_template("museum_app/addItem.html").render(request = request, context= data))
    elif table == 'transaction':
        return HttpResponse(loader.get_template("museum_app/addTransaction.html").render(request = request))
    elif table == 'transaction-item':
        return HttpResponse(loader.get_template("museum_app/addTransactionItem.html").render(request = request))
    else:
        return HttpResponseNotFound(loader.get_template("museum_app/notFound.html").render(request = request))



def read(request):
    return HttpResponse(loader.get_template("museum_app/read.html").render(request = request))

def update(request):
    return HttpResponse(loader.get_template("museum_app/update.html").render(request = request))

def updateResponse(request):
    table = request.POST['table'].lower()
    for i in request.POST.values():
        if i == '':
            print(request.POST)
            return HttpResponseBadRequest('Missing data <form action="/" method="get"><button type="submit">Home</button></form>')


    if table == 'person':
        _updatePerson(request.POST)
    elif table == 'exhibit':
        _updateExhibit(request.POST)
    elif table == 'visit':
        _updateVisit(request.POST)
    elif table == 'item':
        _updateItem(request.POST)
    elif table == 'transaction':
        _updateTransaction(request.POST)
    elif table == 'transaction-item':
        _updateTransactionItem(request.POST)
    else:
        for i in request.POST.keys():
            print(request.POST[i])

        return HttpResponseNotFound(loader.get_template("museum_app/notFound.html").render(request = request))

    return HttpResponse('ok <form action=')

def _updateExhibit(newData):
    rowID = newData['id']
    dbData = Exhibit.objects.get(pk=rowID)
    dbData.name = newData['name']
    dbData.description = newData['description']
    startDate_ = newData['start_date']
    startDate = datetime.date(year=int(startDate_[0:4]), month=int(startDate_[5:7]), day=int(startDate_[8:]))
    dbData.start_date = startDate
    endDate_ = newData['end_date']
    endDate = datetime.date(year=int(endDate_[0:4]), month=int(endDate_[5:7]), day=int(endDate_[8:]))
    dbData.end_date = endDate
    dbData.current_ticket_price = newData['current_ticket_price']
    dbData.save()

def _updatePerson(newData):
    rowID = newData['id']
    dbData = Person.objects.get(pk=rowID)
    dbData.name = newData['name']
    dbData.email = newData['email']
    dbData.phone = newData['phone']
    dbData.role = newData['role']
    dbData.save()

def _updateVisit(newData):
    rowID = newData['id']
    dbData = Visit.objects.get(pk=rowID)
    visitDate_ = newData['visit_date']
    visitDate = datetime.date(year=int(visitDate_[0:4]), month=int(visitDate_[5:7]), day=int(visitDate_[8:]))
    dbData.visit_date = visitDate
    dbData.ticket_price = newData['ticket_price']
    dbData.exhibit = Exhibit.objects.get(pk=int(newData['exhibit']))
    dbData.person = Person.objects.get(pk=int(newData['person']))
    dbData.save()

def _updateItem(newData):
    rowID = newData['id']
    dbData = Item.objects.get(pk=rowID)
    dbData.item_name = newData['item_name']
    dbData.item_description = newData['item_description']
    dbData.category = newData['category']
    dbData.price = newData['price']
    dbData.quantity = newData['quantity']
    dbData.cutoff_price = 0 if newData['cutoff_price'] == 'null' else newData['cutoff_price']
    dbData.exhibit = Exhibit.objects.get(pk=int(newData['exhibit']))
    dbData.owner = Person.objects.get(pk=int(newData['owner']))
    dbData.save()

def _updateTransaction(newData):
    rowID = newData['id']
    dbData = Transaction.objects.get(pk=rowID)
    dbData.transaction_date = newData['transaction_date']
    dbData.total_amount = newData['total_amount']
    dbData.buyer = Person.objects.get(pk=int(newData['buyer']))
    dbData.seller = Person.objects.get(pk=int(newData['seller']))
    dbData.save()

def _updateTransactionItem(newData):
    rowID = newData['id']
    dbData = TransactionItem.objects.get(pk=rowID)
    dbData.transaction = Transaction.objects.get(pk=int(newData['transaction']))
    dbData.item = Item.objects.get(pk=int(newData['item']))
    dbData.quantity = newData['quantity']
    dbData.price = newData['price']
    dbData.save()


def delete(request):
    return HttpResponse(loader.get_template("museum_app/delete.html").render(request = request))

def deleteResponse(request):
    data = request.POST
    print(data)
    dataTable_ = data['table']
    dataTable = dataTable_.lower()
    queryTable = ''
    if dataTable == 'exhibit':
        queryTable = Exhibit
    elif dataTable == 'item':
        queryTable = Item
    elif dataTable == 'person':
        queryTable = Person
    elif dataTable == 'transaction':
        queryTable = Transaction
    elif dataTable == 'transaction-item':
        queryTable = TransactionItem
    elif dataTable == 'visit':
        queryTable = Visit
    else:
        return HttpResponseNotFound(loader.get_template("museum_app/notFound.html").render(request = request))

    row = data['row']
    try:
        oldRow = queryTable.objects.get(pk=row)
    except queryTable.DoesNotExist:
        return HttpResponseNotFound(loader.get_template("museum_app/notFound.html").render(request = request))

    oldRow.delete()
    return HttpResponse('row with id: ' + row + ' of ' + dataTable_ + ' has been deleted.')


########################
# Advanced Functionality
########################
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
