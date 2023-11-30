#streamlit run "C:\Users\ADMIN\Desktop\Que\python file\dashboard.py"
import numpy as np
import pandas as pd
import datetime as dt
import calendar
import os
import plotly.express as px
import plotly.subplots as sp
import streamlit as st
import seaborn as sns
import altair as alt
from matplotlib import pyplot as plt
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards

## set page
st.set_page_config( page_icon= ':bar_chart:', layout= 'wide',page_title= 'Streamlit Dashboard')
#st.title(':bar_chart: Super Store Dashboard')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html= True)

# Load data
data= github.com/QueCinamon/dashboard/blob/main/Sample%20Superstore%20WB.xlsx
df= pd.read_excel(data)

# File upload
#fl= st.file_uploader(':file_folder: Upload a file', type= (['csv','txt','xlsx','xls']))
#if fl is not None:
 #   filename= fl.name
  #  st.write(filename)
   # df= pd.read_csv(filename)
#else:
 #   os.chdir(r'C:\\Users\\ADMIN\\Desktop\\Que\\data')
  #  df= pd.read_excel('C:\\Users\\ADMIN\\Desktop\\Que\\data\\Sample Superstore WB.xlsx')

## filter dataframe 
#with st.expander('Filter Excel data'):
 #   filtered_df= dataframe_explorer(df2, case= False)
  #  st.dataframe(filtered_df, use_container_width= True)

# Column date time
#col1, col2= st.columns((2))
#df['Ship Date']= pd.to_datetime(df['Ship Date']).dt.date
#start_date= pd.to_datetime(df['Ship Date']).min()
#end_date= pd.to_datetime(df['Ship Date']).max()
#with col1:
 #   date1= pd.to_datetime(st.date_input('Start Date'), start_date)
#with col2:
  #  date2= pd.to_datetime(st.date_input('End Date'), end_date)

## Side bar date range
def sales_select():
    with st.sidebar:
        st.title('Please filter (data between 07Jan14 - 05Jan18)')
        start_date= st.date_input(label= 'Start ship date', value= pd.to_datetime('01/05/2017'))
    with st.sidebar:
        end_date= st.date_input(label= 'End ship date', value= pd.to_datetime('01/05/2018'))
#st.error('You chose date from: ' + str(start_date) + ' to ' + str(end_date))
    df2= df[(df['Ship Date']>= str(start_date))& (df['Ship Date']<= str(end_date))]
#st.dataframe(df2)

    region= st.sidebar.multiselect('Region:', options= df2['Region'].unique())#, default = df['Region'].unique())    
    state= st.sidebar.multiselect('State:', options= df2['State'].unique())#, default = df['Category'].unique())
    city= st.sidebar.multiselect('City:', options= df2['City'].unique())#, default = df['Category'].unique())
    customer_name= st.sidebar.multiselect('Customer name:', options= df2['CustomerName'].unique())
#df2= df2.query('Region== @region & City== @city & State== @state & CustomerName== @customer_name')
#st.markdown('---')

## filter data base on Region, City, State
    if not region and not state and not city and not customer_name:
        filtered_df= df2
    elif not region and not state and not city:
        filtered_df= df2[df2['CustomerName'].isin(customer_name)]
    elif not region and not state and not customer_name:
        filtered_df= df2[df2['City'].isin(city)]    
    elif not state and not city and not customer_name:
        filtered_df= df2[df2['Region'].isin(region)]
    elif not region and not city and not customer_name:
        filtered_df= df2[df2['State'].isin(state)]
    elif not region and not state:
        filtered_df= df2[df2['City'].isin(city)&df2['CustomerName'].isin(customer_name)]
    elif not region and not city:
        filtered_df= df2[df2['State'].isin(state)&df2['CustomerName'].isin(customer_name)]
    elif not region and not customer_name:
        filtered_df= df2[df2['State'].isin(state)&df2['City'].isin(city)]
    elif not state and not city:
        filtered_df= df2[df2['Region'].isin(region)&df2['CustomerName'].isin(customer_name)]
    elif not state and not customer_name:
        filtered_df= df2[df2['Region'].isin(region)&df2['City'].isin(city)]
    elif not city and not customer_name:
        filtered_df= df2[df2['Region'].isin(region)&df2['State'].isin(state)]
    elif not region:
        filtered_df= df2[df2['State'].isin(state)&df2['City'].isin(city)&df2['CustomerName'].isin(customer_name)]
    elif not state:
        filtered_df= df2[df2['Region'].isin(region)&df2['City'].isin(city)&df2['CustomerName'].isin(customer_name)]
    elif not city:
        filtered_df= df2[df2['Region'].isin(region)&df2['State'].isin(state)&df2['CustomerName'].isin(customer_name)]
    elif not customer_name:
        filtered_df= df2[df2['Region'].isin(region)&df2['State'].isin(state)&df2['City'].isin(city)]

