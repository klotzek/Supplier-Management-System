import pdb
import os
from bootstrap_datepicker.widgets import DatePicker 
from django import forms
from .models import *
# from .models import Company, Claim, TraceData, UserProfile, Team, D2_CV, D2_SV, D3, Ishikawa_occurance, Ishikawa_detection, Task, W5_occurance, W5_detection, D4, D4_reproduction, File, Comment, D7
from django.contrib.auth.models import User


class NewTaskListForm(forms.ModelForm):
    class Meta:
        model=TaskList
        fields=[
            'company',
            'subproject',
            ]
        
    subproject = forms.CharField(label='Tasklist name', max_length=100)

class OtherCertForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.hereIwork = kwargs.pop('hereIwork', None)
        super(OtherCertForm, self).__init__(*args, **kwargs)
        if not self.hereIwork.NMB_company:  #nur NMB_companies koennen bei mandatory einen Haken machen
           self.fields['mandatory'].widget.attrs['readonly']=True
           self.fields['mandatory'].widget.attrs['disabled']=True
           self.fields['validated'].widget.attrs['readonly']=True
           self.fields['validated'].widget.attrs['disabled']=True
           self.fields['rejected'].widget.attrs['readonly']=True
           self.fields['rejected'].widget.attrs['disabled']=True

    def clean_mandatory(self):
        instance = getattr(self, 'instance', None)
        if not instance:
            instance.mandatory=False
        if not self.hereIwork.NMB_company:  #nicht-NMB_companies speichern die Vorgabe, die bereits in der DB steht
            return instance.mandatory
        else:
            return self.cleaned_data['mandatory']    
    def clean_validated(self):
        instance = getattr(self, 'instance', None)
        if not instance:
            instance.validated=False
        if not self.hereIwork.NMB_company:  #nicht-NMB_companies speichern die Vorgabe, die bereits in der DB steht
            return instance.validated
        else:
            return self.cleaned_data['validated']    
    def clean_rejected(self):
        instance = getattr(self, 'instance', None)
        if not instance:
            instance.rejected=False
        if not self.hereIwork.NMB_company:  #nicht-NMB_companies speichern die Vorgabe, die bereits in der DB steht
            return instance.rejected
        else:
            return self.cleaned_data['rejected']    

    pic=forms.FileField()
    def clean_pic(self):
        uploaded_file = self.cleaned_data['pic']
        try:
            # create an ImageField instance
            im = forms.ImageField()
            # now check if the file is a valid image
            im.to_python(uploaded_file)
        except forms.ValidationError:
            # file is not a valid image;
            # so check if it's a pdf
            name, ext = os.path.splitext(uploaded_file.name)
            if ext not in ['.pdf', '.PDF']:
                raise forms.ValidationError("Only images and PDF files allowed")
        return uploaded_file            
        
    
    class Meta:
        model=OtherCertifications
        fields=[
           'cert_name',
           'mandatory',
           'pic',
           'cert_board',
           'start',
           'stop',
           'validated', 
           'rejected', 
           
           ]


        widgets={
           'start': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                "daysOfWeekHighlighted": [1,2,3,4,5],
                "showOnFocus": False,
          }),
           'stop': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                "daysOfWeekHighlighted": [1,2,3,4,5],
                "showOnFocus": False,
          }),
        }
          
    

class CertForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.hereIwork = kwargs.pop('hereIwork', None)
        super(CertForm, self).__init__(*args, **kwargs)
        if not self.hereIwork.NMB_company:  #nur NMB_companies koennen bei mandatory einen Haken machen
           self.fields['IATF16949_mandatory'].widget.attrs['readonly']=True
           self.fields['IATF16949_mandatory'].widget.attrs['disabled']=True
           self.fields['IATF16949_validated'].widget.attrs['readonly']=True
           self.fields['IATF16949_validated'].widget.attrs['disabled']=True
           self.fields['IATF16949_rejected'].widget.attrs['readonly']=True
           self.fields['IATF16949_rejected'].widget.attrs['disabled']=True
           self.fields['ISO9001_mandatory'].widget.attrs['readonly']=True
           self.fields['ISO9001_mandatory'].widget.attrs['disabled']=True
           self.fields['ISO9001_validated'].widget.attrs['readonly']=True
           self.fields['ISO9001_validated'].widget.attrs['disabled']=True
           self.fields['ISO9001_rejected'].widget.attrs['readonly']=True
           self.fields['ISO9001_rejected'].widget.attrs['disabled']=True
           self.fields['ISO14001_mandatory'].widget.attrs['readonly']=True
           self.fields['ISO14001_mandatory'].widget.attrs['disabled']=True
           self.fields['ISO14001_validated'].widget.attrs['readonly']=True
           self.fields['ISO14001_validated'].widget.attrs['disabled']=True
           self.fields['ISO14001_rejected'].widget.attrs['readonly']=True
           self.fields['ISO14001_rejected'].widget.attrs['disabled']=True
           self.fields['OHSAS18001_mandatory'].widget.attrs['readonly']=True
           self.fields['OHSAS18001_mandatory'].widget.attrs['disabled']=True
           self.fields['OHSAS18001_validated'].widget.attrs['readonly']=True
           self.fields['OHSAS18001_validated'].widget.attrs['disabled']=True
           self.fields['OHSAS18001_rejected'].widget.attrs['readonly']=True
           self.fields['OHSAS18001_rejected'].widget.attrs['disabled']=True

    def clean_IATF16949_mandatory(self):
        instance = getattr(self, 'instance', None)
        if not self.hereIwork.NMB_company:  #nicht-NMB_companies speichern die Vorgabe, die bereits in der DB steht
            return instance.IATF16949_mandatory
        else:
            return self.cleaned_data['IATF16949_mandatory']    
    def clean_IATF16949_validated(self):
        instance = getattr(self, 'instance', None)
        if not self.hereIwork.NMB_company:  #nicht-NMB_companies speichern die Vorgabe, die bereits in der DB steht
            return instance.IATF16949_validated
        else:
            return self.cleaned_data['IATF16949_validated']    
    def clean_IATF16949_rejected(self):
        instance = getattr(self, 'instance', None)
        if not self.hereIwork.NMB_company:  #nicht-NMB_companies speichern die Vorgabe, die bereits in der DB steht
            return instance.IATF16949_rejected
        else:
            return self.cleaned_data['IATF16949_rejected']    
            
    def clean_ISO9001_mandatory(self):
        instance = getattr(self, 'instance', None)
        if not self.hereIwork.NMB_company:  #nicht-NMB_companies speichern die Vorgabe, die bereits in der DB steht
            return instance.ISO9001_mandatory
        else:
            return self.cleaned_data['ISO9001_mandatory']    
    def clean_ISO9001_validated(self):
        instance = getattr(self, 'instance', None)
        if not self.hereIwork.NMB_company:  #nicht-NMB_companies speichern die Vorgabe, die bereits in der DB steht
            return instance.ISO9001_validated
        else:
            return self.cleaned_data['ISO9001_validated']    
    def clean_ISO9001_rejected(self):
        instance = getattr(self, 'instance', None)
        if not self.hereIwork.NMB_company:  #nicht-NMB_companies speichern die Vorgabe, die bereits in der DB steht
            return instance.ISO9001_rejected
        else:
            return self.cleaned_data['ISO9001_rejected']    
            
    def clean_ISO14001_mandatory(self):
        instance = getattr(self, 'instance', None)
        if not self.hereIwork.NMB_company:  #nicht-NMB_companies speichern die Vorgabe, die bereits in der DB steht
            return instance.ISO14001_mandatory
        else:
            return self.cleaned_data['ISO14001_mandatory']    
    def clean_ISO14001_validated(self):
        instance = getattr(self, 'instance', None)
        if not self.hereIwork.NMB_company:  #nicht-NMB_companies speichern die Vorgabe, die bereits in der DB steht
            return instance.ISO14001_validated
        else:
            return self.cleaned_data['ISO14001_validated']    
    def clean_ISO14001_rejected(self):
        instance = getattr(self, 'instance', None)
        if not self.hereIwork.NMB_company:  #nicht-NMB_companies speichern die Vorgabe, die bereits in der DB steht
            return instance.ISO14001_rejected
        else:
            return self.cleaned_data['ISO14001_rejected']    
            
    def clean_OHSAS18001_mandatory(self):
        instance = getattr(self, 'instance', None)
        if not self.hereIwork.NMB_company:  #nicht-NMB_companies speichern die Vorgabe, die bereits in der DB steht
            return instance.OHSAS18001_mandatory
        else:
            return self.cleaned_data['OHSAS18001_mandatory']    
    def clean_OHSAS18001_validated(self):
        instance = getattr(self, 'instance', None)
        if not self.hereIwork.NMB_company:  #nicht-NMB_companies speichern die Vorgabe, die bereits in der DB steht
            return instance.OHSAS18001_validated
        else:
            return self.cleaned_data['OHSAS18001_validated']    
    def clean_OHSAS18001_rejected(self):
        instance = getattr(self, 'instance', None)
        if not self.hereIwork.NMB_company:  #nicht-NMB_companies speichern die Vorgabe, die bereits in der DB steht
            return instance.OHSAS18001_rejected
        else:
            return self.cleaned_data['OHSAS18001_rejected']    


    class Meta:
        model=Certifications
        fields=[
#             'company',
            
           'IATF16949_mandatory',
           'IATF16949_pic',
           'IATF16949_cert_board',
           'IATF16949_start',
           'IATF16949_stop',
           'IATF16949_validated', 
           'IATF16949_rejected', 
           
           'ISO9001_mandatory',
           'ISO9001_pic',
           'ISO9001_cert_board',
           'ISO9001_start',
           'ISO9001_stop',
           'ISO9001_validated', 
           'ISO9001_rejected', 
           
           'ISO14001_mandatory',
           'ISO14001_pic',
           'ISO14001_cert_board',
           'ISO14001_start',
           'ISO14001_stop',
           'ISO14001_validated', 
           'ISO14001_rejected', 
           
           'OHSAS18001_mandatory',
           'OHSAS18001_pic',
           'OHSAS18001_cert_board',
           'OHSAS18001_start',
           'OHSAS18001_stop',
           'OHSAS18001_validated', 
           'OHSAS18001_rejected', 
           
           ]
        
        widgets={
           'IATF16949_start': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                "daysOfWeekHighlighted": [1,2,3,4,5],
                "showOnFocus": False,
          }),
           'IATF16949_stop': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                "daysOfWeekHighlighted": [1,2,3,4,5],
                "showOnFocus": False,
          }),
           'ISO9001_start': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                "daysOfWeekHighlighted": [1,2,3,4,5],
                "showOnFocus": False,
          }),
           'ISO9001_stop': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                "daysOfWeekHighlighted": [1,2,3,4,5],
                "showOnFocus": False,
          }),
           'OHSAS18001_start': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                "daysOfWeekHighlighted": [1,2,3,4,5],
                "showOnFocus": False,
          }),
           'OHSAS18001_stop': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                "daysOfWeekHighlighted": [1,2,3,4,5],
                "showOnFocus": False,
          }),
           'ISO14001_start': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                "daysOfWeekHighlighted": [1,2,3,4,5],
                "showOnFocus": False,
          }),
           'ISO14001_stop': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                "daysOfWeekHighlighted": [1,2,3,4,5],
                "showOnFocus": False,
          }),
        }
          
           
           
