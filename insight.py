import streamlit as st
import pandas as pd 
import numpy as np
from PIL import Image
import pydeck as pdk
from urllib.error import URLError
import altair as alt
from collections import Counter 
import datetime
from datetime import date
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
import logging
import threading
from copy import copy
import scipy
from math import radians, cos, sin, asin, sqrt, atan2
from streamlit_folium import folium_static
import folium
import random
import plotly.graph_objects as go
from plotly import tools
import plotly.offline as py
import plotly.express as px
import plotly.graph_objs as go

st.set_page_config(layout='wide')
#Header

imgs = ['images/logo.png']
st.image(image= imgs, width=700)
st.title('J & J Insights')
# st.image(image= Image.open('images/Logo.jpeg'), width=300)
# st.image(image= Image.open('images/Paxafe.png'), width=300)
##########################################################################
####### Text
st.header("1.0 Transit/Wait time")
transit= pd.read_csv('data/text/Transit time.csv')
transit= transit.dropna()
transit['Percentage of time spent within 2km of origin'] = transit['Percentage of time spent within 2km of origin'].astype(int)
transit['Percentage oftime spent within 10km of origin'] = transit['Percentage of time spent within 10km of origin'].astype(int)
transit["Percentage of shipments close to Google ETA 2km geofence"] = transit["Percentage of shipments close to Google ETA 2km geofence"].astype(int)
transit["Percentage ofshipments close to Google ETA 10km geofence"] = transit["Percentage of shipments close to Google ETA 10km geofence"].astype(int)

transit['Percentage of time spent within 2km of origin']=transit['Percentage of time spent within 2km of origin'].apply(np.floor)
transit['Percentage of time spent within 10km of origin']=transit['Percentage of time spent within 10km of origin'].apply(np.floor)
transit["Percentage of shipments close to Google ETA 2km geofence"]=transit["Percentage of shipments close to Google ETA 2km geofence"].apply(np.floor)
transit["Percentage of shipments close to Google ETA 10km geofence"]=transit["Percentage of shipments close to Google ETA 10km geofence"].apply(np.floor)
# transit=transit.round(decimals=1)
st.subheader("Table 1 : Transit/Wait time of all lanes")
st.write(transit)

##########################################################################
####### Analysis 
### text
st.header("2.0 Fork Analysis: Overview")


Lane = st.radio("Select Lane: Overview",('Groveport','Olive','Lockbourne'))
if Lane == 'Groveport':
    st.image(image= Image.open('images/grove.png'),width=370)
    grove_text= pd.read_csv('data/text/groveport.csv')
    grove_text=grove_text.dropna()
    grove_text['Fork distance (miles)'] = grove_text['Fork distance (miles)'].astype(int)
    grove_text['Fork distance (miles)']=grove_text['Fork distance (miles)'].apply(np.floor)
    st.subheader('Table 2.0.A: Fork Analysis of Groveport lane (Overview)')
    st.write(grove_text)
elif Lane == 'Olive':
    st.image(image= Image.open('images/Nashville.png'),width=370)
    olive_text= pd.read_csv('data/text/olive.csv')
    olive_text=olive_text.dropna()
    olive_text['Fork distance (miles)'] =olive_text['Fork distance (miles)'].astype(int)
    olive_text['Fork distance (miles)']=olive_text['Fork distance (miles)'].apply(np.floor)
    st.subheader('Table 2.0.B: Fork Analysis of Olive lane (Overview)')
    st.write(olive_text)
elif Lane == 'Lockbourne':
    st.image(image= Image.open('images/grove.png'),width=370)
    lock_text= pd.read_csv('data/text/lockbourne.csv')
    lock_text=lock_text.dropna()
    lock_text['Fork distance (miles)'] =lock_text['Fork distance (miles)'].astype(int)
    lock_text['Fork distance (miles)']=lock_text['Fork distance (miles)'].apply(np.floor)
    st.subheader('Table 2.0.C: Fork Analysis of Lockbourne lane (Overview)')
    st.write(lock_text)

###Para

### timeslot
st.header("2.1 Fork Analysis: Time")
Lane_fork_slot = st.radio("Select Lane: Time slot/window analysis ",('Groveport','Olive','Lockbourne', 'Shreveport'))
if Lane_fork_slot == 'Groveport':
    st.image(image= Image.open('images/grove.png'),width=370)
    result_g= pd.read_csv('data/fork/fork_GC_hour.csv')
    cmap = {'Bypass':'lightgreen',
            'City': 'forestgreen',}

    result_g['hour'] = result_g['hour'].astype(str)
    chart1 = alt.Chart(result_g).mark_bar().encode(
        x=alt.X('Route', title=None),
        y='Count',
        column=alt.Column('hour', sort=list(result_g['Count']), title= 'Cincinnati fork: Time'),
        color=alt.Color('Route', scale=alt.Scale(domain=list(cmap.keys()), range=list(cmap.values()))),
        tooltip=["Count",'hour','Route']
        ).properties(width=30)
    result_gl= pd.read_csv('data/fork/fork_GL_hour.csv')
    result_gl['hour'] = result_gl['hour'].astype(str)
    chart2 = alt.Chart(result_gl).mark_bar().encode(
            x=alt.X('Route', title=None),
            y='Count',
            column=alt.Column('hour', sort=list(result_gl['Count']), title= 'Louisville fork: Time'),
            color=alt.Color('Route', scale=alt.Scale(domain=list(cmap.keys()), range=list(cmap.values()))),
            tooltip=["Count",'hour','Route']
            ).properties(width=30)
    chart3= chart2&chart1
    st.subheader('Chart 2.1.A: Fork Analysis of Groveport lane (Time)')
    chart3
