import sys
from PyQt6.QtWidgets import QApplication
from app.shell.main_window import MainWindow
from app.features.items.view import build_items_view


def main():
    app = QApplication(sys.argv)

    try:
        with open("app/core/styles.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass

    win = MainWindow()
    win.add_feature("Items", build_items_view)
    win.resize(900, 560)
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