class D7Form(forms.ModelForm):
    class Meta:
        widgets={
           'DFMEA_done': forms.RadioSelect, 
           'DFMEA_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
           'PFMEA_done': forms.RadioSelect, 
           'PFMEA_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
           'LFMEA_done': forms.RadioSelect, 
           'LFMEA_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
           'controlplan_done': forms.RadioSelect, 
           'controlplan_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
           'WI_done': forms.RadioSelect, 
           'WI_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
           'MP_done': forms.RadioSelect, 
           'MP_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
           'Dstand_done': forms.RadioSelect, 
           'Dstand_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
           'toolDstand_done': forms.RadioSelect, 
           'toolDstand_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
           'LLcard_done': forms.RadioSelect, 
           'LLcard_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
           'Gstand_done': forms.RadioSelect, 
           'Gstand_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
           'Tstand_done': forms.RadioSelect, 
           'Tstand_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
           'procedure_done': forms.RadioSelect, 
           'procedure_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
           'spec_done': forms.RadioSelect, 
           'spec_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
           'other_done': forms.RadioSelect, 
           'other_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
          
        }
        model=D7
        fields=[
          'DFMEA_done',
          'DFMEA_pilot',
          'DFMEA_date',
          'DFMEA_comment',
          'PFMEA_done',
          'PFMEA_pilot',
          'PFMEA_date',
          'PFMEA_comment',
          'LFMEA_done',
          'LFMEA_pilot',
          'LFMEA_date',
          'LFMEA_comment',
          'controlplan_done',
          'controlplan_pilot',
          'controlplan_date',
          'controlplan_comment',
          'WI_done',
          'WI_pilot',
          'WI_date',
          'WI_comment',
          'MP_done',
          'MP_pilot',
          'MP_date',
          'MP_comment',
          'Dstand_done',
          'Dstand_pilot',
          'Dstand_date',
          'Dstand_comment',
          'toolDstand_done',
          'toolDstand_pilot',
          'toolDstand_date',
          'toolDstand_comment', 
          'LLcard_done',
          'LLcard_pilot',
          'LLcard_date',
          'LLcard_comment',
          'Gstand_done',
          'Gstand_pilot',
          'Gstand_date',
          'Gstand_comment',
          'Tstand_done',
          'Tstand_pilot',
          'Tstand_date',
          'Tstand_comment',
          'procedure_done',
          'procedure_pilot',
          'procedure_date',
          'procedure_comment',
          'spec_done',
          'spec_pilot',
          'spec_date',
          'spec_comment',
          'other_done',
          'other_pilot',
          'other_date',
          'other_comment',
        ]
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        hereIwork = kwargs.pop('hereIwork', None)
        hereIwork = hereIwork.name
        super(D7Form, self).__init__(*args, **kwargs)
        if 'PMDM' in hereIwork:    #falls Du zu PMDM gehoerst, darfst Du auch Kollegen von PMDM in die Taskliste einfuegen.
            self.fields['DFMEA_pilot'].queryset=(UserProfile.objects.filter(company=company) | UserProfile.objects.filter(company__name='PMDM')).distinct()      
            self.fields['PFMEA_pilot'].queryset=(UserProfile.objects.filter(company=company) | UserProfile.objects.filter(company__name='PMDM')).distinct()      
            self.fields['LFMEA_pilot'].queryset=(UserProfile.objects.filter(company=company)| UserProfile.objects.filter(company__name='PMDM')).distinct()       
            self.fields['controlplan_pilot'].queryset=(UserProfile.objects.filter(company=company)| UserProfile.objects.filter(company__name='PMDM')).distinct()       
            self.fields['WI_pilot'].queryset=(UserProfile.objects.filter(company=company)| UserProfile.objects.filter(company__name='PMDM')).distinct()       
            self.fields['MP_pilot'].queryset=(UserProfile.objects.filter(company=company) | UserProfile.objects.filter(company__name='PMDM')).distinct()      
            self.fields['Dstand_pilot'].queryset=(UserProfile.objects.filter(company=company)| UserProfile.objects.filter(company__name='PMDM')).distinct()       
            self.fields['toolDstand_pilot'].queryset=(UserProfile.objects.filter(company=company)| UserProfile.objects.filter(company__name='PMDM')).distinct()       
            self.fields['LLcard_pilot'].queryset=(UserProfile.objects.filter(company=company)| UserProfile.objects.filter(company__name='PMDM')).distinct()       
            self.fields['Gstand_pilot'].queryset=(UserProfile.objects.filter(company=company)| UserProfile.objects.filter(company__name='PMDM')).distinct()      
            self.fields['Tstand_pilot'].queryset=(UserProfile.objects.filter(company=company)| UserProfile.objects.filter(company__name='PMDM')).distinct()       
            self.fields['procedure_pilot'].queryset=(UserProfile.objects.filter(company=company) | UserProfile.objects.filter(company__name='PMDM')).distinct()      
            self.fields['spec_pilot'].queryset=(UserProfile.objects.filter(company=company)| UserProfile.objects.filter(company__name='PMDM')).distinct()       
            self.fields['other_pilot'].queryset=(UserProfile.objects.filter(company=company) | UserProfile.objects.filter(company__name='PMDM')).distinct()
        else:
            self.fields['DFMEA_pilot'].queryset=UserProfile.objects.filter(company=company)
            self.fields['PFMEA_pilot'].queryset=UserProfile.objects.filter(company=company)
            self.fields['LFMEA_pilot'].queryset=UserProfile.objects.filter(company=company)
            self.fields['controlplan_pilot'].queryset=UserProfile.objects.filter(company=company)  
            self.fields['WI_pilot'].queryset=UserProfile.objects.filter(company=company)  
            self.fields['MP_pilot'].queryset=UserProfile.objects.filter(company=company)   
            self.fields['Dstand_pilot'].queryset=UserProfile.objects.filter(company=company)     
            self.fields['toolDstand_pilot'].queryset=UserProfile.objects.filter(company=company)  
            self.fields['LLcard_pilot'].queryset=UserProfile.objects.filter(company=company)  
            self.fields['Gstand_pilot'].queryset=UserProfile.objects.filter(company=company)    
            self.fields['Tstand_pilot'].queryset=UserProfile.objects.filter(company=company)    
            self.fields['procedure_pilot'].queryset=UserProfile.objects.filter(company=company) 
            self.fields['spec_pilot'].queryset=UserProfile.objects.filter(company=company)
            self.fields['other_pilot'].queryset=UserProfile.objects.filter(company=company)
              

