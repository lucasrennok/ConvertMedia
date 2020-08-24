from land_view import LandScreen

def main():
    opt = 'convert'
    while(opt=='convert'):
        land_view = LandScreen()
        opt = land_view.convert()
        land_view.closeWindow()
        del land_view

    print("Closing...")

# Start here
main()