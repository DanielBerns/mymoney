import sys
import json
from pathlib import Path

import banks as bk

config = bk.load_config(sys.argv[1])

if config:
    df_patagonia = loaders.load_Patagonia(str(Path('~', config['patagonia']).expanduser()))
    credit_patagonia, debit_patagonia, moves_patagonia, month_patagonia = bk.evaluate_month(df_patagonia, config['month-patagonia'])
    
    df_chubut = loaders.load_Chubut(str(Path('~', config['chubut']).expanduser()))
    
    credit_chubut, debit_chubut, moves_patagonia = bk.evaluate_month(df_chubut, config['month-chubut'])
    
    show_month_dataframe(df_chubut, 'Banco Chubut', config['month-chubut'])

    totals = bk.get_totals(credit_patagonia, debit_patagonia, credit_chubut, debit_chubut)
        
    patagonia = pd.concat([credit_patagonia, debit_patagonia])
    patagonia.to_excel('patagonia.xlsx')
    
    chubut = pd.concat([credit_chubut, debit_chubut])
    chubut.to_excel('chubut.xslx')
    
    
    
else:
    print('Error: no config')
