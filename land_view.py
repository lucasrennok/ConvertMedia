import PySimpleGUI as sg
from PIL import Image
import os

class LandScreen():
    def __init__(self):
        #layout
        layout = [
            [sg.Text('Convert:'),sg.Radio('Image', 'media', key='image', default=True), sg.Radio('Video', 'media', key='video')],
            [sg.Text('Filename'),sg.Input(key='filename', pad=((34,0),0))],
            [sg.Text('New Filename'),sg.Input(key='newFilename', pad=((5,0),0))],
            [sg.Button('Convert', key="convert", pad=((8,0),0)), sg.Button('Quit', key="quit")]
        ]
        #window
        self.window = sg.Window('ConvertMedia').layout(layout)

    def convert(self):
        #data extract
        print("Waiting...")
        self.button, self.data = self.window.Read()

        if(self.button=='convert'):
            # Get the filenames
            filename = self.data['filename']
            newFilename = self.data['newFilename']

            # Image?
            if(self.data['image']==True):
                wait_view = WaitScreen()
                img = Image.open(filename)
                img.save(newFilename)
                wait_view.closeWindow()
            # Or video?
            elif(self.data['video']==True):
                wait_view = WaitScreen()
                os.system('ffmpeg -i '+ filename+' '+ newFilename)
                wait_view.closeWindow()
            print("Converted.")
        return self.button

    def closeWindow(self):
        self.window.close()

class WaitScreen():
    def __init__(self):
        #layout
        layout = [
            [sg.Text('Wait...')]
        ]
        #window
        self.window = sg.Window('Converting...').layout(layout)
        self.button, self.data = self.window.Read(timeout=100)

    def closeWindow(self):
        self.window.close()