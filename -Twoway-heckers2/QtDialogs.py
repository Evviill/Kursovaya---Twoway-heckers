from PyQt5.QtWidgets import QMainWindow, QDialog, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
import base64
import xxtea
import QtGameForm


class SignUp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Checkers | Sign up")
        self.setFixedSize(400, 250)

        # Fonts init
        self.def_font = QtGui.QFont()
        self.def_font.setFamily("Tahoma")
        self.def_font.setPixelSize(25)
        self.def_font.setBold(True)
        self.def_font.setItalic(False)

        self.s_font = QtGui.QFont()
        self.s_font.setFamily("Arial")
        self.s_font.setPixelSize(16)
        self.s_font.setBold(False)
        self.s_font.setItalic(False)

        # Auth text label
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 400, 50))
        self.label.setFont(self.def_font)
        self.label.setObjectName("label")
        self.label.setText("Sign up form")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Inputs
        self.loginInput = QtWidgets.QLineEdit(self)
        self.loginInput.setGeometry(QtCore.QRect(120, 60, 160, 25))
        self.loginInput.setObjectName("loginInput")
        self.loginInput.setPlaceholderText("Login")

        self.passInput = QtWidgets.QLineEdit(self)
        self.passInput.setGeometry(QtCore.QRect(120, 90, 160, 25))
        self.passInput.setObjectName("passInput")
        self.passInput.setPlaceholderText("Password")

        self.mailInput = QtWidgets.QLineEdit(self)
        self.mailInput.setGeometry(QtCore.QRect(120, 120, 160, 25))
        self.mailInput.setObjectName("mailInput")
        self.mailInput.setPlaceholderText("Mail")

        # Buttons
        self.signupBtn = QtWidgets.QPushButton(self)
        self.signupBtn.setGeometry(QtCore.QRect(200, 150, 80, 25))
        self.signupBtn.setText("Sign up")

        # Finally
        self.registerBtns()

    @QtCore.pyqtSlot()
    def registerBtnHandler(self):
        if self.loginInput.text() and self.passInput.text() and self.mailInput.text():
            login = base64.b64encode(xxtea.encrypt(self.loginInput.text(), 'my_super_key'))
            password = base64.b64encode(xxtea.encrypt(self.passInput.text(), 'my_super_key'))
            mail = base64.b64encode(xxtea.encrypt(self.mailInput.text(), 'my_super_key'))
            with open('database.txt', 'rb+') as f:
                data = f.read()

            accounts = []
            if data is not None:
                rows = data.split(b'\n')
                if len(rows) > 1:
                    if len(rows) != 0:
                        accounts = [x.split() for x in rows]

            if len(accounts) != 0:
                find = False
                for acc in accounts:
                    if len(acc) == 3:
                        if acc[0] == login:
                            find = True
                if find:
                    QtWidgets.QMessageBox.information(self, 'Внимание!', 'Пользователь с таким именем уже существует')
                else:
                    with open('database.txt', 'ab+') as f:
                        f.write(login + b' ' + password + b' ' + mail + b'\n')
                    self.close()
            else:
                with open('database.txt', 'ab+') as f:
                    f.write(login + b' ' + password + b' ' + mail + b'\n')
                self.close()
        else:
            QtWidgets.QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля!')

    def registerBtns(self):
        self.signupBtn.clicked.connect(self.registerBtnHandler)


class AuthDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Checkers | Log in")
        self.setFixedSize(400, 250)
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        # Fonts init
        self.def_font = QtGui.QFont()
        self.def_font.setFamily("Tahoma")
        self.def_font.setPixelSize(25)
        self.def_font.setBold(True)
        self.def_font.setItalic(False)

        self.s_font = QtGui.QFont()
        self.s_font.setFamily("Arial")
        self.s_font.setPixelSize(16)
        self.s_font.setBold(False)
        self.s_font.setItalic(False)

        # Auth text label
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 400, 50))
        self.label.setFont(self.def_font)
        self.label.setObjectName("label")
        self.label.setText("Auth form")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Inputs
        self.loginInput = QtWidgets.QLineEdit(self)
        self.loginInput.setGeometry(QtCore.QRect(120, 60, 160, 25))
        self.loginInput.setObjectName("loginInput")
        self.loginInput.setPlaceholderText("Login")

        self.passInput = QtWidgets.QLineEdit(self)
        self.passInput.setGeometry(QtCore.QRect(120, 90, 160, 25))
        self.passInput.setObjectName("passInput")
        self.passInput.setPlaceholderText("Password")

        # Buttons
        self.loginBtn = QtWidgets.QPushButton(self)
        self.loginBtn.setGeometry(QtCore.QRect(120, 150, 80, 25))
        self.loginBtn.setText("Log in")

        self.signupBtn = QtWidgets.QPushButton(self)
        self.signupBtn.setGeometry(QtCore.QRect(200, 150, 80, 25))
        self.signupBtn.setText("Sign up")

        # Finally
        self.registerBtns()

    @QtCore.pyqtSlot()
    def registerBtnHandler(self):
        self.sign_up_wind = SignUp()
        self.sign_up_wind.show()

    @QtCore.pyqtSlot()
    def loginBtnHandler(self):
        login = base64.b64encode(xxtea.encrypt(self.loginInput.text(), 'my_super_key'))
        password = base64.b64encode(xxtea.encrypt(self.passInput.text(), 'my_super_key'))
        if not login or not password:
            QtWidgets.QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля!')
            return
        with open('database.txt', 'rb') as f:
            data = f.read()
        if data is not None:
            rows = data.split(b'\n')
            accounts = [x.split() for x in rows]
            account_data = None
            for k in accounts:
                if len(k) == 3:
                    if k[0] == login:
                        account_data = k
            if account_data is not None:
                if account_data[1] == password:
                    self.close()
                    QtGameForm.run()
                else:
                    QtWidgets.QMessageBox.information(self, 'Внимание!', 'Неверный пароль')
            else:
                QtWidgets.QMessageBox.information(self, 'Внимание!', 'Пользователь не найден')
        else:
            QtWidgets.QMessageBox.information(self, 'Внимание!', 'Пользователь не найден')

    def registerBtns(self):
        self.signupBtn.clicked.connect(self.registerBtnHandler)
        self.loginBtn.clicked.connect(self.loginBtnHandler)