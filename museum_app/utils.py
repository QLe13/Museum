from .models import PopularityReport,Visit
from django.db.models import count,round,quarter

def caclulate_rating():
    visitors_per_exhibit = Visit.objects.filter(exhibit = PopularityReport.exhibit,visit_date__quarter = quarter(PopularityReport.start_date)).count(id)
    total_vistors_to_museum = Visit.objects.all().count(id)

    if total_vistors_to_museum > 0:
       PopularityReport.rating = round((visitors_per_exhibit/total_vistors_to_museum)*100)
    else:
        PopularityReport.rating = 0
    
    return PopularityReport.rating


    





    
        
   