elif Lane_fork_slot == 'Olive':
    st.image(image= Image.open('images/Nashville.png'),width=370)
    result_o=pd.read_csv('data/fork/fork_O_hour.csv')
    cmap = {'Bypass':'palevioletred',
            'City': 'mediumvioletred',}

    result_o['hour'] = result_o['hour'].astype(str)
    chart = alt.Chart(result_o).mark_bar().encode(
        x=alt.X('Route', title=None),
        y='Count',
        column=alt.Column('hour', sort=list(result_o['Count']), title= 'Nashville fork: Time'),
        color=alt.Color('Route', scale=alt.Scale(domain=list(cmap.keys()), range=list(cmap.values()))),
        tooltip=["Count",'hour','Route']
        ).properties (width = 30)
    st.subheader('Chart 2.1.B: Fork Analysis of Olive lane (Time)')
    chart
elif Lane_fork_slot == 'Lockbourne':
    st.image(image= Image.open('images/grove.png'),width=370)
    result_lc= pd.read_csv('data/fork/fork_LC_hour.csv')

    cmap =  {'Bypass':'cornflowerblue',
            'City': 'darkblue',}

    result_lc['hour'] = result_lc['hour'].astype(str)
    chart1 = alt.Chart(result_lc).mark_bar().encode(
        x=alt.X('Route', title=None),
        y='Count',
        column=alt.Column('hour', sort=list(result_lc['Count']), title= 'Cincinnati fork: Time'),
        color=alt.Color('Route', scale=alt.Scale(domain=list(cmap.keys()), range=list(cmap.values()))),
        tooltip=["Count",'hour','Route']
        ).properties (width =30)
    result_ll= pd.read_csv('data/fork/fork_LL_hour.csv')
    result_ll['hour'] = result_ll['hour'].astype(str)
    chart2 = alt.Chart(result_ll).mark_bar().encode(
        x=alt.X('Route', title=None),
        y='Count',
        column=alt.Column('hour', sort=list(result_ll['Count']), title= 'Louisville fork: Time'),
        color=alt.Color('Route', scale=alt.Scale(domain=list(cmap.keys()), range=list(cmap.values()))),
        tooltip=["Count",'hour','Route']
        ).properties (width = 30)
    chart3= chart2&chart1
    st.subheader('Chart 2.1.C: Fork Analysis of Lockbourne lane (Time)')
    chart3

elif Lane_fork_slot == 'Shreveport':
    st.image(image= Image.open('images/Shreveport.png'),width=370)
    st.write('Shreveport does not have any fork, So we are considering the start time for the analysis.')
    result=pd.read_csv('data/fork/time_S_hour.csv')
    chart_n= alt.Chart(result).mark_bar( color='orange', size = 15).encode(
        x = alt.X('Time',axis=alt.Axis(labelAngle=0),sort=alt.EncodingSortField(field='Time', op="count", order='ascending')),
        y=alt.Y('Count'),
        tooltip=["Count",'Time']
    ).properties (title='Start time of Shipments (Shreveport lane)',width = 400)
    st.subheader('Chart 2.1.D: Start time of Shipments (Shreveport lane)')
    chart_n
    
st.header("2.2 Fork Analysis: Day of the Week")

Lane_fork_day = st.radio("Select Lane: Day of the Week Analysis",('Groveport','Olive','Lockbourne', 'Shreveport'))
if Lane_fork_day == 'Groveport':
    st.image(image= Image.open('images/grove.png'),width=370)
    #Visual
    result_g= pd.read_csv('data/fork/fork_GC_day.csv')

    g_L_bypass= pd.read_csv('data/text/groveport_bypass_table_L.csv')
    g_L_bypass= g_L_bypass.dropna()
    g_C_bypass= pd.read_csv('data/text/groveport_bypass_table_C.csv')
    g_C_bypass= g_C_bypass.dropna()

    cmap = {'Bypass':'lightgreen',
            'City': 'forestgreen',}
    result_g['weekday'] = result_g['weekday'].astype(str)
    chart1 = alt.Chart(result_g).mark_bar().encode(
        x=alt.X('Route', title=None),
        y='Count',
        column=alt.Column('weekday', sort=list(result_g['Count']), title= 'Cincinnati fork: Day of the Week'),
        color=alt.Color('Route', scale=alt.Scale(domain=list(cmap.keys()), range=list(cmap.values()))),
        tooltip=["Count",'weekday','Route']
        ).properties(width=60)
    result_gl= pd.read_csv('data/fork/fork_GL_day.csv')
    result_gl['weekday'] = result_gl['weekday'].astype(str)
    chart2 = alt.Chart(result_gl).mark_bar().encode(
            x=alt.X('Route', title=None),
            y='Count',
            column=alt.Column('weekday', sort=list(result_gl['Count']), title= 'Louisville fork: Day of the Week'),
            color=alt.Color('Route', scale=alt.Scale(domain=list(cmap.keys()), range=list(cmap.values()))),
            tooltip=["Count",'weekday','Route']
            ).properties(width=60)
    chart3= chart2|chart1
    st.subheader('Chart 2.2.A: Fork Analysis of Groveport lane (Day of the Week)')
    chart3
    st.subheader('Table 2.2.A: Fork Analysis of Groveport lane (Day of the Week)')
    st.write('Louisville')
    st.write(g_L_bypass)
    st.write('Cincinnati')
    st.write(g_C_bypass)


