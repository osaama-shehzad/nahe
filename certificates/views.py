from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django import forms
from .models import Fellow
from PIL import Image, ImageDraw, ImageFont
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.http import JsonResponse
from django.core import serializers
import os, json
# Create your views here.

class SearchForm(forms.Form):
    cnic = forms.IntegerField(label="CNIC Number", 
    widget=forms.TextInput(attrs={'placeholder': 'CNIC (without dashes)',
    'maxlength': '13', 
    'minlength': '13',
    "class": "form-control",
    'id': "cnicfield"}))

def index (request):
    search = SearchForm()
    form2 = TranscriptForm()
    return render (request, "certificates/index.html", {
            "form": search,
            'form2': form2
        }) 

def search (request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    cnic = data.get("cnic", "")
    if Fellow.objects.filter(CNIC=cnic):
        fellow = Fellow.objects.filter(CNIC=cnic)
        fellow = serializers.serialize('json', fellow)
        return JsonResponse(fellow, status=201, safe=False)
    else: 
        return JsonResponse({
                "error": f"Fellow with CNIC ({cnic}) does not exist."
            }, status=400)
    
    
def success (request, fellow): 
    name = fellow.name.title()
    program = fellow.program
    cnic = fellow.CNIC
    ID = fellow.ID 
    graduation = fellow.graduation
    cnic_x = fellow.CNIC[:5]+ "-" + fellow.CNIC[5:12] + "-" + fellow.CNIC [-1]
    if "Dr." not in name: name = "Dr. " + name
    return render(request, "certificates/verified.html", {
        "graduation": graduation,
        "fellow": fellow, 
        "cnic": cnic,
        "message": f"It is verified that {name} (CNIC # {cnic_x}) has successfully completed NFDP training held during {program}.",
        "email": f"To request the transcript or to verify the authenticity of the certificate, please e-mail <nahe.support@hec.gov.pk>. The certificate ID is: {ID}."
    })


def download (request, date, name, graduation, id):
    if "Dr." not in name: 
        name = f"Dr. {name}"
    date = date.split(" ")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if graduation == "Completed Successfully":
        path = os.path.join(BASE_DIR, "certificates/static/certificates/aX201a0.jpg")
    else:
        path = os.path.join(BASE_DIR, "certificates/static/certificates/xv135gV.jpg") 

    date = f"29-{date[3]}-{date[4][:2]}" 
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
    draw.text (xy=(340, 1230), text=date, fill=(0,102,0), font=font_type_2)
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
        "class": "form-control",
        "id": "t-name"
        }))
    
    organization = forms.CharField(label="Organization", 
    widget=forms.TextInput(attrs={
        'placeholder': 'name of organization/institute',
        'max_length': '64',
        "class": "form-control",
        "id": "organization"}))
    title = forms.CharField(label="Employment Title", 
    widget=forms.TextInput(attrs={
        'placeholder': 'position title',
        'max_length': '64',
        "id": 'title',
        "class": "form-control"}))
    message = forms.CharField(label="Message", 
    widget=forms.Textarea(attrs={
        'placeholder': 'Please provide a short description about why you want to request the transcript.',
        "class": "form-control",
        "id": 'message'}
    ))
    email = forms.CharField(validators=[emailvalidator], widget=forms.TextInput(attrs={
        'placeholder': 'valid official email address',
        "class": "form-control",
        "id": 'email'}
    ))


def sendrequest (request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    cnic = data.get("cnic", "")
    name = data.get("name", "")
    organization = data.get("org", "")
    email = data.get("email", "")
    title = data.get("title", "")
    msg = data.get("msg", "")


    if Fellow.objects.filter(CNIC=cnic):
        fellow = Fellow.objects.get(CNIC=cnic)
        message = f"""A requested for transcript has been generated by:\n\n
            Name: {name.title()}
            Organization: {organization.title()}
            Title: {title.title()}
            Email: {email}
            Message: \n{msg}\n
            This request has been generated for the following NFDP fellow:\n
            Fellow: {fellow.name}
            Program: {fellow.program}
            Cert. ID: {fellow.ID}
            CNIC: {cnic}\n
            THIS IS AN AUTO-GENERATED EMAIL. DO NOT REPLY."""
        emails = ['nahe.support@hec.gov.pk', email]
        try:
            for i in emails:
                send_mail('Transcript Request for NFDP Fellow',
                message,
                None,
                [i],
                fail_silently=False)
            return JsonResponse({"status": 'success'}, status=201, safe=False)
        except: 
            return JsonResponse({"status": 'fail'}, status=400) 
   



