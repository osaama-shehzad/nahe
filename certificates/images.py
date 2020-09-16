from PIL import Image, ImageDraw, ImageFont

image = Image.open("certificates\static\certificates\Certificate_0001.jpg")
font_type = ImageFont.truetype('arial.ttf', 70)
font_type_2 = ImageFont.truetype('arial.ttf', 35)
draw = ImageDraw.Draw(image)
draw.text(xy=(810, 740), text="Dr. Abul Rehman", fill=(0,102,0), font=font_type)
draw.text (xy=(330, 1230), text="24 July 2020", fill=(0,102,0), font=font_type_2)
image.save("test.pdf", "PDF", resolution=100.0)