elif Lane_fork_day == 'Olive':
    st.image(image= Image.open('images/Nashville.png'),width=370)
    result_o=pd.read_csv('data/fork/fork_O_day.csv')
    o_bypass= pd.read_csv('data/text/olive_bypass_table.csv')
    o_bypass= o_bypass.dropna()


    cmap = {'Bypass':'palevioletred',
            'City': 'mediumvioletred',}

    result_o['weekday'] = result_o['weekday'].astype(str)
    chart = alt.Chart(result_o).mark_bar().encode(
        x=alt.X('Route', title=None),
        y='Count',
        column=alt.Column('weekday', sort=list(result_o['Count']), title= 'Nashiville: Day of the Week'),
        color=alt.Color('Route', scale=alt.Scale(domain=list(cmap.keys()), range=list(cmap.values()))),
        tooltip=["Count",'weekday','Route']
        ).properties (width = 100)
    st.subheader('Chart 2.2.B: Fork Analysis of Olive lane (Day of the Week)')
    chart
    st.subheader('Table 2.2.B: Fork Analysis of Olive lane (Day of the Week)')
    st.write('Nashville')
    st.write(o_bypass)


elif Lane_fork_day == 'Lockbourne':
    st.image(image= Image.open('images/grove.png'),width=370)
    result_lc= pd.read_csv('data/fork/fork_LC_day.csv')
    
    #text
    L_L_bypass= pd.read_csv('data/text/lockbourne_bypass_table_L.csv')
    L_L_bypass= L_L_bypass.dropna()
    L_C_bypass= pd.read_csv('data/text/lockbourne_bypass_table_C.csv')
    L_C_bypass= L_C_bypass.dropna()
    

    cmap = {'Bypass':'cornflowerblue',
            'City': 'darkblue',}

    result_lc['weekday'] = result_lc['weekday'].astype(str)
    chart1 = alt.Chart(result_lc).mark_bar().encode(
        x=alt.X('Route', title=None),
        y='Count',
        column=alt.Column('weekday', sort=list(result_lc['Count']), title= 'Cincinnati fork: Day of the Week'),
        color=alt.Color('Route', scale=alt.Scale(domain=list(cmap.keys()), range=list(cmap.values()))),
        tooltip=["Count",'weekday','Route']
        ).properties (width = 100)
    result_ll= pd.read_csv('data/fork/fork_LL_day.csv')
    result_ll['weekday'] = result_ll['weekday'].astype(str)
    chart2 = alt.Chart(result_ll).mark_bar().encode(
        x=alt.X('Route', title=None),
        y='Count',
        column=alt.Column('weekday', sort=list(result_ll['Count']), title= 'Louisville fork: Day of the Week'),
        color=alt.Color('Route', scale=alt.Scale(domain=list(cmap.keys()), range=list(cmap.values()))),
        tooltip=["Count",'weekday','Route']
        ).properties (width = 100)
    chart3= chart2|chart1
    st.subheader('Chart 2.2.C: Fork Analysis of Lockbourne lane (Day of the Week)')
    chart3
    st.subheader('Table 2.2.C: Fork Analysis of Lockbourne lane (Day of the Week)')
    st.write('Louisville')
    st.write(L_L_bypass)
    st.write('Cincinnati')
    st.write(L_C_bypass)

elif Lane_fork_day == 'Shreveport':
    st.image(image= Image.open('images/Shreveport.png'),width=370)
    st.write('Shreveport does not have any fork, So we are considering the start day for the analysis.')
    result2=pd.read_csv('data/fork/time_S_day.csv')
    chart= alt.Chart(result2).mark_bar( color='orange', size = 30).encode(
        x = alt.X('weekday',axis=alt.Axis(labelAngle=0),sort=alt.EncodingSortField(field="weekday", op="count", order='ascending')),
        y=alt.Y('Count'),
        tooltip=["Count",'weekday']
    ).properties (title='Start Day of Shipments (Shreveport lane)',width = 400)
    st.subheader('Chart 2.2.D: Start Day of Shipments (Shreveport lane)')
    chart
    ### Weekday

##########################################################################
### Stop analysis text
st.header("3.0 Stop Analysis")
stops= pd.read_csv('data/text/Stop Analysis.csv')
st.subheader('Table 3.0: Overview of Stop Analysis')
st.write(stops)

