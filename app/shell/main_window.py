from PyQt6.QtWidgets import (
    QLabel,
    QMainWindow,
    QWidget,
    QHBoxLayout,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Rentals and Services")

        # Central container
        container = QWidget()
        self.layout = QHBoxLayout(container)
        self.setCentralWidget(container)

        self.features = {}

    def add_feature(self, name: str, factory):
        # Create widget for feature
        widget = factory()
        self.features[name] = widget

        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            w = item.widget()
            if w is not None:
                self.layout.removeWidget(w)
                w.deleteLater()

        self.layout.addWidget(widget)


