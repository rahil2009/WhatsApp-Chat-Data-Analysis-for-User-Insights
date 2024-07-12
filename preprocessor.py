import re
import pandas as pd

def preprocess(data):
    pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[ap]m\s-\s'

    dates=re.findall(pattern,data)

    messages=re.split(pattern,data)[1:]

    df=pd.DataFrame({'Date':dates,'User_messages':messages})

    df["Date"] =pd.to_datetime(df["Date"],format='%d/%m/%Y, %H:%M %p - ')

    df['Username'] = df['User_messages'].apply(lambda x: x.split(':')[0] if ':' in x else 'Group Notifications')
    df['Message'] = df['User_messages'].apply(lambda x: x.split(':')[1] if ':' in x else df['User_messages'][1])

    df.drop(['User_messages'], axis=1, inplace=True)

    df['Year']=df['Date'].dt.year
    df['Month']=df['Date'].dt.month_name()
    df['Month_num']=df['Date'].dt.month
    df['Day']=df['Date'].dt.day_name()
    df['Hour']=df['Date'].dt.hour
    df['Minute']=df['Date'].dt.minute

    df["Next Hour"] = df['Hour'] + 1
    df["Hour Range"] = df["Hour"].astype(str) + "-" + df["Next Hour"].astype(str)


    return df