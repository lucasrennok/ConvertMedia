from PIL import Image
import os

while(True):
    option = input("\n\nSelect one option:\n 1- Convert Image\n 2- Convert Video\n Any Key- Exit\n> OPTION: ")
    if(option!='1' and option!='2'):
        break
    
    file = input("> Filename and extension(ex: img.png, video.mp4): ")
    newfile = input("> New filename and extension: ")
    if(option=='1'):
        im1 = Image.open(file)
        im1.save(newfile)
    elif(option=='2'):
        os.system('ffmpeg -i '+ file+' '+ newfile)
    
print("Closing...")