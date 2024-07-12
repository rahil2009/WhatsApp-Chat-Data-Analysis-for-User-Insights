import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import keyboard
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    # st.text(data)
    df=preprocessor.preprocess(data)

    # st.dataframe(df)

    #fetch by unique users
    user_list=df['Username'].unique().tolist()
    user_list.sort()
    # user_list.remove('Group Notifications')
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox('Show analysis with respect to',user_list)

    #Implementing Analysis
    if st.sidebar.button("Show Analysis"):

        number_messages,num_words,num_media,links=helper.fetch_stats(selected_user,df)

        # Add a description
        st.write("""
                 <span style="font-family: Arial, sans-serif; font-size: 20px;">
                 <strong>
                 We conducted an extensive analysis of WhatsApp chat data, revealing crucial trends and patterns. 
                 These insights deepened our understanding of user behavior, allowing us to tailor strategies and services to better meet their needs.
                  By employing diverse data analysis methodologies and tools, we enhanced our ability to interpret and understand data.
                  Ultimately, this informed decision-making and improved strategic planning.
                 </strong>
                 </span>
        """, unsafe_allow_html=True)
        st.title("Top Statistics")

        col1,col2,col3,col4= st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(number_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Media Shared")
            st.title(num_media)

        with col4:
            st.header("Link Shared") 
            st.title(links)
    # key = st.keypress()
    # if key == "k":
    #     st.sidebar.button("Button clicked!")
    
    key = keyboard.read_event()
    if key.name == "k":
        st.sidebar.button("Button clicked!")

        # finding busiest users (group level)
        if selected_user=='Overall':
            st.title("Most Busy Users")
            x ,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()


            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color="green")
                ax.set_xticklabels(x.index, rotation=45) 
                #plt.xticks(rotation=45) #same code
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


        #Message Graph chart
        st.title("Monthly Timeline")
        timeline_df = helper.message_graph_chart(selected_user,df)
        
        
        fig , ax = plt.subplots()
        ax.plot(timeline_df["Timestamp"],timeline_df["Message"])
        plt.xticks(rotation=90)
        # ax.plot(timeline["Timestamp"],timeline["Message"])
        st.pyplot(fig)

        #Message Graph chart Daily
        st.title("Daily Timeline")
        timeline_df_daily = helper.message_graph_chart_daily(selected_user,df)

        fig , ax = plt.subplots()
        ax.plot(timeline_df_daily["Date"],timeline_df_daily["Message"],color="black")
        plt.xticks(rotation=90)
        st.pyplot(fig)

        #Weekly Activity
        st.title("Activity Map")
        col1 , col2 = st.columns(2)

        with col1:
            st.title("Weekly Activity Map")
            week_activity = helper.week_activity_map(selected_user,df)
            fig , ax = plt.subplots()
            ax.bar(week_activity.index,week_activity.values)
            plt.xticks(rotation=90)
            st.pyplot(fig)

        #Monthly Activity
        with col2:
            st.title("Monthly Activity Map")
            month_activity = helper.month_activity_map(selected_user,df)
            fig , ax = plt.subplots()
            ax.bar(month_activity.index,month_activity.values,color='green')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        #Activity heatmap
        activity_hmap = helper.activity_heatmap(selected_user,df)
        st.title("Acitvity Heatmap")
        fig , ax = plt.subplots(figsize=(10,6))
        ax = sns.heatmap(activity_hmap)
        plt.xticks(rotation=0)
        st.pyplot(fig)


        
        # WORDCLOUD
        df_wc = helper.create_Word_cloud(selected_user,df)
        fig , ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most Common words
        # # st.dataframe(helper.most_common_words(selected_user,df))   (same code works)

        # words = helper.most_common_words(selected_user,df)
        # st.dataframe(words)           
        # ---------> Above code suits for dataframe but we will use bar plot --------<

        words = helper.most_common_words(selected_user,df)
        fig , ax = plt.subplots()
        ax.barh(words[0],words[1])
        plt.xticks(rotation =  90)
        st.title("Most Common Words")
        st.pyplot(fig)

        #Most Emojis used
        most_emojis = helper.most_emojis_used(selected_user,df)
        st.title("Most Emojis Used")

        col1,col2,col3 = st.columns(3)

        with col1:
            st.dataframe(most_emojis)      
        
        with col2:
            fig , ax = plt.subplots()
            ax.pie(most_emojis["count"].head(),labels=most_emojis["emoji"].head(),autopct='%0.2f')
            st.pyplot(fig)

        with col3:
            fig , ax = plt.subplots(figsize=(10, 10.3))
            ax.bar(most_emojis["emoji"].head(),most_emojis["count"].head())
            st.pyplot(fig)

        

       
       
       
       
        # while not keyboard.is_pressed('k'):
        #     pass

        # st.sidebar.button("Button clicked!")

        # key = keyboard.read_event()
        # if key.name == "k":
        #     st.sidebar.button("Button clicked!")