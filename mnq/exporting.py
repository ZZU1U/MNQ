# coding: utf8
from fpdf import FPDF
import pandas as pd
import tempfile
from matplotlib.pyplot import Figure
from sklearn.metrics import mean_absolute_error as acc
from calculating import *


def export_pdf(student: str, info: str, model: LinearRegression | SimpleRegression | MeanValue, data: pd.DataFrame,
               x_label: str, y_label: str, fig: Figure, filename: str) -> None:
    # Init
    pdf = FPDF()

    # Fonts with russian lang
    pdf.add_page()

    # Info
    try:
        pdf.add_font('Helvetic', '', './mnq/times.ttf', True)
    except:
        pass

    try:
        pdf.add_font('Helvetic', '', './times.ttf', True)
    except:
        pass
    
    pdf.set_font('Helvetic', '', 24)
    pdf.cell(40, 10, info, ln=1)

    pdf.set_font('Helvetic', '', 20)
    pdf.cell(40, 10, student, ln=1)

    pdf.set_font('Helvetic', '', 14)
    pdf.cell(40, 10, 'Полученные результаты:', ln=1)
    pdf.cell(40, 10, f'Вид зависимости {model.name(x_label, y_label)}', ln=1)
    pdf.cell(40, 10, f'Найденные коэфиценты {model.info()}', ln=1)
    y = data[y_label].to_numpy().reshape(-1, 1)
    x = data[x_label].to_numpy().reshape(-1, 1)
    pdf.cell(40, 10, f'Среднее отклонение {acc(y, model.predict(x))}', ln=1)
    pdf.cell(40, 10, f'Кореляция величин: \
    {np.corrcoef(data[x_label].to_numpy(), data[y_label].to_numpy())[0][1]}', ln=1)

    with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
        fig.savefig(tmp.name, format='png', transparent=True, dpi=300)
        pdf.image(tmp.name, w=200)
        tmp.close()

    # Saving
    pdf.output(filename)


if __name__ == "__main__":
    export_pdf('', '', MeanValue(), pd.DataFrame(), '', '',  Figure(), 'report.pdf')
