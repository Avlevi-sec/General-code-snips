import pandas as pd
a=1
while a<13:
    str = f'=SUMIFS(expense!D2:D,expense!E2:E,">="&DATE(2022,{a},1),expense!E2:E,"<="&DATE(2022,{a},31))'
    print(str)
    a= a+1
