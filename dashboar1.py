# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 12:47:48 2023

@author: inpri
"""

import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
from datetime import datetime
#from streamlit.option_menu import option_menu

st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")
st.subheader("🔔 Analytics Dashboard")
st.markdown("##")
tab1, tab2 = st.tabs(["Data", "📈 Chart"])

with tab1:
    
    def load_Data():
        df = pd.read_csv('OT.csv')
        df.columns = ['Project Name', 'Departmant', 'Job Title', 'Start Date', 'End Date', 'Estimation Date', 'Feedback', 'Manager', 'Project Owner',
        'Progress', 'Status']
        df['Start Date'] = pd.to_datetime(df['Start Date'], format='mixed')
        df['End Date'] = pd.to_datetime(df['End Date'], format='mixed')
        df['Estimation Date'] = pd.to_datetime(df['Estimation Date'], format='mixed')
        df['Status'].fillna('InProgress', inplace = True) #Status kolonu boş olan satırlar için bu kolona inprogress yazdırıyorum
        
        return df
    
    def filter_Data(df):
        df_group = df.groupby('Departmant')
        df_colums = df_group[['Progress', 'Feedback']]
        return df_colums 
    
    
    def create_metrics(df):
        with open("style.css")as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    
        row_count = len(df.index)
        active = len(df[df['Status'] == 'InProgress'].index)
        done = len(df[df['Status'] == 'done'].index)
         
        col1, col2, col3 = st.columns(3,gap='large')
        with col1:
            st.info('Total Onboarding',icon="📌")
            st.metric(label='Count', value=row_count, delta='%12', delta_color= 'normal ')
        with col2:
            st.info('Active Onboarding',icon="📌")
            st.metric(label='Count', value=active, delta='-%3', delta_color='normal')
        with col3:
            st.info('Completed Onboarding',icon="📌")
            st.metric(label='Count', value=done, delta='%36', delta_color='normal' )
        st.divider()
#Grid ile tüm datayı bas        
        st.data_editor(df, column_config={
        'Progress': st.column_config.ProgressColumn(
        'Progress Bar',
        help='Completed tasks progress',
        format='$%f',
        min_value= 0,
        max_value=100,
        ),
        }, hide_index=True , width=5500
        )

    
    def create_sidebar(df):
        st.sidebar.image("logo.jpg",caption="Developed and Maintaned by: Onur Cinemre")
        selected_boxed = st.sidebar.selectbox('Select a Type of Analytic Dashboard', options=['General by Onboarding', 'Detail Onboarding'])
        if selected_boxed =='General by Onboarding':
            create_SelectboxesForGeneral(df)
        else:
           load_Data_OnboardinDetail()
    
    def create_SelectboxesForGeneral(df):
        selected_departman = st.sidebar.multiselect('Select one or multiple departmans',df['Departmant'].unique(), df['Departmant'].unique().tolist(), key="deneme")
        df = df[df["Departmant"].isin(selected_departman)]
        selected_job_title = st.sidebar.multiselect('Select one or multiple Job Title',df['Job Title'].unique(),df['Job Title'].unique().tolist(), key='deneme2')
        df = df[df['Job Title'].isin(selected_job_title)]
     
        selected_manager = st.sidebar.multiselect('Select one or multiple Manager',df['Manager'].unique(),df['Manager'].unique().tolist(), key='deneme3')
        df = df[df['Manager'].isin(selected_manager)]
        selected_owner = st.sidebar.multiselect('Select one or multiple Project Owner',df['Project Owner'].unique(),df['Project Owner'].unique().tolist(), key='deneme4')
        df = df[df['Project Owner'].isin(selected_owner)]
        create_metrics(df)


def load_Data_OnboardinDetail():
    df_detail = pd.read_csv('OT_Detail.csv')
    df_detail.columns = ['Project Type', 'Project Name', 'Project Departmant', 'Project Owner', 'Task Name',
                         'Task Assignee', 'Task Type', 'Created Date', 'Assignee Date', 'Completed Date',
                         'Duration', 'Task Departmant', 'Job Title', 'Estimated Duration']
    df_detail['Created Date'] = pd.to_datetime(df_detail['Created Date'], format='mixed')
    df_detail['Assignee Date'] = pd.to_datetime(df_detail['Assignee Date'], format='mixed')
    df_detail['Completed Date'] = pd.to_datetime(df_detail['Completed Date'], format='mixed')
    df_detail['Project Type'] = 'Onboarding'
    df_detail['Fark'] = df_detail['Completed Date'] - df_detail['Assignee Date']
    return df_detail


df = load_Data()    
df = create_sidebar(df)
    


# avg_feedback = df['Feedback'].mean()
# df_filtered = filter_Data(df).mean()
# df_filtered['AVG Feedback'] = avg_feedback




 
# with tab2:
#     st.data_editor(df)
#     fig_investment=px.bar(
#         df_filtered,
#         x="Feedback",
#         y=df_filtered.index,
#         orientation="h",
#         title="<b> Investment by Business Type </b>",
#         color_discrete_sequence=["#0083B8"]*len(df_filtered),
#         template="plotly_white",
#     )
#     fig_investment.update_layout(
#     plot_bgcolor="rgba(0,0,0,0)",
#     xaxis=(dict(showgrid=False))
#      )
#     left,right,center=st.columns(3)
#     right.plotly_chart(fig_investment,use_container_width=True)    

 

    