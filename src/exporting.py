from fpdf import FPDF
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score as acc
from calculating import *


def export_pdf(student: str, info: str, model: LinearRegression | SimpleRegression | MeanValue, data: pd.DataFrame,
               x_label: str, y_label: str, filename: str) -> None:
    # Init
    pdf = FPDF()

    # Fonts with russian lang
    pdf.add_page()
    pdf.add_font('times', '', './assets/times/times.ttf', uni=True)
    pdf.add_font('times', 'B', './assets/times/times-bold.ttf', uni=True)
    pdf.add_font('times', 'I', './assets/times/times-italic.ttf', uni=True)

    # Info
    pdf.set_font('times', '', 24)
    pdf.cell(40, 10, info, ln=1)

    pdf.set_font('times', '', 20)
    pdf.cell(40, 10, student, ln=1)

    pdf.set_font('times', '', 14)
    pdf.cell(40, 10, 'Полученные результаты:', ln=1)
    pdf.cell(40, 10, f'Вид зависимости {model.name}', ln=1)
    pdf.cell(40, 10, f'Коэфиценты {model.info()}', ln=1)
    y = data[y_label].to_numpy().reshape(-1, 1)
    x = data[x_label].to_numpy().reshape(-1, 1)
    pdf.cell(40, 10, f'Среднее отклонение {acc(y, model.predict(x))}', ln=1)

    pdf.image('plot.png', w=200)

    # Saving
    pdf.output(filename)