### Map Single Stop
st.header("3.1 Shipments with one stop")
Lane_map = st.radio("Select Lane: Shipments with 1 Stop",('Groveport','Olive','Shreveport'))
if Lane_map == 'Groveport':
        ####### text
        st.subheader('Map 3.1.A: Shipments with 1 Stop (Groveport lane)')
        
        ####### data
        map_g_1= pd.read_csv('3dmap_data/G_just1stop.csv')
        coor_g_l_city= pd.read_json('3dmap_data/coor_g.json')
        coor_g_l=pd.read_json('3dmap_data/coor_g_l.json')
        coor_g_c_bypass=pd.read_json('3dmap_data/coor_g_c.json')
        df_g = pd.DataFrame({
        'lat':[39.8452332],
        'lon':[-82.9143159],
        'name':['Groveport end']
        })
        df_g_start = pd.DataFrame({
        'lat':[37.98829],
        'lon':[-85.71463],
        'name':['Groveport start']
        })
        data = pd.read_json("3dmap_data/geo_grove.json")

        #plot
        c_bypass=pdk.Layer(
        "TripsLayer",
        coor_g_c_bypass,
        get_path="coordinates",
        get_color=[20, 100, 753],
        opacity=0.8,
        width_min_pixels=5,
        ),

        l_city=pdk.Layer(
        "TripsLayer",
        coor_g_l_city,
        get_path="coordinates",
        get_color=[20, 100, 753],
        opacity=0.8,
        width_min_pixels=5,
        ),

        g_route=pdk.Layer(
        "TripsLayer",
        coor_g_l,
        get_path="coordinates",
        get_color=[20, 100, 753],
        opacity=0.8,
        width_min_pixels=5,
        ),

        barstop=pdk.Layer(
        "HexagonLayer",
        map_g_1,
        get_position=["lon", "lat"],
        auto_highlight=True,
        radius=4600,
        elevation_scale=150,
        pickable=True,
        elevation_range=[0, 500],
        extruded=True,
        coverage=1,
        ),
        endpt= pdk.Layer(
        'ScatterplotLayer',
        df_g,
        get_position='[lon, lat]',
        get_color='[500, 0, 0, 500]',
        get_radius=2000,
        radius_scale=2,
        ),
        startpt= pdk.Layer(
        'ScatterplotLayer',
        df_g_start,
        get_position='[lon, lat]',
        get_color='[0, 500, 0, 500]',
        get_radius=2000,
        radius_scale=2,
        ),
        icon_data = {
            "url": "https://img.icons8.com/material/96/000000/place-marker--v1.png",
            "width": 128,
            "height":128,
            "anchorY": 128
        }
        
        data['icon_data']= None
        for i in data.index:
            data['icon_data'][i] = icon_data

        view_state = pdk.ViewState(
            longitude=-84.512016,
            latitude=39.103119,
            zoom=7,
            pitch=60
        )

        icon_layer = pdk.Layer(
            type='IconLayer',
            data=data,
            get_icon='icon_data',
            get_size=4,
            pickable=True,
            size_scale=15,
            get_position='coordinates'
        )
        tooltip = {
        "html": "<b>Name:</b> {name}<br/><b>Shipment Count :</b> {elevationValue} <br/> <b>Shipment Count :</b> {count} <br/><b>Stop type:</b>  {type} <br/> <b>max stop in minutes:</b> {max} <br/> <b>min stop in minutes:</b> {min} <br/> ",
        "style": {
                "backgroundColor": "steelblue",
                "color": "white",
                "z-index": 2,
        }
        }
        r = pdk.Deck(layers=[icon_layer,barstop,c_bypass,l_city,g_route,endpt,startpt], map_style="mapbox://styles/mapbox/light-v9",initial_view_state=view_state, tooltip=tooltip)
        # r = pdk.Deck(layers=[g_route,l_city,endpt,startpt,c_bypass], map_style="mapbox://styles/mapbox/light-v9",initial_view_state=view_state, tooltip=tooltip)
        
        
        st.image(image= 'images/3d_legends.png', width=300)
        r


