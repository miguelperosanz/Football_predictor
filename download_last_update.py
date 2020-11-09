import time, threading
import pandas as pd
import requests
from itertools import chain   
import requests
import numpy as np


WAIT_SECONDS = 172800

def scrap_last_update():
    


    l= []   
    
    for i in range(0,661,60):
        
       
        name = 'https://sofifa.com/teams?type=club&showCol%5B0%5D=ti&showCol%5B1%5D=oa&showCol%5B2%5D=at&showCol%5B3%5D=md&showCol%5B4%5D=df&showCol%5B5%5D=tb&showCol%5B6%5D=bs&showCol%5B7%5D=bd&showCol%5B8%5D=bp&showCol%5B9%5D=bps&showCol%5B10%5D=cc&showCol%5B11%5D=cp&showCol%5B12%5D=cs&showCol%5B13%5D=cps&showCol%5B14%5D=da&showCol%5B15%5D=dm&showCol%5B16%5D=dw&showCol%5B17%5D=dd&showCol%5B18%5D=dp&showCol%5B19%5D=ip&showCol%5B20%5D=ps&showCol%5B21%5D=sa&offset=' + '%02d' % i 


        r1 = requests.get(name)
        

        l.append(pd.read_html(r1.content))
  
        
    df= pd.concat(chain.from_iterable(l))
    
    df = df.drop(['Unnamed: 0'], axis=1)

    df['Transfer Budget']=df['Transfer Budget'].str.replace('€',"")
    df['Transfer Budget']=df['Transfer Budget'].str.replace('.',"")
    df['Transfer Budget']=df['Transfer Budget'].str.replace('M',"000000")
    df['Transfer Budget']=df['Transfer Budget'].str.replace('K',"000")
    df['Speed'] = df['Speed'].replace({'Slow' : '0', 'Fast' : '1', 'Balanced' : '2' })
    df['Dribbling'] = df['Dribbling'].replace({'Little' : '0', 'Normal' : '1', 'Lots' : '2' })
    df['Passing'] = df['Passing'].replace({'Short' : '0', 'Long' : '1', 'Mixed' : '2' })
    df['Positioning'] = df['Positioning'].replace({'Organised' : '0', 'Free Form' : '1'})
    df['Crossing'] = df['Crossing'].replace({'Little' : '0', 'Normal' : '1', 'Lots' : '2' })
    df['Passing.1'] = df['Passing.1'].replace({'Safe' : '0', 'Risky' : '1', 'Normal' : '2' })
    df['Shooting'] = df['Shooting'].replace({'Little' : '0', 'Lots' : '1', 'Normal' : '2' })
    df['Positioning.1'] = df['Positioning.1'].replace({'Organised' : '0', 'Free Form' : '1'})
    df['Aggression'] = df['Aggression'].replace({'Contain' : '0', 'Press' : '1', 'Double' : '2' })
    df['Pressure'] = df['Pressure'].replace({'Deep' : '0', 'High' : '1', 'Medium' : '2' })
    df['Team Width'] = df['Team Width'].replace({'Narrow' : '0', 'Normal' : '1', 'Wide' : '2' })
    df['Defender Line'] = df['Defender Line'].replace({'Cover' : '0', 'Offside Trap' : '1' })


    df['Transfer Budget'] = df['Transfer Budget'].astype(float)

    df['Transfer Budget'] = df['Transfer Budget']/1000000

    df = df.rename(columns={'Transfer Budget': "Transfer Budget(M€)"})

    df.to_csv('list_last_update.csv', index=False) 
    
    threading.Timer(WAIT_SECONDS, scrap_last_update).start()
    
    
scrap_last_update()

