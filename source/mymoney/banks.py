import pandas as pd

def evaluate_month(df, month):
    mask = (df['AAAA-MM'] == month)
    df_month = df[mask]
    df_month = df_month[['Concepto', 'Débito', 'Crédito']]
    moves = df_month.groupby(by=['Concepto']).sum() 
    debit = moves['Débito'].sum() / 100.0
    credit = moves['Crédito'].sum() / 100.0
    moves = moves / 100.0
    return debit, credit, moves, df_month


def load_Patagonia(filename):
    df = pd.read_excel(filename, 
                       skiprows=4, 
                       skipfooter=1, 
                       usecols=[1, 2, 4, 6, 8]).fillna(value=0)
    df.columns = ['Fecha', 'Concepto', 'Débito', 'Crédito', 'Saldo']
    df['Concepto'] = df['Concepto'].str.replace('\n',' ')
    df['Débito'] = (df['Débito']*100).astype('int32')
    df['Crédito'] = (df['Crédito']*100).astype('int32')
    df['Saldo'] = (df['Saldo']*100).astype('int32')
    df['AAAA-MM'] = pd.to_datetime(df['Fecha']).apply(lambda x: f'{x.year:4d}-{x.month:02d}')
    df = df[['AAAA-MM', 'Concepto', 'Débito', 'Crédito', 'Saldo']]
    return df

def load_Chubut(filename):
    df = pd.read_excel(filename, skiprows=9, usecols=[1, 2, 3, 4]).fillna(0)
    df['Concepto'] = df['Movimientos'].str.replace('\n',' ')
    df['Importe'] = (df['Importe']*100).astype('int32')
    df['AAAA-MM'] = df['Fecha'].apply(lambda x: f'{str(x)[6:10]:s}-{str(x)[3:5]:s}')
    df['Débito'] = df['Importe'].apply(lambda x: 0 if x > 0 else -x)
    df['Crédito'] = df['Importe'].apply(lambda x: 0 if x < 0 else x)
    df['Saldo'] = df['Crédito'] - df['Débito']
    df = df[['AAAA-MM', 'Concepto', 'Débito', 'Crédito', 'Saldo']]
    return df

        
def get_totals(debit_patagonia, debit_chubut, credit_patagonia, credit_chubut):
    data = [[debit_patagonia, credit_patagonia, credit_patagonia - debit_patagonia],
            [debit_chubut, credit_chubut, credit_chubut - debit_chubut],
            [debit_patagonia + debit_chubut, credit_patagonia + credit_chubut, credit_patagonia + credit_chubut - debit_patagonia - debit_chubut]]
    
    df = pd.DataFrame(data, columns = ['Débito', 'Crédito', 'Saldo'], index=['Patagonia', 'Chubut', 'P+C'])
    return df

# References
# https://www.geeksforgeeks.org/different-ways-to-create-pandas-dataframe/
