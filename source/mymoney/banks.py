import pandas as pd

def load_config(filename):             
    config = None
    try:
        config_file = open(filename, 'r')
        config = json.load(config_file)
    except Exception as message:
        print(str(message))
    return config 


def evaluate_month(df, month):
    mask = (df['AAAA-MM'] == month)
    df_month = df[mask]
    df_month = df_month[['Concepto', 'Débito', 'Crédito']]
    moves = df_month.groupby(by=['Concepto']).sum() 
    debit = moves['Débito'].sum() / 100.0
    credit = moves['Crédito'].sum() / 100.0
    moves = moves / 100.0
    return credit, debit, moves, df_month


def get_totals_by_bank(credit, debit):
    data = [credit, debit, credit - debit]
    df = pd.DataFrame(data, columns = ['Crédito', 'Débito', 'Saldo'])
    return df

        
def get_totals(info):
    rows = []
    index = []
    credit_total, debit_total, balance_total = 0
    for credit, debit, balance, key in info:
        rows.append((credit, debit, balance))
        index.append(key)
        credit_total += credit
        debit_total += debit
        balance_total += balance
    rows.append((credit_total, debit_total, balance_total))
    index.append('total')
    
    df = pd.DataFrame(rows, columns = ['Crédito', 'Débito', 'Saldo'], index=index)
    return df

# References
# https://www.geeksforgeeks.org/different-ways-to-create-pandas-dataframe/
