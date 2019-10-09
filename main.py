import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from db.db import MySQLDB


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.file_name = None
        self.initUI(self)

    def initUI(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(640, 480)
        self.setWindowTitle('WishList')
        self.setWindowIcon(QtGui.QIcon('img/list.png'))

        self.mysql = MySQLDB('wish_list_db')
        self.connect_db()

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.resize(480, 480)

        btn_add = QtWidgets.QPushButton('Добавить элемент', self)
        btn_add.move(490, 10)
        btn_add.resize(140, 33)
        btn_add.clicked.connect(self.add_item)

        vbox = QtWidgets.QVBoxLayout(self.centralWidget)
        self.TableWidget = QtWidgets.QTableWidget()
        self.TableWidget.setMinimumSize(QtCore.QSize(240, 460))
        vbox.addWidget(self.TableWidget)
        self.TableWidget.setColumnCount(4)
        self.TableWidget.setHorizontalHeaderLabels(('', 'name', 'price', 'link'))
        self.TableWidget.horizontalHeader().setStretchLastSection(True)
        self.TableWidget.setColumnWidth(0, 10)
        self.TableWidget.setColumnWidth(1, 120)

        style = """
        QTableWidget::item {background-color: white;
        border-style: outset}
        
        QHeaderView::section{Background-color: rgb(230,230,230)}
        
        QTableWidget::item:selected {border-width: 1px; color: black ; border-color: green}
        """

        self.setStyleSheet(style)
        self.update_table()

    def connect_db(self):
        """Подключение к базе данных."""
        self.mysql.connect()
        self.mysql.create_db()
        self.mysql.create_table()

    def add_item(self):
        """Добавить элемент в таблицу wish list."""
        dialog = Dialog(self)
        if dialog.exec_():
            self.mysql.add_item(dialog.name.text(),
                                dialog.price.text(),
                                dialog.link.text())
            items = self.mysql.get_items()
            self.TableWidget.setRowCount(len(items))
            btn = QtWidgets.QPushButton(QtGui.QIcon('img/del.png'), '', self)
            btn.clicked.connect(self.delete_item)
            self.TableWidget.setCellWidget(len(items)-1, 0, btn)
            for i, line in enumerate(items[-1][1:]):
                widget_item = QtWidgets.QTableWidgetItem(line)
                self.TableWidget.setItem(len(items)-1, i+1, widget_item)

    def delete_item(self):
        """Удалить выбрынный элемент из таблицы wish list"""
        index_row = self.TableWidget.currentRow()
        items = self.mysql.get_items()
        id = items[index_row][0]
        self.mysql.delete_item(id)
        self.TableWidget.removeRow(self.TableWidget.currentRow())

    def update_table(self):
        """Обновить таблицу wish list"""
        items = self.mysql.get_items()
        for i in range(len(items)):
            self.TableWidget.setRowCount(len(items))
            btn = QtWidgets.QPushButton(QtGui.QIcon('img/del.png'), '', self)
            btn.clicked.connect(self.delete_item)
            self.TableWidget.setCellWidget(i, 0, btn)
            for j, line in enumerate(items[i][1:]):
                widget_item = QtWidgets.QTableWidgetItem(str(line))
                self.TableWidget.setItem(i, j+1, widget_item)


class Dialog(QtWidgets.QDialog):
    """Диалоговое окно с полями: название, цена, ссылка"""
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)

        self.name = QtWidgets.QLineEdit(self)
        self.name.move(0, 0)
        self.name.resize(250, 33)
        self.name.setPlaceholderText("Введите название товара")

        self.price = QtWidgets.QLineEdit(self)
        self.price.move(0, 45)
        self.price.resize(250, 33)
        self.price.setPlaceholderText("Введите цену товара")

        self.link = QtWidgets.QLineEdit(self)
        self.link.move(0, 90)
        self.link.resize(250, 33)
        self.link.setPlaceholderText("Введите ссылку на страницу с покупкой")

        btn_ok = QtWidgets.QPushButton('ok', self)
        btn_ok.move(250 - 90, 150)
        btn_ok.resize(90, 33)
        btn_ok.clicked.connect(self.btn_ok)

        btn_cancel = QtWidgets.QPushButton('cancel', self)
        btn_cancel.move(0, 150)
        btn_cancel.resize(90, 33)
        btn_cancel.clicked.connect(self.btn_cancel)

    def btn_cancel(self):
        self.close()

    def btn_ok(self):
        self.accept()


def main_application():
    """
    function to initialize and display the main application window
    """
    app = QApplication(sys.argv)
    app.setStyle('cleanlooks')
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main_application()
