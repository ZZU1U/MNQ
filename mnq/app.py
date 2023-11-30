# Libraries
import tempfile
import pandas as pd
import PyQt5
import PyQt5.QtCore
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QInputDialog,
                             QMessageBox, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QPixmap

# Modules
from utils import open_link
from config import GITHUB_PAGE, TELEGRAM_LINK
from plotting import get_plot
import calculating as calc
from exporting import export_pdf


# Popup windows

def table_warning(action: str) -> None:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Выберите таблицу")
    msg.setInformativeText(f"Что-бы {action} необходимо выбрать таблицу")
    msg.setWindowTitle("Не выбрана таблица")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def calculation_warning(action: str) -> None:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Постройте график")
    msg.setInformativeText(f"Сначала постройте график, что-бы {action}")
    msg.setWindowTitle("Не построен график")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def get_report_info(window: QMainWindow) -> None | tuple[str, str]:
    info, ok_pressed = QInputDialog.getText(window, "Введите информацию", "Нзвание работы, тема и т.д.")

    if not ok_pressed:
        info = ''

    name, ok_pressed = QInputDialog.getText(window, "Введите имя", "Как тебя зовут?")

    if not ok_pressed:
        name = ''

    return info, name


# Application class
class MNQ(QMainWindow):
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(865, 556)
        icon = QtGui.QIcon.fromTheme("application-menu")
        self.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(125, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(125, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.layoutWidget = QtWidgets.QWidget(self.frame_2)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 30, 111, 122))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.simple_butt = QtWidgets.QRadioButton(self.layoutWidget)
        self.simple_butt.setObjectName("simple_butt")
        self.verticalLayout.addWidget(self.simple_butt)
        self.mean_butt = QtWidgets.QRadioButton(self.layoutWidget)
        self.mean_butt.setObjectName("mean_butt")
        self.verticalLayout.addWidget(self.mean_butt)
        self.linreg_butt = QtWidgets.QRadioButton(self.layoutWidget)
        self.linreg_butt.setObjectName("linreg_butt")
        self.verticalLayout.addWidget(self.linreg_butt)
        self.calcul_butt = QtWidgets.QPushButton(self.layoutWidget)
        self.calcul_butt.setObjectName("calcul_butt")
        self.verticalLayout.addWidget(self.calcul_butt)
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(0, 10, 121, 19))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.frame_2)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.plot = QtWidgets.QLabel(self.frame)
        self.plot.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.plot.setText("")
        self.plot.setObjectName("plot")
        self.horizontalLayout_2.addWidget(self.plot)
        self.horizontalLayout.addWidget(self.frame)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 865, 22))
        self.menubar.setObjectName("menubar")
        self.menuExport = QtWidgets.QMenu(self.menubar)
        self.menuExport.setObjectName("menuExport")
        self.menuContact = QtWidgets.QMenu(self.menubar)
        self.menuContact.setObjectName("menuContact")
        self.menuImport = QtWidgets.QMenu(self.menubar)
        self.menuImport.setObjectName("menuImport")
        self.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)
        self.actionExcel_table = QtWidgets.QAction(self)
        self.actionExcel_table.setObjectName("actionExcel_table")
        self.actionCSV_table = QtWidgets.QAction(self)
        self.actionCSV_table.setObjectName("actionCSV_table")
        self.actionSave_plot = QtWidgets.QAction(self)
        self.actionSave_plot.setObjectName("actionSave_plot")
        self.actionSave_report = QtWidgets.QAction(self)
        self.actionSave_report.setObjectName("actionSave_report")
        self.actionGithub = QtWidgets.QAction(self)
        self.actionGithub.setObjectName("actionGithub")
        self.actionTelegram = QtWidgets.QAction(self)
        self.actionTelegram.setObjectName("actionTelegram")
        self.actionChoose_columns = QtWidgets.QAction(self)
        self.actionChoose_columns.setObjectName("actionChoose_columns")
        self.actionView_table = QtWidgets.QAction(self)
        self.actionView_table.setObjectName("actionView_table")
        self.menuExport.addAction(self.actionSave_plot)
        self.menuExport.addSeparator()
        self.menuExport.addAction(self.actionSave_report)
        self.menuExport.addSeparator()
        self.menuExport.addAction(self.actionView_table)
        self.menuContact.addAction(self.actionGithub)
        self.menuContact.addSeparator()
        self.menuContact.addAction(self.actionTelegram)
        self.menuImport.addAction(self.actionExcel_table)
        self.menuImport.addSeparator()
        self.menuImport.addAction(self.actionCSV_table)
        self.menuImport.addSeparator()
        self.menuImport.addAction(self.actionChoose_columns)
        self.menubar.addAction(self.menuImport.menuAction())
        self.menubar.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuContact.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MNQ"))
        self.simple_butt.setText(_translate("MainWindow", "y = ax"))
        self.mean_butt.setText(_translate("MainWindow", "y = a"))
        self.linreg_butt.setText(_translate("MainWindow", "y = ax + b"))
        self.calcul_butt.setText(_translate("MainWindow", "Посчитать"))
        self.label.setText(_translate("MainWindow", "Зависимость"))
        self.menuExport.setTitle(_translate("MainWindow", "Экспорт"))
        self.menuContact.setTitle(_translate("MainWindow", "Контакты"))
        self.menuImport.setTitle(_translate("MainWindow", "Импорт"))
        self.actionExcel_table.setText(_translate("MainWindow", "Excel"))
        self.actionCSV_table.setText(_translate("MainWindow", "CSV"))
        self.actionSave_plot.setText(_translate("MainWindow", "Сохранить график"))
        self.actionSave_report.setText(_translate("MainWindow", "Сохранить работу"))
        self.actionGithub.setText(_translate("MainWindow", "Github"))
        self.actionTelegram.setText(_translate("MainWindow", "Telegram"))
        self.actionChoose_columns.setText(_translate("MainWindow", "Выбрать столбцы"))
        self.actionView_table.setText(_translate("MainWindow", "Показать таблицу"))
        
    def __init__(self):
        super().__init__()

        # Init UI
        self.setupUi()

        # Fields
        self.data = None
        self.method = 0
        self.model = None
        self.is_calculated = False
        self.fig = None

        self.x_column = None
        self.y_column = None

        # Windows
        self.table = None

        # Contact
        self.actionGithub.triggered.connect(open_link(GITHUB_PAGE))
        self.actionTelegram.triggered.connect(open_link(TELEGRAM_LINK))

        # Import
        self.actionCSV_table.triggered.connect(self.load_csv)
        self.actionExcel_table.triggered.connect(self.load_excel)
        self.actionChoose_columns.triggered.connect(self.choose_columns)

        # Export
        self.actionView_table.triggered.connect(self.view_table)
        self.actionSave_plot.triggered.connect(self.save_plot)
        self.actionSave_report.triggered.connect(self.save_report)

        self.calcul_butt.pressed.connect(self.calculate)
        self.linreg_butt.toggled.connect(self.lrb)
        self.simple_butt.toggled.connect(self.srb)
        self.mean_butt.toggled.connect(self.mb)
        self.linreg_butt.setChecked(True)

        self.plot.installEventFilter(self)
        self.plot.setMinimumSize(1, 1)
        self.pixmap = QPixmap('plot.png')

    # https://stackoverflow.com/questions/43569167/pyqt5-resize-label-to-fill-the-whole-window
    def eventFilter(self, source, event):
        if source is self.plot and event.type() == PyQt5.QtCore.QEvent.Resize:
            self.plot.setPixmap(self.pixmap.scaled(
                self.plot.size(), PyQt5.QtCore.Qt.KeepAspectRatio,
                PyQt5.QtCore.Qt.SmoothTransformation))
        return super(MNQ, self).eventFilter(source, event)

    # Switchers
    def lrb(self):
        self.method = 3
        self.is_calculated = False

    def srb(self):
        self.method = 2
        self.is_calculated = False

    def mb(self):
        self.method = 1
        self.is_calculated = False

    # Import
    def load_csv(self):
        csv_file = QFileDialog.getOpenFileName(self, 'Открыть таблицу', '', "CSV(*.csv)")[0]

        if not csv_file:
            return

        self.data = pd.read_csv(csv_file)

        if not self.choose_columns():
            self.data = None

    def load_excel(self):
        excel_file = QFileDialog.getOpenFileName(self, 'Открыть таблицу', '', "Excel(*.xlsx)")[0]

        if not excel_file:
            return

        self.data = pd.read_excel(excel_file)

        if not self.choose_columns():
            self.data = None

    def choose_columns(self):
        if self.data is None:
            table_warning('выбрать таблицу')
            return

        self.is_calculated = False

        self.x_column, ok_pressed = QInputDialog.getItem(
            self, "Выберите столбец с зависимой переменной", "Какой столбец содержит зависимою переменную?",
            self.data.columns, 1, False)

        if not ok_pressed:
            return False

        self.y_column, ok_pressed = QInputDialog.getItem(
            self, "Выберите столбец с независимой переменной", "Какой столбец содержит независимою переменную?",
            set(self.data.columns) - {self.x_column}, 1, False)

        if not ok_pressed:
            return False

        return True

    # Export
    def view_table(self):
        if self.data is None:
            table_warning('посмотреть содержимое таблицы')
            return

        self.table = QTableWidget()
        self.table.setWindowTitle('Просмотр таблицы')
        self.table.resize(600, 600)
        self.table.setColumnCount(len(self.data.columns))
        self.table.setHorizontalHeaderLabels(self.data.columns)

        for i, row in self.data.iterrows():
            self.table.setRowCount(self.table.rowCount() + 1)

            for j in range(self.table.columnCount()):
                self.table.setItem(int(i), j, QTableWidgetItem(str(row.iloc[j])))

        self.table.resizeColumnsToContents()
        self.table.show()

    def save_report(self):
        # TODO fix reports

        if not self.is_calculated:
            calculation_warning('сохранить работу')
            return

        work, name = get_report_info(self)

        file_name, ok_pressed = QFileDialog.getSaveFileName(self, "Сохранить работу", "report.pdf", "PDF(*.pdf)")

        if not ok_pressed:
            return

        export_pdf(name, work, self.model, self.data, self.x_column, self.y_column, self.fig, file_name)

    def save_plot(self):
        if not self.is_calculated:
            calculation_warning('сохранить график')
            return

        file_name, ok_pressed = QFileDialog.getSaveFileName(self, "Сохранить график", "plot.png", "PNG(*.png);;JPEG(*.jpg)")

        if not ok_pressed:
            return

        self.fig.savefig(file_name, dpi=400, transparent=True)

    # Calculate plot
    def calculate(self):
        if self.data is None:
            table_warning('начать расчет')
            return

        x = self.data[self.x_column].to_numpy().reshape(-1, 1)
        y = self.data[self.y_column].to_numpy().reshape(-1, 1)

        match self.method:
            case 1:
                self.model = calc.MeanValue()
                self.model.train(x, y)
            case 2:
                self.model = calc.SimpleRegression()
                self.model.train(x, y)
            case 3:
                self.model = calc.LinearRegression()
                self.model.train(x, y)

        self.fig = get_plot(x, y, self.model, self.x_column, self.y_column)
        self.is_calculated = True

        self.statusBar.showMessage("Найденные коэфиценты: " + self.model.info())

        with tempfile.NamedTemporaryFile() as tmp:
            self.fig.savefig(tmp.name, format='png', transparent=True, dpi=300)

            self.pixmap = QPixmap(tmp.name)

            tmp.close()

        self.plot.setPixmap(self.pixmap.scaled(self.plot.size(), PyQt5.QtCore.Qt.KeepAspectRatio,
                                               PyQt5.QtCore.Qt.SmoothTransformation))

        self.plot.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.plot.show()