class FileForm(forms.ModelForm):
    class Meta:
        model=File
        fields=[
          'title',
          'file',
        ]

class D4Form(forms.ModelForm):
    class Meta:
        model=D4
        widgets={
          'root_cause_occ':forms.Textarea(attrs={'rows':2, 'cols':40}),
          'root_cause_det':forms.Textarea(attrs={'rows':2, 'cols':40}),
        }
        fields=[
          'root_cause_occ', 
          'root_cause_det', 
        ]

class D4Form_reproduction(forms.ModelForm):
    class Meta:
        model=D4_reproduction
        widgets={
           'defect_occ_reproduced': forms.RadioSelect, 
           'reproduction_occ_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
           'defect_det_reproduced': forms.RadioSelect, 
           'reproduction_det_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
          }
        fields=[
          'reproduction_occ_pilot', 
          'reproduction_occ_date',
          'defect_occ_reproduced',
          'reproduction_det_pilot', 
          'reproduction_det_date',
          'defect_det_reproduced',
        ]
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        hereIwork = kwargs.pop('hereIwork', None)
        hereIwork = hereIwork.name
        super(D4Form_reproduction, self).__init__(*args, **kwargs)
        if 'PMDM' in hereIwork:    #falls Du zu PMDM gehoerst, darfst Du auch Kollegen von PMDM in die Taskliste einfuegen.
            self.fields['reproduction_occ_pilot'].queryset=(UserProfile.objects.filter(company=company) | UserProfile.objects.filter(company__name='PMDM')).distinct()    
            self.fields['reproduction_det_pilot'].queryset=UserProfile.objects.filter(company=company).distinct() | UserProfile.objects.filter(company__name='PMDM').distinct()    
        else:
            self.fields['reproduction_occ_pilot'].queryset=UserProfile.objects.filter(company=company).distinct()    
            self.fields['reproduction_det_pilot'].queryset=UserProfile.objects.filter(company=company).distinct()    
