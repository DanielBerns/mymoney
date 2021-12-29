import sys
import json
from pathlib import Path

import streamlit as st

import banks as bk


def show_original_dataframe(df, bank_name):
    st.title('Reporte')
    st.header(bank_name)
    st.subheader('Planilla original')
    st.write(df.style.format(
        {'Débito': lambda x: f"{float(x/100.0):>10.2f}", 
         'Crédito': lambda x: f"{float(x/100.0):>10.2f}",
         'Saldo': lambda x: f"{float(x/100.0):>10.2f}"}))

def show_month_dataframe(df, bank_name, month):
    debit, credit, moves, df_month = bk.evaluate_month(df, month)
    st.subheader('Movimientos por mes')
    st.write(df_month.style.format({'Débito': lambda x: f"{(x/100.0):>10.2f}", 'Crédito': lambda x: f"{(x/100.0):>10.2f}"}))
    st.subheader('Movimientos por lugar')
    st.write(moves.style.format({'Débito': lambda x: f"{float(x):>10.2f}", 'Crédito': lambda x: f"{float(x):>10.2f}"}))
    return debit, credit
             
config = None
try:
    config_file = open(sys.argv[1], 'r')
    config = json.load(config_file)
except Exception as message:
    print(str(message))
    sys.exit(1)

df_patagonia = bk.load_Patagonia(str(Path('~', config['patagonia']).expanduser()))
show_original_dataframe(df_patagonia, 'Banco Patagonia')
debit_patagonia, credit_patagonia = show_month_dataframe(df_patagonia, 'Banco Patagonia', config['month-patagonia'])

df_chubut = bk.load_Chubut(str(Path('~', config['chubut']).expanduser()))
show_original_dataframe(df_chubut, 'Banco Chubut')
debit_chubut, credit_chubut = show_month_dataframe(df_chubut, 'Banco Chubut', config['month-chubut'])



 
st.header('Totales')

totals = bk.get_totals(debit_patagonia, debit_chubut, credit_patagonia, credit_chubut)
st.write(totals.style.format(
    {'Débito': lambda x: f"{float(x):>10.2f}", 
     'Crédito': lambda x: f"{float(x):>10.2f}", 
     'Saldo': lambda x: f"{float(x):>10.2f}"}))
