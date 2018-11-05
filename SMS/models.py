from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_countries.fields import CountryField
from datetime import datetime, timedelta

# Create your models here.
class Company(models.Model):                                        
   name =  models.CharField(max_length=200, unique=True, verbose_name='Company name')
   NMB_company = models.BooleanField(default=False)
   customer = models.BooleanField(default = False)
   belongs_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
   can_be_viewed_by = models.ManyToManyField("self")
   DUNS = models.CharField(max_length=10, unique=True,  blank=True, null=True)
   vendor_nb = models.CharField(max_length=200, blank=True, null=True, verbose_name='vendor nb / customer nb')
   adress1 = models.CharField(max_length=200)
   adress2 = models.CharField(max_length=200, blank=True)
   postcode = models.CharField(max_length=15)
   town = models.CharField(max_length=200)
   country = CountryField()
   
   def __str__(self):
      return self.name

class OtherCertifications(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    cert_name = models.CharField(blank=True, null=True, max_length=200) 
    mandatory = models.BooleanField(default= False)
    pic = models.FileField(blank=True, null=True)
    cert_board = models.CharField(blank=True, null=True, max_length=200)
    start = models.DateField(blank=True, null=True)
    stop = models.DateField(blank=True, null=True)
    validated = models.BooleanField(default= False)
    rejected = models.BooleanField(default= False)
   
    @property
    def failed(self):
        if self.rejected:
            return True
        if (not self.pic)  and self.mandatory:
            return True
        if self.stop:
           if datetime.date(timezone.now()) > self.stop:
                return True
#         return False  
   
    def __str__(self):
       return str(self.company)      

class Certifications(models.Model):
    
    company = models.OneToOneField(Company, on_delete=models.SET_NULL, null=True) 
    IATF16949_mandatory = models.BooleanField(default= True)
    IATF16949_pic = models.FileField(blank=True, null=True)
    IATF16949_cert_board = models.CharField(blank=True, null=True, max_length=200)
    IATF16949_start = models.DateField(blank=True, null=True)
    IATF16949_stop = models.DateField(blank=True, null=True)
    IATF16949_validated = models.BooleanField(default= False)
    IATF16949_rejected = models.BooleanField(default= False)
   
    ISO9001_mandatory = models.BooleanField(default= False)
    ISO9001_pic = models.FileField(blank=True, null=True, upload_to='uploads/')
    ISO9001_cert_board = models.CharField(blank=True, null=True, max_length=200)
    ISO9001_start = models.DateField(blank=True, null=True)
    ISO9001_stop = models.DateField(blank=True, null=True)
    ISO9001_validated = models.BooleanField(default= False)
    ISO9001_rejected = models.BooleanField(default= False)
   
    ISO14001_mandatory = models.BooleanField(default= False)
    ISO14001_pic = models.FileField(blank=True, null=True, upload_to='uploads/')
    ISO14001_cert_board = models.CharField(blank=True, null=True, max_length=200)
    ISO14001_start = models.DateField(blank=True, null=True)
    ISO14001_stop = models.DateField(blank=True, null=True)
    ISO14001_validated = models.BooleanField(default= False)
    ISO14001_rejected = models.BooleanField(default= False)
   
    OHSAS18001_mandatory = models.BooleanField(default= False)
    OHSAS18001_pic = models.FileField(blank=True, null=True, upload_to='uploads/')
    OHSAS18001_cert_board = models.CharField(blank=True, null=True, max_length=200)
    OHSAS18001_start = models.DateField(blank=True, null=True)
    OHSAS18001_stop = models.DateField(blank=True, null=True)
    OHSAS18001_validated = models.BooleanField(default= False)
    OHSAS18001_rejected = models.BooleanField(default= False)
   
    @property
    def IATF16949_failed(self):
        if self.IATF16949_rejected:
            return True
        if (not self.IATF16949_pic)  and self.IATF16949_mandatory:
            return True
        if self.IATF16949_stop:
           if datetime.date(timezone.now()) > self.IATF16949_stop:
                return True
          
    def ISO9001_failed(self):
        if self.ISO9001_rejected:
            return True
        if (not self.ISO9001_pic)  and self.ISO9001_mandatory:
            return True
        if self.ISO9001_stop:
           if datetime.date(timezone.now()) > self.ISO9001_stop:
                return True
          
    def ISO14001_failed(self):
        if self.ISO14001_rejected:
            return True
        if (not self.ISO14001_pic)  and self.ISO14001_mandatory:
            return True
        if self.ISO14001_stop:
           if datetime.date(timezone.now()) > self.ISO14001_stop:
                return True
          
    def OHSAS18001_failed(self):
        if self.OHSAS18001_rejected:
            return True
        if (not self.OHSAS18001_pic)  and self.OHSAS18001_mandatory:
            return True
        if self.OHSAS18001_stop:
           if datetime.date(timezone.now()) > self.OHSAS18001_stop:
                return True
          
    def __str__(self):
       return str(self.company)      

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
    IQC = models.IntegerField(blank=True, null=True)
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
    def __str__(self):
        return str(self.pk)
       
  
    @property
    def next_due_date(self):
#         if ('Opened' in self.status.status or 'D3 rejected' in self.status.status):
        if ('Opened' in self.status.status or 'D3 rejected'  in self.status.status):
            return self.due_date_D3
        elif ('D3 accepted' in self.status.status or 'D4 rejected' in self.status.status or 'D3 uploaded' in self.status.status):
            return self.due_date_D4
        elif ('D4 accepted' in self.status.status or 'D5 rejected' in self.status.status or 'D4 uploaded' in self.status.status):
            return self.due_date_D5
        elif ('D5 accepted' in self.status.status or 'D6 rejected' in self.status.status or 'D5 uploaded' in self.status.status):
            return self.due_date_D6
        elif ('D6 accepted' in self.status.status or 'D7 rejected' in self.status.status or 'D6 uploaded' in self.status.status):
            return self.due_date_D8
        elif ('D7 accepted' in self.status.status or 'D8 rejected' in self.status.status or 'D7 uploaded' in self.status.status):
            return self.due_date_D8
        else:
            return self.due_date_D8
            
    def late(self):
        if timezone.now() > self.next_due_date:
            return True
        else:
            return False 
        
    def is_past_D3(self):
        if timezone.now() > self.due_date_D3:
            return True
        return False
    def is_past_D4(self):
        if timezone.now() > self.due_date_D4:
            return True
        return False
    def is_past_D5(self):
        if timezone.now() > self.due_date_D5:
            return True
        return False
    def is_past_D6(self):
        if timezone.now() > self.due_date_D6:
            return True
        return False
    def is_past_D8(self):
        if timezone.now() > self.due_date_D8:
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
    
class TraceData(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.SET_NULL, null=True)
    production_date=models.DateField()
    operator=models.CharField(max_length=25)
    batch=models.CharField(max_length=25)
    cavity=models.CharField(max_length=25)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    function = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
#     aus  https://www.b-list.org/weblog/2006/sep/02/django-tips-user-registration/
    email = models.EmailField()    
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null = True)
    isAdmin = models.BooleanField(default=False)
    isStaff = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=40, default='1234')
