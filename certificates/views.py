from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django import forms
from .models import Fellow
from PIL import Image, ImageDraw, ImageFont
from django.core.mail import send_mail
from django.core.validators import EmailValidator


import os
# Create your views here.

class SearchForm(forms.Form):
    cnic = forms.IntegerField(label="CNIC Number", 
    widget=forms.TextInput(attrs={'placeholder': 'CNIC (without dashes)',
    'maxlength': '13', 
    'minlength': '13',
    "class": "form-control"}))
    
def index (request): 
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            cnic = form.cleaned_data["cnic"]
            if Fellow.objects.filter(CNIC=cnic):
                fellow = Fellow.objects.get(CNIC=cnic)
                return success(request, fellow)
            else:
                return fail(request, cnic) 

        else: 
            return render(request, "certificates/index.html", {
                "form": form
            })
    else:
        search = SearchForm()
        return render (request, "certificates/index.html", {
            "form": search
        })
    
def success (request, fellow): 
    name = fellow.name.title()
    program = fellow.program
    cnic = fellow.CNIC
    ID = fellow.ID 
    cnic_x = fellow.CNIC[:5]+ "-" + fellow.CNIC[5:12] + "-" + fellow.CNIC [-1]
    if "Dr." not in name: name = "Dr. " + name
    return render(request, "certificates/verified.html", {
        "name": name, 
        "program": program,
        "cnic": cnic,
        "id": ID,
        "message": f"It is verified that {name} (CNIC # {cnic_x}) has successfully completed NFDP training held during {program}.",
        "email": f"To request the transcript or to verify the authenticity of the certificate, please e-mail <nahe.support@hec.gov.pk>. The certificate ID is: {ID}."
    })

def fail (request, cnic): 
    return render(request, "certificates/fail.html", {
        "message": f"Record not found! No NFDP graduate holds the CNIC # {cnic}. Please try again with a different CNIC number."
    })

def download (request, date, name, id):
    x = date.split(" ")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "certificates/static/certificates/aX201a0.jpg")
    date = f"29-{x[3]}-{x[4][:2]}" 
    image = Image.open(path)
    draw = ImageDraw.Draw(image)
    path = os.path.join(BASE_DIR, "certificates/static/certificates/ITCEDSCR.TTF")
    bounding_box = [600, 745, 1460, 800]
    x1, y1, x2, y2 = bounding_box
    font_type = ImageFont.truetype(path, 90)
    w, h = draw.textsize(name, font=font_type)
    x = (x2 - x1 - w)/2 + x1
    y = (y2 - y1 - h)/2 + y1
    path = os.path.join(BASE_DIR, "certificates/static/certificates/arial.ttf")
    font_type_2 = ImageFont.truetype(path, 35)  
    draw.text((x,y), name, align='center', font=font_type, fill=(0,102,0)) 
    font_type_3 = ImageFont.truetype(path, 30)
    msg = f"Cert. ID: {id}"
    draw.text (xy=(330, 1230), text=date, fill=(0,102,0), font=font_type_2)
    draw.text (xy=(1750, 1565), text=msg, fill=(0,0,0), font=font_type_3)
    path = os.path.join(BASE_DIR, f"certificates/static/certificates/{name}.pdf")
    image.save(path, "PDF", resolution=100.0)
    with open(path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline;filename=NFDP-{name}.pdf'
        return response

emailvalidator = EmailValidator(message="invalid email")
class TranscriptForm(forms.Form):
    name = forms.CharField(label="Name", 
    widget=forms.TextInput(attrs={
        'placeholder': 'full name',
        'max_length': '64',
        "class": "form-control"
        }))
    
    organization = forms.CharField(label="Organization", 
    widget=forms.TextInput(attrs={
        'placeholder': 'name of organization/institute',
        'max_length': '64',
        "class": "form-control"}))
    title = forms.CharField(label="Employment Title", 
    widget=forms.TextInput(attrs={
        'placeholder': 'position title',
        'max_length': '64',
        "class": "form-control"}))
    message = forms.CharField(label="Message", 
    widget=forms.Textarea(attrs={
        'placeholder': 'Please provide a short description about why you want to request the transcript.',
        "class": "form-control"}
    ))
    email = forms.CharField(validators=[emailvalidator], widget=forms.TextInput(attrs={
        'placeholder': 'valid official email address',
        "class": "form-control"}
    ))


def transcript (request, cnic):
    form = TranscriptForm()
    return render (request, "certificates/transcripts.html", {
        "form": form,
        "cnic": cnic
    })



def sendrequest (request, id): 
    # return HttpResponse("works")
    if request.method == "POST": 
        form = TranscriptForm(request.POST)
        if form.is_valid():
            #fellow details
            fellow = Fellow.objects.get(CNIC=id)
            f_name = fellow.name.title()
            f_program = fellow.program
            f_cert_id = fellow.ID
            #requester details
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            organization = form.cleaned_data["organization"]
            title = form.cleaned_data["title"]
            message = form.cleaned_data["message"]

            message = f"""A requested for transcript has been generated by:\n\n
            Name: {name.title()}
            Organization: {organization.title()}
            Title: {title.title()}
            Email: {email}
            Message: {message}\n
            This request has been generated for the following NFDP fellow:\n
            Fellow: {f_name}
            Program: {f_program}
            Cert. ID: {f_cert_id}
            CNIC: {id}\n
            THIS IS AN AUTO-GENERATED EMAIL. DO NOT REPLY."""
            emails = ['nahe.support@hec.gov.pk', email]
            # try:
            for i in emails:
                send_mail('Transcript Request for NFDP Fellow',
                message,
                None,
                [i],
                fail_silently=False)
            return render (request, "certificates/email_sent.html")
            # except: 
            #     return render (request, "certificates/email_fail.html")
        else: 
            return render(request, "certificates/transcripts.html", {
                "form": form,
                "cnic": id
            })
    else:
        form = TranscriptForm()
        return render(request, "certificates/transcripts.html", {
                "form": form,
                "cnic": id
            })