elif Lane_map == 'Olive':
        st.subheader('Map 3.1.B: Shipments with 1 Stop (Olive Lane)')
        map_o_1 = pd.read_csv('3dmap_data/O_1stop.csv')
        coor_o1= pd.read_json('3dmap_data/coor_o.json')
        coor_obypass= pd.read_json('3dmap_data/coor_o_bypass.json') 
        df_o1 = pd.DataFrame({
        'lat':[34.961766],
        'lon':[-89.829872],
        'name':['Olive branch']
        })

        df_o1_start= pd.DataFrame({
        'lat':[37.9882],
        'lon':[-85.714],
        'name':['Olive branch start']
        })    

        data = pd.read_json("3dmap_data/geo_olive.json")
        
        trip=pdk.Layer(
        "TripsLayer",
        coor_o1,
        get_path="coordinates",
        get_color=[20, 100, 753],
        opacity=0.8,
        width_min_pixels=5,
        ),

        bypass= pdk.Layer(
        "TripsLayer",
        coor_obypass,
        get_path="coordinates",
        get_color=[20, 100, 753],
        opacity=0.8,
        width_min_pixels=5,
        ),

        barstop= pdk.Layer(
        "HexagonLayer",
        data=map_o_1,
        get_position=["lon", "lat"],
        auto_highlight=True,
        radius=4600,
        elevation_scale=150,
        pickable=True,
        elevation_range=[0, 500],
        extruded=True,
        coverage=1,
        ),
        endpt= pdk.Layer(
        'ScatterplotLayer',
        df_o1,
        get_position='[lon, lat]',
        get_color='[500, 0, 0, 500]',
        get_radius=2000,
        radius_scale=3,
        ),
        startpt= pdk.Layer(
        'ScatterplotLayer',
        df_o1_start,
        get_position='[lon, lat]',
        get_color='[0, 500, 0, 500]',
        get_radius=2000,
        radius_scale=3,
        ),

        icon_data = {
        "url": "https://img.icons8.com/material/96/000000/place-marker--v1.png",
        "width": 128,
        "height":128,
        "anchorY": 128
        }
    
        data['icon_data']= None
        for i in data.index:
            data['icon_data'][i] = icon_data

        view_state = pdk.ViewState(
            longitude=-86.767960,
            latitude=36.174465,
            zoom=7,
            pitch=60
        )

        icon_layer = pdk.Layer(
            type='IconLayer',
            data=data,
            get_icon='icon_data',
            get_size=4,
            pickable=True,
            size_scale=15,
            get_position='coordinates'
        )
        tooltip = {
        "html": "<b>Name:</b> {name}<br/><b>Shipment Count :</b> {elevationValue} <br/> <b>Shipment Count :</b> {count} <br/><b>Stop type:</b>  {type} <br/> <b>max stop in minutes:</b> {max} <br/> <b>min stop in minutes:</b> {min} <br/> ",
        "style": {
                "backgroundColor": "steelblue",
                "color": "white",
                "z-index": 2,
        }
        }
        r = pdk.Deck(layers=[icon_layer,barstop,trip,bypass,endpt,startpt], map_style="mapbox://styles/mapbox/light-v9",initial_view_state=view_state, tooltip=tooltip)
        
        # r = pdk.Deck(layers=[trip,bypass,endpt,startpt], map_style="mapbox://styles/mapbox/light-v9",initial_view_state=view_state, tooltip=tooltip)
        
        st.image(image= 'images/3d_legends.png', width=300)
        r

elif Lane_map == 'Shreveport':
    st.subheader('Map 3.1.C: Shipments with 1 Stop (Shreveport Lane)')
    map_s_1_up = pd.read_csv('3dmap_data/S_1stop_updated.csv')

    coor_s= pd.read_json('3dmap_data/coor_s.json')
    df_s1 = pd.DataFrame({
        'lat':[32.408259],
        'lon':[-93.698005],
        'name':['Shreveport branch']
        })  
    df_s1_start=  pd.DataFrame({
        'lat':[38.0051691],
        'lon':[-85.7067154],
        'name':['Shreveport branch']
        })  
    data = pd.read_json("3dmap_data/geo_shrev.json")
    trip=pdk.Layer(
        "TripsLayer",
        coor_s,
        get_path="coordinates",
        get_color=[20, 100, 753],
        opacity=0.8,
        width_min_pixels=5,
        ),
    barstop= pdk.Layer(
        "HexagonLayer",
        data=data,
        get_position=["lon", "lat"],
        auto_highlight=True,
        radius=4600,
        elevation_scale=150,
        pickable=True,
        elevation_range=[0, 500],
        extruded=True,
        coverage=1,
        ),
    endpt= pdk.Layer(
        'ScatterplotLayer',
        df_s1,
        get_position='[lon, lat]',
        get_color='[500, 0, 0, 500]',
        get_radius=2000,
        radius_scale=3,
        ),
    startpt= pdk.Layer(
        'ScatterplotLayer',
        df_s1_start,
        get_position='[lon, lat]',
        get_color='[0, 500, 0, 500]',
        get_radius=2000,
        radius_scale=3,
        ),
    icon_data = {
        "url": "https://img.icons8.com/material/96/000000/place-marker--v1.png",
        "width": 128,
        "height":128,
        "anchorY": 128
    }
    
    data['icon_data']= None
    for i in data.index:
        data['icon_data'][i] = icon_data

    view_state = pdk.ViewState(
        longitude=-89.971107,
        latitude=35.117500,
        zoom=6,
        pitch=60
    )

    icon_layer = pdk.Layer(
        type='IconLayer',
        data=data,
        get_icon='icon_data',
        get_size=4,
        pickable=True,
        size_scale=15,
        get_position='coordinates'
    )
    tooltip = {
    "html": "<b>Name:</b> {name}<br/> <b>Shipment Count :</b> {count} <br/><b>Stop type:</b>  {type} <br/> <b>max stop in minutes:</b> {max} <br/> <b>min stop in minutes:</b> {min} <br/> ",
    "style": {
            "backgroundColor": "steelblue",
            "color": "white",
            "z-index": 2,
    }
    }
    r = pdk.Deck(layers=[icon_layer,barstop,trip,endpt,startpt], map_style="mapbox://styles/mapbox/light-v9",initial_view_state=view_state, tooltip=tooltip)
    # r = pdk.Deck(layers=[trip,endpt,startpt], map_style="mapbox://styles/mapbox/light-v9",initial_view_state=view_state, tooltip=tooltip)
    st.image(image= 'images/3d_legends.png', width=300)
    r
