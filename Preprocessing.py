import streamlit as st
import re
import pandas as pd 

def prepocessing(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}'
    messages_original= re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({'user_names':messages_original,'message_date':dates})
    # converting date time formate 
    # df['message_date']=pd.to_datetime(df['message_date'],format="%m/%d/%y, %H:%M")
    df['message_date'] = pd.to_datetime(df['message_date'], format='mixed')
    df.rename(columns={'message_date':'Date'},inplace=True)
    user = []
    messages=[]
    
    
    for message in df['user_names']:
        entry =re.split('([\w\W]+?):\s',message)
        if entry[1:]:#user name
            user.append(entry[1])
            messages.append(entry[2])
        else:
            user.append('group_message')
            messages.append(entry[0])    
    
    df['user']=user
    df['messages']=messages
    df2=df.drop(columns=['user_names'],axis=1)
    df2['hours']=df2['Date'].dt.hour
    df2['min']=df2['Date'].dt.minute
    df2['Day']=df2['Date'].dt.day
    # df2=df2[['Date','months','Day','hours','min','user','messages']]    
    df2['month']=df2['Date'].dt.month
    df2['name_month']=df2['Date'].dt.month_name()
    
    return df2