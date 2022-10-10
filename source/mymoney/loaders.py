import pandas as pd


def load_Patagonia(filename):
    df = pd.read_excel(filename, 
                       skiprows=4, 
                       skipfooter=1, 
                       usecols=[1, 2, 4, 6, 8]).fillna(value=0)
    df.columns = ['Fecha', 'Concepto', 'Débito', 'Crédito', 'Saldo']
    df['Concepto'] = df['Concepto'].str.replace('\n',' ')
    df['Crédito'] = (df['Crédito']*100).astype('int32')
    df['Débito'] = (df['Débito']*100).astype('int32')
    df['Saldo'] = (df['Saldo']*100).astype('int32')
    df['AAAA-MM'] = pd.to_datetime(df['Fecha']).apply(lambda x: f'{x.year:4d}-{x.month:02d}')
    return df[['AAAA-MM', 'Concepto', 'Crédito', 'Débito', 'Saldo']]


def load_Chubut(filename):
    df = pd.read_excel(filename, skiprows=9, usecols=[1, 2, 3, 4]).fillna(0)
    df['Concepto'] = df['Movimientos'].str.replace('\n',' ')
    df['Importe'] = (df['Importe']*100).astype('int32')
    df['AAAA-MM'] = df['Fecha'].apply(lambda x: f'{str(x)[6:10]:s}-{str(x)[3:5]:s}')
    df['Crédito'] = df['Importe'].apply(lambda x: 0 if x < 0 else x)
    df['Débito'] = df['Importe'].apply(lambda x: 0 if x > 0 else -x)
    df['Saldo'] = df['Crédito'] - df['Débito']
    return df[['AAAA-MM', 'Concepto', 'Crédito', 'Débito', 'Saldo']] 
