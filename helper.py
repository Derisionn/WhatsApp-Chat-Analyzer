import App
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
extract=URLExtract()


def fetch_stats(selected_user,df):
    
    if selected_user!='OverAll':
        df=df[df['user']==selected_user]
    word=[]
    #number of messages
    num_msg=df.shape[0]
    #number of messages 
    num_media=df[df['messages']=='<Media omitted>\n'].shape[0]
    
    for msg in df['messages']:
        word.extend(msg.split())
      

    #to extreact the links 
    links =[]
    for msg in df['messages']:
        links.extend(extract.find_urls(msg))
    
        
    return num_msg,len(word),num_media,len(links)  
    
def most_busy_user(df):
    x=df['user'].value_counts().head()
    newdf=round((df['user'].value_counts()/df.shape[0])*100,2).head().reset_index().rename(columns={'count':'%'})
    return x,newdf 

def wordCloud(df,selected_user):
    if selected_user!='OverAll':
        df=df[df['user']==selected_user]
    
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white') 
    newdf45=df[df['messages']!='<Media omitted>\n']
    newdf45=newdf45[newdf45['messages']!='This message was deleted\n']
    return wc.generate(newdf45['messages'].str.cat(sep=""))      
                

def mostCommon_word(df,selected_user):
    
    f=open('stop_hinglish.txt','r')
    stop_hinglish=f.read()
    if selected_user!='OverAll':
        df=df[df['user']==selected_user]
        
    newdf45=df[df['messages']!='<Media omitted>\n']
    newdf45=newdf45[newdf45['user']!='group_message']
    newdf45=newdf45[newdf45['messages']!='This message was deleted\n']
    
    word56=[]
    for message in newdf45['messages']:
        for word in message.lower().split():
            if word not in stop_hinglish:
                word56.append(word)
    return pd.DataFrame(Counter(word56).most_common(20))
    
    
# monthly timeline 
def monthlyTime(df,selected_user):
    if selected_user!='OverAll':
        df=df[df['user']==selected_user] 
        
    df['num_month']=df['Date'].dt.month
    df['name_month']=df['Date'].dt.month_name()
    df['Year']=df['Date'].dt.year  
    timeline =df.groupby(['Year','num_month','name_month']).count()['messages'].reset_index()    
    random34=[]
    for i in range(timeline.shape[0]):
        random34.append(str(timeline['Year'][i])+" "+timeline['name_month'][i])
    timeline['month_year']=pd.DataFrame(random34)
    
    return timeline
    
def busy_day(df,selected_user):
    if selected_user!= 'OverAll':
        df=df[df['user']==selected_user]
    
    df['day']=df['Date'].dt.day_name()
    day_only=df['day'].value_counts().reset_index()    
        
    return day_only


def busyMonth(df,selected_user):
    if selected_user!= 'OverAll':
        df=df[df['user']==selected_user]
    
    months_only=df['name_month'].value_counts().reset_index()    
        
    return months_only
    
    
    
    
    
    # if selected_user=='OverAll':
    #     word=[]

    #     for msg in df['messages']:
    #         word.extend(msg.split())
    #     return df.shape[0],len(word)
    # else:
    #     word=[]
    #     num=df[df['user']==selected_user].shape[0]
    #     for msg in df['messages'][df['user']==selected_user]:
    #         word.extend(msg.split())
            
    #     return num,len(word)
    
    
    