##########################################################################
### Map Multi Stops
st.header("3.2 Shipments with more than one stop")
Lane_map2 = st.radio("Select Lane: Shipments with more than one stops",('Olive','Shreveport'))

if Lane_map2 == 'Olive':
    st.subheader('Map 3.2.A: Shipments with more than one stop (Olive lane)')
    map_o_2 = pd.read_csv('3dmap_data/O_2stop.csv')
    coor_o1= pd.read_json('3dmap_data/coor_o.json')
    coor_obypass= pd.read_json('3dmap_data/coor_o_bypass.json') 
    df_o1 = pd.DataFrame({
        'lat':[34.961766],
        'lon':[-89.829872],
        'name':['Olive branch']
        })

    df_o1_start= pd.DataFrame({
        'lat':[37.9882],
        'lon':[-85.714],
        'name':['Olive branch start']
        })     

    data = pd.read_json("3dmap_data/geo_olive2.json")
        
    trip=pdk.Layer(
        "TripsLayer",
        coor_o1,
        get_path="coordinates",
        get_color=[20, 100, 753],
        opacity=0.8,
        width_min_pixels=5,
        ),

    bypass= pdk.Layer(
        "TripsLayer",
        coor_obypass,
        get_path="coordinates",
        get_color=[20, 100, 753],
        opacity=0.8,
        width_min_pixels=5,
        ),

    barstop= pdk.Layer(
        "HexagonLayer",
        data=map_o_2,
        get_position=["lon", "lat"],
        auto_highlight=True,
        radius=4600,
        elevation_scale=150,
        pickable=True,
        elevation_range=[0, 500],
        extruded=True,
        coverage=1,
        ),
    endpt= pdk.Layer(
        'ScatterplotLayer',
        df_o1,
        get_position='[lon, lat]',
        get_color='[500, 0, 0, 500]',
        get_radius=2000,
        radius_scale=3,
        ),
    startpt= pdk.Layer(
        'ScatterplotLayer',
        df_o1_start,
        get_position='[lon, lat]',
        get_color='[0, 500, 0, 500]',
        get_radius=2000,
        radius_scale=3,
        ),

    icon_data = {
        "url": "https://img.icons8.com/material/96/000000/place-marker--v1.png",
        "width": 128,
        "height":128,
        "anchorY": 128
        }
    
    data['icon_data']= None
    for i in data.index:
        data['icon_data'][i] = icon_data

    view_state = pdk.ViewState(
            longitude=-86.767960,
            latitude=36.174465,
            zoom=7,
            pitch=60
        )

    icon_layer = pdk.Layer(
            type='IconLayer',
            data=data,
            get_icon='icon_data',
            get_size=4,
            pickable=True,
            size_scale=15,
            get_position='coordinates'
        )
    tooltip = {
        "html": "<b>Name:</b> {name}<br/><b>Shipment Count :</b> {elevationValue} <br/> <b>Shipment Count :</b> {count} <br/><b>Stop type:</b>  {type} <br/> <b>max stop in minutes:</b> {max} <br/> <b>min stop in minutes:</b> {min} <br/> ",
        "style": {
                "backgroundColor": "steelblue",
                "color": "white",
                "z-index": 2,
        }
        }
    r = pdk.Deck(layers=[icon_layer,barstop,trip,bypass,endpt,startpt], map_style="mapbox://styles/mapbox/light-v9",initial_view_state=view_state, tooltip=tooltip)
    st.image(image= 'images/3d_legends.png', width=300)
    r

elif Lane_map2 == 'Shreveport':
    st.subheader('Map 3.2.B: Shipments with more than one stop (Shreveport lane)')      
    map_s_1_up = pd.read_csv('3dmap_data/S_2stop.csv')

    coor_s= pd.read_json('3dmap_data/coor_s.json')
    df_s1 = pd.DataFrame({
        'lat':[32.408259],
        'lon':[-93.698005],
        'name':['Shreveport branch']
        })  
    df_s1_start=  pd.DataFrame({
        'lat':[38.0051691],
        'lon':[-85.7067154],
        'name':['Shreveport branch']
        })  
    data = pd.read_json("3dmap_data/geo_shrev2.json")
    trip=pdk.Layer(
        "TripsLayer",
        coor_s,
        get_path="coordinates",
        get_color=[20, 100, 753],
        opacity=0.8,
        width_min_pixels=5,
        ),
    barstop= pdk.Layer(
        "HexagonLayer",
        data=data,
        get_position=["lon", "lat"],
        auto_highlight=True,
        radius=4600,
        elevation_scale=150,
        pickable=True,
        elevation_range=[0, 500],
        extruded=True,
        coverage=1,
        ),
    endpt= pdk.Layer(
        'ScatterplotLayer',
        df_s1,
        get_position='[lon, lat]',
        get_color='[500, 0, 0, 500]',
        get_radius=2000,
        radius_scale=3,
        ),
    startpt= pdk.Layer(
        'ScatterplotLayer',
        df_s1_start,
        get_position='[lon, lat]',
        get_color='[0, 500, 0, 500]',
        get_radius=2000,
        radius_scale=3,
        ),
    icon_data = {
        "url": "https://img.icons8.com/material/96/000000/place-marker--v1.png",
        "width": 128,
        "height":128,
        "anchorY": 128
    }
    
    data['icon_data']= None
    for i in data.index:
        data['icon_data'][i] = icon_data

    view_state = pdk.ViewState(
        longitude=-89.971107,
        latitude=35.117500,
        zoom=7,
        pitch=60
    )

    icon_layer = pdk.Layer(
        type='IconLayer',
        data=data,
        get_icon='icon_data',
        get_size=4,
        pickable=True,
        size_scale=15,
        get_position='coordinates'
    )
    tooltip = {
    "html": "<b>Name:</b> {name}<br/> <b>Shipment Count :</b> {elevationValue} <br/><br/> <b>Shipment Count :</b> {count} <br/><b>Stop type:</b>  {type} <br/> <b>max stop in minutes:</b> {max} <br/> <b>min stop in minutes:</b> {min} <br/> ",
    "style": {
            "backgroundColor": "steelblue",
            "color": "white",
            "z-index": 2,
    }
    }
    r = pdk.Deck(layers=[icon_layer,barstop,trip,endpt,startpt], map_style="mapbox://styles/mapbox/light-v9",initial_view_state=view_state, tooltip=tooltip)
    
    st.image(image= 'images/3d_legends.png', width=300)
    r



