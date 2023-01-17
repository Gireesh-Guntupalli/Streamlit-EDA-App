import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import html
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from sklearn.preprocessing import OneHotEncoder,LabelEncoder
import json
import requests
from streamlit_lottie import st_lottie

hide_menu_style = """
<style>
#MainMenu {visibility: hidden; }
footer {visibility: hidden; }
</style>
"""
st.markdown (hide_menu_style, unsafe_allow_html=True)

@st.experimental_memo
def convert_df(dataframe):
    return dataframe.to_csv(index = False).encode("utf-8")
    
    
def load_lottie(url:str):
    r = requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()
lottie1 = load_lottie('https://assets8.lottiefiles.com/packages/lf20_pp6psjrv.json')

st.title("Welcome to EDA app")
st_lottie(lottie1, speed=1, reverse = False, loop = True, width = 600, height=200)
st.markdown("This simple EDA app can be used to perform Explorartory Data Analysis on your csv data. This application helps you in understanding the data and analyzing the relationship among variables. This app also, allows you to drop columns that are not needed after the analysis.")
st.write(" ")
st.markdown("This app is build using Streamlit and Pandas Profiling Report. In case of any queries please contact me via 'guntupallygireesh@yahoo.com'")


##Uploading file Button
st.header("Upload your file here")
uploadfile = st.file_uploader("Upload a file of type 'csv'", type = "csv")


##If file upload is successfull.        
if uploadfile is not None:
    st.success("The file is uploaded successfully.")
    df = pd.read_csv(uploadfile)
    numerical_columns = []
    categorical_columns = []
    for i in df.columns:
        column_type = df[i].dtypes
        if column_type == 'object':
            categorical_columns.append(i)
        else:
            numerical_columns.append(i)      

    with st.form(key='form1'):
        with st.sidebar:
           st.title('**View Data**')
           view_dataset = st.form_submit_button (label='View')
           
           st.title("**Qucik Look**")
           column_names = st.form_submit_button (label="Column Names")
           column_dtypes = st.form_submit_button (label='Column dtypes')
           check_missing_values = st.form_submit_button("Missing Values")
           scatter_matrix = st.multiselect("Select Dimensions of PairPlot", df.columns)
           pairplot = st.form_submit_button("Pair Plot")
           
           st.title("**Generate Profile Report**")
           generate_pr = st.form_submit_button (label='Generate')
          
           
    if view_dataset:
        st.header("The data can be viewed as:")
        st.write(df)
        
    if column_names:
        st.subheader("Column titles of uploaded data are:")
        st.text(df.columns)
            
    if column_dtypes:
        st.subheader("Column dtypes of uploaded data are:")
        st.text(df.dtypes)
        
             
    if check_missing_values:
        st.subheader("Missing Values..")
        #############  finding number of null values in each column
        missing_values = []
        for i in df.columns:
            nulls = sum(pd.isnull(df[i]))
            missing_values.append(nulls)
            
    ##########  if no of nul values are zero it will display some text else it will display bar plot by each column
        if max(missing_values) == 0:
            st.write("Total no.of Null Values  "+str(max(missing_values)))
        else:
            st.write("Total no.of Null Values  "+str(sum(missing_values)))
            st.write(df.isna().sum())
    
    if pairplot:
        with st.form('form'):
            st.header('Pairplot for selected variables')
            st.info("Please Understand that this might take a while. Also, note that no 'HUE' is set for the pairplot and  'dropna' is set to True")
            fig = sns.pairplot(df, vars = scatter_matrix) 
            st.pyplot(fig,dropna = True)
    
    if generate_pr:
        report = ProfileReport(df, explorative=True)
        st.header('**Pandas Profiling Report**')
        st.info("This might take some time. Please don't refresh the page.")
        st_profile_report(report)
        
    with st.form("form_"):   
        st.header("Modify dataframe.")
        selection1 = st.multiselect("Choose columns to be dropped", df.columns, key=1)
        modify =  st.form_submit_button(label = 'Modify')   
        st.info("Pressing 'Modify' removes selected columns from the dataframe and imputes missing values in remaining numerical and categorical columns with mean and mode respectively.")
       
        
    if modify:
        Encoder = LabelEncoder()
        df1 = df.drop(selection1, axis =1)
        df1 = df1.apply(Encoder.fit_transform)
        for i in df1.columns:
            clas = df1[i].dtypes
            if clas == 'object' or clas == 'bool':
                 df1[i].fillna(df1[i].mode()[0], inplace=True)
            else:
                df1[i].fillna(df1[i].mean(), inplace=True)
        st.write(df1)
        st.info("Please observe that all the categorical columns of the data are label encoded.")
        st.write("The shape of the dataset after dropping selected columns is:", df1.shape)
           
        csv = convert_df (df1)
        lottie2= load_lottie("https://assets2.lottiefiles.com/packages/lf20_7iqfdthd.json")
        st_lottie(lottie2, loop= True, width = 50, height = 50)
        st.download_button(
            "Download modifed data",
            csv,
            "Modified data.csv",
            "text/csv",
            key='download-csv'
            )
        
    
            
            
        