#     key_expires = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=9999))
    class Meta:
        ordering = ('user__username',)
        
    def __str__(self):
        return str(self.firstname) + " " + str(self.lastname) 
#         return str(self.pk) 
        
class Team(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.SET_NULL, null=True)
    member=models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    isPilot=models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.member) 
            
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
#     containment_actions = models.CharField()
    actions_ongoing = models.BooleanField(choices=BOOL_CHOICES, default=False)
    actions_necessary = models.BooleanField(choices=BOOL_CHOICES, default=False)
    completion_date = models.DateTimeField(blank=True, null=True)
    action= models.CharField(max_length=200, blank=True, null=True)
#     pilot_1= models.CharField(max_length=50, blank=True, null=True)
#     date_1= models.DateTimeField(blank=True, null=True)
#     action_2= models.CharField(max_length=50, blank=True, null=True)
#     pilot_2= models.CharField(max_length=50, blank=True, null=True)
#     date_2= models.DateTimeField(blank=True, null=True)
#     action_3= models.CharField(max_length=50, blank=True, null=True)
#     pilot_3= models.CharField(max_length=50, blank=True, null=True)
#     date_3= models.DateTimeField(blank=True, null=True)
    FC_necessary = models.BooleanField(choices=BOOL_CHOICES, default=False)  #FC=final customer