#     def __init__(self, *args, **kwargs):
#         company = kwargs.pop('firma', None)
#         hereIwork = kwargs.pop('hereIwork', None)
#         super(TaskFormEdit, self).__init__(*args, **kwargs)
#         if company:
#             hereIwork = hereIwork.name
#             if 'PMDM' in hereIwork:    #falls Du zu PMDM gehoerst, darfst Du auch Kollegen von PMDM in die Taskliste einfuegen.
#                 self.fields['pilot'].queryset = UserProfile.objects.filter(company=company).distinct() | UserProfile.objects.filter(company__name='PMDM').distinct()
#             else:
#                 self.fields['pilot'].queryset = UserProfile.objects.filter(company=company).distinct()
                


class D6Form_effectiveness(forms.ModelForm):
    class Meta:
        model=D6_effectiveness
        widgets={
           'effective_occ_reproduced': forms.RadioSelect, 
           'effective_occ_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
           'effective_det_reproduced': forms.RadioSelect, 
           'effective_det_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          }),
          }
        fields=[
          'effective_occ_pilot',
          'effective_occ_date',
          'effective_occ_reproduced',
          'effective_det_pilot',
          'effective_det_date',
          'effective_det_reproduced',
        ]
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        hereIwork = kwargs.pop('hereIwork', None)
        hereIwork = hereIwork.name
        super(D6Form_effectiveness, self).__init__(*args, **kwargs)
        if 'PMDM' in hereIwork:    #falls Du zu PMDM gehoerst, darfst Du auch Kollegen von PMDM in die Taskliste einfuegen.
            self.fields['effective_occ_pilot'].queryset=UserProfile.objects.filter(company=company).distinct() | UserProfile.objects.filter(company__name='PMDM').distinct()    
            self.fields['effective_det_pilot'].queryset=UserProfile.objects.filter(company=company).distinct() | UserProfile.objects.filter(company__name='PMDM').distinct()    
        else:
            self.fields['effective_occ_pilot'].queryset=UserProfile.objects.filter(company=company).distinct()    
            self.fields['effective_det_pilot'].queryset=UserProfile.objects.filter(company=company).distinct()    
#     def __init__(self, *args, **kwargs):
#         company = kwargs.pop('firma', None)
#         hereIwork = kwargs.pop('hereIwork', None)
#         super(TaskFormEdit, self).__init__(*args, **kwargs)
#         if company:
#             hereIwork = hereIwork.name
#             if 'PMDM' in hereIwork:    #falls Du zu PMDM gehoerst, darfst Du auch Kollegen von PMDM in die Taskliste einfuegen.
#                 self.fields['pilot'].queryset = UserProfile.objects.filter(company=company).distinct() | UserProfile.objects.filter(company__name='PMDM').distinct()
#             else:
#                 self.fields['pilot'].queryset = UserProfile.objects.filter(company=company).distinct()
                


