from django import forms
from .models import Person, Exhibit, Visit, Item, Transaction, TransactionItem, PopularityReport

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

class ExhibitForm(forms.ModelForm):
    class Meta:
        model = Exhibit
        fields = '__all__'

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = '__all__'

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

class TransactionItemForm(forms.ModelForm):
    class Meta:
        model = TransactionItem
        fields = '__all__'

class PopularityReportForm(forms.ModelForm):
    class Meta:
        model = PopularityReport
        fields = '__all__'
