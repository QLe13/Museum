from django.db import models
class Person(models.Model):
    ROLE_CHOICES = (
        ('visitor', 'Visitor'),
        ('staff', 'Staff'),
        ('admin', 'Administrator'),
        # Add more roles as needed
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name

class Exhibit(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    current_ticket_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Visit(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    exhibit = models.ForeignKey(Exhibit, on_delete=models.CASCADE)
    visit_date = models.DateField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)

class Item(models.Model):
    item_name = models.CharField(max_length=255)
    item_description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    exhibit = models.ForeignKey(Exhibit, null=True, blank=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(Person, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.item_name

class Transaction(models.Model):
    transaction_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    buyer = models.ForeignKey(Person, related_name='transactions_as_buyer', null=True, blank=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(Person, related_name='transactions_as_seller', null=True, blank=True, on_delete=models.SET_NULL)

class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class PopularityReport(models.Model):
    title = models.TextField(null = True, blank = True)
    start_date = models.DateField()
    end_date = models.DateField()
    rating = models.PositiveIntegerField()
    exhibit = models.ForeignKey(Exhibit,on_delete=models.CASCADE)