# class D4Form_det(forms.ModelForm):
#     class Meta:
#         model=D4_reproduction
#         fields=[
#           'reproduction_det_pilot', 
#           'reproduction_det_date',
#           'defect_det_reproduced',
#           'effective_det_pilot',
#           'effective_det_date',
#           'effective_det_reproduced',
#         ]

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        widgets={
          'comment':forms.Textarea(attrs={'rows':2, 'cols':120}),
        }
        fields=[
          'comment', 
          'file', 
        ]


class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        widgets={
          'task':forms.Textarea(attrs={'rows':2, 'cols':50}),
          'task_comment':forms.Textarea(attrs={'rows':2, 'cols':50}),
          'due_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          })
        }
        fields=[
          'type',
          'action', 
          'task', 
          'pilot',
          'due_date',
          'task_comment',
          'status',
          'importance',
        ]
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        hereIwork = kwargs.pop('hereIwork', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if company:
            hereIwork = hereIwork.name
            if 'PMDM' in hereIwork:    #falls Du zu PMDM gehoerst, darfst Du auch Kollegen von PMDM in die Taskliste einfuegen.
                self.fields['pilot'].queryset = UserProfile.objects.filter(company=company).distinct() | UserProfile.objects.filter(company__name='PMDM').distinct()
            else:
                self.fields['pilot'].queryset = UserProfile.objects.filter(company=company).distinct()
                
#             self.fields['pilot'].queryset = UserProfile.objects.filter(pilot_of_task__project=project).distinct()
            
    def clean_importance(self):
        imp =  self.cleaned_data.get('importance', '')
#         pdb.set_trace()
        if 'IMP' in imp:
#             pdb.set_trace()
            raise forms.ValidationError("Do not choose `Importance`!")
        return imp
    def clean_pilot(self):
        pilot=self.cleaned_data.get('pilot', '')
#         pdb.set_trace()
        if 'pilot' in pilot.user.username:
            raise forms.ValidationError("Do not choose `Pilot`!")
        return pilot    

class TaskFormEdit(forms.ModelForm):
    class Meta:
        model=Task
        widgets={
          'task':forms.Textarea(attrs={'rows':1, 'cols':40}),
#           'task_comment':forms.Textarea(attrs={'rows':3, 'cols':40}),
          'due_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          })
        }
        fields=[
          'type',
          'action', 
          'task', 
          'pilot',
          'due_date',
#           'task_comment',
          'importance',
          'status',
#           'file',
        ]
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('firma', None)
        hereIwork = kwargs.pop('hereIwork', None)
        super(TaskFormEdit, self).__init__(*args, **kwargs)
        if company:
            hereIwork = hereIwork.name
            if 'PMDM' in hereIwork:    #falls Du zu PMDM gehoerst, darfst Du auch Kollegen von PMDM in die Taskliste einfuegen.
                self.fields['pilot'].queryset = UserProfile.objects.filter(company=company).distinct() | UserProfile.objects.filter(company__name='PMDM').distinct()
            else:
                self.fields['pilot'].queryset = UserProfile.objects.filter(company=company).distinct()
                
    def clean_importance(self):
        imp =  self.cleaned_data.get('importance', '')
#         pdb.set_trace()
        if 'IMP' in imp:
#             pdb.set_trace()
            raise forms.ValidationError("Do not choose `Importance`!")
        return imp
    def clean_pilot(self):
        pilot=self.cleaned_data.get('pilot', '')
#         pdb.set_trace()
        if 'pilot' in pilot.user.username:
            raise forms.ValidationError("Do not choose `Pilot`!")
        return pilot    


class W5_Occ_Form(forms.ModelForm):
    class Meta:
        model=W5_occurance
        widgets={
          'Why1':forms.Textarea(attrs={'rows':2, 'cols':20}),
          'Why2':forms.Textarea(attrs={'rows':2, 'cols':20}),
          'Why3':forms.Textarea(attrs={'rows':2, 'cols':20}),
          'Why4':forms.Textarea(attrs={'rows':2, 'cols':20}),
          'Why5':forms.Textarea(attrs={'rows':2, 'cols':20}),
        }
        fields=[
        'Why1',
        'Why2',
        'Why3',
        'Why4',
        'Why5',
        ]
        
class W5_Det_Form(forms.ModelForm):
    class Meta:
        model=W5_detection
        widgets={
          'Why1':forms.Textarea(attrs={'rows':2, 'cols':20}),
          'Why2':forms.Textarea(attrs={'rows':2, 'cols':20}),
          'Why3':forms.Textarea(attrs={'rows':2, 'cols':20}),
          'Why4':forms.Textarea(attrs={'rows':2, 'cols':20}),
          'Why5':forms.Textarea(attrs={'rows':2, 'cols':20}),
        }
        fields=[
        'Why1',
        'Why2',
        'Why3',
        'Why4',
        'Why5',
        ]
        
class Ishi_Occ_Form(forms.ModelForm):
    class Meta:
        model=Ishikawa_occurance
        widgets={
          'method':forms.Textarea(attrs={'rows':2, 'cols':20}),
          'machine':forms.Textarea(attrs={'rows':2, 'cols':20}),
          'man':forms.Textarea(attrs={'rows':2, 'cols':20}),
          'material':forms.Textarea(attrs={'rows':2, 'cols':20}),
          'problem':forms.Textarea(attrs={'rows':2, 'cols':20}),
        }
        fields=[
        'method',
        'machine',
        'man',
        'material',
        'problem',
        ]
        
class Ishi_Det_Form(forms.ModelForm):
    class Meta:
        model=Ishikawa_detection
        widgets={
          'method':forms.Textarea(attrs={'rows':2, 'cols':20}),
          'machine':forms.Textarea(attrs={'rows':2, 'cols':20}),
          'man':forms.Textarea(attrs={'rows':2, 'cols':20}),
          'material':forms.Textarea(attrs={'rows':2, 'cols':20}),
          'problem':forms.Textarea(attrs={'rows':2, 'cols':20}),
        }
        fields=[
        'method',
        'machine',
        'man',
        'material',
        'problem',
        ]
        


class D3_Form(forms.ModelForm):
    class Meta:
        model = D3
        widgets={
           'actions_ongoing': forms.RadioSelect, 
           'actions_necessary': forms.RadioSelect,
           'completion_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
          'action':forms.Textarea(attrs={'rows':3, 'cols':85}),
#            'date_1': DatePicker(options={
#                 "format": "yyyy-mm-dd",
#                 "autoclose": True,
#                 "calendarWeeks":True,
#                 "weekStart":1,
#                 "todayHighlight": True,
#                 }
#               ), 
#            'date_2': DatePicker(options={
#                 "format": "yyyy-mm-dd",
#                 "autoclose": True,
#                 "calendarWeeks":True,
#                 "weekStart":1,
#                 "todayHighlight": True,
#                 }
#               ), 
#            'date_3': DatePicker(options={
#                 "format": "yyyy-mm-dd",
#                 "autoclose": True,
#                 "calendarWeeks":True,
#                 "weekStart":1,
#                 "todayHighlight": True,
#                 }
#               ), 
           'FC_necessary': forms.RadioSelect,
           'FC_sorting_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'FC_NOK_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'FC_date_from': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'FC_date_to': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'FC_transit_necessary': forms.RadioSelect,
           'FC_transit_sorting_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'FC_transit_NOK_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'FC_transit_date_from': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'FC_transit_date_to': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'NMB_necessary': forms.RadioSelect,
           'NMB_sorting_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'NMB_NOK_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'NMB_date_from': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'NMB_date_to': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'NMB_transit_necessary': forms.RadioSelect,
           'NMB_transit_sorting_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'NMB_transit_NOK_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'NMB_transit_date_from': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'NMB_transit_date_to': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'supplier_necessary': forms.RadioSelect,
           'supplier_sorting_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'supplier_NOK_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'supplier_date_from': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'supplier_date_to': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'sub_supplier_necessary': forms.RadioSelect,
           'sub_supplier_sorting_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'sub_supplier_NOK_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'sub_supplier_date_from': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ), 
           'sub_supplier_date_to': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ),
           'fst_OK_parts_del_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ),
        }
        fields=[
        'actions_ongoing',
        'actions_necessary',
        'completion_date',
        'action',
#         'pilot_1',
#         'date_1',
#         'action_2',
#         'pilot_2',
#         'date_2',
#         'action_3',
#         'pilot_3',
#         'date_3',
        'FC_necessary',
        'FC_sorting_date',
        'FC_qty',
        'FC_NOK',
        'FC_NOK_date',
        'FC_date_from',
        'FC_date_to',
        'FC_comment',
        'FC_transit_necessary',
        'FC_transit_sorting_date',
        'FC_transit_qty',
        'FC_transit_NOK',
        'FC_transit_NOK_date',
        'FC_transit_date_from',
        'FC_transit_date_to',
        'FC_transit_comment',
        'NMB_necessary',
        'NMB_sorting_date',
        'NMB_qty',
        'NMB_NOK',
        'NMB_NOK_date',
        'NMB_date_from',
        'NMB_date_to',
        'NMB_comment',
        'NMB_transit_necessary',
        'NMB_transit_sorting_date',
        'NMB_transit_qty',
        'NMB_transit_NOK',
        'NMB_transit_NOK_date',
        'NMB_transit_date_from',
        'NMB_transit_date_to',
        'NMB_transit_comment',
        'supplier_necessary',
        'supplier_sorting_date',
        'supplier_qty',
        'supplier_NOK',
        'supplier_NOK_date',
        'supplier_date_from',
        'supplier_date_to',
        'supplier_comment',
        'sub_supplier_necessary',
        'sub_supplier_sorting_date',
        'sub_supplier_qty',
        'sub_supplier_NOK',
        'sub_supplier_NOK_date',
        'sub_supplier_date_from',
        'sub_supplier_date_to',
        'sub_supplier_comment',
#         'total_supplier_qty',
#         'total_supplier_NOK',
#         'total_NMB_qty',
#         'total_NMB_NOK',
        'LL',
        'fst_OK_parts_qty',
        'fst_OK_parts_del_note',
        'fst_OK_parts_del_date',
        'mark_on_parts',
        'mark_on_labels',

        ]
