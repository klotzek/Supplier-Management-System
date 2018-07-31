import pdb
import os
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Company, Claim, ClaimStatus, Team, TraceData, D2_CV, D2_SV, D3, PenaltyPeriods, Ishikawa_occurance, Ishikawa_detection, Task, W5_occurance, W5_detection, D4, D4_reproduction, File , Comment, D7
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .forms import Claim_New_Form, CompanyForm, UserForm, UserProfileForm, Team_Form, Data_Form, Acceptance_Form, D2_CV_Form, D2_SV_Form, Claim_Form, D3_Form, Ishi_Occ_Form , Ishi_Det_Form, TaskForm, TaskFormEdit,  W5_Occ_Form , W5_Det_Form, D4Form, D4Form_reproduction, FileForm, CommentForm, D7Form, PasswordForm 
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.template import loader

# from django.core.files.storage import FileSystemStorage

# Create your views here.
@login_required
def index(request):
    user_profile = UserProfile.objects.get(user_id=request.user)
    if request.method == 'POST':                                                #Der Benutzer ist NMB und hat eine Firma zur Ansicht gewaehlt (nur dann ist ein POST moeglich)
        company = request.POST.get("vendor_choice")                             #Das ist die vom NMB-Benutzer gewaehlte Firma
        return redirect('base_data', company)                                   #Gehe zu bas_data und zeige die Daten dieser Firma an.
                                                                                
    company = Company.objects.get(pk=user_profile.company_id)
    companyusers = UserProfile.objects.filter(company=company.pk)
#     hereIwork = UserProfile.objects.get(user=request.user)
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.filter(can_be_viewed_by__name__startswith=user_profile.company).order_by('name')]
    return render(request, 'SMS/index.html',{'user_profile':user_profile, 'companyusers':companyusers, 'company':company, 'vendors':vendors, 'request':request})

@login_required
def base_data(request, company_id):
    user_profile = UserProfile.objects.get(user_id=request.user)
    company = Company.objects.get(pk=company_id)
    companyusers = UserProfile.objects.filter(company=company.pk)
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.filter(can_be_viewed_by__name__startswith=user_profile.company).order_by('name')]
#     vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.filter(can_be_viewed_by__name__startswith="PMDM")]
    return render(request, 'SMS/index.html',{'user_profile':user_profile, 'companyusers':companyusers, 'company':company, 'vendors':vendors, 'request':request})

@login_required
def vendor_new(request):
    user_profile = UserProfile.objects.get(user_id=request.user)
    company = Company.objects.get(pk=user_profile.company_id)                   #Hier: Die NMB-company
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.filter(can_be_viewed_by__name__startswith=user_profile.company).order_by('name')]

    form = CompanyForm()
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.belongs_to = company                                         #company ist in dem Fall die NMB-company
            vendor.save()
            vendor.can_be_viewed_by.add(company)                                #company ist in dem Fall die NMB-company
            vendor.save()
            company = Company.objects.get(DUNS=vendor.DUNS)
            return redirect('base_data', company.pk)
    return render(request, 'SMS/form.html',{'user_profile':user_profile, 'company':company, 'vendors':vendors,  'form': form})

def user_activate(request, user_Nb):
    user_profile = UserProfile.objects.get(user_id=user_Nb)
    user = User.objects.get(id=user_Nb)
    form = PasswordForm()
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk = user_Nb)
            user.is_active = True
            user.set_password(request.POST.get("password1"))
            update_session_auth_hash(request, user_Nb)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            user.save()
            return redirect('login')
        else:
            messages.error(request, 'Your input is not correct.')
            
            

    return render(request, 'SMS/user_activate.html',{'user_profile':user_profile, 'form': form})
    

@login_required
def user_new(request, company_id):
    user_profile = UserProfile.objects.get(user_id=request.user)
    company = Company.objects.get(pk=company_id)
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.filter(can_be_viewed_by__name__startswith=user_profile.company).order_by('name')]

    form1 = UserForm()
    form2 = UserProfileForm()
    if request.method == "POST":
        form1 = UserForm(request.POST)
        form2 = UserProfileForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            new_user = User.objects.create_user(**form1.cleaned_data)
            new_user.is_active = False
            new_user.save()
            new_user_profile = form2.save(commit=False)
            user = User.objects.get(username = request.POST.get("username"))
            new_user_profile.user_id =  user.pk
            new_user_profile.company_id=company_id 
            new_user_profile.save()
            html_message = loader.render_to_string(
            'SMS/activation_mail.html',
            {
                'user_name': new_user_profile.firstname + ' ' + new_user_profile.lastname,
                'subject':  'Please activate your account by clicking this link: http://localhost:8000/SMS/user_activate/' + str(user.pk),
#                 //...  
            }
        )            
            mail_text=''
            send_mail('Welcome to PMDM SupplierManagementSystem', mail_text, 'juergen.klotzek@nmb-minebea.com', [new_user_profile.email], fail_silently=False, html_message=html_message)
            return redirect('base_data', company_id)
    return render(request, 'SMS/two_forms.html',{'user_profile':user_profile, 'company':company, 'vendors':vendors,  'form1': form1, 'form2':form2})


@login_required
def user_edit(request, user):
#     actual_user_id = user
    user_profile = UserProfile.objects.get(user_id=user)
#     user_profile = UserProfile.objects.get(user_id=actual_user_id)
    user = User.objects.get(id=user)
    company = Company.objects.get(pk=user_profile.company_id)
#     show_company = company.pk
#     vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.all()]
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.filter(can_be_viewed_by__name__startswith=user_profile.company).order_by('name')]

    if request.method == "POST":
        form1 = PasswordChangeForm(request.user, request.POST)
        form2 = UserProfileForm(request.POST, instance=user_profile)
        if form1.is_valid() and form2.is_valid():
            user_edit=form1.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        
            edit_user_profile = form2.save(commit=False)
            edit_user_profile.save()
            return redirect('user_edit', actual_user_id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form1 = PasswordChangeForm(request.user)
        form2 = UserProfileForm(instance=user_profile)
    return render(request, 'SMS/user_edit.html',{'user_profile':user_profile, 'company':company, 'vendors':vendors,  'form1': form1, 'form2':form2})
#     return render(request, 'SMS/user_edit.html',{'user_profile':user_profile, 'company':company, 'show_company':show_company, 'vendors':vendors,  'form1': form1, 'form2':form2})


@login_required
def vendor_edit(request, vendor):
    user_profile = UserProfile.objects.get(user_id=request.user)
    company = Company.objects.get(pk=vendor)
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.filter(can_be_viewed_by__name__startswith=user_profile.company).order_by('name')]

    form = CompanyForm(instance=company)
    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            company = form.save(commit = False)
            company.save()
            return redirect('base_data', vendor)
    return render(request, 'SMS/form.html',{'user_profile':user_profile, 'company':company, 'vendors':vendors,  'form': form})

    
