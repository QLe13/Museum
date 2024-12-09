from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.utils.http import urlencode
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework import viewsets
from .models import Person, Exhibit, Visit, Item, Transaction, TransactionItem, find_total_revenue, find_total_visitors, PopularityReport
from .serializers import (
    PersonSerializer, ExhibitSerializer, VisitSerializer,
    ItemSerializer, TransactionSerializer, TransactionItemSerializer,
    PopularityReportSerializer
)

from .serializers import CutOffPriceResponseSerializer
from .signals import update_popularity_report
from .utils import update_cutoff_prices
from .forms import PersonForm, ExhibitForm, VisitForm, ItemForm, TransactionForm, TransactionItemForm, PopularityReportForm


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

#Allow us to access the home page or home.html
def home(request):
    """
    Renders the main page with links to other pages.
    """
    return render(request, 'museum_app/home.html')

#Connect to the crud.html
def crud(request):
    """
    Allows us to be able to view all of our models data and will give us access the add,update and delete function
    """
    # Define the models you want to manage
    models = {
        'Person': Person,
        'Exhibit': Exhibit,
        'Visit': Visit,
        'Item': Item,
        'Transaction': Transaction,
        'TransactionItem': TransactionItem
    }

    selected_model = request.GET.get('model', None)
    objects = None

    if selected_model in models:
        model_class = models[selected_model]
        objects = model_class.objects.all().values()

    return render(request, 'museum_app/crud.html', {
        'models': models.keys(),
        'selected_model': selected_model,
        'objects': objects,
    })

models_map = {
    'Person': (Person, PersonForm),
    'Exhibit': (Exhibit, ExhibitForm),
    'Visit': (Visit, VisitForm),
    'Item': (Item, ItemForm),
    'Transaction': (Transaction, TransactionForm),
    'TransactionItem': (TransactionItem, TransactionItemForm)
}

def add_object(request, model):
    if model not in models_map:
        messages.error(request, 'Invalid model selected.')
        return redirect('crud')

    obj_model, obj_form_class = models_map[model]

    if request.method == 'POST':
        form = obj_form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"{model} has been added.")
            base_url = reverse('crud')
            query_string = urlencode({'model': model})
            url = f"{base_url}?{query_string}"
            return redirect(url)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = obj_form_class()
    return render(request, 'museum_app/add_object.html', {
        'model': model,
        'form': form
    })

def delete_object(request, model, pk):
    if model not in models_map:
        messages.error(request, 'Invalid model selected.')
        return redirect('crud')

    obj_model, _ = models_map[model]
    obj = get_object_or_404(obj_model, pk=pk)

    if request.method == 'POST':
        obj.delete()
        messages.success(request, f"{model} (id={pk}) has been deleted.")
        base_url = reverse('crud')
        query_string = urlencode({'model': model})
        url = f"{base_url}?{query_string}"
        return redirect(url)
    else:
        # Optionally, show a confirmation page or just redirect
        messages.error(request, 'Invalid request method for delete.')
        return redirect('crud')


def edit_object(request, model, pk):
    if model not in models_map:
        messages.error(request, 'Invalid model selected.')
        return redirect('crud')

    obj_model, obj_form_class = models_map[model]
    obj = get_object_or_404(obj_model, pk=pk)

    if request.method == 'POST':
        form = obj_form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"{model} (id={pk}) has been updated.")
            base_url = reverse('crud') 
            query_string = urlencode({'model': model})
            url = f"{base_url}?{query_string}"
            return redirect(url)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = obj_form_class(instance=obj)

    return render(request, 'museum_app/edit_object.html', {
        'model': model,
        'obj': obj,
        'form': form
    })

def total_revenue(request):
    revenue_list = find_total_revenue()
    print(revenue_list)
    return render(request, 'museum_app/total_revenue.html', {'revenue_list':revenue_list})

def total_visitors(request):
    visitors_list = find_total_visitors()
    return render(request, 'museum_app/total_visitors.html', {'visitors_list': visitors_list})


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

def item_list(request):
    """
    Displays the list of items with their cut-off prices and a button to regenerate them.
    """
    items = Item.objects.all()
    return render(request, 'museum_app/item_list.html', {'items': items})

@extend_schema(
    methods = ['POST'],
    description = 'Return the CutOff Price',
    responses={
        200: CutOffPriceResponseSerializer,  # Successful response
        400: {"description": "Invalid request or data."},  # Error response
    }
)

@api_view(['POST'])
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

