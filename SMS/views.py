import pdb
import os
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import UserProfile, Company, Claim, ClaimStatus, Team, D2_CV, D2_SV, D3, PenaltyPeriods, Ishikawa_occurance, Ishikawa_detection, Task, W5_occurance, W5_detection, D4, D4_reproduction, File
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import Claim_New_Form, CompanyForm, UserForm, UserProfileForm, Team_Form, Data_Form, D2_CV_Form, D2_SV_Form, Claim_Form, D3_Form, Ishi_Occ_Form , Ishi_Det_Form, TaskForm, TaskFormBig, W5_Occ_Form , W5_Det_Form, D4Form, D4Form_reproduction, FileForm 
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail

# from django.core.files.storage import FileSystemStorage

# Create your views here.
@login_required
def index(request):
    actual_user_id = request.user
    user_profile = UserProfile.objects.get(user_id=actual_user_id)
    if request.method == 'POST':
        user_profile.company_id = request.POST.get("vendor_choice")
    company = Company.objects.get(pk=user_profile.company_id)
    show_company = Company.objects.get(pk=user_profile.company_id).id

    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.all()]
    return render(request, 'SMS/index.html',{'user_profile':user_profile, 'company':company, 'show_company':show_company, 'vendors':vendors, 'request':request})

@login_required
def vendor_new(request):
    actual_user_id = request.user
    user_profile = UserProfile.objects.get(user_id=actual_user_id)
    company = Company.objects.get(pk=user_profile.company_id)
    show_company = Company.objects.get(pk=user_profile.company_id).id
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.all()]

    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.save()
            return redirect('index')
    else:
        form = CompanyForm()
        return render(request, 'SMS/form.html',{'user_profile':user_profile, 'company':company, 'show_company':show_company, 'vendors':vendors,  'form': form})
#         return render(request, 'SMS/vendor_edit.html',{'user_profile':user_profile, 'company':company, 'show_company':show_company, 'vendors':vendors,  'form': form})

@login_required
def user_new(request, company_id):
    actual_user_id = request.user
    user_profile = UserProfile.objects.get(user_id=actual_user_id)
    user_profile.company_id = company_id
    company = Company.objects.get(pk=user_profile.company_id)
    show_company = company_id
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.all()]

    if request.method == "POST":
        form1 = UserForm(request.POST)
        form2 = UserProfileForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            new_user = User.objects.create_user(**form1.cleaned_data)
            new_user_profile = form2.save(commit=False)
            user = User.objects.get(username = request.POST.get("username"))
            new_user_profile.user_id =  user.pk
            new_user_profile.company_id=show_company 
            new_user_profile.save()
            return redirect('index')
    else:
        form1 = UserForm()
        form2 = UserProfileForm()
        return render(request, 'SMS/two_forms.html',{'user_profile':user_profile, 'company':company, 'show_company':show_company, 'vendors':vendors,  'form1': form1, 'form2':form2})


@login_required
def user_edit(request, company_id):
    actual_user_id = request.user
    user_profile = UserProfile.objects.get(user_id=actual_user_id)
    user_profile.company_id = company_id
    company = Company.objects.get(pk=user_profile.company_id)
    show_company = company_id
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.all()]

    if request.method == "POST":
        form1 = UserForm(request.POST)
        form2 = UserProfileForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            new_user = User.objects.create_user(**form1.cleaned_data)
            new_user_profile = form2.save(commit=False)
            user = User.objects.get(username = request.POST.get("username"))
            new_user_profile.user_id =  user.pk
            new_user_profile.company_id=show_company 
            new_user_profile.save()
            return redirect('index')
    else:
        form1 = UserForm()
        form2 = UserProfileForm()
        return render(request, 'SMS/two_forms.html',{'user_profile':user_profile, 'company':company, 'show_company':show_company, 'vendors':vendors,  'form1': form1, 'form2':form2})


@login_required
def vendor_edit(request, vendor):
    actual_user_id = request.user
    user_profile = UserProfile.objects.get(user_id=actual_user_id)
    company = Company.objects.get(pk=vendor)
    show_company = vendor
#     show_company = Company.objects.get(pk=user_profile.company_id).id
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.all()]

    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            company = form.save(commit = False)
            company.save()
            return redirect('index')
    else:
        form = CompanyForm(instance=company)
        return render(request, 'SMS/form.html',{'user_profile':user_profile, 'company':company, 'show_company':show_company, 'vendors':vendors,  'form': form})