## metrics
    total_quantity= int(filtered_df['Quantity'].sum())
    total_sales= int(filtered_df['Sales'].sum())
    total_profit= int(filtered_df['Profit'].sum())
    cola, colb, colc= st.columns(3)
    
    cola.metric(label= 'Total Quantity', value= f'{total_quantity:,.0f}')#, delta= 'High Price')
    colb.metric(label= 'Total Amount', value= f'{total_sales:,.0f}')#, delta= 'High Price')
    colc.metric(label= 'Total Profit', value= f'{total_profit:,.0f}')#, delta= 'High Price')
    style_metric_cards (background_color= '#071021', border_left_color= '#1f66bd')

## Sales by Sub Category (bar chart)
    col1,col2= st.columns(2)
    sub_bar= filtered_df.groupby(by= ['Sub-Category'], as_index= False)[['Sales']].sum().sort_values(by='Sales')
    #product_bar= filtered_df.groupby(by= ['Product Name'], as_index= False)[['Sales']].sum().sort_values(by='Sales')
    with col1:    
        fig= px.bar(sub_bar, x= 'Sales', y= 'Sub-Category', orientation= 'h', title= '<b> Amount by Sub Category</b>')#, template= 'plotly_white') #color_discrete_sequence= ['#0083B8']* len(sub_bar),text_auto=True)
        st.plotly_chart(fig, use_container_width= True, height= 400)
        
        #source1= pd.DataFrame({'Amount (US $)': filtered_df['Sales'], 'Sub Category': filtered_df['Sub-Category']})
        #subcate_barchart2= alt.Chart(source1, title='Amount by Sub Category').encode(x='sum(Amount (US $)):Q' , y= alt.Y( 'Sub-Category:N', sort= '-x'))#, text= 'sum(Sales (US $)):Q')
        #subcate_barchart3= subcate_barchart2.mark_bar()+subcate_barchart2.mark_text(align='left', dx=2)
        #st.altair_chart(subcate_barchart3, use_container_width= True)
        
    
    with col2:
        fig= px.pie(filtered_df, values= 'Sales', names= 'Category', hole= 0.5, title= '<b> Amount by Category</b>')
        fig.update_traces(text= filtered_df['Category'], textposition= 'inside')
        st.plotly_chart(fig, use_container_width= True)

#st.subheader('Sales by Product Name', divider= 'rainbow')
    def bar1():
        source1= pd.DataFrame({'Amount (US $)': filtered_df['Sales'], 'Product Name': filtered_df['Product Name']})
        subcate_barchart2= alt.Chart(source1, title='Amount by Product Name').encode(x='sum(Amount (US $)):Q' , y= alt.Y( 'Product Name:N', sort= '-x'))#, text= 'sum(Sales (US $)):Q')
        subcate_barchart3= subcate_barchart2.mark_bar()+subcate_barchart2.mark_text(align='left', dx=2)
        st.altair_chart(subcate_barchart3, use_container_width= True)
    bar1()