################################################################################################
###################################################################################################
###################################################################################################
# with st.echo():
from streamlit_folium import folium_static
import folium

########### map functions
def draw_polylines(points, speeds, map):
    colors = [speed_color(x) for x in speeds]
    n = len(colors)
    if n != len(points):
            raise ValueError
    i = 0
    j = 1
    curr = colors[0]
    while i < n and j < n:
        if colors[i] != colors[j]:
            line = folium.PolyLine(points[i:j], color=curr, weight=2.5, opacity=1)
            line.add_to(m)
            curr = colors[j]
            i = j
        j += 1
    if i < j:
        folium.PolyLine(points[i:j], color=curr, weight=2.5, opacity=1).add_to(m)

def speed_color(speed):
    if speed < 0:
        raise ValueError
    elif speed >= 0 and speed < 20:
        return 'red'
    elif speed >= 20 and speed < 60:
        return 'yellow'
    else:
        return 'green'
########### data

st.header("4.0 Map for Speed analysis")
Speed_MapG = st.radio("Select Lane: Map for Speed analysis",('Groveport','Lockbourne','Olive','Shreveport'))

if Speed_MapG == 'Groveport':
    st.subheader('Map 4.0.A: Speed Analysis of Groveport lane')
    df= pd.read_csv('data/speed_map/G_df.csv')
    m = folium.Map(location=[df['latitude'][0], df['longitude'][0]], zoom_start=7) 
    for item in list(df['shipment_id'].unique()):
        temp_df = df[df['shipment_id'] == item].reset_index()
        points = zip(temp_df['latitude'], temp_df['longitude'])
        points = list(points)
        draw_polylines(points, temp_df['speed'], m)
    st.image(image= 'images/speed_legend.png', width=500)
    folium_static(m)

elif Speed_MapG == 'Olive':
    st.subheader('Map 4.0.B: Speed Analysis of Olive lane')
    df= pd.read_csv('data/speed_map/O_df.csv')
    m = folium.Map(location=[df['latitude'][0], df['longitude'][0]], zoom_start=7) 
    for item in list(df['shipment_id'].unique()):
        temp_df = df[df['shipment_id'] == item].reset_index()
        points = zip(temp_df['latitude'], temp_df['longitude'])
        points = list(points)
        draw_polylines(points, temp_df['speed'], m)
    st.image(image= 'images/speed_legend.png', width=500)
    folium_static(m)

elif Speed_MapG == 'Lockbourne':
    st.subheader('Map 4.0.C: Speed Analysis of Lockbourne lane')
    df= pd.read_csv('data/speed_map/L_df.csv')
    m = folium.Map(location=[df['latitude'][0], df['longitude'][0]], zoom_start=7) 
    for item in list(df['shipment_id'].unique()):
        temp_df = df[df['shipment_id'] == item].reset_index()
        points = zip(temp_df['latitude'], temp_df['longitude'])
        points = list(points)
        draw_polylines(points, temp_df['speed'], m)
    st.image(image= 'images/speed_legend.png', width=500)
    folium_static(m)

elif Speed_MapG == 'Shreveport':
    st.subheader('Map 4.0.D: Speed Analysis of Shreveport lane')
    df= pd.read_csv('data/speed_map/S_df.csv')
    m = folium.Map(location=[df['latitude'][0], df['longitude'][0]], zoom_start=7) 
    for item in list(df['shipment_id'].unique()):
        temp_df = df[df['shipment_id'] == item].reset_index()
        points = zip(temp_df['latitude'], temp_df['longitude'])
        points = list(points)
        draw_polylines(points, temp_df['speed'], m)
    st.image(image= 'images/speed_legend.png', width=500)
    folium_static(m)
    