#         return render(request, 'SMS/vendor_edit.html',{'user_profile':user_profile, 'company':company, 'show_company':show_company, 'vendors':vendors,  'form': form})

    
@login_required
def claims(request, company_id):
    actual_user_id = request.user
    user_profile = UserProfile.objects.get(user_id=actual_user_id)
    company = Company.objects.get(pk=company_id)
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.all()]
    show_company = company_id
    claims = Claim.objects.filter(related_to = company_id, valid = 'True')
#     pdb.set_trace()
     
    return render(request, 'SMS/claims.html', {'vendors':vendors, 'user_profile':user_profile, 'claims':claims, 'show_company':show_company, 'company':company,}) 
    
@login_required
def claim_edit(request, claim):
    claim = get_object_or_404(Claim, pk=claim)
    try:
        d2 = D2_CV.objects.get(claim_id=claim.pk) #vielleicht gibt es den Eintrag noch gar nicht
    except:
        d2=None
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.all()]
    user_profile = UserProfile.objects.get(user_id=request.user)
    company_id = claim.related_to_id
    show_company = company_id
    company = Company.objects.get(pk=company_id)

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
            return redirect('claims', company_id)

    else:
        form = Claim_New_Form(instance=claim)
        form2 = D2_CV_Form(instance=d2)
    return render(request, 'SMS/form_claim_base_data.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form2': form2, 'claim':claim })
            

@login_required
def new_claim(request, company_id):
#     pdb.set_trace()
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.all()]
    user_profile = UserProfile.objects.get(user_id=request.user)
    show_company = company_id
    company = Company.objects.get(pk=company_id)
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
#         else:
#             return render(request, 'SMS/form_claim_base_data.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form2': form2, 'no_label': no_label})
        
        
    else:
        no_label = True
        form = Claim_New_Form()
        form2 = D2_CV_Form()
    return render(request, 'SMS/form_claim_base_data.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form2': form2, 'no_label': no_label})

  
@login_required
def claim_remove(request, claim):
    claim = get_object_or_404(Claim, pk=claim)
    company_id = claim.related_to_id
    claim.valid = False
    claim.save()
    return redirect('claims', company_id)


@login_required
def D1D8(request, claim):

    team = Team.objects.filter(claim_id=claim).first()
    d2_cv = D2_CV.objects.filter(claim_id=claim).first()
    d2_sv = D2_SV.objects.filter(claim_id=claim).first()
    d3 = D3.objects.filter(claim_id=claim).first()
    ishi_occ = Ishikawa_occurance.objects.filter(claim_id=claim).first()
    ishi_det = Ishikawa_detection.objects.filter(claim_id=claim).first()
    W5_occ = W5_occurance.objects.filter(claim_id=claim).first()
    W5_det = W5_detection.objects.filter(claim_id=claim).first()
          
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
            
        
    claim = get_object_or_404(Claim, pk=claim)
    company_id = claim.related_to_id
    vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.all()]
    user_profile = UserProfile.objects.get(user_id=request.user)
    company_id = claim.related_to_id
    show_company = company_id
    company = Company.objects.get(pk=company_id)
    creator = UserProfile.objects.get(user_id=claim.created_by)

#     pdb.set_trace()
    
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
            form = Data_Form(request.POST, instance = claim)
            if form.is_valid():
#                 open_reject_id = Claim.objects.get(status__status__contains="rejection opened by vendor").pk 
                open_reject_id = claim.status
