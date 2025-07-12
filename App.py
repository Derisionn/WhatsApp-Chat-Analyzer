import streamlit as st 
import Preprocessing,helper
import matplotlib.pyplot as plt 

st.set_page_config(layout="wide")
st.sidebar.title('WhatsApp Analysier')

uploaded_file = st.sidebar.file_uploader("Choose a file",key="file_uploader")

if uploaded_file is None:
    st.warning("plz upload your file")


if uploaded_file is not None:
    st.success("file is uploaded")
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df =Preprocessing.prepocessing(data)
    
    # st.dataframe(df)
    
    
    #fetch unique user 
    user_list=df['user'].unique().tolist()
    
    #
    # user_list.remove('group_message')
    user_list.sort()
    user_list.insert(0,"OverAll")
    selected_user =st.sidebar.selectbox("show analysis wrt",user_list)
    
    if st.sidebar.button("Show Analysis"):
        num_msg,num_word,num_media,num_link=helper.fetch_stats(selected_user,df)
        
        col1,col2,col3,col4=st.columns(4)
        
        with col1:
            st.header("Total Msg ")
            st.title(num_msg)
        with col2:  
            st.header("Total Words ")
            st.title(num_word) 
        with col3:
            st.header("Total media shared")
            st.title(num_media)
        with col4:
            st.header("linked shared")
            st.title(num_link)  
        
        
        #monthlyTimeLine
        st.title("Monthly time Line ")
        monthlyTimeLne=helper.monthlyTime(df,selected_user)
        fig,ax =plt.subplots()
        ax.plot(monthlyTimeLne['month_year'],monthlyTimeLne['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        #day wise activity 
        st.title("Busy Days")
        day_only=helper.busy_day(df,selected_user)
        pie_data=day_only['count'].apply(lambda x : (x/day_only['count'].sum())*100).tolist()
        col1,col2=st.columns(2)
        
        
        with col1:
            st.title("Bar Graph")
            fig,ax=plt.subplots()
            ax.bar(day_only['day'],day_only['count'])
            plt.xticks(rotation=90)
            st.pyplot(fig)
            
        with col2 :
            st.title("Pie chart")
            fig,ax=plt.subplots()
            ax.pie(pie_data,labels=day_only['day'],autopct='%1.1f%%')
            st.pyplot(fig)
            
            
            
        #busy month
        st.title("Busy Month")
        month_only=helper.busyMonth(df,selected_user) 
        pie_data2=month_only['count'].apply(lambda x :(x/month_only['count'].sum())*100)
        col1,col2=st.columns(2)
        
        
        with col1:
            st.title("Bar Graph")
            fig,ax=plt.subplots()
            ax.bar(month_only['name_month'],month_only['count'])
            plt.xticks(rotation=90)
            st.pyplot(fig)
            
        with col2 :
            st.title("Pie chart")
            fig,ax=plt.subplots()
            ax.pie(pie_data2,labels=month_only['name_month'],autopct='%1.1f%%')
            st.pyplot(fig)
            
            
        col1,col2=st.columns(2)  
        
        
        if selected_user=='OverAll':  
            
            
            x,newdf=helper.most_busy_user(df) 
            fig,ax = plt.subplots()
            
            with col1:
                st.header("Most_Busy_User") 
                ax.bar(x.index,x.values)
                plt.xticks(rotation=90)
                st.pyplot(fig)
            with col2:
                st.header(" % of msg sent")  
                st.dataframe(newdf)  
                
                
        #WordCloud 
        
        df_wc =helper.wordCloud(df,selected_user)  
        fig,ax=plt.subplots()
        ax.imshow(df_wc)   
        st.pyplot(fig)   
                
                
        #Most Common word 
        df_mostCommon_word =helper.mostCommon_word(df,selected_user)  
              
        col1,col2=st.columns(2)
        
        with col1:
            st.header("most common word") 
            st.dataframe(df_mostCommon_word) 
            
        with col2:
            st.header("graph for most word")  
            fig,ax =plt.subplots(figsize=(10, 10))
            ax.barh(df_mostCommon_word[0],df_mostCommon_word[1])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)       
          
                
           
        # user_input = st.text_input("Enter your name:", placeholder="Type your name here...")
        # st.text(f"Hello, {user_input}! Welcome to the app!")
        
    
# st.sidebar.title("Text Sentimental Analysis")
# user_input = st.sidebar.text_input("Enter your name:", placeholder="Type your name here...")    

# # Add a submission button
# if st.sidebar.button("Submit"):
#     if user_input:
#         st.write(f"Hello, {user_input}! Welcome to the app!")
#     else:
#             st.write("Please enter your name before submitting.")
    
# st.sidebar.title("Text Summarized Analysis")    
# choice =st.sidebar.selectbox("Select your choice",["Summarize Text","Summarize Document"])

# if choice=="Summarize Text":
#     st.subheader("Summarize Text")
#     input_text=st.text_area("ENTER YOUR TEXT HERE")
    
# if choice==None :
#     st.subheader(" ")
 
# if choice=="Summarize Document" :
#     st.subheader("Summarize Document")
      
        
           
                    
         
                    
            