class Acceptance_Form(forms.ModelForm):
    class Meta:
        model = Claim
        fields=[
        'accepted',
        'refused',
        ]

class Data_Form(forms.ModelForm):
    class Meta:
        model = TraceData
        widgets={
          'production_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ),
        }

        fields=[
        'production_date',
        'operator',
        'batch',
        'cavity',

        ]

class D2_CV_Form(forms.ModelForm):
    class Meta:
        model = D2_CV
        fields=[
        'what_happened',
        'why_problem',
        'when_detected',
        'who_detected',
        'where_detected',
        'how_detected',
        'how_many_NOK',

        ]

class D2_SV_Form(forms.ModelForm):
    class Meta:
        model = D2_SV
        fields=[
        'difference',
        'standard_process',
        'when_produced',
        'who_produced',
        'other_application',
        'reinjecting',
        'similar_problem',

        ]

class Team_Form(forms.ModelForm):
    class Meta:
        model = Team
        fields=[
        'member',
        ]

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        hereIwork = kwargs.pop('hereIwork', None)
#         hereIwork = hereIwork.name
        super(Team_Form, self).__init__(*args, **kwargs)
        if hereIwork.NMB_company:    #falls Du zu PMDM gehoerst, darfst Du auch Kollegen von PMDM in die Taskliste einfuegen.
            self.fields['member'].queryset=(UserProfile.objects.filter(company=company) | UserProfile.objects.filter(company__NMB_company = True) | UserProfile.objects.filter(company__customer=False)).distinct()    
        else:
            self.fields['member'].queryset=UserProfile.objects.filter(company=company)
            
