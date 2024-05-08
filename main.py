from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QInputDialog, QGraphicsTextItem, QGraphicsRectItem, QMessageBox
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout,QComboBox
import sys, os
from datetime import datetime
from misc import is_license_plate, calculate_fee

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("登录")
        self.role = None  # Add a new attribute to save the role of the current user

        self.username_label = QLabel("用户名")
        self.username_edit = QLineEdit()

        self.password_label = QLabel("密码")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        
        self.login_button = QPushButton("登录")
        self.login_button.clicked.connect(self.login)

        self.register_button = QPushButton("注册新账户")
        self.register_button.clicked.connect(self.registnew)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        # 检查用户名和密码是否正确
        with open('./user_information.txt', 'r') as f:
            for line in f:
                saved_username, saved_password, saved_role = line.strip().split(':')
                if username == saved_username and password == saved_password :
                    QMessageBox.information(self, "成功", f"登录成功，用户名：{username}")
                    self.role = saved_role
                    self.username = username
                    self.accept()  # Close the login dialog
                    return
            else:
                QMessageBox.warning(self, "错误", "用户名或密码错误")
        if username == saved_username and password == saved_password :
            QMessageBox.information(self, "成功", f"登录成功，用户名：{username}")
            self.role = saved_role  # Save the role of the current user
            self.username = username  # Save the username of the current user
            self.accept()  # Close the login dialog
            return
    
    def registnew(self):
        class RegisterDialog(QDialog):
            def __init__(self):
                super().__init__()

                self.username_label = QLabel("用户名（车牌号）")
                self.username_edit = QLineEdit()

                self.password_label = QLabel("密码")
                self.password_edit = QLineEdit()
                self.password_edit.setEchoMode(QLineEdit.Password)

                self.confirm_password_label = QLabel("确认密码")
                self.confirm_password_edit = QLineEdit()
                self.confirm_password_edit.setEchoMode(QLineEdit.Password)

                self.register_button = QPushButton("注册")
                self.register_button.clicked.connect(self.register)

                layout = QVBoxLayout()
                layout.addWidget(self.username_label)
                layout.addWidget(self.username_edit)
                layout.addWidget(self.password_label)
                layout.addWidget(self.password_edit)

                layout.addWidget(self.confirm_password_label)
                layout.addWidget(self.confirm_password_edit)
                
                self.role_label = QLabel("角色")
                self.role_combobox = QComboBox()
                self.role_combobox.addItem("管理员")
                self.role_combobox.addItem("车主")
                layout.addWidget(self.role_combobox)  # Add the role combobox to the layout

                layout.addWidget(self.register_button)
                
                self.setLayout(layout)

            def register(self):
                username = self.username_edit.text()
                password = self.password_edit.text()
                confirm_password = self.confirm_password_edit.text()
                role = self.role_combobox.currentText()  # Get the selected role

                if password != confirm_password:
                    QMessageBox.warning(self, "错误", "两次输入的密码不一致")
                    return
                # 如果角色是车主，检查用户名是否是车牌号
                if role == "车主" and not is_license_plate(username):
                    QMessageBox.warning(self, "错误", "用户名必须是车牌号")
                    return
                
                if not os.path.exists('./user_information.txt'):
                    open('./user_information.txt', 'w').close()
                    
                # 检查用户名是否已经存在
                with open('./user_information.txt', 'r') as f:
                    for line in f:
                        saved_username, _, _ = line.strip().split(':')
                        if username == saved_username:
                            QMessageBox.warning(self, "错误", "用户名已存在")
                            return
                        
                # 保存新的用户名和密码
                with open('./user_information.txt', 'a') as f:
                    f.write(f"{username}:{password}:{role}\n")  # Save the role along with the username and password

                QMessageBox.information(self, "成功", f"注册成功，用户名：{username}")
                # 退出窗口
                self.accept()

        dialog = RegisterDialog()
        dialog.exec_()
                                    