###################################################################################################
###################################################################################################
###################################################################################################
# z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')
# z = z_data.values
# sh_0, sh_1 = z.shape
# x, y = np.linspace(0, 1, sh_0), np.linspace(0, 1, sh_1)
# fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
# fig.update_layout(title='IRR', autosize=False,
# width=800, height=800,
# margin=dict(l=40, r=40, b=40, t=40))
# st.plotly_chart(fig)

# df= pd.read_csv('data/plotly/G_plotly.csv')
# # Time based window
# df['time_passed'] = df['device_time'] - df['start_time']
# df_2km = pd.DataFrame()
# for i in range(len(review_df)):
#   df_sample = df[df['shipment_id'] == review_df['shipment_id'][i]]
#   df_sample = df_sample[(df_sample['time_passed'] > review_df['20km_hours'][i])]
#   df_2km = pd.concat([df_2km, df_sample])

# df_2km.reset_index(drop=True, inplace=True)
# start_time_dict = df_2km.groupby('shipment_id')['device_time'].agg('min').to_dict()
# df_2km['start_time'] = df_2km['shipment_id'].map(start_time_dict)
# df_2km['time_passed'] = df_2km['device_time'] - df_2km['start_time']
# unq_shipment_list = list(df_2km['shipment_id'].unique())
# rolling_time_df = pd.DataFrame()
# route_length = int(pd.Timedelta('0 days 04:00:00').total_seconds() / 60)
# window = pd.Timedelta('0 days 00:30:00')

# for item in unq_shipment_list:
#   df_sample = df_2km[df_2km['shipment_id'] == item]
#   df_sample.reset_index(drop=True, inplace=True)
#   window_start_l = []
#   window_end_l = []
#   pings_l = []
#   rolling_sample = pd.DataFrame()
#   for i in range(route_length):
#     window_start = pd.to_timedelta(i, unit='min')
#     window_end = pd.to_timedelta(i, unit='min')+window
#     pings = len(df_sample[(df_sample['time_passed']>window_start) & (df_sample['time_passed']<window_end)])
#     window_start_l.append(window_start)
#     window_end_l.append(window_end)
#     pings_l.append(pings)
#   rolling_sample['start_min'] = window_start_l
#   rolling_sample['end_min'] = window_end_l
#   rolling_sample['pings'] = pings_l
#   rolling_sample['shipment_id'] = item
#   rolling_time_df = pd.concat([rolling_time_df,rolling_sample])

# #include_list = list(rolling_time_df[(rolling_time_df['start_min'] == 0) & (rolling_time_df['pings'] != 0)]['shipment_id'])
# rolling_mean_time_df = rolling_time_df.groupby(['start_min','end_min'])['pings'].agg('mean').reset_index()
# rolling_mean_time_df['start_min_int'] = [int(rolling_mean_time_df['start_min'][i].total_seconds()/60) \
#                                          for i in range(len(rolling_mean_time_df))]
# opening_increasing = go.Scatter(
#                 x=rolling_mean_time_df.start_min_int,
#                 y=rolling_mean_time_df.pings,
#                 line = dict(color = '#17BECF'),
#                 opacity = 0.8)
# data = [opening_increasing]
# layout = dict(
#     title = "Rolling mean (30 min window) of average pings"
# )

# fig = dict(data=data, layout=layout)
# py.iplot(fig, filename = "Manually Set Range")

# # Distance based window
# unq_shipment_list = list(df['shipment_id'].unique())
# rolling_df = pd.DataFrame()
# route_distance = 320
# window = 10

# for item in unq_shipment_list:
#   df_sample = df[df['shipment_id'] == item]
#   df_sample.reset_index(drop=True, inplace=True)
#   window_start_l = []
#   window_end_l = []
#   pings_l = []
#   rolling_sample = pd.DataFrame()
#   for i in range(route_distance):
#     window_start = i
#     window_end = i+window
#     pings = len(df_sample[(df_sample['distance_from_origin']>window_start) & (df_sample['distance_from_origin']<window_end)])
#     window_start_l.append(window_start)
#     window_end_l.append(window_end)
#     pings_l.append(pings)
#   rolling_sample['start_km'] = window_start_l
#   rolling_sample['end_km'] = window_end_l
#   rolling_sample['pings'] = pings_l
#   rolling_sample['shipment_id'] = item
#   rolling_df = pd.concat([rolling_df,rolling_sample])

# include_list = list(rolling_df[(rolling_df['start_km'] == 0) & (rolling_df['pings'] != 0)]['shipment_id'])
# rolling_mean_df = rolling_df[rolling_df['shipment_id'].isin(include_list)].groupby(['start_km','end_km'])['pings'].agg('mean').reset_index()

# opening_increasing = go.Scatter(
#                 x=rolling_mean_df.start_km,
#                 y=rolling_mean_df.pings,
#                 line = dict(color = '#17BECF'),
#                 opacity = 0.8)


# data = [opening_increasing]

# layout = dict(
#     title = "Rolling mean (10km window) of average pings"
# )

# fig = dict(data=data, layout=layout)
# st.plotly_chart(fig)
# py.iplot(fig, filename = "Manually Set Range")

###################################################################################################
###################################################################################################
###################################################################################################