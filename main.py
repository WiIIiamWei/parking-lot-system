from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QInputDialog, QGraphicsTextItem, QGraphicsRectItem, QMessageBox
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QRectF
import sys

class ParkingSpace(QGraphicsRectItem):
    def __init__(self, x, y, width, height, parent=None):
        super().__init__(x, y, width, height, parent)
        self.setBrush(QBrush(QColor(0, 255, 0)))
        self.plate_number = None
        self.text_item = None

    def mousePressEvent(self, event):
        if self.plate_number is None:
            plate_number, ok = QInputDialog.getText(None, "Car Info", "Enter the car plate number:")
            if ok and plate_number:
                self.plate_number = plate_number
                self.setBrush(QBrush(QColor(255, 0, 0)))
                self.text_item = QGraphicsTextItem(self.plate_number, self)
                self.text_item.setPos(self.rect().center() - self.text_item.boundingRect().center())
                self.save_state()
        else:
            reply = QMessageBox.question(None, 'Remove Car', 'Are you sure you want to remove the car?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.plate_number = None
                self.setBrush(QBrush(QColor(0, 255, 0)))
                self.scene().removeItem(self.text_item)
                self.text_item = None
                self.save_state()

    def save_state(self):
        with open('parking_lot_state.txt', 'w') as f:
            for item in self.scene().items():
                if isinstance(item, ParkingSpace) and item.plate_number is not None:
                    f.write(item.plate_number + '\n')

class ParkingLot(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Parking Lot")
        self.setGeometry(100, 100, 500, 500)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 500, 500)

        self.draw_parking_lot()
        self.load_state()

    def draw_parking_lot(self):
        self.scene.clear()

        # Draw parking spaces
        space_width = 80
        space_height = 100
        space_margin = 10
        num_spaces = 5

        for i in range(num_spaces):
            x = space_margin + (space_width + space_margin) * i
            y = space_margin
            parking_space = ParkingSpace(x, y, space_width, space_height)
            self.scene.addItem(parking_space)

    def load_state(self):
        try:
            with open('parking_lot_state.txt', 'r') as f:
                plate_numbers = f.read().splitlines()
                parking_spaces = [item for item in reversed(self.scene.items()) if isinstance(item, ParkingSpace)]
                for i, plate_number in enumerate(plate_numbers):
                    parking_space = parking_spaces[i]
                    parking_space.plate_number = plate_number
                    parking_space.setBrush(QBrush(QColor(255, 0, 0)))
                    parking_space.text_item = QGraphicsTextItem(parking_space.plate_number, parking_space)
                    parking_space.text_item.setPos(parking_space.rect().center() - parking_space.text_item.boundingRect().center())
        except FileNotFoundError:
            pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawRect(0, 0, 500, 500)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    parking_lot = ParkingLot()
    parking_lot.show()
    sys.exit(app.exec_())