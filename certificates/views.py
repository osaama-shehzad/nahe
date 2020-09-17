from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django import forms
from .models import Fellow
from PIL import Image, ImageDraw, ImageFont
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
    cnic = fellow.CNIC[:5]+ "-" + fellow.CNIC[5:12] + "-" + fellow.CNIC [-1]
    if "Dr." not in name: name = "Dr. " + name
    return render(request, "certificates/verified.html", {
        "name": name, 
        "program": program,
        "cnic": cnic,
        "id": ID,
        "message": f"It is verified that {name} (CNIC # {cnic}) has successfully completed NFDP training held during {program}.",
        "email": f"Please e-mail <nahe.support@hec.gov.pk> to request the transcript. The certificate ID is: {ID}."
    })

def fail (request, cnic): 
    return render(request, "certificates/fail.html", {
        "message": f"Record not found! No NFDP graduate holds the CNIC # {cnic}. Please try again with a different CNIC number."
    })

import os
def download (request, date, name, id):
    x = date.split(" ")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "certificates/static/certificates/Certificate_0001.jpg")
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
    msg = f"Certificate ID: {id}. To verify the authenticity of this e-certificate, email <nahe.support@hec.gov.pk>"
    draw.text (xy=(330, 1230), text=date, fill=(0,102,0), font=font_type_2)
    draw.text (xy=(209, 1410), text=msg, fill=(0,102,0), font=font_type_3)
    path = os.path.join(BASE_DIR, f"certificates/static/certificates/{name}.pdf")
    image.save(path, "PDF", resolution=100.0)
    with open(path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline;filename=NFDP-{name}.pdf'
        return response
