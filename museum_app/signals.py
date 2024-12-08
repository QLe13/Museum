from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PopularityReport, Visit
from datetime import date
import calendar


def get_quarter(dt):
    return (dt.month-1)//3 + 1

@receiver(post_save, sender=Visit)
def update_popularity_report(sender, instance, created, **kwargs):
    visit_date = instance.visit_date
    quarter = get_quarter(visit_date)
    year = visit_date.year

    start_month = (quarter - 1) * 3 + 1
    end_month = start_month + 2

    start_date = date(year, start_month, 1)
    end_day = calendar.monthrange(year, end_month)[1]
    end_date = date(year, end_month, end_day)

    exhibit = instance.exhibit

    report, created_report = PopularityReport.objects.get_or_create(
        exhibit=exhibit,
        start_date=start_date,
        end_date=end_date,
        defaults={'title': f'Popularity Report Q{quarter} {year}', 'rating': 0}
    )

    total_visits = Visit.objects.filter(
        visit_date__range=(start_date, end_date)
    ).count()

    exhibit_visits = Visit.objects.filter(
        exhibit=exhibit,
        visit_date__range=(start_date, end_date)
    ).count()

    if total_visits > 0:
        rating = round((exhibit_visits / total_visits) * 100)
    else:
        rating = 0

    report.rating = rating
    report.save()