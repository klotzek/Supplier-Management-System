from django.contrib import admin
from .models import Company, UserProfile, Claim, ClaimStatus, ClaimClassification, Plant, Team, D2_CV, D2_SV, D3, PenaltyPeriods, Ishikawa_occurance, Ishikawa_detection, Task, D4, D4_reproduction, File, W5_occurance, W5_detection

# Register your models here.
  
admin.site.register(Company)
admin.site.register(UserProfile)
admin.site.register(Claim)
admin.site.register(ClaimStatus)
admin.site.register(ClaimClassification)
admin.site.register(Plant)
admin.site.register(Team)
admin.site.register(D2_CV)
admin.site.register(D2_SV)
admin.site.register(D3)
admin.site.register(PenaltyPeriods)
admin.site.register(Ishikawa_occurance)
admin.site.register(Ishikawa_detection)
admin.site.register(Task)
admin.site.register(D4)
admin.site.register(D4_reproduction)
admin.site.register(File)
admin.site.register(W5_occurance)
admin.site.register(W5_detection)

                 