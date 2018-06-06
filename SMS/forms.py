import pdb
from bootstrap_datepicker.widgets import DatePicker 
from django import forms
from .models import Company, Claim, UserProfile, Team, D2_CV, D2_SV, D3, Ishikawa_occurance, Ishikawa_detection, Task, W5_occurance, W5_detection, D4, D4_reproduction, File
from django.contrib.auth.models import User


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
           'effective_occ_reproduced': forms.RadioSelect, 
           'effective_occ_date': DatePicker(options={
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
          'reproduction_occ_pilot', 
          'reproduction_occ_date',
          'defect_occ_reproduced',
          'effective_occ_pilot',
          'effective_occ_date',
          'effective_occ_reproduced',

          'reproduction_det_pilot', 
          'reproduction_det_date',
          'defect_det_reproduced',
          'effective_det_pilot',
          'effective_det_date',
          'effective_det_reproduced',
        ]

class D4Form_det(forms.ModelForm):
    class Meta:
        model=D4_reproduction
        fields=[
          'reproduction_det_pilot', 
          'reproduction_det_date',
          'defect_det_reproduced',
          'effective_det_pilot',
          'effective_det_date',
          'effective_det_reproduced',
        ]

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        widgets={
          'task':forms.Textarea(attrs={'rows':1, 'cols':40}),
          'comment':forms.Textarea(attrs={'rows':1, 'cols':40}),
          'due_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          })
        }
        fields=[
          'action', 
          'task', 
          'pilot',
          'due_date',
          'comment',
          'importance',
          'file',
        ]
    def clean_importance(self):
        imp =  self.cleaned_data.get('importance', '')
#         pdb.set_trace()
        if 'IMP' in imp:
#             pdb.set_trace()
            raise forms.ValidationError("Do not choose `Importance`!")
        return imp

class TaskFormBig(forms.ModelForm):
    class Meta:
        model=Task
        widgets={
          'task':forms.Textarea(attrs={'rows':3, 'cols':40}),
          'comment':forms.Textarea(attrs={'rows':3, 'cols':40}),
          'due_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                "todayHighlight": True,
          })
        }
        fields=[
          'action', 
          'task', 
          'pilot',
          'due_date',
          'comment',
          'importance',
          'file',
        ]
    def clean_importance(self):
        imp =  self.cleaned_data.get('importance', '')
#         pdb.set_trace()
        if 'IMP' in imp:
#             pdb.set_trace()
            raise forms.ValidationError("Do not choose `Importance`!")
        return imp

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
                }
              ), 
           'date_1': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'date_2': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'date_2': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'FC_necessary': forms.RadioSelect,
           'FC_sorting_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'FC_NOK_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'FC_date_from': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'FC_date_to': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'FC_transit_necessary': forms.RadioSelect,
           'FC_transit_sorting_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'FC_transit_NOK_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'FC_transit_date_from': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'FC_transit_date_to': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'NMB_necessary': forms.RadioSelect,
           'NMB_sorting_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'NMB_NOK_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'NMB_date_from': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'NMB_date_to': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'NMB_transit_necessary': forms.RadioSelect,
           'NMB_transit_sorting_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'NMB_transit_NOK_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'NMB_transit_date_from': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'NMB_transit_date_to': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'supplier_necessary': forms.RadioSelect,
           'supplier_sorting_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'supplier_NOK_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'supplier_date_from': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'supplier_date_to': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'sub_supplier_necessary': forms.RadioSelect,
           'sub_supplier_sorting_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'sub_supplier_NOK_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'sub_supplier_date_from': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ), 
           'sub_supplier_date_to': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ),
           'fst_OK_parts_del_date': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ),
        }
        fields=[
        'actions_ongoing',
        'actions_necessary',
        'completion_date',
        'action_1',
        'pilot_1',
        'date_1',
        'action_2',
        'pilot_2',
        'date_2',
        'action_3',
        'pilot_3',
        'date_3',
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

class Data_Form(forms.ModelForm):
    class Meta:
        model = Claim
        widgets={
          'production_date_1': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ),
          'production_date_2': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
            }
          ), #datepicker           
          'production_date_3': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ),



        }

        fields=[
        'accepted',
        'refused',
        'production_date_1',
        'production_date_2',
        'production_date_3',
        'operator_1',
        'operator_2',
        'operator_3',
        'batch_1',
        'batch_2',
        'batch_3',
        'cavity_1',
        'cavity_2',
        'cavity_3',

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
        'pilot',
        'mail',
        'function',
        'phone',
        'teammember_1',
        'function_1',
        'mail_1',
        'phone_1',
        'teammember_2',
        'function_2',
        'mail_2',
        'phone_2',
        'teammember_3',
        'function_3',
        'mail_3',
        'phone_3',
        ]
    def clean(self):
        member1 = self.cleaned_data.get('teammember_1')
        function1  = self.cleaned_data.get('function_1')
        mail1  = self.cleaned_data.get('mail_1')
        member2 = self.cleaned_data.get('teammember_2')
        function2 = self.cleaned_data.get('function_2')
        mail2 = self.cleaned_data.get('mail_2')
        member3 = self.cleaned_data.get('teammember_3')
        function3 = self.cleaned_data.get('function_3')
        mail3 = self.cleaned_data.get('mail_3')
        msg=forms.ValidationError("This field is required")

        if member1:
            if not function1:
                self.add_error('function_1', msg)
            if not mail1:
                self.add_error('mail_1', msg)
        else:
            self.cleaned_data['function_1']=''
            self.cleaned_data['mail_1']=''

        if member2:
            if not function2:
                self.add_error('function_2', msg)
            if not mail2:
                self.add_error('mail_2', msg)
        else:
            self.cleaned_data['function_2']=''
            self.cleaned_data['mail_2']=''

        if member3:
            if not function3:
                self.add_error('function_3', msg)
            if not mail3:
                self.add_error('mail_3', msg)
        else:
            self.cleaned_data['function_3']=''
            self.cleaned_data['mail_3']=''

        return self.cleaned_data    
    
            

class Claim_Form(forms.ModelForm):
    class Meta:
        model = Claim
        widgets={
          'due_date_D3': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ),
          'due_date_D4': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ),
          'due_date_D5': DatePicker(options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
                "calendarWeeks":True,
                "weekStart":1,
                }
              ),
              }
        fields = [
        'due_date_D3',
        'due_date_D4',
        'due_date_D5',
        ]
    
class Claim_New_Form(forms.ModelForm):
    class Meta:
        model = Claim
        fields = [
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
        fields = ['name', 'DUNS', 'adress1', 'adress2', 'postcode', 'town', 'country']
        

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')  
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields =('firstname', 'lastname', 'email', 'isAdmin')

        
                