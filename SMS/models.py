from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_countries.fields import CountryField
from datetime import datetime

# Create your models here.

class Company(models.Model):
   name =  models.CharField(max_length=200, unique=True, verbose_name='Vendor name')
   DUNS = models.CharField(max_length=10, unique=True)
   adress1 = models.CharField(max_length=200)
   adress2 = models.CharField(max_length=200, blank=True)
   postcode = models.CharField(max_length=15)
   town = models.CharField(max_length=200)
   country = CountryField()
   
   def __str__(self):
       return self.name

class ClaimStatus(models.Model):
    status = models.CharField(max_length=50)
    def __str__(self):
        return str(self.status)
    
class ClaimClassification(models.Model):
    classification = models.CharField(max_length=30)       
    def __str__(self):
        return str(self.classification)
            
class Plant(models.Model):
    plant = models.CharField(max_length=20, default='NMB-plant')
    class Meta:
        ordering = ('plant', )
    def __str__(self):
        return str(self.plant)

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))    
class Claim(models.Model):
    related_to = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(ClaimStatus, on_delete=models.DO_NOTHING)
    D2_description = models.TextField()
    part_number = models.CharField(max_length=50)
    speaking_name = models.CharField(max_length=50)
    project = models.CharField(max_length=50, blank=True, null=True)
    car_maker= models.CharField(max_length=25, blank=True, null=True)
    classification = models.ForeignKey(ClaimClassification, on_delete=models.SET_NULL, null=True)
    milage=models.IntegerField(blank=True, null=True)
    RMA = models.IntegerField(blank=True, null=True)
    due_date_D3 = models.DateTimeField(default = datetime.now())
    due_date_D4 = models.DateTimeField(default = datetime.now())
    due_date_D5 = models.DateTimeField(default = datetime.now())
    due_date_D6 = models.DateTimeField(default = datetime.now())
    due_date_D8 = models.DateTimeField(default = datetime.now())
    valid = models.BooleanField(default=True)
    File = models.FileField(blank=True, null=True, upload_to='uploads/')
    OK_picture = models.ImageField(blank=True, null=True, upload_to='uploads/')
    NOK_picture = models.ImageField(blank=True, null=True, upload_to='uploads/')
    plant = models.ForeignKey(Plant, verbose_name = 'NMB-plant', on_delete=models.SET_NULL, null=True)
    responsible_in_plant=models.CharField(max_length=20, blank=True, null=True)
    special_characteristic_impact=models.BooleanField(default=False)
    reoccurance = models.BooleanField(default=False)
    accepted = models.BooleanField(default= False)
    refused = models.BooleanField(default=False)
    production_date_1=models.DateTimeField(blank=True, null=True)
    production_date_2=models.DateTimeField(blank=True, null=True)
    production_date_3=models.DateTimeField(blank=True, null=True)
    operator_1=models.CharField(max_length=25, blank=True, null=True)
    operator_2=models.CharField(max_length=25, blank=True, null=True)
    operator_3=models.CharField(max_length=25, blank=True, null=True)
    batch_1=models.CharField(max_length=25, blank=True, null=True)
    batch_2=models.CharField(max_length=25, blank=True, null=True)
    batch_3=models.CharField(max_length=25, blank=True, null=True)
    cavity_1=models.CharField(max_length=25, blank=True, null=True)
    cavity_2=models.CharField(max_length=25, blank=True, null=True)
    cavity_3=models.CharField(max_length=25, blank=True, null=True)
       
  
    @property
    def is_past_D3(self):
        if timezone.now() > self.due_date_D3:
            return True
        return False
    def is_past_D4(self):
        if timezone.now() > self.due_date_D4:
            return True
        return False
        
    def __str__(self):
        return str(self.pk)
        
class claim_Data(models.Model):
    claim = models.OneToOneField(Claim, on_delete=models.SET_NULL, null=True)
    accepted = models.BooleanField(default= False)
    refused = models.BooleanField(default=False)
    production_date=models.DateTimeField()
    production_date_to=models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return str(self.claim)        
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
#     aus  https://www.b-list.org/weblog/2006/sep/02/django-tips-user-registration/
    email = models.EmailField()    
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null = True)
    isAdmin = models.BooleanField(default=False)
    isStaff = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=40, default='1234')