#                 pdb.set_trace()
                if 'Refusal' in request.POST:
                    claim.status_id = ClaimStatus.objects.get(status='rejection accepted (closed)').pk
                if 'refused' in request.POST and not 'Refusal' in request.POST:
                    claim.status_id = ClaimStatus.objects.get(status='rejection opened by vendor').pk
                claim=form.save(commit= False)
                claim.save()
                return redirect('claim_Data', claim)
            else:
                return render(request, 'SMS/claim_Data.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'claim':claim, 'creator':creator })
        
        if '/SMS/D1/' in request.path:
            form=Team_Form(request.POST, instance=team)
            if form.is_valid():
                team_form=form.save(commit=False)
                team_form.save()
                return redirect('D1', claim)
            else:
                return render(request, 'SMS/D1.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'claim':claim, 'creator':creator })

        if '/SMS/D2/' in request.path:
            form=D2_SV_Form(request.POST, instance=d2_sv)
            if form.is_valid():
                d2_form=form.save(commit=False)
                d2_form.claim_id=claim.pk
                d2_form.save()
                return redirect('D2', claim)
            else:
                return render(request, 'SMS/D2.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'claim':claim, 'creator':creator , 'd2_cv':d2_cv })
        
        if '/SMS/D3/' in request.path:
            tasks_D3 = Task.objects.filter(project=claim, subproject='D3', closed=False).order_by('due_date')
            form=D3_Form(request.POST, instance=d3)
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
            return render(request, 'SMS/D3.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company,
                                                   'form': form, 'form_due': form_due, 'claim':claim, 'creator':creator, 'd2_cv':d2_cv, 'sorting_data':sorting_data, 'tasks_D3':tasks_D3  })

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
            form_D4_occ =  D4Form_reproduction(request.POST, instance= occ_D4)
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
                return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
#                 return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company,
#                                                    'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator 
#                                                    , 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4 })
                
            if 'Save_Ishi_Det' in request.POST:
                if form_ishi_det.is_valid():
#                     pdb.set_trace()
                    edit_ishi_det = form_ishi_det.save(commit=False)
                    edit_ishi_det.claim_id=claim.pk
                    edit_ishi_det.save()
                    return redirect('D4', claim)
                return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
#                 return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company,
#                                                    'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator 
#                                                    , 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4 })
                
#             pdb.set_trace()
            if 'Save_W5_occ' in request.POST:
                pdb.set_trace()
                if form_W5_occ.is_valid():
                    pdb.set_trace()
                    edit_W5_occ = form_W5_occ.save(commit=False)
                    edit_W5_occ.claim_id=claim.pk
                    edit_W5_occ.save()
                    return redirect('D4', claim)
                return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
#                 return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company,
#                                                    'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator 
#                                                    , 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4 })
                
            if 'Save_W5_det' in request.POST:
                if form_W5_det.is_valid():
                    pdb.set_trace()
                    edit_W5_det = form_W5_det.save(commit=False)
                    edit_W5_det.claim_id=claim.pk
                    edit_W5_det.save()
                    return redirect('D4', claim)
                return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
#                 return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company,
#                                                    'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 
#                                                     'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4 })

            if 'save_root_causes' in request.POST:
                if form.is_valid():
#                     pdb.set_trace()
                    edit = form.save(commit=False)
                    edit.claim_id=claim.pk
                    edit.save()
                    return redirect('D4', claim)
                return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
#                 return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company,
#                                                    'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ })

            if 'save_reproduction' in request.POST:
                if form_D4_occ.is_valid():
#                     pdb.set_trace()
                    edit_repro = form_D4_occ.save(commit=False)
                    edit_repro.claim_id=claim.pk
                    edit_repro.save()
                    return redirect('D4', claim)
                return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
#                 return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company,
#                                                    'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ })
                
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
                return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
#                 return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company,
#                                                    'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ,
#                                                    'form_files_det':form_files_det })
                
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
                return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'form_ishi_occ': form_ishi_occ, 'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ, 'form_files_det':form_files_det })
                
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
            tasks_D5 = Task.objects.filter(project=claim, subproject='D5 Occurance', closed=False).order_by('due_date')
            tasks_D5_det = Task.objects.filter(project=claim, subproject='D5 Detection', closed=False).order_by('due_date')
            form_due= Claim_Form(request.POST, instance=claim)

                

    else:    
        if '/SMS/claim_Data/' in request.path:     
            form=Data_Form(instance=claim)
            return render(request, 'SMS/claim_Data.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'claim':claim, 'creator':creator })

        if '/SMS/D1/' in request.path:
                 
            form=Team_Form(instance=team, initial={'pilot': user_profile.firstname + ' ' + user_profile.lastname, 'mail': user_profile.email})
            return render(request, 'SMS/D1.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'claim':claim, 'creator':creator })

        if '/SMS/D2/' in request.path:
            form=D2_SV_Form(instance=d2_sv)
            return render(request, 'SMS/D2.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'form': form, 'claim':claim, 'creator':creator, 'd2_cv':d2_cv })

        if '/SMS/D3/' in request.path:
            tasks_D3 = Task.objects.filter(project=claim, subproject='D3', closed=False).order_by('due_date')
            form=D3_Form(instance=d3)
            form_due=Claim_Form(instance=claim)
#             pdb.set_trace()
            return render(request, 'SMS/D3.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company,
                                                   'form': form, 'form_due': form_due, 'claim':claim, 'creator':creator, 'd2_cv':d2_cv, 'sorting_data':sorting_data, 'tasks_D3':tasks_D3 })

        if '/SMS/D4/' in request.path:
            tasks_D4 = Task.objects.filter(project=claim, subproject='D4', closed=False).order_by('due_date')
            files_occ = File.objects.filter(project = claim, subproject='occ')
            files_det = File.objects.filter(project = claim, subproject='det')
            root_causes = D4.objects.filter(claim_id=claim).first()
            occ_D4 = D4_reproduction.objects.filter(claim_id = claim).first()
            form = D4Form(instance = root_causes)
            form_due= Claim_Form(instance=claim)
            form_ishi_occ = Ishi_Occ_Form(instance=ishi_occ)
            form_ishi_det = Ishi_Det_Form(instance=ishi_det)
            form_W5_occ = W5_Occ_Form(instance=W5_occ)
            form_W5_det = W5_Det_Form(instance=W5_det)
            form_D4_occ =  D4Form_reproduction(instance= occ_D4)
            form_files_occ = FileForm()
            form_files_det = FileForm()
#             pdb.set_trace()
            return render(request, 'SMS/D4.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company,
                                                   'form': form, 'form_ishi_occ': form_ishi_occ, 'form_W5_occ': form_W5_occ, 'form_W5_det': form_W5_det, 
                                                   'form_ishi_det': form_ishi_det, 'form_due': form_due, 'claim':claim, 'creator':creator, 
                                                   'tasks_D4':tasks_D4, 'form_D4_occ':form_D4_occ, 'files_occ':files_occ, 'files_det':files_det, 'form_files_occ':form_files_occ,
                                                   'form_files_det':form_files_det})

        if '/SMS/D5/' in request.path:
            form_due= Claim_Form(instance=claim)
            tasks_D5 = Task.objects.filter(project=claim, subproject='D5 Occurance', closed=False).order_by('due_date')
            tasks_D5_det = Task.objects.filter(project=claim, subproject='D5 Detection', closed=False).order_by('due_date')
#             pdb.set_trace()
            return render(request, 'SMS/D5.html', {'vendors':vendors, 'user_profile':user_profile, 'show_company':show_company, 'company':company, 'claim':claim, 'creator':creator,
                                                    'form_due':form_due, 'tasks_D5':tasks_D5, 'tasks_D5_det':tasks_D5_det
                                                   })

           

@login_required
def task_tracker(request, order, project, subproject, id):

    actual_user_id = request.user
#     pdb.set_trace()
    user_profile = UserProfile.objects.get(user_id=actual_user_id)
#     user_profile = UserProfile.objects.filter(user_id=actual_user_id).first
#     try:
#         user_profile = UserProfile.objects.get(user_id=actual_user_id)
#     except:
#         user_profile=None
    
    
    company = Claim.objects.get(pk=project).related_to.name
    path = 'uploads/' + company + '/Claim_' + str(project)
    tasks = Task.objects.filter(project=project, subproject=subproject, closed=False).order_by(order)
    tasks_done = Task.objects.filter(project=project, subproject=subproject, closed = True)
    task_to_edit = None
    if id < 9000:
        task_to_edit = Task.objects.get(project=project, subproject=subproject, pk=id)

    proj = 'Claim Nb. ' + str(project)
    subproj = ', Division ' + subproject
    task_data = [proj, subproj, id, order]
    
    
    form = TaskForm()
    form_edit = TaskFormBig(instance=task_to_edit)
    if request.method == "POST":
        if 'new_task' in request.POST:
            form=TaskForm(request.POST, request.FILES)
            if form.is_valid():
              new_task=form.save(commit=False)
              new_task.project = project
              new_task.subproject = subproject
              new_task.original_due_date =  form.cleaned_data['due_date']
              new_task.file.field.upload_to = path
              new_task.save()
              
#               send_mail('new task', 'Es gibt neue Aufgaben. Juhu!', 'juergen@klotzek.de', ('juergen.klotzek@nmb-minebea.com', 'juergen@klotzek.de'))
              return redirect('task_tracker', order, project, subproject, 9999)

        if 'edit_task' in request.POST:
            form_edit=TaskFormBig(request.POST, request.FILES, instance = task_to_edit)
            if form_edit.is_valid():
              task_edit = form_edit.save(commit=False)
              task_edit.file.field.upload_to = path
              task_edit.save()
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

    return render(request, 'SMS/task_tracker.html', {'user_profile':user_profile, 'task_data':task_data, 'form':form, 'tasks':tasks, 'tasks_done':tasks_done, 'form_edit':form_edit })        
 
# 
# @login_required
# def certs(request, company_id):
#     actual_user_id = request.user
#     user_profile = UserProfile.objects.get(user_id=actual_user_id)
#     vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.all()]
# #     company_id=1
# #     claims = Claim.objects.filter(related_to = company_id)
#     return render(request, 'SMS/claims.html', {'vendors':vendors, 'user_profile':user_profile})        
# 
# @login_required
# def ppaps(request, company_id):
#     actual_user_id = request.user
#     user_profile = UserProfile.objects.get(user_id=actual_user_id)
#     vendors=[(vendor.pk, vendor.name) for vendor in Company.objects.all()]
# #     company_id=1
# #     claims = Claim.objects.filter(related_to = company_id)
#     return render(request, 'SMS/claims.html', {'vendors':vendors, 'user_profile':user_profile})        
    