def product_select():
    with st.sidebar:
        st.title('Please filter (data between 07Jan14 - 05Jan18)')
        start_date= st.date_input(label= 'Start ship date', value= pd.to_datetime('01/05/2017'))
    with st.sidebar:
        end_date= st.date_input(label= 'End ship date', value= pd.to_datetime('01/05/2018'))
    df3= df[(df['Ship Date']>= str(start_date))& (df['Ship Date']<= str(end_date))]    
    category= st.sidebar.multiselect('Category:', options= df3['Category'].unique())
    sub_category= st.sidebar.multiselect('Sub Category:', options= df3['Sub-Category'].unique())
    product_name= st.sidebar.multiselect('Product Name:', options= df3['Product Name'].unique())
    if not category and not sub_category and not product_name:
        filtered_df= df3
    if category and sub_category:
        filtered_df= df3[df3['Category'].isin(category)& df3['Sub-Category'].isin(sub_category)]
    if category and product_name:
        filtered_df= df3[df3['Category'].isin(category)& df3['Product Name'].isin(product_name)]
    if sub_category and product_name:
        filtered_df= df3[df3['Sub-Category'].isin(sub_category)& df3['Product Name'].isin(product_name)]
    if category:
        filtered_df= df3[df3['Category'].isin(category)]
    if sub_category:
        filtered_df= df3[df3['Sub-Category'].isin(sub_category)]
    if product_name:
        filtered_df= df3[df3['Product Name'].isin(product_name)]
        
    ## metrics
    total_quantity= int(filtered_df['Quantity'].sum())
    total_sales= int(filtered_df['Sales'].sum())
    total_profit= int(filtered_df['Profit'].sum())
    cola, colb, colc= st.columns(3)
    cola.metric(label= 'Total Quantity', value= f'{total_quantity:,.0f}')#, delta= 'High Price')
    colb.metric(label= 'Total Amount', value= f'{total_sales:,.0f}')#, delta= 'High Price')
    colc.metric(label= 'Total Profit', value= f'{total_profit:,.0f}')#, delta= 'High Price')
    style_metric_cards (background_color= '#071021', border_left_color= '#1f66bd')

       ## Sales by Sub Category (bar chart)
    col1,col2= st.columns(2)
    state_bar= filtered_df.groupby(by= ['State'], as_index= False)[['Quantity']].sum().sort_values(by='Quantity')
    #city_bar= filtered_df.groupby(by= ['City'], as_index= False)[['Sales']].sum().sort_values(by='Sales')
    with col1:    
        fig= px.bar(state_bar, x= 'Quantity', y= 'State', orientation= 'h', title= '<b> Quantity by State</b>')#, template= 'plotly_white') #color_discrete_sequence= ['#0083B8']* len(sub_bar),text_auto=True)
        st.plotly_chart(fig, use_container_width= True, height= 400)
    with col2:
        fig= px.pie(filtered_df, values= 'Quantity', names= 'Region', hole= 0.5, title= '<b> Quantity by Region</b>')
        fig.update_traces(text= filtered_df['Region'], textposition= 'inside')
        st.plotly_chart(fig, use_container_width= True)

#st.subheader('Sales by Product Name', divider= 'rainbow')
    def bar1():
        source1= pd.DataFrame({'Quantity (US $)': filtered_df['Quantity'], 'City': filtered_df['City']})
        subcate_barchart2= alt.Chart(source1, title='Quantity by City').encode(x='sum(Quantity (US $)):Q' , y= alt.Y( 'City:N', sort= '-x'))#, text= 'sum(Sales (US $)):Q')
        subcate_barchart3= subcate_barchart2.mark_bar()#+subcate_barchart2.mark_text(align='left', dx=2)
        st.altair_chart(subcate_barchart3, use_container_width= True)
    bar1()


         
def sideBar():
    with st.sidebar:
        selected= option_menu(menu_title= 'Main menu', options= ['Sales Dashboard','Product Dashboard'], default_index= 0)
    if selected== 'Sales Dashboard':
        st.subheader(f'Page: {selected}')
        sales_select()
        
    if selected== 'Product Dashboard':
        st.subheader(f'Page: {selected}')
        product_select()

sideBar()









