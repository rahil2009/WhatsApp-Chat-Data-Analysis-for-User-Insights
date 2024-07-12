import app
from urlextract  import URLExtract 
extract=URLExtract() #making object

from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji


def fetch_stats(selected_user,df):

    if selected_user!="Overall":
        df=df[df["Username"]==selected_user]
    
    # word=[]
    # links=[]
    # for message in df['Message']:
    #     word.extend(message.split())
    #     links.extend(extract.find_urls(message))

    word = [w for message in df['Message'] for w in message.split()]
    links = [link for message in df['Message'] for link in extract.find_urls(message)]


    num_words=len(word)

    num_media = df[df["Message"].str.strip() == '<Media omitted>'].shape[0]

    return df.shape[0],num_words,num_media,len(links) 

def most_busy_users(df):
    x = df['Username'].value_counts().head()
    name_per = round((df['Username'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'Username':"Name/Contact","count":"Percentage"})
    return x,name_per

def create_Word_cloud(selected_user,df):
    f=open("stop_hinglish.txt",'r')
    stop_words=f.read()

    if selected_user!="Overall":
        df=df[df["Username"] == selected_user]
    
    #Cleaning dataframe
    clean_df=df[df["Message"]!=' <Media omitted>\n']
    clean_df=clean_df[clean_df["Username"]!='Group Notifications']
    clean_df=clean_df[clean_df["Message"].str.strip()!='This message was deleted']
    clean_df=clean_df[clean_df["Message"].str.strip()!='https']

    
    def remove_commas(message):
        words1=[]
        for word in message.lower().split():
            if word not in stop_words:
                words1.append(word)
        return " ".join(words1)


    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    clean_df["Message"]=clean_df['Message'].apply(remove_commas)
    df_wc= wc.generate(clean_df['Message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f=open("stop_hinglish.txt",'r')
    stop_words=f.read()

    if selected_user!="Overall":
        df=df[df["Username"] == selected_user]

    clean_df=df[df["Message"]!=' <Media omitted>\n']
    clean_df=clean_df[clean_df["Username"]!='Group Notifications']

    words=[]
    for message in clean_df['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    # most_common_words= pd.DataFrame(Counter(words).most_common(20)) (same....)
    # return most_common_words                                                  (...code works)
    
    return pd.DataFrame(Counter(words).most_common(20))

def most_emojis_used(selected_user,df):
    if selected_user!="Overall":
        df=df[df["Username"] == selected_user]

    emojis=[]
    for message in df["Message"]:
        for c in message:
            if c in emoji.EMOJI_DATA:
                emojis.extend(c)

    return pd.DataFrame(Counter(emojis).most_common(None), columns=['emoji', 'count'])
    
def message_graph_chart(selected_user,df):
    if selected_user!="Overall":
        df=df[df["Username"] == selected_user]

    timeline_df=df.groupby(['Year', 'Month','Month_num']).count()["Message"].reset_index()

    Timestamp=[]
    for i in range(timeline_df.shape[0]):
        Timestamp.append(timeline_df["Month"][i] + "-" + str(timeline_df["Year"][i]))

    timeline_df['Timestamp']=Timestamp
    timeline_df=timeline_df.sort_values(by=['Year', 'Month_num'])

    return timeline_df


def message_graph_chart_daily(selected_user,df):
    if selected_user!="Overall":
        df=df[df["Username"] == selected_user]

    daily_timeline_df=df.groupby(["Date"]).count()["Message"].reset_index()

    return daily_timeline_df
    
def week_activity_map(selected_user,df):
    if selected_user!="Overall":
        df=df[df["Username"] == selected_user]

    df["Day name"]=df["Date"].dt.day_name()
    return df["Day name"].value_counts()


def month_activity_map(selected_user,df):
    if selected_user!="Overall":
        df=df[df["Username"] == selected_user]

    return df["Month"].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user!="Overall":
        df=df[df["Username"] == selected_user]
    
    return df.pivot_table(index='Day',columns='Hour Range',values='Message',aggfunc='count').fillna(0)




    
# ================================ OLD CODE ===================================
    # if selected_user=='Overall':
        
    
    #     word=[]
    #     for message in df['Message']:
    #         word.extend(message.split())
    #     num_words=len(word)
    #     return df.shape[0],num_words
    

    # else:
    #     word=[]
    #     for message in  df[df["Username"]==selected_user]['Message']:

    #         word.extend(message.split())
    #     num_words=len(word)
    #     return df[df["Username"]==selected_user].shape[0],num_words