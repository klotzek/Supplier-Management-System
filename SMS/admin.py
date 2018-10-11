from django.contrib import admin
# from .models import Company, UserProfile, Claim, ClaimStatus, ClaimClassification, Plant, Team, TraceData, D2_CV, D2_SV, D3, PenaltyPeriods, Ishikawa_occurance, Ishikawa_detection, Task, Comment, D4, D4_reproduction, File, W5_occurance, W5_detection, D7
from .models import *

# Register your models here.
  
admin.site.register(Company)
admin.site.register(UserProfile)
admin.site.register(Claim)
admin.site.register(ClaimStatus)
admin.site.register(ClaimClassification)
admin.site.register(Plant)
admin.site.register(Team)
admin.site.register(D2_CV)
admin.site.register(TraceData)
admin.site.register(D2_SV)
admin.site.register(D3)
admin.site.register(PenaltyPeriods)
admin.site.register(Ishikawa_occurance)
admin.site.register(Ishikawa_detection)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(D4)
admin.site.register(D4_reproduction)
admin.site.register(D6_effectiveness)
admin.site.register(File)
admin.site.register(W5_occurance)
admin.site.register(W5_detection)
admin.site.register(D7)
admin.site.register(Certifications)
admin.site.register(OtherCertifications)
admin.site.register(TaskList)

                 