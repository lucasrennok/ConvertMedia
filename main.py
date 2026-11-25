from land_view import LandScreen


def main() -> None:
    while True:
        screen = LandScreen()
        action = screen.convert()
        screen.closeWindow()
        if action == "quit":
            break
    print("Encerrando...")


if __name__ == "__main__":
    main()
