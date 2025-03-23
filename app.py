# import streamlit as st
# import pandas as pd
# import numpy as np

# # Load Data
# @st.cache_data
# def load_data():
#     df = pd.read_csv("data/real_estate.csv",encoding='latin-1')
#     return df

# df = load_data()

# st.title("Canadian Mortgage and Housing Corporation Story")
# st.write("Analyze real estate trends in Canada for a decade")
# Import libraries
from pyparsing import col
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import json

#######################
# Page configuration
st.set_page_config(
    page_title="Canada Automobiles Sales Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# CSS styling
# st.markdown("""
# <style>

# [data-testid="block-container"] {
#     padding-left: 2rem;
#     padding-right: 2rem;
#     padding-top: 1rem;
#     padding-bottom: 0rem;
#     margin-bottom: -7rem;
# }

# [data-testid="stVerticalBlock"] {
#     padding-left: 0rem;
#     padding-right: 0rem;
# }

# [data-testid="stMetric"] {
#     background-color: #393939;
#     text-align: center;
#     padding: 15px 0;
# }

# [data-testid="stMetricLabel"] {
#   display: flex;
#   justify-content: center;
#   align-items: center;
# }

# [data-testid="stMetricDeltaIcon-Up"] {
#     position: relative;
#     left: 38%;
#     -webkit-transform: translateX(-50%);
#     -ms-transform: translateX(-50%);
#     transform: translateX(-50%);
# }

# [data-testid="stMetricDeltaIcon-Down"] {
#     position: relative;
#     left: 38%;
#     -webkit-transform: translateX(-50%);
#     -ms-transform: translateX(-50%);
#     transform: translateX(-50%);
# }

# </style>
# """, unsafe_allow_html=True)



#######################
# Load data
df_reshaped = pd.read_csv("data/cars.csv",encoding='latin-1')


#######################
# Sidebar
with st.sidebar:
    st.title('🚗 Canada Automobiles Sales Dashboard for 2024')
    year_list = list(df_reshaped.REF_DATE.unique())[::-1]
    selected_year = st.selectbox('Select a Month', year_list)
    df_selected_year = df_reshaped[df_reshaped.REF_DATE == selected_year]
    
    Vehicle_type_list = list(df_selected_year.Vehicle_type.unique())[::-1]
    selected_Vehicle_type = st.selectbox('Select a type of Vehicle', Vehicle_type_list)
    df_selected_Vehicle_type = df_selected_year[df_selected_year.Vehicle_type == selected_Vehicle_type]
    
    origin_list = list(df_selected_Vehicle_type.Origin_of_manufacture.unique())[::-1]
    selected_origin = st.selectbox('Select a origin of manufacturer', origin_list)
    df_selected_origin = df_selected_Vehicle_type[df_selected_Vehicle_type.Origin_of_manufacture == selected_origin]
    
    
    df_selected_origin_sorted = df_selected_origin.sort_values(by="Units_Sold", ascending=False)

    # color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    # selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
    
    
#######################
# Plots

# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Month", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap

# Choropleth map
# Assign mp to the geojson data
with open("data/cars.geojson", "r") as geo:
    mp = json.load(geo)
def make_choropleth(input_df, input_id, input_column):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, 
                               geojson=mp,
                            featureidkey="properties.Province",
                            
                               color_continuous_scale='plasma',
                               range_color=(0, max(df_selected_origin.Units_Sold)),
                               scope="north america",
                               labels={'Units_Sold':'Units'}
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth
    
    

 #######################
# Dashboard Main Panel
col = st.columns((1.5, 4.5, 2), gap='small')
with col[1]:   
     st.markdown('#### Number of units of motor vehicles sold in 2024')
     choropleth = make_choropleth(df_selected_origin, 'Province', 'Units_Sold')
     st.plotly_chart(choropleth, use_container_width=True)
     
     
     st.markdown('#### Top Provinces')

     st.dataframe(df_selected_origin_sorted,
                 column_order=("Name_of_Province", "Units_Sold"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Name_of_Province": st.column_config.TextColumn(
                        "Province",
                    ),
                    "Units_Sold": st.column_config.ProgressColumn(
                        "Units Sold",
                        format="%f",
                        min_value=0,
                        max_value=max(df_selected_origin_sorted.Units_Sold),
                     )}
                 )
