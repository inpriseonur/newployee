# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 12:47:48 2023

@author: inpri
"""

import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime



def load_Data():
    df = pd.read_csv('OT.csv')
    df.columns = ['Project Name', 'Departmant', 'Job Title', 'Start Date', 'End Date', 'Estimation Date', 'Feedback', 'Manager', 'Project Owner',
    'Progress', 'Status']
    df['Start Date'] = pd.to_datetime(df['Start Date'], format='mixed')
    df['End Date'] = pd.to_datetime(df['End Date'], format='mixed')
    df['Estimation Date'] = pd.to_datetime(df['Estimation Date'], format='mixed')
    df['Status'].fillna('InProgress', inplace = True) #Status kolonu boş olan satırlar için bu kolona inprogress yazdırıyorum
    
    return df



def create_sidebar():
    df = load_Data()
    st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")
    st.sidebar.image("logo.jpg",caption="Developed and Maintaned by: Onur Cinemre")
    selected_box = st.sidebar.multiselect('Select one or multiple departmans',df['Departmant'].unique(),df['Departmant'].unique().tolist())
    df = df[df["Departmant"].isin(selected_box)]
    selected_owner = st.sidebar.selectbox('Seç departman', df['Job Title'].unique())
    df = df[df['Job Title'] == selected_owner]
    return df
 

def create_metrics(df):
    
    st.subheader("🔔 Analytics Dashboard")
    st.markdown("##")
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

    
df = create_sidebar()
create_metrics(df)








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
