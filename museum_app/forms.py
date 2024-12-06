from django.forms import ModelForm
from .models import Exhibit,Item,Person,visit,Transaction,TransactionItem

class exhibitForm(ModelForm):
    class Meta:
        model = Exhibit
        fields = '__all__'
