# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 12:47:48 2023

@author: inpri
"""

import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
#from streamlit.option_menu import option_menu

st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")
st.subheader("🔔 Analytics Dashboard")
st.markdown("##")
tab1, tab2 = st.tabs(["Data", "📈 Chart"])

    
def load_Data():
    df = pd.read_csv('OT.csv')
    df.columns = ['Project Name', 'Departmant', 'Job Title', 'Start Date', 'End Date', 'Estimation Date', 'Feedback', 'Manager', 'Project Owner',
    'Progress', 'Status']
    df['Start Date'] = pd.to_datetime(df['Start Date'])
    df['End Date'] = pd.to_datetime(df['End Date'])
    df['Estimation Date'] = pd.to_datetime(df['Estimation Date'])
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


def create_sidebar():
    st.sidebar.image("logo.jpg",caption="Developed and Maintaned by: Onur Cinemre")
    selected_boxed = st.sidebar.selectbox('Select a Type of Analytic Dashboard', options=['General by Onboarding', 'Detail Onboarding'])
    if selected_boxed =='General by Onboarding':
        df = load_Data()
        create_SelectboxesForGeneral(df)
    else:
        load_Data_OnboardingDetail()
 

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
    
def create_SelectboxesForDetail(df_detail):
    selected_project_departmant = st.sidebar.selectbox('Choose Departmant', df_detail['Project Departmant'].unique().tolist(), key='detail')
    df_detail = df_detail[df_detail['Project Departmant'] == selected_project_departmant]
    #df_detail = df_detail.groupby(['Task Type']).mean()
    
    #df_detail = df_detail.groupby(['Task Type'])['Reminder'].sum()
    df_detail = df_detail.groupby(by=["Task Type"])[['Reminder']].sum()[["Reminder"]].sort_values(by="Reminder")

    #gk = df_detail.groupby('Task Type')      
    #st.data_editor(gk.get_group('Setup'))
    #st.write(df_detail)
    draw_graph(df_detail)
    deneme(df_detail)
    

def load_Data_OnboardingDetail():
    df_detail = pd.read_csv('OT_Detail.csv')
    df_detail.columns = ['Project Type', 'Project Name', 'Project Departmant', 'Project Owner', 'Task Name',
                         'Task Assignee', 'Task Type', 'Created Date', 'Assignee Date', 'Completed Date',
                         'Duration', 'Task Departmant', 'Job Title', 'Estimated Duration', 'Reminder']
    df_detail['Created Date'] = pd.to_datetime(df_detail['Created Date'])
    df_detail['Assignee Date'] = pd.to_datetime(df_detail['Assignee Date'])
    df_detail['Completed Date'] = pd.to_datetime(df_detail['Completed Date'])
    df_detail['Project Type'] = 'Onboarding'
    df_detail['Fark'] = df_detail['Completed Date'] - df_detail['Assignee Date']
    create_SelectboxesForDetail(df_detail)

def draw_graph(df_graph):
    st.data_editor(df_graph)
    fig_investment=px.bar(
        df_graph,
        x="Reminder",
        y=df_graph.index,
        orientation="h",
        title="<b> Sending Manuel Reminder By Departmant</b>",
        color_discrete_sequence=["#0083B8"]*len(df_graph),
        template="plotly_white",
    )
    fig_investment.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
      )
    left,right,center=st.columns(3)
    right.plotly_chart(fig_investment,use_container_width=True)    


def update_point(df_graph):
    st.data_editor(df_graph)
    fig_investment=px.bar(
        df_graph,
        x="Reminder",
        y=df_graph.index,
        orientation="h",
        title="<b> Sending Manuel Reminder By Departmant</b>",
        color_discrete_sequence=["#0083B8"]*len(df_graph),
        template="plotly_white",
    )
    fig_investment.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
      )
    left,right,center=st.columns(3)
    right.plotly_chart(fig_investment,use_container_width=True) 

def deneme(df):
   
    fig = px.bar(df, x=df.index, y='Reminder',
                 hover_data=['Reminder', 'Reminder'], color='Reminder',
                 labels={'pop':'population of Canada'}, height=400,
                 color_continuous_scale=px.colors.sequential.Reds)
    left,right,center=st.columns(3)
    left.plotly_chart(fig)

#     left.plotly_chart(f)
# def deneme(df):
# #    np.random.seed(1)
# #    x = np.random.rand(100)
# #    y = np.random.rand(100)
#     x = df.index
#     y = df['Reminder']
    
#     f = go.FigureWidget([go.Scatter(x=x, y=y, mode='markers')])
    
#     scatter = f.data[0]
#     colors = ['#a3a7e4'] * 100
#     scatter.marker.color = colors
#     scatter.marker.size = [10] * 100
#     f.layout.hovermode = 'closest'
#     left,right,center=st.columns(3)
#     left.plotly_chart(f)
#     # create our callback function
#     def update_point(trace, points, selector):
#         c = list(scatter.marker.color)
#         s = list(scatter.marker.size)
#         for i in points.point_inds:
#             c[i] = '#bae2be'
#             s[i] = 20
#             with f.batch_update():
#                 scatter.marker.color = c
#                 scatter.marker.size = s
#     scatter.on_click(update_point)
#     f


with tab1:
    create_sidebar()
    #deneme()

    
long_df = px.data.medals_long()
fig = px.bar(long_df, x="nation", y="count", color="medal", title="Long-Form Input")
left,right,center=st.columns(3)
left.plotly_chart(fig)


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

 

    