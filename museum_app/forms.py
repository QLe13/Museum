from django import forms
from django.core.exceptions import ValidationError
from .models import Person, Exhibit, Visit, Item, Transaction, TransactionItem, PopularityReport

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

class ExhibitForm(forms.ModelForm):
    def clean(self):
        # print('self', self)
        super_ = super().clean()
        # print('self 2', self)
        # print('super', super_)
        # print(super_['start_date'] > super_['end_date'])
        # print('start', self.instance.start_date)
        # print('end', self.instance.end_date)
        if(super_['start_date'] > super_['end_date']):
            print('validation error')
            raise ValidationError(("Start date after end date"), code='invalid')
        return super_

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