#     key_expires = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=9999))
    
    def __str__(self):
        return str(self.user)
        
class Team(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.SET_NULL, null=True)
    pilot=models.CharField(max_length=50)
    function=models.CharField(max_length=50)
    mail=models.EmailField(max_length=50)
    phone = models.CharField(max_length=25, blank = True, null = True)
    teammember_1= models.CharField(max_length=25, blank=True, null=True)
    function_1=models.CharField(max_length=25, blank=True, null=True, 
#     help_text="Only required if 'teammember 1' is selected.",
    )
    mail_1=models.EmailField(max_length=25, blank=True, null=True)
    phone_1 = models.CharField(max_length=25, blank = True, null = True)
    teammember_2= models.CharField(max_length=25, blank=True, null=True)
    function_2=models.CharField(max_length=25, blank=True, null=True)
    mail_2=models.EmailField(max_length=25, blank=True, null=True)
    phone_2 = models.CharField(max_length=25, blank = True, null = True)
    teammember_3= models.CharField(max_length=25, blank=True, null=True)
    function_3=models.CharField(max_length=25, blank=True, null=True)
    mail_3=models.EmailField(max_length=25, blank=True, null=True)
    phone_3 = models.CharField(max_length=25, blank = True, null = True)
    
    def __str__(self):
        return str(self.claim)
            
# class D1D3(models.Model):
#     claim = models.OneToOneField(Claim, on_delete=models.SET_NULL, null=True)
#     accepted = models.BooleanField(default= False)
#     refused = models.BooleanField(default=False)
#     production_date=models.DateTimeField()
#     production_date_to=models.DateTimeField(blank=True, null=True)
#     
#     def __str__(self):
#         return str(self.claim)        
    
class D2_CV(models.Model):  # CV = customer view
    claim = models.OneToOneField(Claim, on_delete=models.SET_NULL, null=True)
    what_happened = models.CharField(max_length=50)
    why_problem = models.CharField(max_length=50)
    when_detected = models.CharField(max_length=50)
    who_detected = models.CharField(max_length=50)
    where_detected = models.CharField(max_length=50)
    how_detected = models.CharField(max_length=50)
    how_many_NOK = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.claim)        
    
class D2_SV(models.Model):  # SV = supplier view
    claim = models.OneToOneField(Claim, on_delete=models.SET_NULL, null=True)
    difference = models.CharField(max_length=50)
    standard_process = models.CharField(max_length=50)
    when_produced = models.CharField(max_length=50)
    who_produced = models.CharField(max_length=50)
    other_application = models.CharField(max_length=50)
    reinjecting = models.CharField(max_length=50)
    similar_problem = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.claim)        

# BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))    
class D3(models.Model):  
    claim = models.OneToOneField(Claim, on_delete=models.SET_NULL, null=True)
    actions_ongoing = models.BooleanField(choices=BOOL_CHOICES, default=False)
    actions_necessary = models.BooleanField(choices=BOOL_CHOICES, default=False)
    completion_date = models.DateTimeField(blank=True, null=True)
    action_1= models.CharField(max_length=50, blank=True, null=True)
    pilot_1= models.CharField(max_length=50, blank=True, null=True)
    date_1= models.DateTimeField(blank=True, null=True)
    action_2= models.CharField(max_length=50, blank=True, null=True)
    pilot_2= models.CharField(max_length=50, blank=True, null=True)
    date_2= models.DateTimeField(blank=True, null=True)
    action_3= models.CharField(max_length=50, blank=True, null=True)
    pilot_3= models.CharField(max_length=50, blank=True, null=True)
    date_3= models.DateTimeField(blank=True, null=True)
    FC_necessary = models.BooleanField(choices=BOOL_CHOICES, default=False)  #FC=final customer
    FC_sorting_date= models.DateTimeField(blank=True, null=True, verbose_name='sorting date')
    FC_qty= models.IntegerField(blank=True, null=True, verbose_name='Qty sorted')
    FC_NOK= models.IntegerField(blank=True, null=True, verbose_name='Nb NOK found')
    FC_NOK_date= models.CharField(max_length=25, blank=True, null=True, verbose_name='NOK part production date')
    FC_date_from= models.CharField(max_length=25, blank=True, null=True, verbose_name='from prod. date sorted parts')
    FC_date_to= models.CharField(max_length=25, blank=True, null=True, verbose_name='to prod. date sorted parts')
    FC_comment = models.CharField(max_length=100, blank = True, null = True, verbose_name = 'comment')
    FC_transit_necessary = models.BooleanField(choices=BOOL_CHOICES, default=False)  #FC=final customer
    FC_transit_sorting_date= models.DateTimeField(blank=True, null=True, verbose_name='sorting date')
    FC_transit_qty= models.IntegerField(blank=True, null=True, verbose_name='Qty sorted')
    FC_transit_NOK= models.IntegerField(blank=True, null=True, verbose_name='Nb NOK found')
    FC_transit_NOK_date= models.CharField(max_length=25, blank=True, null=True, verbose_name='NOK part production date')
    FC_transit_date_from= models.CharField(max_length=25, blank=True, null=True, verbose_name='from prod. date sorted parts')
    FC_transit_date_to= models.CharField(max_length=25, blank=True, null=True, verbose_name='to prod. date sorted parts')
    FC_transit_comment = models.CharField(max_length=100, blank = True, null = True, verbose_name = 'comment')
    NMB_necessary = models.BooleanField(choices=BOOL_CHOICES, default=False)  
    NMB_sorting_date= models.DateTimeField(blank=True, null=True, verbose_name='sorting date')
    NMB_qty= models.IntegerField(blank=True, null=True, verbose_name='Qty sorted')
    NMB_NOK= models.IntegerField(blank=True, null=True, verbose_name='Nb NOK found')
    NMB_NOK_date= models.CharField(max_length=25, blank=True, null=True, verbose_name='NOK part production date')
    NMB_date_from= models.CharField(max_length=25, blank=True, null=True, verbose_name='from prod. date sorted parts')
    NMB_date_to= models.CharField(max_length=25, blank=True, null=True, verbose_name='to prod. date sorted parts')
    NMB_comment = models.CharField(max_length=100, blank = True, null = True, verbose_name = 'comment')
    NMB_transit_necessary = models.BooleanField(choices=BOOL_CHOICES, default=False)  
    NMB_transit_sorting_date= models.DateTimeField(blank=True, null=True, verbose_name='sorting date')
    NMB_transit_qty= models.IntegerField(blank=True, null=True, verbose_name='Qty sorted')
    NMB_transit_NOK= models.IntegerField(blank=True, null=True, verbose_name='Nb NOK found')
    NMB_transit_NOK_date= models.CharField(max_length=25, blank=True, null=True, verbose_name='NOK part production date')
    NMB_transit_date_from= models.CharField(max_length=25, blank=True, null=True, verbose_name='from prod. date sorted parts')
    NMB_transit_date_to= models.CharField(max_length=25, blank=True, null=True, verbose_name='to prod. date sorted parts')
    NMB_transit_comment = models.CharField(max_length=100, blank = True, null = True, verbose_name = 'comment')
    supplier_necessary = models.BooleanField(choices=BOOL_CHOICES, default=False)  
    supplier_sorting_date= models.DateTimeField(blank=True, null=True, verbose_name='sorting date')
    supplier_qty= models.IntegerField(blank=True, null=True, verbose_name='Qty sorted')
    supplier_NOK= models.IntegerField(blank=True, null=True, verbose_name='Nb NOK found')
    supplier_NOK_date= models.CharField(max_length=25, blank=True, null=True, verbose_name='NOK part production date')
    supplier_date_from= models.CharField(max_length=25, blank=True, null=True, verbose_name='from prod. date sorted parts')
    supplier_date_to= models.CharField(max_length=25, blank=True, null=True, verbose_name='to prod. date sorted parts')
    supplier_comment = models.CharField(max_length=100, blank = True, null = True, verbose_name = 'comment')
    sub_supplier_necessary = models.BooleanField(choices=BOOL_CHOICES, default=False)  
    sub_supplier_sorting_date= models.DateTimeField(blank=True, null=True, verbose_name='sorting date')
    sub_supplier_qty= models.IntegerField(blank=True, null=True, verbose_name='Qty sorted')
    sub_supplier_NOK= models.IntegerField(blank=True, null=True, verbose_name='Nb NOK found')
    sub_supplier_NOK_date= models.CharField(max_length=25, blank=True, null=True, verbose_name='NOK part production date')
    sub_supplier_date_from= models.CharField(max_length=25, blank=True, null=True, verbose_name='from prod. date sorted parts')
    sub_supplier_date_to= models.CharField(max_length=25, blank=True, null=True, verbose_name='to prod. date sorted parts')
    sub_supplier_comment = models.CharField(max_length=100, blank = True, null = True, verbose_name = 'comment')