class ParkingSpace(QGraphicsRectItem):
    def __init__(self, id, x, y, width, height, parent=None):
        super().__init__(x, y, width, height, parent)
        self.setBrush(QBrush(QColor(0, 255, 0)))
        self.plate_number = None
        self.text_item = None
        self.id = id  # Add id attribute
        self.id_text_item = QGraphicsTextItem(str(self.id), self)  # Display id on the parking space
        self.id_text_item.setPos(self.rect().topLeft())
        self.entry_time = None
    
    def save_state(self):
        with open('parking_lot_state.txt', 'w') as f:
            for item in self.scene().items():
                if isinstance(item, ParkingSpace) and item.plate_number is not None:
                    f.write(f'{item.id}:{item.plate_number}\n')  # Include id in the file

    def mousePressEvent(self, event):
        if login_dialog.role == "车主" or login_dialog.role == "管理员":
            if self.plate_number is not None and self.plate_number != login_dialog.username and login_dialog.role != "管理员":
                QMessageBox.warning(None, "错误", "你没有权限更改这个车位")
                return
    
            if self.plate_number is None:
                if login_dialog.role == "管理员":
                    text, ok = QInputDialog.getText(None, '输入车牌号', '请输入车牌号:')
                    if not ok:
                        return
                    if ok and is_license_plate(text):
                        # Check if the car is already parked
                        for item in self.scene().items():
                            if isinstance(item, ParkingSpace) and item.plate_number == text:
                                QMessageBox.warning(None, "错误", "这辆车已经停在停车场中")
                                return
                        self.plate_number = text
                    else:
                        QMessageBox.warning(None, "错误", "请输入有效的车牌号")
                        return
                else:
                    # Check if the car is already parked
                    for item in self.scene().items():
                        if isinstance(item, ParkingSpace) and item.plate_number == login_dialog.username:
                            QMessageBox.warning(None, "错误", "你的车已经停在停车场中")
                            return
                    self.plate_number = login_dialog.username
                self.setBrush(QBrush(QColor(255, 0, 0)))
                self.text_item = QGraphicsTextItem(self.plate_number, self)
                self.text_item.setPos(self.rect().center() - self.text_item.boundingRect().center())
                self.entry_time = datetime.now()  # Record the entry time
                self.save_state()
            else:
                reply = QMessageBox.question(None, '移除该车', '确定要移除该车？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    parking_duration = datetime.now() - self.entry_time  # Calculate the parking duration
                    fee = calculate_fee(self.entry_time, datetime.now())  # Calculate the fee
    
                    QMessageBox.information(None, "停车时间", f"停车时间：{parking_duration}，费用：{fee}")
                    self.plate_number = None
                    self.setBrush(QBrush(QColor(0, 255, 0)))
                    self.scene().removeItem(self.text_item)
                    self.text_item = None
                    self.entry_time = None  # Reset the entry time
            self.save_state()

    def save_state(self):
        with open('parking_lot_state.txt', 'w') as f:
            for item in self.scene().items():
                if isinstance(item, ParkingSpace) and item.plate_number is not None:
                    f.write(f'{item.id}:{item.plate_number}\n')

class ParkingLot(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("停车场管理系统")
        self.setGeometry(100, 100, 1000, 1000)  # Increase the window size
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 1000, 1000)  # Increase the view size

        self.draw_parking_lot()
        self.load_state()
    def load_state(self):
        try:
            with open('parking_lot_state.txt', 'r') as f:
                parking_spaces = {item.id: item for item in reversed(self.scene.items()) if isinstance(item, ParkingSpace)}
                for line in f:
                    if ':' in line:  # Check if the line contains a colon
                        id, plate_number, entry_time = line.strip().split(':')
                        parking_space = parking_spaces[int(id)]
                        parking_space.plate_number = plate_number
                        parking_space.entry_time = datetime.strptime(entry_time, "%Y-%m-%d %H:%M:%S.%f")  # Parse the entry time
                        parking_space.setBrush(QBrush(QColor(255, 0, 0)))
                        parking_space.text_item = QGraphicsTextItem(parking_space.plate_number, parking_space)
                        parking_space.text_item.setPos(parking_space.rect().center() - parking_space.text_item.boundingRect().center())
        except FileNotFoundError:
            pass

    def draw_parking_lot(self):
        self.scene.clear()

        # Draw parking spaces
        space_width = 60  # Reduce the space width
        space_height = 80  # Reduce the space height
        space_margin = 10
        num_rows = 4
        num_columns = 10

        for row in range(num_rows):
            for column in range(num_columns):
                x = space_margin + (space_width + space_margin) * column
                y = space_margin + (space_height + space_margin) * row
                parking_space = ParkingSpace(row * num_columns + column, x, y, space_width, space_height)
                self.scene.addItem(parking_space)
    
    def save_state(self):
        with open('parking_lot_state.txt', 'w') as f:
            for item in self.scene().items():
                if isinstance(item, ParkingSpace) and item.plate_number is not None:
                    f.write(f'{item.id}:{item.plate_number}:{item.entry_time}\n')  # Include entry time in the file


    def load_state(self):
        try:
            with open('parking_lot_state.txt', 'r') as f:
                parking_spaces = {item.id: item for item in reversed(self.scene.items()) if isinstance(item, ParkingSpace)}
                for line in f:
                    if ':' in line:  # Check if the line contains a colon
                        id, plate_number = line.strip().split(':')
                        parking_space = parking_spaces[int(id)]
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
        
    def draw_parking_lot(self):
        self.scene.clear()

        # Draw parking spaces
        space_width = 80
        space_height = 100
        space_margin = 10
        num_rows = 4
        num_columns = 10
        extra_margin = 50

        for row in range(num_rows):
            for column in range(num_columns):
                x = space_margin + (space_width + space_margin) * column
                y = space_margin + (space_height + space_margin) * row
                if row >= 1:
                    y += extra_margin
                    if row >= 3:
                        y += extra_margin
                id = row * num_columns + column + 1  # Modify the ID index
                parking_space = ParkingSpace(id, x, y, space_width, space_height)
                self.scene.addItem(parking_space)
        
        # Display ID on top of parking spaces
        for item in self.scene.items():
            if isinstance(item, ParkingSpace):
                item.id_text_item.setPos(item.rect().topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:  # Check if the login was successful
        parking_lot = ParkingLot()
        parking_lot.show()
    sys.exit(app.exec_())