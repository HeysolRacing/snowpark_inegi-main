import altair as alt
from snowflake.snowpark.session import Session
from config import connection_parameters
import streamlit as st
from PIL import Image
from style import divContainer,formatoNumero

@st.cache_resource
def snowsesion() -> Session:
    sesion = Session.builder.configs(connection_parameters).create()
    if sesion != None:
        print("Connected")
        sesion.use_database('inegi')
        print(sesion.sql("select current_warehouse(), current_database(), current_role()").collect()) 
        return sesion
    else:
        print("Connection Error: Unable to establish a connection to SnowFlake")

def run_query(sesion,query):
    try:
        return sesion.sql(query)
    except :
        print("Connection Error: Unable to establish a connection to SnowFlake")

#@st.experimental_memo() 
def inegiDataSet():
    st.set_page_config(
    page_title="INEGI App",
    page_icon="☻",
    layout="wide",
    initial_sidebar_state="expanded",)
    st.header("Mexico population rate")
    
    with st.sidebar:
        image = Image.open('img/inegi.png')
        st.image(image, caption='INEGI',width=220)
        add_n_hab = st.slider("Select the volume of the population (# residents):", 700000, 17000000,2125000 ,500000)
        query = "SELECT * FROM INEGI.PUBLIC.INEGI_MAPA where TOTAL_POPULATION > " + str(add_n_hab) + " order by TOTAL_POPULATION desc;"
        sesion = snowsesion()
        snowDF = run_query(sesion,query)
        snowPD = snowDF.to_pandas()
    
    col1,col2 = st.columns([3,1])
    with col1:
        with st.container():
            mapa = snowPD[['TOTAL_POPULATION','LATITUDE', 'LONGITUDE']]
            mapa = mapa.rename(columns={'LATITUD':'latitude', 'LONGITUD':'longitude'})
            st.map(mapa,zoom=4,use_container_width=True)
            
    with col2:
        with st.container():  
            st.write('Total values:') 
            totalpod = snowPD['TOTAL_POPULATION'].sum()
            formatoTotal = formatoNumero(totalpod)
            st.markdown(divContainer(), unsafe_allow_html=True)
            st.metric(label="Total" , value=formatoTotal, delta="2%",delta_color="inverse")
            #--  
            maxp = snowPD['TOTAL_POPULATION'].max()
            result_df = snowPD.loc[snowPD['TOTAL_POPULATION'] == maxp]
            st.markdown(divContainer(), unsafe_allow_html=True)
            formatMaxp = formatoNumero(maxp)
            label_max = str(result_df.loc[0].at['NOM_ENTIDAD'])
            st.metric(label="Major entity: " + label_max, value=formatMaxp, delta="5%",delta_color="inverse")

    with st.container():
        st.subheader('Histogram by entity > a ' + formatoNumero(add_n_hab) + ' residents')
        barDF = snowPD[['NOM_ENTIDAD','TOTAL_POPULATION']]
        chart = alt.Chart(barDF).mark_bar().encode(
        x='NOM_ENTIDAD',
        y='TOTAL_POPULATION',
        ).interactive()
        st.altair_chart(chart, use_container_width=True)        
       
    with st.container():
        st.table(snowPD)  

inegiDataSet()

