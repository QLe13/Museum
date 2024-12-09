from rest_framework import serializers
from .models import Person, Exhibit, Visit, Item, Transaction, TransactionItem,PopularityReport

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class ExhibitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exhibit
        fields = '__all__'

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class TransactionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionItem
        fields = '__all__'

class PopularityReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularityReport
        fields = '__all__'

class CutOffPriceResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    cutoff_prices = serializers.ListField(
        child=serializers.DictField(
            child=serializers.FloatField(),
            allow_empty=False,
        )
    )