#     total_supplier_qty= models.CharField(max_length=25, blank=True, null=True, verbose_name='Qty sorted')
#     total_supplier_NOK= models.CharField(max_length=25, blank=True, null=True, verbose_name='Nb NOK found')
#     total_NMB_qty= models.CharField(max_length=25, blank=True, null=True, verbose_name='Qty sorted')
#     total_NMB_NOK= models.CharField(max_length=25, blank=True, null=True, verbose_name='Nb NOK found')
    LL = models.CharField(max_length=75, blank=True, null=True, verbose_name='Lessons Learned')
    fst_OK_parts_qty = models.IntegerField(blank=True, null=True, verbose_name='Qty')
    fst_OK_parts_del_note = models.CharField(max_length=25, blank=True, null=True, verbose_name='delivery note Nb')
    fst_OK_parts_del_date = models.DateTimeField(blank=True, null=True, verbose_name='delivery date NMB')
    mark_on_parts = models.CharField(max_length=75, blank=True, null=True, verbose_name='on parts')
    mark_on_labels = models.CharField(max_length=75, blank=True, null=True, verbose_name='on labels')
        
    def __str__(self):
        return str(self.claim)        
    
class D4(models.Model):  
    claim = models.OneToOneField(Claim, on_delete=models.SET_NULL, null=True)
    root_cause_occ = models.CharField(max_length = 500, verbose_name='root cause for occurance')
    root_cause_det = models.CharField(max_length = 500, verbose_name='root cause for non detection')
    
    def __str__(self):
        return str(self.claim)        

class D4_reproduction(models.Model):  
    claim = models.OneToOneField(Claim, on_delete=models.SET_NULL, null=True)
    reproduction_occ_pilot = models.CharField(max_length = 50, blank=True, null=True, verbose_name='pilot' )
    reproduction_occ_date = models.DateField(blank=True, null=True, verbose_name='date' )
    defect_occ_reproduced = models.BooleanField(choices=BOOL_CHOICES, default=False, verbose_name='occurance of defect reproduced?' )
    effective_occ_pilot = models.CharField(max_length = 50, blank=True, null=True , verbose_name='pilot' )
    effective_occ_date = models.DateField(blank=True, null=True, verbose_name='date' )
    effective_occ_reproduced = models.BooleanField(choices=BOOL_CHOICES, default=False, verbose_name='action is effective!' )
    reproduction_det_pilot = models.CharField(max_length = 50, blank=True, null=True, verbose_name='pilot' )
    reproduction_det_date = models.DateField(blank=True, null=True, verbose_name='date')
    defect_det_reproduced = models.BooleanField(choices=BOOL_CHOICES, default=False, verbose_name='non-detection of defect reproduced?')
    effective_det_pilot = models.CharField(max_length = 50, blank=True, null=True, verbose_name='pilot' )
    effective_det_date = models.DateField(blank=True, null=True, verbose_name='date')
    effective_det_reproduced = models.BooleanField(choices=BOOL_CHOICES, default=False, verbose_name='action is effective!')
    
    def __str__(self):
        return str(self.claim)        


class PenaltyPeriods(models.Model):
    penaltyModel = models.CharField (max_length = 25, default = "Standard")
    duration_D3 = models.DurationField (default = '2 days')
    duration_D4 = models.DurationField (default = '10 days')
    duration_D5 = models.DurationField (default = '20 days')
    duration_D6 = models.DurationField (default = '30 days')
    duration_D8 = models.DurationField (default = '35 days')
    delta = models.DurationField (default = '7 days', verbose_name='time_between_supplier_updates')
    def __str__(self):
        return "penaltyModel"
            