#     FC_sorting_date= models.DateTimeField(blank=True, null=True, verbose_name='sorting date')
    FC_sorting_date= models.DateField(blank=True, null=True, verbose_name='sorting date')
    FC_qty= models.IntegerField(blank=True, null=True, verbose_name='Qty sorted')
    FC_NOK= models.IntegerField(blank=True, null=True, verbose_name='Nb NOK found')
    FC_NOK_date= models.DateField(max_length=25, blank=True, null=True, verbose_name='NOK part production date')
    FC_date_from= models.DateField(max_length=25, blank=True, null=True, verbose_name='from prod. date sorted parts')
    FC_date_to= models.DateField(max_length=25, blank=True, null=True, verbose_name='to prod. date sorted parts')
    FC_comment = models.CharField(max_length=100, blank = True, null = True, verbose_name = 'comment')
    FC_transit_necessary = models.BooleanField(choices=BOOL_CHOICES, default=False)  #FC=final customer
    FC_transit_sorting_date= models.DateField(blank=True, null=True, verbose_name='sorting date')
    FC_transit_qty= models.IntegerField(blank=True, null=True, verbose_name='Qty sorted')
    FC_transit_NOK= models.IntegerField(blank=True, null=True, verbose_name='Nb NOK found')
    FC_transit_NOK_date= models.DateField(max_length=25, blank=True, null=True, verbose_name='NOK part production date')
    FC_transit_date_from= models.DateField(max_length=25, blank=True, null=True, verbose_name='from prod. date sorted parts')
    FC_transit_date_to= models.DateField(max_length=25, blank=True, null=True, verbose_name='to prod. date sorted parts')
    FC_transit_comment = models.CharField(max_length=100, blank = True, null = True, verbose_name = 'comment')
    NMB_necessary = models.BooleanField(choices=BOOL_CHOICES, default=False)  
    NMB_sorting_date= models.DateField(blank=True, null=True, verbose_name='sorting date')
    NMB_qty= models.IntegerField(blank=True, null=True, verbose_name='Qty sorted')
    NMB_NOK= models.IntegerField(blank=True, null=True, verbose_name='Nb NOK found')
    NMB_NOK_date= models.DateField(max_length=25, blank=True, null=True, verbose_name='NOK part production date')
    NMB_date_from= models.DateField(max_length=25, blank=True, null=True, verbose_name='from prod. date sorted parts')
    NMB_date_to= models.DateField(max_length=25, blank=True, null=True, verbose_name='to prod. date sorted parts')
    NMB_comment = models.CharField(max_length=100, blank = True, null = True, verbose_name = 'comment')
    NMB_transit_necessary = models.BooleanField(choices=BOOL_CHOICES, default=False)  
    NMB_transit_sorting_date= models.DateField(blank=True, null=True, verbose_name='sorting date')
    NMB_transit_qty= models.IntegerField(blank=True, null=True, verbose_name='Qty sorted')
    NMB_transit_NOK= models.IntegerField(blank=True, null=True, verbose_name='Nb NOK found')
    NMB_transit_NOK_date= models.DateField(max_length=25, blank=True, null=True, verbose_name='NOK part production date')
    NMB_transit_date_from= models.DateField(max_length=25, blank=True, null=True, verbose_name='from prod. date sorted parts')
    NMB_transit_date_to= models.DateField(max_length=25, blank=True, null=True, verbose_name='to prod. date sorted parts')
    NMB_transit_comment = models.CharField(max_length=100, blank = True, null = True, verbose_name = 'comment')
    supplier_necessary = models.BooleanField(choices=BOOL_CHOICES, default=False)  
    supplier_sorting_date= models.DateField(blank=True, null=True, verbose_name='sorting date')
    supplier_qty= models.IntegerField(blank=True, null=True, verbose_name='Qty sorted')
    supplier_NOK= models.IntegerField(blank=True, null=True, verbose_name='Nb NOK found')
    supplier_NOK_date= models.DateField(max_length=25, blank=True, null=True, verbose_name='NOK part production date')
    supplier_date_from= models.DateField(max_length=25, blank=True, null=True, verbose_name='from prod. date sorted parts')
    supplier_date_to= models.DateField(max_length=25, blank=True, null=True, verbose_name='to prod. date sorted parts')
    supplier_comment = models.CharField(max_length=100, blank = True, null = True, verbose_name = 'comment')
    sub_supplier_necessary = models.BooleanField(choices=BOOL_CHOICES, default=False)  
    sub_supplier_sorting_date= models.DateField(blank=True, null=True, verbose_name='sorting date')
    sub_supplier_qty= models.IntegerField(blank=True, null=True, verbose_name='Qty sorted')
    sub_supplier_NOK= models.IntegerField(blank=True, null=True, verbose_name='Nb NOK found')
    sub_supplier_NOK_date= models.DateField(max_length=25, blank=True, null=True, verbose_name='NOK part production date')
    sub_supplier_date_from= models.DateField(max_length=25, blank=True, null=True, verbose_name='from prod. date sorted parts')
    sub_supplier_date_to= models.DateField(max_length=25, blank=True, null=True, verbose_name='to prod. date sorted parts')
    sub_supplier_comment = models.CharField(max_length=100, blank = True, null = True, verbose_name = 'comment')
