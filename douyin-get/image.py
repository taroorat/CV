from PIL import Image
import os
for i in os.listdir("iron_man"):
    img = Image.open("iron_man/"+i)

    width = img.size[0]
    height= img.size[1]
    new_width=max(width,height)
    new_height=new_width
    new_img = Image.new("RGBA",(new_width,new_height),(0,0,0,1))
    if height >width:
        new_img.paste(img, (int((height-width)/2), 0))
    else:
        new_img.paste(img, (0,int(( width-height) / 2)))
    new_img.save('sq_iron_man/'+i)

