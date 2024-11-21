from .models import PopularityReport,Visit
from django.db.models import count,round,quarter,year
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone

def caclulate_rating():
    visitors_per_exhibit = Visit.objects.filter(exhibit = PopularityReport.exhibit,visit_date__quarter = quarter(PopularityReport.start_date)).count(id)
    total_vistors_to_museum = Visit.objects.all().count(id)

    if total_vistors_to_museum > 0:
       PopularityReport.rating = round((visitors_per_exhibit/total_vistors_to_museum)*100)
    else:
        PopularityReport.rating = 0
    
    return PopularityReport.rating

@receiver(post_save,sender=Visit)
def generate_popularity_report(sender,instance,created, **kwargs):
    if created:
        quarter = instance.visit_date.quarter
        year = instance.vist_date.year

        exhibit_report = PopularityReport.objects.filter(start_date__year = year,start_date__quarter = quarter)

        if not exhibit_report:
            start_date = instance.visit_date.replace(month=quarter * 3 - 2, day=1)
            end_date = instance.visit_date - timedelta(days=instance.visit_date.day)

            total_visits = Visit.objects.filter(visit_date__range=(start_date, end_date)).count()
            exhibit_visits = Visit.objects.filter(visit_date__range=(start_date, end_date), exhibit=instance.exhibit).count()
            rating = round((exhibit_visits / total_visits) * 100, 2)

            # Create a new PopularityReport
            PopularityReport.objects.create(
                title='Quarterly Report',
                start_date=start_date,
                end_date=end_date,
                rating=rating,
                exhibit=instance.exhibit
            )

    





    
        
   