#     total_supplier_qty= models.CharField(max_length=25, blank=True, null=True, verbose_name='Qty sorted')
#     total_supplier_NOK= models.CharField(max_length=25, blank=True, null=True, verbose_name='Nb NOK found')
#     total_NMB_qty= models.CharField(max_length=25, blank=True, null=True, verbose_name='Qty sorted')
#     total_NMB_NOK= models.CharField(max_length=25, blank=True, null=True, verbose_name='Nb NOK found')
    LL = models.CharField(max_length=75, blank=True, null=True, verbose_name='Lessons Learned')
    fst_OK_parts_qty = models.IntegerField(blank=True, null=True, verbose_name='Qty')
    fst_OK_parts_del_note = models.CharField(max_length=25, blank=True, null=True, verbose_name='delivery note Nb')
    fst_OK_parts_del_date = models.DateField(blank=True, null=True, verbose_name='delivery date NMB')
    mark_on_parts = models.CharField(max_length=75, blank=True, null=True, verbose_name='on parts')
    mark_on_labels = models.CharField(max_length=75, blank=True, null=True, verbose_name='on labels')
        
    def __str__(self):
        return str(self.claim)        
    
class D4(models.Model):  
    claim = models.OneToOneField(Claim, on_delete=models.SET_NULL, null=True)
    root_cause_occ = models.CharField(max_length = 500, verbose_name='root cause for occurence')
    root_cause_det = models.CharField(max_length = 500, verbose_name='root cause for non detection')
    
    def __str__(self):
        return str(self.claim)        

class D4_reproduction(models.Model):  
    claim = models.OneToOneField(Claim, on_delete=models.SET_NULL, null=True)
    reproduction_occ_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, verbose_name='pilot', related_name="some_special_name" )
    reproduction_occ_date = models.DateField(blank=True, null=True, verbose_name='date' )
    defect_occ_reproduced = models.BooleanField(choices=BOOL_CHOICES, default=False, verbose_name='occurance of defect reproduced?' )
    reproduction_det_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, verbose_name='pilot', related_name="third_name"  )
    reproduction_det_date = models.DateField(blank=True, null=True, verbose_name='date')
    defect_det_reproduced = models.BooleanField(choices=BOOL_CHOICES, default=False, verbose_name='non-detection of defect reproduced?')
    
    def __str__(self):
        return str(self.claim)        


class D6_effectiveness(models.Model):  
    claim = models.OneToOneField(Claim, on_delete=models.SET_NULL, null=True)
    effective_occ_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, verbose_name='pilot', related_name="some_other_special_name"  )
    effective_occ_date = models.DateField(blank=True, null=True, verbose_name='date' )
    effective_occ_reproduced = models.BooleanField(choices=BOOL_CHOICES, default=False, verbose_name='action is effective!' )
    effective_det_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, verbose_name='pilot', related_name="forth_name"  )
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
TYPE_CHOICES = (('TASK', 'task'),
                ('INFO', 'info'),
                ('DEC', 'decision')
                )                     
class Task(models.Model):
    project = models.CharField(max_length=25)
    subproject = models.CharField(max_length=25)
    valid = models.BooleanField(default=True)
    number = models.IntegerField(null=True)
    importance = models.CharField(max_length=10, choices=IMPORTANCE_CHOICES, default='IMP')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='TASK') 
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default = 'INTERNAL')
    action = models.CharField(max_length = 25)
    task = models.CharField(max_length = 250)
    pilot = models.ForeignKey(UserProfile, related_name='pilot_of_task', on_delete=models.SET_NULL, null = True, default=15) #default, damit im pulldown "pilot" angezeigt wird"
    date_issued = models.DateField(auto_now_add=True)
#     datetime_issued = models.DateField(auto_now_add=True)
    original_due_date = models.DateField()
    due_date = models.DateField()
    task_comment = models.CharField(max_length = 1500, blank=True, null=True)
    closed_date = models.DateField(blank=True, null=True)
    closed = models.BooleanField(default = False)
    file = models.FileField(blank=True, null=True, upload_to='uploads/')