@login_required
def claims(request, company_id):
    user_profile = UserProfile.objects.get(user_id=request.user)
    company = Company.objects.get(pk=company_id)
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.filter(can_be_viewed_by__name__startswith=user_profile.company).order_by('name')]
#     pdb.set_trace()
    if not user_profile.company.NMB_company:                   #der eingloggte User gehoert NICHT zu PMDM
        if not company == user_profile.company:   #der eingloggte User ruft Daten einer anderen Firma auf!
            messages.add_message(request, messages.ERROR, 'You are not allowed to see other companies items!')
            return render(request, 'SMS/error.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company,}) 
         
    claims = Claim.objects.filter(related_to = company_id, valid = 'True').exclude(status__status = 'Closed')
    claims_closed = Claim.objects.filter(related_to = company_id, valid = 'True', status__status = 'Closed')
     
    return render(request, 'SMS/claims.html', {'vendors':vendors, 'user_profile':user_profile, 'claims_closed':claims_closed, 'claims':claims, 'company':company,}) 
    
@login_required
def claim_edit(request, claim):
    claim = get_object_or_404(Claim, pk=claim)
    try:
        d2 = D2_CV.objects.get(claim_id=claim.pk) #vielleicht gibt es den Eintrag noch gar nicht
    except:
        d2=None
#     vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.all()]
    user_profile = UserProfile.objects.get(user_id=request.user)
#     company_id = claim.related_to_id
    company = Company.objects.get(pk=claim.related_to_id)
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.filter(can_be_viewed_by__name__startswith=user_profile.company).order_by('name')]
    if not user_profile.company.NMB_company:                   #der eingloggte User gehoert NICHT zu PMDM
        if not company == user_profile.company:   #der eingloggte User ruft Daten einer anderen Firma auf!
            messages.add_message(request, messages.ERROR, 'You are not allowed to see other companies items!')
            return render(request, 'SMS/error.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company,}) 
         

    form = Claim_New_Form(instance=claim)
    form2 = D2_CV_Form(instance=d2)
    if request.method=="POST":
        form = Claim_New_Form(request.POST, request.FILES, instance=claim)
        form2 = D2_CV_Form(request.POST, instance=d2)
        if form.is_valid() and form2.is_valid():
            claim_edit=form.save(commit=False)
            d2_edit=form2.save(commit=False)
            path= 'uploads/' + company.name + '/Claim_' + str(claim.pk)
            claim_edit.File.field.upload_to = path
            claim_edit.OK_picture.field.upload_to = path
            claim_edit.NOK_picture.field.upload_to = path
            claim_edit.save()
            d2_edit.save()
            return redirect('claims', claim.related_to_id)
    return render(request, 'SMS/form_claim_base_data.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'form2': form2, 'claim':claim })
            

@login_required
def new_claim(request, company_id):
#     pdb.set_trace()
    user_profile = UserProfile.objects.get(user_id=request.user)
#     show_company = company_id
    company = Company.objects.get(pk=company_id)
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.filter(can_be_viewed_by__name__startswith=user_profile.company).order_by('name')]
#     vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.all()]
    no_label = True
    time_for_D3 = PenaltyPeriods.objects.get(penaltyModel="Standard").duration_D3
    time_for_D4 = PenaltyPeriods.objects.get(penaltyModel="Standard").duration_D4
    time_for_D5 = PenaltyPeriods.objects.get(penaltyModel="Standard").duration_D5
    time_for_D6 = PenaltyPeriods.objects.get(penaltyModel="Standard").duration_D6
    time_for_D8 = PenaltyPeriods.objects.get(penaltyModel="Standard").duration_D8

    if request.method == "POST":
        form = Claim_New_Form(request.POST, request.FILES)
        form2 = D2_CV_Form(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            d2 = form2.save(commit=False)
            claim = form.save(commit=False)
            claim.status_id = ClaimStatus.objects.get(status='Opened').pk
            claim.related_to_id = company_id
#             pdb.set_trace()
            claim.created_by = request.user
            claim.due_date_D3 = datetime.now() + time_for_D3
            claim.due_date_D4 = datetime.now() + time_for_D4
            claim.due_date_D5 = datetime.now() + time_for_D5
            claim.due_date_D6 = datetime.now() + time_for_D6
            claim.due_date_D8 = datetime.now() + time_for_D8
            File=claim.File
            OKFile=claim.OK_picture
            NOKFile=claim.NOK_picture
            claim.save()
            
            if File:
                path= 'uploads/' + company.name + '/Claim_' + str(claim.pk) + '/pr' 
                oldfile=claim.File.name
                filename=os.path.basename(oldfile)
                newfile= path + filename
                claim.File.storage.delete( newfile )
                claim.File.storage.save( newfile, File )
                claim.File.name = newfile
                claim.File.close()
                claim.File.storage.delete( oldfile )
            if OKFile:
                path= 'uploads/' + company.name + '/Claim_' + str(claim.pk) + '/pr' 
                OKoldfile=claim.OK_picture.name
                OKfilename=os.path.basename(OKoldfile)
                OKnewfile=path + OKfilename 
                claim.OK_picture.storage.delete( OKnewfile )
                claim.OK_picture.storage.save( OKnewfile, OKFile )
                claim.OK_picture.name = OKnewfile
                claim.OK_picture.close()
                claim.OK_picture.storage.delete( OKoldfile )
            if NOKFile:
                path= 'uploads/' + company.name + '/Claim_' + str(claim.pk) + '/pr' 
                NOKoldfile=claim.NOK_picture.name
                NOKfilename=os.path.basename(NOKoldfile)
                NOKnewfile=path + NOKfilename 
                claim.NOK_picture.storage.delete( NOKnewfile )
                claim.NOK_picture.storage.save( NOKnewfile, NOKFile )
                claim.NOK_picture.name = NOKnewfile
                claim.NOK_picture.close()
                claim.NOK_picture.storage.delete( NOKoldfile )
            
            d2.claim_id = claim.pk
            d2.save()
            claim.save() 
            return redirect('claims', company_id)

    else:
        no_label = True
        form = Claim_New_Form()
        form2 = D2_CV_Form()
    return render(request, 'SMS/form_claim_base_data.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'form2': form2, 'no_label': no_label})

  
@login_required
def claim_remove(request, claim):
    claim = get_object_or_404(Claim, pk=claim)
    company_id = claim.related_to_id
    claim.valid = False
    claim.save()
    return redirect('claims', company_id)


@login_required
def D1D8(request, claim):

    claim = get_object_or_404(Claim, pk=claim)
    company_id = claim.related_to_id
    user_profile = UserProfile.objects.get(user_id=request.user)
    company = Company.objects.get(pk=company_id)
    creator = UserProfile.objects.get(user_id=claim.created_by)
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.filter(can_be_viewed_by__name__startswith=user_profile.company).order_by('name')]
    if not user_profile.company.NMB_company:                   #der eingloggte User gehoert NICHT zu PMDM
        if not company == user_profile.company:   #der eingloggte User ruft Daten einer anderen Firma auf!
            messages.add_message(request, messages.ERROR, 'You are not allowed to see other companies items!')
            return render(request, 'SMS/error.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company,}) 

#     team = Team.objects.filter(claim_id=claim).first()
    d2_cv = D2_CV.objects.filter(claim_id=claim).first()
    d2_sv = D2_SV.objects.filter(claim_id=claim).first()
    d3 = D3.objects.filter(claim_id=claim).first()
    ishi_occ = Ishikawa_occurance.objects.filter(claim_id=claim).first()
    ishi_det = Ishikawa_detection.objects.filter(claim_id=claim).first()
    W5_occ = W5_occurance.objects.filter(claim_id=claim).first()
    W5_det = W5_detection.objects.filter(claim_id=claim).first()
    D7docu = D7.objects.filter(claim_id=claim).first()
          
    sorting_data = [0,0,'-',0,0,'-'] 
       
    if d3:
        FC_transit_qty=d3.FC_transit_qty
        if not d3.FC_transit_qty:
            FC_transit_qty=0
        FC_qty=d3.FC_qty
        if not d3.FC_qty:
            FC_qty=0
        NMB_qty=d3.NMB_qty
        if not d3.NMB_qty:
            NMB_qty=0
        
        FC_transit_NOK=d3.FC_transit_NOK
        if not d3.FC_transit_NOK:
            FC_transit_NOK=0
        FC_NOK=d3.FC_NOK
        if not d3.FC_NOK:
            FC_NOK=0
        NMB_NOK=d3.NMB_NOK
        if not d3.NMB_NOK:
            NMB_NOK=0
        
        if FC_transit_qty or FC_qty or NMB_qty:
            total_customer_qty = FC_transit_qty + FC_qty + NMB_qty
            total_customer_NOK = FC_transit_NOK + FC_NOK + NMB_NOK
            total_customer_ppm =  total_customer_NOK / total_customer_qty * 1000000
        else:
            total_customer_qty ='-'
            total_customer_NOK = '-'
            total_customer_ppm =  '-'
        if not total_customer_qty:
            total_customer_qty = '-'
        if not total_customer_NOK:
            total_customer_NOK = '-'
            

        NMB_transit_qty=d3.NMB_transit_qty
        if not d3.NMB_transit_qty:
            NMB_transit_qty=0
        
        supplier_qty=d3.supplier_qty
        if not d3.supplier_qty:
            supplier_qty=0
        sub_supplier_qty=d3.sub_supplier_qty
        if not d3.sub_supplier_qty:
            sub_supplier_qty=0
        
        NMB_transit_NOK=d3.NMB_transit_NOK
        if not d3.NMB_transit_NOK:
            NMB_transit_NOK=0
        supplier_NOK=d3.supplier_NOK
        if not d3.supplier_NOK:
            supplier_NOK=0
        sub_supplier_NOK=d3.sub_supplier_NOK
        if not d3.sub_supplier_NOK:
            sub_supplier_NOK=0
        
        if NMB_transit_qty or supplier_qty or sub_supplier_qty:
            total_supplier_qty = NMB_transit_qty + supplier_qty + sub_supplier_qty
            total_supplier_NOK = NMB_transit_NOK + supplier_NOK + sub_supplier_NOK
            total_supplier_ppm =  total_supplier_NOK / total_supplier_qty * 1000000
        else:
            total_supplier_qty ='-'
            total_supplier_NOK = '-'
            total_supplier_ppm =  '-'
        if not total_supplier_qty:
            total_supplier_qty = '-'
        if not total_supplier_NOK:
            total_supplier_NOK = '-'
            

#         pdb.set_trace()
        sorting_data[0]=total_supplier_qty
        sorting_data[1]=total_supplier_NOK
        sorting_data[2]=total_supplier_ppm
        sorting_data[3]=total_customer_qty
        sorting_data[4]=total_customer_NOK
        sorting_data[5]=total_customer_ppm
            
        
    if request.method == "POST":
#         pdb.set_trace()
        if 'Button_due_date' in request.POST:
            form_due=Claim_Form(request.POST, instance=claim)
#                 pdb.set_trace()
            if form_due.is_valid():
#                    pdb.set_trace()
                edit_due_date=form_due.save(commit=False)
                edit_due_date.save()
                return redirect('claims', company_id)

    
        if '/SMS/claim_Data/' in request.path:     
            trace_data=TraceData.objects.filter(claim=claim.pk)     
            form2=Acceptance_Form(request.POST, instance=claim)
            form = Data_Form(request.POST)
            if 'save_trace_data' in request.POST:
                if form.is_valid():
                    new_trace=form.save(commit=False)
                    new_trace.claim=claim
                    new_trace.save()
                    return redirect('claim_Data', claim)
                else:
                    return render(request, 'SMS/claim_Data.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'form2': form2, 'claim':claim, 'creator':creator, 'trace_data':trace_data })
                
            if form2.is_valid():
                open_reject_id = claim.status
#                 pdb.set_trace()
                if 'Refusal' in request.POST:
                    claim.status_id = ClaimStatus.objects.get(status='rejection accepted (closed)').pk
                if 'refused' in request.POST and not 'Refusal' in request.POST:
                    claim.status_id = ClaimStatus.objects.get(status='rejection opened by vendor').pk
                claim=form2.save(commit= False)
                claim.save()
                return redirect('claim_Data', claim)
            else:
                return render(request, 'SMS/claim_Data.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'form2': form2, 'claim':claim, 'creator':creator })
        
        if '/SMS/D1/' in request.path:
            team_members = Team.objects.filter(claim=claim.pk)
            form=Team_Form(request.POST, company=company)    #nur User der company werden angezeigt
#             form=Team_Form(request.POST, company=company)    #nur User der company werden angezeigt
            if form.is_valid():
                team_form=form.save(commit=False)
                if not team_members:  #noch kein Team, der erste Eintrag wird Pilot
                    team_form.isPilot = True
                team_form.claim=claim
                team_form.save()
                return redirect('D1', claim)
            
            return render(request, 'SMS/D1.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'claim':claim, 'creator':creator, 'team_members':team_members })

        if '/SMS/D2/' in request.path:
            form=D2_SV_Form(request.POST, instance=d2_sv)
            if form.is_valid():
                d2_form=form.save(commit=False)
                d2_form.claim_id=claim.pk
                d2_form.save()
                return redirect('D2', claim)
            else:
                return render(request, 'SMS/D2.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'claim':claim, 'creator':creator , 'd2_cv':d2_cv })
#                 return render(request, 'SMS/D2.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'claim':claim, 'creator':creator , 'd2_cv':d2_cv })
        
        if '/SMS/D3/' in request.path:
            tasks_D3 = Task.objects.filter(project=claim, subproject='D3', closed=False).order_by('due_date')
            form=D3_Form(request.POST, instance=d3)
            form_due=Claim_Form(request.POST, instance=claim)
#             pdb.set_trace()
            if form.is_valid():
#                 pdb.set_trace()
                if 'Submit' in request.POST:
                  claim.status_id = ClaimStatus.objects.get(status='D3 uploaded').pk
                  claim.save()
                if 'Accept' in request.POST:
                   claim.status_id = ClaimStatus.objects.get(status='D3 accepted').pk
                   claim.save()
                if 'Reject' in request.POST:
                   claim.status_id = ClaimStatus.objects.get(status='D3 rejected').pk
                   claim.save()
                d3_data=form.save(commit=False)
                d3_data.claim_id=claim.pk
                d3_data.save()
                return redirect('D3', claim)    
            return render(request, 'SMS/D3.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company,
                                                   'form': form, 'form_due': form_due, 'claim':claim, 'creator':creator, 'd2_cv':d2_cv, 'sorting_data':sorting_data, 'tasks_D3':tasks_D3  })
#             return render(request, 'SMS/D3.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company,
#                                                    'form': form, 'form_due': form_due, 'claim':claim, 'creator':creator, 'd2_cv':d2_cv, 'sorting_data':sorting_data, 'tasks_D3':tasks_D3  })

        if '/SMS/D4/' in request.path:
            tasks_D4 = Task.objects.filter(project=claim, subproject='D4', closed=False).order_by('due_date')
            files_occ = File.objects.filter(project = claim, subproject='occ')
            files_det = File.objects.filter(project = claim, subproject='det')
            root_causes = D4.objects.filter(claim_id=claim).first()
            occ_D4 = D4_reproduction.objects.filter(claim_id = claim).first()
            
            form_due= Claim_Form(request.POST, instance=claim)
            form_ishi_occ = Ishi_Occ_Form(request.POST, instance=ishi_occ)
            form_ishi_det = Ishi_Det_Form(request.POST, instance=ishi_det)
            form_W5_occ = W5_Occ_Form(request.POST, instance=W5_occ)
            form_W5_det = W5_Det_Form(request.POST, instance=W5_det)
            form = D4Form(request.POST, instance = root_causes)
            form_D4_occ =  D4Form_reproduction(request.POST, instance= occ_D4, company=company)
            form_files_occ = FileForm(request.POST, request.FILES)
            form_files_det = FileForm(request.POST, request.FILES)

#             pdb.set_trace()
            if 'Save_Ishi_Occ' in request.POST:
                if form_ishi_occ.is_valid():
#                     pdb.set_trace()
                    edit_ishi_occ = form_ishi_occ.save(commit=False)
                    edit_ishi_occ.claim_id=claim.pk
                    edit_ishi_occ.save()
                    return redirect('D4', claim)
                return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
#                 return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
                
            if 'Save_Ishi_Det' in request.POST:
                if form_ishi_det.is_valid():
#                     pdb.set_trace()
                    edit_ishi_det = form_ishi_det.save(commit=False)
                    edit_ishi_det.claim_id=claim.pk
                    edit_ishi_det.save()
                    return redirect('D4', claim)
                return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
#                 return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
                
#             pdb.set_trace()
            if 'Save_W5_occ' in request.POST:
                pdb.set_trace()
                if form_W5_occ.is_valid():
                    pdb.set_trace()
                    edit_W5_occ = form_W5_occ.save(commit=False)
                    edit_W5_occ.claim_id=claim.pk
                    edit_W5_occ.save()
                    return redirect('D4', claim)
                return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
#                 return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
                
            if 'Save_W5_det' in request.POST:
                if form_W5_det.is_valid():
                    pdb.set_trace()
                    edit_W5_det = form_W5_det.save(commit=False)
                    edit_W5_det.claim_id=claim.pk
                    edit_W5_det.save()
                    return redirect('D4', claim)
                return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
#                 return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })

            if 'save_root_causes' in request.POST:
                if form.is_valid():
#                     pdb.set_trace()
                    edit = form.save(commit=False)
                    edit.claim_id=claim.pk
                    edit.save()
                    return redirect('D4', claim)
                return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
#                 return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })

            if 'save_reproduction' in request.POST:
                if form_D4_occ.is_valid():
                    edit_repro = form_D4_occ.save(commit=False)
                    edit_repro.claim_id=claim.pk
                    if request.POST.get("reproduction_occ_pilot"):
                        try:
                            treffer= Team.objects.get(claim_id=claim, member=request.POST.get("reproduction_occ_pilot"))
                        except Team.MultipleObjectsReturned:
                            pass
                        except Team.DoesNotExist:
                            instance=UserProfile(pk=request.POST.get("reproduction_occ_pilot"))
                            new_member = Team(claim=claim, member=instance, isPilot=False)
                            new_member.save()        

                    if request.POST.get("reproduction_det_pilot"):
                        try:
                            treffer= Team.objects.get(claim_id=claim, member=request.POST.get("reproduction_det_pilot"))
                        except Team.MultipleObjectsReturned:
                            pass
                        except Team.DoesNotExist:
                            instance=UserProfile(pk=request.POST.get("reproduction_det_pilot"))
                            new_member = Team(claim=claim, member=instance, isPilot=False)
                            new_member.save()        

                    if request.POST.get("effective_occ_pilot"):
                        try:
                            treffer= Team.objects.get(claim_id=claim, member=request.POST.get("effective_occ_pilot"))
                        except Team.MultipleObjectsReturned:
                            pass
                        except Team.DoesNotExist:
                            instance=UserProfile(pk=request.POST.get("effective_occ_pilot"))
                            new_member = Team(claim=claim, member=instance, isPilot=False)
                            new_member.save()        

                    if request.POST.get("effective_det_pilot"):
                        try:
                            treffer= Team.objects.get(claim_id=claim, member=request.POST.get("effective_det_pilot"))
                        except Team.MultipleObjectsReturned:
                            pass
                        except Team.DoesNotExist:
                            instance=UserProfile(pk=request.POST.get("effective_det_pilot"))
                            new_member = Team(claim=claim, member=instance, isPilot=False)
                            new_member.save()        


#                     pdb.set_trace()
                    edit_repro.save()
                    return redirect('D4', claim)
                return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
#                 return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
                
            if 'new_occ_file' in request.POST:
                if form_files_occ.is_valid():
                    company = Claim.objects.get(pk=claim.pk).related_to.name
                    path = 'uploads/' + company + '/Claim_' + str(claim.pk)
                
#                     pdb.set_trace()
                    new_occ_file = form_files_occ.save(commit=False)
                    new_occ_file.project=claim.pk
                    new_occ_file.subproject='occ'
                    new_occ_file.file.field.upload_to = path
                    new_occ_file.save()
                    return redirect('D4', claim)
                return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
#                 return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
                
            if 'new_det_file' in request.POST:
                if form_files_det.is_valid():
                    company = Claim.objects.get(pk=claim.pk).related_to.name
                    path = 'uploads/' + company + '/Claim_' + str(claim.pk)
                
#                     pdb.set_trace()
                    new_det_file = form_files_det.save(commit=False)
                    new_det_file.project=claim.pk
                    new_det_file.subproject='det'
                    new_det_file.file.field.upload_to = path
                    new_det_file.save()
                    return redirect('D4', claim)
                return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
#                 return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
                
            if 'SubmitD4' in request.POST:
                if tasks_D4:
                    messages.add_message(request, messages.ERROR, 'You still have open tasks.') 
                if not root_causes:   
                    messages.add_message(request, messages.ERROR, 'You need to fill in the root-causes.') 
                if not ishi_occ:
                    messages.add_message(request, messages.ERROR, 'You need to fill in the Occurance Ishikawa.') 
                if not ishi_det:
                    messages.add_message(request, messages.ERROR, 'You need to fill in the Detection Ishikawa.') 
                if not W5_occ:
                    messages.add_message(request, messages.ERROR, 'You need to fill in the Occurance 5Why.') 
                if not W5_det:
                    messages.add_message(request, messages.ERROR, 'You need to fill in the Detection 5Why.') 
                if root_causes and ishi_occ and ishi_det and W5_occ and W5_det and not tasks_D4:
                    claim.status_id = ClaimStatus.objects.get(status='D4 uploaded').pk
                    claim.save()
                    return redirect('claims', company_id)
                return redirect('D4', claim)
                
            if 'AcceptD4' in request.POST:
                claim.status_id = ClaimStatus.objects.get(status='D4 accepted').pk
                claim.save()
                return redirect('claims', company_id)
                
            if 'RejectD4' in request.POST:
                claim.status_id = ClaimStatus.objects.get(status='D4 rejected').pk
                claim.save()
                return redirect('claims', company_id)



        if '/SMS/D5/' in request.path:
            tasks_D5_occ = Task.objects.filter(project=claim, subproject='D5_Occurance', closed=False).order_by('due_date')
            tasks_D5_det = Task.objects.filter(project=claim, subproject='D5_Detection', closed=False).order_by('due_date')
            tasks_D5_occ_all = Task.objects.filter(project=claim, subproject='D5_Occurance').order_by('due_date')
            tasks_D5_det_all = Task.objects.filter(project=claim, subproject='D5_Detection').order_by('due_date')
            pdb.set_trace()
            
            if 'SubmitD5' in request.POST:
                if tasks_D5_occ:
                    messages.add_message(request, messages.ERROR, 'You still have open tasks at occurance.') 
                if tasks_D5_det:
                    messages.add_message(request, messages.ERROR, 'You still have open tasks at detection.') 
                if not tasks_D5_occ_all:
                    messages.add_message(request, messages.ERROR, 'You don`t have any tasks at occurance.') 
                if not tasks_D5_det_all:
                    messages.add_message(request, messages.ERROR, 'You don`t have any tasks at detection.') 

                if tasks_D5_occ_all and tasks_D5_det_all and not tasks_D5_occ and not tasks_D5_det:
                    claim.status_id = ClaimStatus.objects.get(status='D5 uploaded').pk
                    claim.save()
                    return redirect('claims', company_id)
                return redirect('D5', claim)
                
            if 'AcceptD5' in request.POST:
                claim.status_id = ClaimStatus.objects.get(status='D5 accepted').pk
                claim.save()
                return redirect('claims', company_id)
                
            if 'RejectD5' in request.POST:
                claim.status_id = ClaimStatus.objects.get(status='D5 rejected').pk
                claim.save()
                return redirect('claims', company_id)
                

#         if '/SMS/D5/' in request.path:
#             tasks_D5 = Task.objects.filter(project=claim, subproject='D5 Occurance', closed=False).order_by('due_date')
#             tasks_D5_det = Task.objects.filter(project=claim, subproject='D5 Detection', closed=False).order_by('due_date')
#             form_due= Claim_Form(request.POST, instance=claim)

                

        if '/SMS/D6/' in request.path:
            tasks_D6_occ = Task.objects.filter(project=claim, subproject='D6_Occurance', closed=False).order_by('due_date')
            tasks_D6_det = Task.objects.filter(project=claim, subproject='D6_Detection', closed=False).order_by('due_date')
            tasks_D6_occ_all = Task.objects.filter(project=claim, subproject='D6_Occurance').order_by('due_date')
            tasks_D6_det_all = Task.objects.filter(project=claim, subproject='D6_Detection').order_by('due_date')
            pdb.set_trace()
            
            if 'SubmitD6' in request.POST:
                if tasks_D6_occ:
                    messages.add_message(request, messages.ERROR, 'You still have open tasks at occurance.') 
                if tasks_D6_det:
                    messages.add_message(request, messages.ERROR, 'You still have open tasks at detection.') 
                if not tasks_D6_occ_all:
                    messages.add_message(request, messages.ERROR, 'You don`t have any tasks at occurance.') 
                if not tasks_D6_det_all:
                    messages.add_message(request, messages.ERROR, 'You don`t have any tasks at detection.') 

                if tasks_D6_occ_all and tasks_D6_det_all and not tasks_D6_occ and not tasks_D6_det:
                    claim.status_id = ClaimStatus.objects.get(status='D6 uploaded').pk
                    claim.save()
                    return redirect('claims', company_id)
                return redirect('D6', claim)
                
            if 'AcceptD6' in request.POST:
                claim.status_id = ClaimStatus.objects.get(status='D6 accepted').pk
                claim.save()
                return redirect('claims', company_id)
                
            if 'RejectD6' in request.POST:
                claim.status_id = ClaimStatus.objects.get(status='D6 rejected').pk
                claim.save()
                return redirect('claims', company_id)
                

        if '/SMS/D7/' in request.path:
            form=D7Form(request.POST, instance=D7docu, company=company)
            form_due=Claim_Form(request.POST, instance=claim)
#             pdb.set_trace()
            if form.is_valid():
#                 pdb.set_trace()
                if 'Submit8D' in request.POST:
                  claim.status_id = ClaimStatus.objects.get(status='D7 uploaded').pk
                  claim.save()
                if 'AcceptD7' in request.POST:
                   claim.status_id = ClaimStatus.objects.get(status='D7 accepted').pk
                   claim.save()
                if 'RejectD7' in request.POST:
                   claim.status_id = ClaimStatus.objects.get(status='D7 rejected').pk
                   claim.save()
#                 d7_data=form.save()
                d7_data=form.save(commit=False)
                d7_data.claim_id=claim.pk
                if request.POST.get("DFMEA_pilot"):
                    try:
                        treffer= Team.objects.get(claim_id=claim, member=request.POST.get("DFMEA_pilot"))
                    except Team.MultipleObjectsReturned:
                        pass
                    except Team.DoesNotExist:
                        instance=UserProfile(pk=request.POST.get("DFMEA_pilot"))
                        new_member = Team(claim=claim, member=instance, isPilot=False)
                        new_member.save()        
                if request.POST.get("PFMEA_pilot"):
                    try:
                        treffer= Team.objects.get(claim_id=claim, member=request.POST.get("PFMEA_pilot"))
                    except Team.MultipleObjectsReturned:
                        pass
                    except Team.DoesNotExist:
                        instance=UserProfile(pk=request.POST.get("PFMEA_pilot"))
                        new_member = Team(claim=claim, member=instance, isPilot=False)
                        new_member.save()        
                if request.POST.get("LFMEA_pilot"):
                    try:
                        treffer= Team.objects.get(claim_id=claim, member=request.POST.get("LFMEA_pilot"))
                    except Team.MultipleObjectsReturned:
                        pass
                    except Team.DoesNotExist:
                        instance=UserProfile(pk=request.POST.get("LFMEA_pilot"))
                        new_member = Team(claim=claim, member=instance, isPilot=False)
                        new_member.save()        
                if request.POST.get("controlplan_pilot"):
                    try:
                        treffer= Team.objects.get(claim_id=claim, member=request.POST.get("controlplan_pilot"))
                    except Team.MultipleObjectsReturned:
                        pass
                    except Team.DoesNotExist:
                        instance=UserProfile(pk=request.POST.get("controlplan_pilot"))
                        new_member = Team(claim=claim, member=instance, isPilot=False)
                        new_member.save()        
                if request.POST.get("WI_pilot"):
                    try:
                        treffer= Team.objects.get(claim_id=claim, member=request.POST.get("WI_pilot"))
                    except Team.MultipleObjectsReturned:
                        pass
                    except Team.DoesNotExist:
                        instance=UserProfile(pk=request.POST.get("WI_pilot"))
                        new_member = Team(claim=claim, member=instance, isPilot=False)
                        new_member.save()        
                if request.POST.get("MP_pilot"):
                    try:
                        treffer= Team.objects.get(claim_id=claim, member=request.POST.get("MP_pilot"))
                    except Team.MultipleObjectsReturned:
                        pass
                    except Team.DoesNotExist:
                        instance=UserProfile(pk=request.POST.get("MP_pilot"))
                        new_member = Team(claim=claim, member=instance, isPilot=False)
                        new_member.save()        
                if request.POST.get("Dstand_pilot"):
                    try:
                        treffer= Team.objects.get(claim_id=claim, member=request.POST.get("Dstand_pilot"))
                    except Team.MultipleObjectsReturned:
                        pass
                    except Team.DoesNotExist:
                        instance=UserProfile(pk=request.POST.get("Dstand_pilot"))
                        new_member = Team(claim=claim, member=instance, isPilot=False)
                        new_member.save()        
                if request.POST.get("toolDstand_pilot"):
                    try:
                        treffer= Team.objects.get(claim_id=claim, member=request.POST.get("toolDstand_pilot"))
                    except Team.MultipleObjectsReturned:
                        pass
                    except Team.DoesNotExist:
                        instance=UserProfile(pk=request.POST.get("toolDstand_pilot"))
                        new_member = Team(claim=claim, member=instance, isPilot=False)
                        new_member.save()        
                if request.POST.get("LLcard_pilot"):
                    try:
                        treffer= Team.objects.get(claim_id=claim, member=request.POST.get("LLcard_pilot"))
                    except Team.MultipleObjectsReturned:
                        pass
                    except Team.DoesNotExist:
                        instance=UserProfile(pk=request.POST.get("LLcard_pilot"))
                        new_member = Team(claim=claim, member=instance, isPilot=False)
                        new_member.save()        
                if request.POST.get("Gstand_pilot"):
                    try:
                        treffer= Team.objects.get(claim_id=claim, member=request.POST.get("Gstand_pilot"))
                    except Team.MultipleObjectsReturned:
                        pass
                    except Team.DoesNotExist:
                        instance=UserProfile(pk=request.POST.get("Gstand_pilot"))
                        new_member = Team(claim=claim, member=instance, isPilot=False)
                        new_member.save()        
                if request.POST.get("Tstand_pilot"):
                    try:
                        treffer= Team.objects.get(claim_id=claim, member=request.POST.get("Tstand_pilot"))
                    except Team.MultipleObjectsReturned:
                        pass
                    except Team.DoesNotExist:
                        instance=UserProfile(pk=request.POST.get("Tstand_pilot"))
                        new_member = Team(claim=claim, member=instance, isPilot=False)
                        new_member.save()        
                if request.POST.get("procedure_pilot"):
                    try:
                        treffer= Team.objects.get(claim_id=claim, member=request.POST.get("procedure_pilot"))
                    except Team.MultipleObjectsReturned:
                        pass
                    except Team.DoesNotExist:
                        instance=UserProfile(pk=request.POST.get("procedure_pilot"))
                        new_member = Team(claim=claim, member=instance, isPilot=False)
                        new_member.save()        
                if request.POST.get("spec_pilot"):
                    try:
                        treffer= Team.objects.get(claim_id=claim, member=request.POST.get("spec_pilot"))
                    except Team.MultipleObjectsReturned:
                        pass
                    except Team.DoesNotExist:
                        instance=UserProfile(pk=request.POST.get("spec_pilot"))
                        new_member = Team(claim=claim, member=instance, isPilot=False)
                        new_member.save()        
                if request.POST.get("other_pilot"):
                    try:
                        treffer= Team.objects.get(claim_id=claim, member=request.POST.get("other_pilot"))
                    except Team.MultipleObjectsReturned:
                        pass
                    except Team.DoesNotExist:
                        instance=UserProfile(pk=request.POST.get("other_pilot"))
                        new_member = Team(claim=claim, member=instance, isPilot=False)
                        new_member.save()        
                
                d7_data.save()
                return redirect('D7', claim)    
            return render(request, 'SMS/D7.html', {'vendors':vendors, 'show_company':show_company, 'company':company, 'claim':claim, 'creator':creator,
                                                    'form_due':form_due, 'form':form
                                                   })
#             return render(request, 'SMS/D7.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'claim':claim, 'creator':creator,
#                                                     'form_due':form_due, 'form':form
#                                                    })
        if '/SMS/D8/' in request.path:
            form_due=Claim_Form(request.POST, instance=claim)
            if 'Accept8D' in request.POST:
                   claim.status_id = ClaimStatus.objects.get(status='Closed').pk
                   claim.save()
            if 'Reopen8D' in request.POST:
                   claim.status_id = ClaimStatus.objects.get(status='Opened').pk
                   claim.save()
            return redirect('D8', claim)    
#             return render(request, 'SMS/D8.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'claim':claim, 'creator':creator,
#                                                     'form_due':form_due
#                                                    })
#         if '/SMS/D5/' in request.path:
#             tasks_D5 = Task.objects.filter(project=claim, subproject='D5 Occurance', closed=False).order_by('due_date')
#             tasks_D5_det = Task.objects.filter(project=claim, subproject='D5 Detection', closed=False).order_by('due_date')
#             form_due= Claim_Form(request.POST, instance=claim)

                

    else:    
#         pdb.set_trace()
        if '/SMS/claim_Data/' in request.path:
            trace_data=TraceData.objects.filter(claim=claim.pk)     
            form=Data_Form()
            form2=Acceptance_Form(instance=claim)
            return render(request, 'SMS/claim_Data.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'form2': form2, 'claim':claim, 'creator':creator, 'trace_data':trace_data })

        if '/SMS/D1/' in request.path:
            team_members = Team.objects.filter(claim=claim.pk)
            form=Team_Form(company=company)    #nur User der company werden angezeigt
#             pdb.set_trace()
            return render(request, 'SMS/D1.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'claim':claim, 'creator':creator, 'team_members':team_members })

        if '/SMS/D2/' in request.path:
            form=D2_SV_Form(instance=d2_sv)
            return render(request, 'SMS/D2.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'form': form, 'claim':claim, 'creator':creator, 'd2_cv':d2_cv })
#             return render(request, 'SMS/D2.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'claim':claim, 'creator':creator, 'd2_cv':d2_cv })

        if '/SMS/D3/' in request.path:
            tasks_D3 = Task.objects.filter(project=claim, subproject='D3', closed=False).order_by('due_date')
            form=D3_Form(instance=d3)
            form_due=Claim_Form(instance=claim)
#             pdb.set_trace()
            return render(request, 'SMS/D3.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company,
                                                   'form': form, 'form_due': form_due, 'claim':claim, 'creator':creator, 'd2_cv':d2_cv, 'sorting_data':sorting_data, 'tasks_D3':tasks_D3 })
#             return render(request, 'SMS/D3.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company,
#                                                    'form': form, 'form_due': form_due, 'claim':claim, 'creator':creator, 'd2_cv':d2_cv, 'sorting_data':sorting_data, 'tasks_D3':tasks_D3 })

        if '/SMS/D4/' in request.path:
            tasks_D4 = Task.objects.filter(project=claim, subproject='D4', closed=False).order_by('due_date')
            files_occ = File.objects.filter(project = claim, subproject='occ')
            files_det = File.objects.filter(project = claim, subproject='det')
            root_causes = D4.objects.filter(claim_id=claim).first()
            occ_D4 = D4_reproduction.objects.filter(claim_id = claim).first()   #deckt auch det ab.
            form = D4Form(instance = root_causes)
            form_due= Claim_Form(instance=claim)
            form_ishi_occ = Ishi_Occ_Form(instance=ishi_occ)
            form_ishi_det = Ishi_Det_Form(instance=ishi_det)
            form_W5_occ = W5_Occ_Form(instance=W5_occ)
            form_W5_det = W5_Det_Form(instance=W5_det)
            form_D4_occ =  D4Form_reproduction(company=company, instance= occ_D4)    #deckt auch det ab.
            form_files_occ = FileForm()
            form_files_det = FileForm()
#             pdb.set_trace()
            return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company,
                                                   'form': form, 'form_ishi_occ': form_ishi_occ, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 
                                                   'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 
                                                   'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ,
                                                   'form_files_det':form_files_det})

        if '/SMS/D5/' in request.path:
            form_due= Claim_Form(instance=claim)
            tasks_D5 = Task.objects.filter(project=claim, subproject='D5 Occurence', closed=False).order_by('due_date')
            tasks_D5_det = Task.objects.filter(project=claim, subproject='D5 Detection', closed=False).order_by('due_date')
#             pdb.set_trace()
            return render(request, 'SMS/D5.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'claim':claim, 'creator':creator,
                                                    'form_due':form_due, 'tasks_D5':tasks_D5, 'tasks_D5_det':tasks_D5_det
                                                   })

        if '/SMS/D6/' in request.path:
            form_due= Claim_Form(instance=claim)
            tasks_D6 = Task.objects.filter(project=claim, subproject='D6 Occurence', closed=False).order_by('due_date')
            tasks_D6_det = Task.objects.filter(project=claim, subproject='D6 Detection', closed=False).order_by('due_date')
#             pdb.set_trace()
            return render(request, 'SMS/D6.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'claim':claim, 'creator':creator,
                                                    'form_due':form_due, 'tasks_D6':tasks_D6, 'tasks_D6_det':tasks_D6_det
                                                   })

        if '/SMS/D7/' in request.path:
            form_due= Claim_Form(instance=claim)
            form=D7Form(instance=D7docu, company=company)
#             pdb.set_trace()
            return render(request, 'SMS/D7.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'claim':claim, 'creator':creator,
                                                    'form_due':form_due, 'form':form
                                                   })

        if '/SMS/D8/' in request.path:
            form_due= Claim_Form(instance=claim)
#             pdb.set_trace()
            return render(request, 'SMS/D8.html', {'vendors':vendors, 'user_profile':user_profile, 'company':company, 'claim':claim, 'creator':creator,
                                                    'form_due':form_due
                                                   })

           

@login_required
def task_tracker(request, order, project, subproject, id):

    user_profile = UserProfile.objects.get(user_id=request.user)
    company = Claim.objects.get(pk=project).related_to
    if not user_profile.isStaff:                  #der eingloggte User gehoert NICHT zu PMDM
        if not company == user_profile.company:   #der eingloggte User ruft Daten einer anderen Firma auf!
            messages.add_message(request, messages.ERROR, 'You are not allowed to see other companies items!')
         
    path = 'uploads/' + company.name + '/Claim_' + str(project)
    tasks = Task.objects.filter(project=project, subproject=subproject, closed=False).order_by(order)
    tasks_done = Task.objects.filter(project=project, subproject=subproject, closed = True).order_by(order)
    task_to_edit = None
#     pdb.set_trace()
    if id < 9000:
        task_to_edit = Task.objects.get(project=project, subproject=subproject, pk=id)

    proj = 'Claim Nb. ' + str(project)
    subproj = ', Division ' + subproject
    task_data = [proj, subproj, id, order, company]
    
    hereIwork = UserProfile.objects.get(user=request.user).company
    form = TaskForm(company=company, hereIwork=hereIwork)
    if request.method == "POST":
        if 'new_task' in request.POST:
            form=TaskForm(request.POST, company=company, hereIwork=hereIwork)
            if form.is_valid():
                new_task=form.save(commit=False)
                new_task.project = project
                new_task.subproject = subproject
                new_task.original_due_date =  form.cleaned_data['due_date']
                new_task.number = len(tasks) + len(tasks_done) + 1
                new_task.save()

                first_comment = Comment.objects.create(project=project, subproject=subproject, task=new_task.pk, author=user_profile, comment=form.cleaned_data['task_comment'])
                first_comment.save()
              
#               send_mail('new task', 'Es gibt neue Aufgaben. Juhu!', 'juergen@klotzek.de', ('juergen.klotzek@nmb-minebea.com', 'juergen@klotzek.de'))
                return redirect('task_tracker', order, project, subproject, 9999)

        if 'reopen' in request.POST:
            task_to_edit.closed = False
            task_to_edit.closed_date = None
            task_to_edit.save()
            return redirect('task_tracker', order, project, subproject, 9999)

        if 'task_done' in request.POST:
            task_to_edit.closed = True
            task_to_edit.closed_date = timezone.now()
            task_to_edit.save()
            return redirect('task_tracker', order, project, subproject, 9999)

    return render(request, 'SMS/task_tracker.html', {'user_profile':user_profile, 'task_data':task_data, 'form':form, 'tasks':tasks, 'tasks_done':tasks_done,
#      'form_edit':form_edit 
     })        
 
@login_required
def task_details(request, order, project, subproject, id):
    actual_user_id = request.user
    user_profile = UserProfile.objects.get(user_id=request.user)
    company = Claim.objects.get(pk=project).related_to
    if not user_profile.isStaff:                  #der eingloggte User gehoert NICHT zu PMDM
        if not company == user_profile.company:   #der eingloggte User ruft Daten einer anderen Firma auf!
            messages.add_message(request, messages.ERROR, 'You are not allowed to see other companies items!')
            return render(request, 'SMS/error.html', {'user_profile':user_profile, 'company':company,}) 
         
    path = 'uploads/' + company.name + '/Claim_' + str(project) + '/Task_' + str(id)
    task_to_edit = Task.objects.get(project=project, subproject=subproject, pk=id)
    try:
        comments = Comment.objects.filter(project=project, subproject=subproject, task=id).order_by('-pk')
    except:
        comments = None

    proj = 'Claim Nb. ' + str(project)
    subproj = ', Division ' + subproject
    task_data = [proj, subproj, id, order, company]
    hereIwork = UserProfile.objects.get(user=request.user).company
    
    form = TaskFormEdit(instance = task_to_edit, firma=company, hereIwork=hereIwork)
    form2 = CommentForm()
    if request.method == "POST":
        form=TaskFormEdit(request.POST, instance = task_to_edit, firma=company, hereIwork=hereIwork)
        form2=CommentForm(request.POST, request.FILES)
        if form.is_valid():
            new_task=form.save(commit=False)
            new_task.project = project
            new_task.subproject = subproject
            new_task.original_due_date =  task_to_edit.original_due_date
            new_task.file.field.upload_to = path
            if request.POST.get('comment'):
                new_task.task_comment=request.POST.get('comment')
            new_task.save()
            if request.POST.get('comment'):
                subject = 'new comment ( ' + proj + subproj + ', Task Nb. ' + str(id) + ')'
                mail_text = str(user_profile.user) + ' wrote: ' +  request.POST.get('comment')
                new_comment=form2.save(commit=False)
                new_comment.project=project
                new_comment.subproject=subproject
                new_comment.task=id
                new_comment.author=user_profile
                new_comment.file.field.upload_to = path
                new_comment.save()
                send_mail(subject, mail_text, 'juergen.klotzek@nmb-minebea.com', [task_to_edit.pilot.email], fail_silently=False,)
            if 'new_comment' in request.POST:
                return redirect('task_details', order, project, subproject, id)
            return redirect('task_tracker', order, project, subproject, 9999)
                
#         return render(request, 'SMS/task_details.html', {'user_profile':user_profile, 'task_data':task_data, 'form':form, 'form2':form2, 
#                                                       'comments':comments, 
#                                                       })        
    return render(request, 'SMS/task_details.html', {'user_profile':user_profile, 'task_data':task_data, 'form':form, 'form2':form2, 
                                                      'comments':comments, 
                                                      })        
    
    
    