class Ishikawa_occurance(models.Model):
    claim = models.OneToOneField(Claim, on_delete=models.SET_NULL, null=True)
    method=models.CharField(max_length=250, blank=True, null=True)
    machine=models.CharField(max_length=250, blank=True, null=True)
    man=models.CharField(max_length=250, blank=True, null=True)
    material=models.CharField(max_length=250, blank=True, null=True)
    problem=models.CharField(max_length=250, blank=True, null=True)
    def __str__(self):
        return str(self.claim)        
    
class Ishikawa_detection(models.Model):
    claim = models.OneToOneField(Claim, on_delete=models.SET_NULL, null=True)
    method=models.CharField(max_length=250, blank=True, null=True)
    machine=models.CharField(max_length=250, blank=True, null=True)
    man=models.CharField(max_length=250, blank=True, null=True)
    material=models.CharField(max_length=250, blank=True, null=True)
    problem=models.CharField(max_length=250, blank=True, null=True)
    def __str__(self):
        return str(self.claim)        
    
class W5_occurance(models.Model):
    claim = models.OneToOneField(Claim, on_delete=models.SET_NULL, null=True)
    Why1=models.CharField(max_length=250)
    Why2=models.CharField(max_length=250)
    Why3=models.CharField(max_length=250)
    Why4=models.CharField(max_length=250)
    Why5=models.CharField(max_length=250)
    def __str__(self):
        return str(self.claim)        
    
class W5_detection(models.Model):
    claim = models.OneToOneField(Claim, on_delete=models.SET_NULL, null=True)
    Why1=models.CharField(max_length=250)
    Why2=models.CharField(max_length=250)
    Why3=models.CharField(max_length=250)
    Why4=models.CharField(max_length=250)
    Why5=models.CharField(max_length=250)
    def __str__(self):
        return str(self.claim)        
    


STATUS_CHOICES = (('INTERNAL', 'internal'), 
                  ('ALL', 'all'))
IMPORTANCE_CHOICES = (('LOW', 'low'),
                      ('MID', 'mid'),
                      ('HIGH', 'high'),
                      ('IMP', 'Importance'))                     
class Task(models.Model):
    project = models.CharField(max_length=25)
    subproject = models.CharField(max_length=25)
    action = models.CharField(max_length = 25)
    task = models.CharField(max_length = 250)
    pilot = models.EmailField(max_length=45, verbose_name='(mail of) Pilot')
    date_issued = models.DateField(auto_now_add=True)
    original_due_date = models.DateField()
    due_date = models.DateField()
    comment = models.CharField(max_length = 500, blank=True, null=True)
    closed_date = models.DateField(blank=True, null=True)
    closed = models.BooleanField(default = False)
    importance = models.CharField(max_length=10, choices=IMPORTANCE_CHOICES, default='IMP')
    file = models.FileField(blank=True, null=True, upload_to='uploads/')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default = 'INTERNAL')
    @property
    def timely_status(self):
        if datetime.date(timezone.now()) > self.due_date:
            return "Overdue"
        return "In time"
    def __str__(self):
        return str(self.project) + " " + str(self.subproject) + "  Task " + str(self.pk)
        
class File(models.Model):
    project = models.CharField(max_length=25)
    subproject = models.CharField(max_length=25)
    title =  models.CharField(max_length=25)
    file = models.FileField(blank=True, null=True, upload_to='uploads/')
    
    def __str__(self):
        return str(self.project) + " " + str(self.subproject) + "  File " + str(self.pk)
        
class Comment(models.Model):
    project = models.CharField(max_length=25)
    subproject = models.CharField(max_length=25)
    task = models.IntegerField()
    author =  models.CharField(max_length=25)
    comment =  models.TextField(verbose_name='new comment')
    date_issued = models.DateField(auto_now_add=True)
    file = models.FileField(blank=True, null=True, upload_to='uploads/')
    
    def __str__(self):
        return str(self.project) + " " + str(self.subproject) + "  Comment " + str(self.pk)
        
    
    
    
                           