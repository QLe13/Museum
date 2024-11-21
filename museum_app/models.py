from django.db import models
from django.db import connection
import django.dispatch 

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


def GeneratePopularityReportTrigger():
    with connection.cursor() as cursor:
        cursor.execute("""
                    CREATE TRIGGER generate_popularity_report
                    AFTER INSERT ON museum_app_visit
                    FOR EACH ROW
                    BEGIN
                       DECLARE new_quarter INT;
                       DECLARE new_year INT;
                       DECLARE start_date DATE;
                       DECLARE end_date DATE;
                       DECLARE exhibit_id INT;
                       DECLARE total_visitors INT;
                       DECLARE exhibit_visitors INT;

                       SET new_quarter = QUARTER(NEW.visit_date);
                       SET new_year = YEAR(NEW.visit_date);
                       SET start_date = DATE_SUB(NEW.visit_date, INTERVAL MOD(MONTH(NEW.visit_date) - 1, 3) MONTH);
                       SET end_date = LAST_DAY(DATE_SUB(NEW.visit_date, INTERVAL 1 MONTH));
                       SET exhibit_id = NEW.exhibit_id;
                       IF NOT EXISTS (
                          SELECT 1
                          FROM museum_app_popularityreport
                          WHERE start_date = start_date AND end_date = end_date
                       ) THEN
                          SELECT COUNT(*), SUM(CASE WHEN v.exhibit_id = exhibit_id THEN 1 ELSE 0 END)
                          INTO total_visitors, exhibit_visitors
                          FROM museum_app_visit v
                          WHERE v.visit_date BETWEEN start_date AND end_date;
                              INSERT INTO museum_app_popularityreport(title, start_date,end_date,rating, exhibit_id)
                              VALUES (
                              'New Popularity Report',
                               start_date,
                               end_date,
                               exhibit_id,
                               ROUND((exhibit_visitors / total_visitors) * 100, 2)
                               );
                        END IF;
                    END;
                """)