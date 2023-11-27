# Libraries
import sys
import pandas as pd
import PyQt5
import PyQt5.QtCore
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QInputDialog,
                             QMessageBox, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QPixmap

# Modules
from utils import open_link
from config import GITHUB_PAGE, TELEGRAM_LINK
from plotting import make_plot
import calculating as calc
from exporting import export_pdf


# Popup windows
def show_table_viewer(df: pd.DataFrame) -> None:
    table = QTableWidget()
    table.setWindowTitle('View table')
    table.resize(600, 600)
    table.setColumnCount(len(df.columns))
    table.setHorizontalHeaderLabels(df.columns)

    for i, row in df.iterrows():
        table.setRowCount(table.rowCount() + 1)

        for j in range(table.columnCount()):
            table.setItem(int(i), j, QTableWidgetItem(str(row.iloc[j])))

    table.resizeColumnsToContents()
    table.show()


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
    def __init__(self):
        super().__init__()
        uic.loadUi('app.ui', self)
        # Fields
        self.data = None
        self.method = 0
        self.model = None
        self.is_calculated = False

        self.x_column = None
        self.y_column = None

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
        csv_file = QFileDialog.getOpenFileName(self, 'Open file', '', "CSV table (*.csv)")[0]

        if not csv_file:
            return

        self.data = pd.read_csv(csv_file)

        if not self.choose_columns():
            self.data = None

    def load_excel(self):
        excel_file = QFileDialog.getOpenFileName(self, 'Open file', '', "Excel table (*.xlsx)")[0]

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

        show_table_viewer(self.data)

    def save_report(self):
        if not self.is_calculated:
            calculation_warning('сохранить работу')
            return

        work, name = get_report_info(self)

        file_name, ok_pressed = QFileDialog.getSaveFileName(self, "Save File", "report.pdf", "PDF(*.pdf)")

        if not ok_pressed:
            return

        export_pdf(name, work, self.model, self.data, self.x_column, self.y_column, file_name)

    def save_plot(self):
        if not self.is_calculated:
            calculation_warning('сохранить график')
            return

        file_name, ok_pressed = QFileDialog.getSaveFileName(self, "Save File", "plot.png", "PNG(*.png);;JPEG(*.jpg)")

        if not ok_pressed:
            return

        x = self.data[self.x_column].to_numpy().reshape(-1, 1)
        y = self.data[self.y_column].to_numpy().reshape(-1, 1)
        make_plot(x, y, self.model, self.x_column, self.y_column, file_name)

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

        if self.model is None:
            assert Exception('No model were chosen')

        make_plot(x, y, self.model, self.x_column, self.y_column)
        self.is_calculated = True

        self.statusBar.showMessage("Найденные коэфиценты: " + self.model.info())

        self.pixmap = QPixmap("plot.png")
        self.plot.setPixmap(self.pixmap.scaled(self.plot.size()))

        self.plot.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.plot.show()


# Launch
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MNQ()
    win.show()
    win.data = pd.read_csv('example.csv')
    win.x_column = 'X'
    win.y_column = 'Y'
    sys.exit(app.exec_())
