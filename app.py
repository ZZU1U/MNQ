import sys
import pandas as pd
import PyQt5.QtCore
from utils import open_link
from config import GITHUB_PAGE, TELEGRAM_LINK
from plotting import make_plot
import calculating as calc

from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QInputDialog,
                             QMessageBox, QTableWidget, QTableWidgetItem, QGridLayout,
                             QHeaderView, QWidget, QHBoxLayout)
from PyQt5.QtGui import QPixmap


def show_table_viewer(df: pd.DataFrame):
    table = QTableWidget()
    table.setWindowTitle('View table')
    table.resize(600, 600)
    table.setColumnCount(len(df.columns))
    table.setHorizontalHeaderLabels(df.columns)

    for i, row in df.iterrows():
        table.setRowCount(table.rowCount() + 1)

        for j in range(table.columnCount()):
            table.setItem(i, j, QTableWidgetItem(str(row.iloc[j])))

    table.resizeColumnsToContents()
    table.show()


def table_warning():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Выберите таблицу")
    msg.setInformativeText("Что-бы выбрать столбцы необходимо выбрать таблицу")
    msg.setWindowTitle("Не выбрана таблица")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def calculation_warning():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Постройте график")
    msg.setInformativeText("Сначала постройте график, что-бы проверить его правильность")
    msg.setWindowTitle("Не построен график")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


class MNQ(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('app.ui', self)
        self.data = None
        self.method = 0
        self.is_calculated = False;

        self.x_column = None
        self.y_column = None

        self.actionGithub.triggered.connect(open_link(GITHUB_PAGE))
        self.actionTelegram.triggered.connect(open_link(TELEGRAM_LINK))

        self.actionCSV_table.triggered.connect(self.load_csv)
        self.actionExcel_table.triggered.connect(self.load_excel)
        self.actionChoose_columns.triggered.connect(self.choose_columns)
        self.actionView_table.triggered.connect(self.view_table)

        self.calcul_butt.pressed.connect(self.calculate)
        self.linreg_butt.toggled.connect(self.lrb)
        self.simple_butt.toggled.connect(self.srb)
        self.mean_butt.toggled.connect(self.mb)
        self.linreg_butt.setChecked(True)

    def lrb(self):
        self.method = 3
        self.is_calculated = False

    def srb(self):
        self.method = 2
        self.is_calculated = False

    def mb(self):
        self.method = 1
        self.is_calculated = False

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
            table_warning()
            return

        self.is_calculated = False;

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

    def view_table(self):
        if self.data is None:
            table_warning()
            return

        show_table_viewer(self.data)

    def calculate(self):
        if self.data is None:
            table_warning()
            return

        x = self.data[self.x_column].to_numpy().reshape(-1, 1)
        y = self.data[self.y_column].to_numpy().reshape(-1, 1)

        model = None

        match self.method:
            case 1:
                model = calc.MeanValue()
                model.train(x, y)
            case 2:
                model = calc.SimpleRegression()
                model.train(x, y)
            case 3:
                model = calc.LinearRegression()
                model.train(x, y)

        if model is None:
            assert Exception('No model were chosen')

        make_plot(x, y, model)

        self.statusBar.showMessage("Найденные коэфиценты: " + model.info())

        self.plot.setPixmap(QPixmap("plot.png"))

        self.plot.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.plot.show()

    def save_to_html(self):
        if not self.is_calculated:
            calculation_warning()
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MNQ()
    win.show()
    sys.exit(app.exec_())
