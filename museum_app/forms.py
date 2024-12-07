from django.forms import ModelForm
from .models import Exhibit,Item,Person,Visit,Transaction,TransactionItem

class exhibitForm(ModelForm):
    class Meta:
        model = Exhibit
        fields = '__all__'

class itemFrom(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
class personForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

class transactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

class transactionItemForm(ModelForm):
    class Meta:
        model = TransactionItem
        field = '__all__'
class visitForm(ModelForm):
    class Meta:
        model = Visit
        fields = '__all__'
