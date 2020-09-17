from PIL import Image, ImageDraw, ImageFont

def download ():
    path = "certificates/static/certificates/Certificate_0001.jpg"
    date = "31-Aug-20"
    name = "Dr. Mohammad Osaama Bin Shehzad"
    image = Image.open(path)
    draw = ImageDraw.Draw(image)

    bounding_box = [600, 745, 1460, 800]
    x1, y1, x2, y2 = bounding_box

    font_type = ImageFont.truetype('C:\Windows\Fonts\ITCEDSCR.TTF', 90)

    w, h = draw.textsize(name, font=font_type)

    x = (x2 - x1 - w)/2 + x1
    y = (y2 - y1 - h)/2 + y1

    draw.text((x,y), name, align='center', font=font_type, fill=(0,102,0))
    
    font_type_2 = ImageFont.truetype('arial.ttf', 35)
    font_type_3 = ImageFont.truetype('arial.ttf', 30)
    msg = "Certificate ID: A7XMZ. To verify the authenticity of this e-certificate, email <nahe.support@hec.gov.pk"

    
    draw.rectangle([x1, y1, x2, y2])
    draw.text (xy=(335, 1220), text=date, fill=(0,102,0), font=font_type_2)
    draw.text (xy=(209, 1410), text=msg, fill=(0,102,0), font=font_type_3)
    image.show()

download()
