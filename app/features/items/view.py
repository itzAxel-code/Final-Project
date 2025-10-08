from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QSpinBox,
    QPushButton,
    QTableWidget,
    QListWidget,
    QTableWidgetItem,
    QLabel,
)
from PyQt6.QtCore import Qt
from app.core.db import get_conn
from .repository import ItemRepository
from .service import ItemService
from .models import Item


def build_items_view() -> QWidget:
    return ItemsView()


class ItemsView(QWidget):
    CAR_PRICES = {
        "Toyota Vios": 1500,
        "Honda Civic": 2000,
        "Nissan Almera": 1300,
        "Hyundai Accent": 1400,
        "Kia Rio": 1200,
        "Mazda 3": 1600,
        "Ford Focus": 1700,
        "Mitsubishi Montero": 2500,
        "Toyota Fortuner": 2700,
        "Honda CR-V": 2600,
        "Nissan X-Trail": 2500,
        "Ford Everest": 2800,
        "Hyundai Tucson": 2400,
        "Kia Sportage": 2300,
        "Ford Ranger": 3000,
        "Toyota Hilux": 2900,
        "Nissan Navara": 2850,
        "Isuzu D-Max": 2700,
        "Mitsubishi Strada": 2800,
        "Toyota Innova": 2200,
        "Mitsubishi Xpander": 2100,
        "Kia Carnival": 3200,
        "Hyundai Starex": 3000,
        "BMW 3 Series": 6000,
        "Mercedes-Benz C-Class": 6500,
        "Audi A4": 6200,
        "Lexus RX": 7000,
        "Porsche Cayenne": 9000,
    }

    def __init__(self):
        super().__init__()
        self.setObjectName("ItemsView")
        self.service = ItemService(ItemRepository(get_conn()))

        root = QHBoxLayout(self)

        left_side = QVBoxLayout()
        left_side.addWidget(QLabel("Available Car Models:"))
        self.items_list = QListWidget()
        self.items_list.addItems(self.CAR_PRICES.keys())
        left_side.addWidget(self.items_list)

        right_side = QVBoxLayout()

        form = QHBoxLayout()
        self.name = QLineEdit()
        self.name.setPlaceholderText("Car Models")
        self.price = QLineEdit()
        self.price.setPlaceholderText("Price (₱)")
        self.stock = QSpinBox()
        self.stock.setRange(0, 10_000)
        self.note = QLineEdit()
        self.note.setPlaceholderText("Note (optional)")
        self.btn_add = QPushButton("Add Car")

        form.addWidget(QLabel("Name:"))
        form.addWidget(self.name)
        form.addWidget(QLabel("Price:"))
        form.addWidget(self.price)
        form.addWidget(QLabel("Stock:"))
        form.addWidget(self.stock)
        form.addWidget(self.note, 1)
        form.addWidget(self.btn_add)
        right_side.addLayout(form)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Stock", "Note"])
        self.table.horizontalHeader().setStretchLastSection(True)
        right_side.addWidget(self.table)

        actions = QHBoxLayout()
        self.btn_refresh = QPushButton("Refresh")
        self.btn_delete = QPushButton("Delete Selected")
        self.btn_book = QPushButton("Book Car")
        self.btn_return = QPushButton("Return Car")
        actions.addWidget(self.btn_refresh)
        actions.addWidget(self.btn_delete)
        actions.addWidget(self.btn_book)
        actions.addWidget(self.btn_return)
        right_side.addLayout(actions)

        root.addLayout(left_side, 1)
        root.addLayout(right_side, 3)

        self._editing_id: int | None = None

        self.items_list.itemDoubleClicked.connect(self.on_item_selected)
        self.btn_add.clicked.connect(self.on_add_car)
        self.btn_book.clicked.connect(self.on_book_car)
        self.btn_return.clicked.connect(self.on_return_car)
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_delete.clicked.connect(self.on_delete)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)

        self.refresh()

    def on_item_selected(self, item):
        car_name = item.text()
        self.name.setText(car_name)
        if car_name in self.CAR_PRICES:
            self.price.setText(str(self.CAR_PRICES[car_name]))
        else:
            self.price.clear()
        self.stock.setValue(1)
        self.items_list.takeItem(self.items_list.row(item))

    def on_add_car(self):
        try:
            name = self.name.text().strip()
            pesos = float(self.price.text() or 0)
            price_cents = int(round(pesos * 100))
            stock = int(self.stock.value())
            note = self.note.text().strip()

            if not name or price_cents <= 0 or stock <= 0:
                print("Please enter valid details (name, price, stock).")
                return

            if self._editing_id:
                it = Item(id=self._editing_id, name=name, price_cents=price_cents, stock=stock, note=note)
                self.service.update(it)
            else:
                self.service.create(name, price_cents, stock, note)

            self.clear_form()
            self.refresh()

        except Exception as e:
            print(f"Error while adding car: {e}")

    def on_book_car(self):
        row = self.table.currentRow()
        if row < 0:
            return

        id_ = int(self.table.item(row, 0).text())
        name = self.table.item(row, 1).text()
        price_text = self.table.item(row, 2).text().replace("₱", "").replace(",", "")
        price_cents = int(round(float(price_text) * 100))
        stock = int(self.table.item(row, 3).text())
        note = self.table.item(row, 4).text()

        if stock > 0:
            new_stock = stock - 1
            it = Item(id=id_, name=name, price_cents=price_cents, stock=new_stock, note=note)
            self.service.update(it)
            self.refresh()

    def on_return_car(self):
        row = self.table.currentRow()
        if row < 0:
            return

        id_ = int(self.table.item(row, 0).text())
        name = self.table.item(row, 1).text()
        price_text = self.table.item(row, 2).text().replace("₱", "").replace(",", "")
        price_cents = int(round(float(price_text) * 100))
        stock = int(self.table.item(row, 3).text())
        note = self.table.item(row, 4).text()

        new_stock = stock + 1
        it = Item(id=id_, name=name, price_cents=price_cents, stock=new_stock, note=note)
        self.service.update(it)
        self.refresh()

    def on_delete(self):
        row = self.table.currentRow()
        if row < 0:
            return
        id_ = int(self.table.item(row, 0).text())
        self.service.delete(id_)
        if self._editing_id == id_:
            self.clear_form()
        self.refresh()

    def on_cell_double_clicked(self, row, _col):
        self._editing_id = int(self.table.item(row, 0).text())
        self.name.setText(self.table.item(row, 1).text())
        price_text = self.table.item(row, 2).text().replace("₱", "").replace(",", "")
        self.price.setText(price_text)
        self.stock.setValue(int(self.table.item(row, 3).text()))
        self.note.setText(self.table.item(row, 4).text())
        self.btn_add.setText("Save Changes")

    def clear_form(self):
        self._editing_id = None
        self.name.clear()
        self.price.clear()
        self.note.clear()
        self.stock.setValue(0)
        self.btn_add.setText("Add Car")

    def refresh(self):
        items = self.service.list()
        self.table.setRowCount(len(items))
        for r, it in enumerate(items):
            self.table.setItem(r, 0, QTableWidgetItem(str(it.id)))
            self.table.setItem(r, 1, QTableWidgetItem(it.name))
            self.table.setItem(r, 2, QTableWidgetItem(it.price_display))
            self.table.setItem(r, 3, QTableWidgetItem(str(it.stock)))
            self.table.setItem(r, 4, QTableWidgetItem(it.note))
        self.table.resizeColumnsToContents()