class Claim_Form(forms.ModelForm):
    class Meta:
        model = Claim
        widgets={
          'due_date_D3': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ),
          'due_date_D4': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ),
          'due_date_D5': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ),
          'due_date_D6': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ),
          'due_date_D8': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
                }
              ),
              }
        fields = [
        'due_date_D3',
        'due_date_D4',
        'due_date_D5',
        'due_date_D6',
        'due_date_D8',
        ]
    
class Claim_New_Form(forms.ModelForm):
    class Meta:
        model = Claim
        fields = [
        'RMA',
        'IQC',
        'OK_picture', 
        'NOK_picture', 
        'File', 
        'D2_description', 
        'part_number', 
        'speaking_name', 
        'plant', 
        'responsible_in_plant', 
        'classification', 
        'RMA', 
        'project', 
        'car_maker', 
        'milage', 
        'special_characteristic_impact',
        'reoccurance'
        ]
    
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'DUNS', 'adress1', 'adress2', 'postcode', 'town', 'country', 'customer', 'NMB_company', ]
        

class PasswordForm(forms.Form):
    password1 = forms.CharField(label="",max_length=50,min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': 'password','class':'form-control input-perso'}))
    password2 = forms.CharField(label="",max_length=50,min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': 'confirm password','class':'form-control input-perso'}))

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            self._errors['password2'] = "The passwords are not identical."

        return self.cleaned_data
        
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)  
#         fields = ('username', 'password')  
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields =('firstname', 'lastname', 'email', 'isAdmin')

        
                