#     class Meta:
#         ordering = ('pilot__user__username',)

    @property
    def timely_status(self):
        if datetime.date(timezone.now()) > self.due_date:
            return "Overdue"
        elif datetime.date(timezone.now()) == self.due_date:
            return "Today"
        return "In time"
    def __str__(self):
        return str(self.project) + " " + str(self.subproject) + "  Task " + str(self.pk) +" Nb. " + str(self.number)
        
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
#     author =  models.CharField(max_length=25)
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null = True)
    comment =  models.TextField(blank=True, null=True, verbose_name='new comment')
    date_issued = models.DateField(auto_now_add=True)
    file = models.FileField(blank=True, null=True, upload_to='uploads/')
    
    def __str__(self):
        return str(self.project) + " " + str(self.subproject) + "  Task " + str(self.task) + "  Comment " + str(self.pk)
        
class D7(models.Model):
    claim = models.OneToOneField(Claim, on_delete=models.SET_NULL, null=True)
    DFMEA_done = models.BooleanField(choices=BOOL_CHOICES,default=False)
    DFMEA_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, related_name="1+" )
    DFMEA_date= models.DateField(blank=True, null=True)
    DFMEA_comment=models.CharField(max_length=100, blank=True, null=True)
    PFMEA_done = models.BooleanField(choices=BOOL_CHOICES,default=False)
    PFMEA_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, related_name="2+" )
    PFMEA_date= models.DateField(blank=True, null=True)
    PFMEA_comment=models.CharField(max_length=100, blank=True, null=True)
    LFMEA_done = models.BooleanField(choices=BOOL_CHOICES,default=False)
    LFMEA_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, related_name="3+" )
    LFMEA_date= models.DateField(blank=True, null=True)
    LFMEA_comment=models.CharField(max_length=100, blank=True, null=True)
    controlplan_done = models.BooleanField(choices=BOOL_CHOICES,default=False)
    controlplan_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, related_name="4+" )
    controlplan_date= models.DateField(blank=True, null=True)
    controlplan_comment=models.CharField(max_length=100, blank=True, null=True)
    WI_done = models.BooleanField(choices=BOOL_CHOICES,default=False)
    WI_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, related_name="5+" )
    WI_date= models.DateField(blank=True, null=True)
    WI_comment=models.CharField(max_length=100, blank=True, null=True)
    MP_done = models.BooleanField(choices=BOOL_CHOICES,default=False)
    MP_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, related_name="6+" )
    MP_date= models.DateField(blank=True, null=True)
    MP_comment=models.CharField(max_length=100, blank=True, null=True)
    Dstand_done = models.BooleanField(choices=BOOL_CHOICES,default=False)
    Dstand_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, related_name="7+" )
    Dstand_date= models.DateField(blank=True, null=True)
    Dstand_comment=models.CharField(max_length=100, blank=True, null=True)
    toolDstand_done = models.BooleanField(choices=BOOL_CHOICES,default=False)
    toolDstand_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, related_name="8+" )
    toolDstand_date= models.DateField(blank=True, null=True)
    toolDstand_comment=models.CharField(max_length=100, blank=True, null=True)
    LLcard_done = models.BooleanField(choices=BOOL_CHOICES,default=False)
    LLcard_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, related_name="9+" )
    LLcard_date= models.DateField(blank=True, null=True)
    LLcard_comment=models.CharField(max_length=100, blank=True, null=True)
    Gstand_done = models.BooleanField(choices=BOOL_CHOICES,default=False)
    Gstand_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, related_name="10+" )
    Gstand_date= models.DateField(blank=True, null=True)
    Gstand_comment=models.CharField(max_length=100, blank=True, null=True)
    Tstand_done = models.BooleanField(choices=BOOL_CHOICES,default=False)
    Tstand_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, related_name="11+" )
    Tstand_date= models.DateField(blank=True, null=True)
    Tstand_comment=models.CharField(max_length=100, blank=True, null=True)
    procedure_done = models.BooleanField(choices=BOOL_CHOICES,default=False)
    procedure_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, related_name="12+" )
    procedure_date= models.DateField(blank=True, null=True)
    procedure_comment=models.CharField(max_length=100, blank=True, null=True)
    spec_done = models.BooleanField(choices=BOOL_CHOICES,default=False)
    spec_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, related_name="13+" )
    spec_date= models.DateField(blank=True, null=True)
    spec_comment=models.CharField(max_length=100, blank=True, null=True)
    other_done = models.BooleanField(choices=BOOL_CHOICES,default=False)
    other_pilot = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank = True, related_name="14+" )
    other_date= models.DateField(blank=True, null=True)
    other_comment=models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return str(self.claim)    
        
class TaskList(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.IntegerField()
    subproject = models.CharField(max_length=100, unique=True)
    creation_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.company) + ' ' + self.subproject   
    
         
                           