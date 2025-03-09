'''
This dahsboard is built to consolidate data to form a holistic picture 
of the world economy with individual micro focus

Data sources
1. Annual macro data from the world bank
2. Quarterly data from individual economic bureaus

Outputs:
1. Terrain understanding of the global landscape
    1. Data picture
    2. 
2. Macro activity forecasts for top 2 econmics

Use:


Open dash:
In terminal: streamlit run 00_dash_macro.py

'''

import pandas as pd  # pip install pandas
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from Functions.db_call import manage_sqlite_db
from Functions.df_colRename import colrename_Transpose

# ------ 1. Set up config ------------
st.set_page_config(page_title="Macro Dashboard",
                   page_icon=":globe_with_meridians:",
                   layout="wide")

# ------- 2. Import Dataset(s) -----------
project_directory = '.' # Update relative path from project folder

## ------2a. GDP (Countries data) ----------
database_name = 'Data_worldgdp_countryIndexed_2025-02-12' 
df_gdp_c = manage_sqlite_db(relative_project_dir=project_directory ,db_name=database_name)

database_name = 'Data_worldgdp_timeIndexed_2025-02-13' 
df_gdp_t = manage_sqlite_db(relative_project_dir=project_directory ,db_name=database_name)
df_gdp_t.set_index('year')

database_name = 'Data_RealGDPgrowth_timeIndexed_2025-02-16'
df_RgdpG_t = manage_sqlite_db(relative_project_dir=project_directory ,db_name=database_name) 
df_RgdpG_t = df_RgdpG_t.set_index('quarter')

database_name = 'Data_NominalGdpGrowth_timeIndexed_2025-02-17'
df_nomGdpG_t = manage_sqlite_db(relative_project_dir=project_directory ,db_name=database_name) 
df_nomGdpG_t = df_nomGdpG_t.set_index('year')

# ------- 3a. Sidebar to create vairables with filtered data ----------
# 3a. Sidebar for filtering data (Country)
st.sidebar.header("Select data for GDP Trending:")
economy_gdp = st.sidebar.multiselect(           # output is a list
    "Select Economy:",
    options=df_gdp_c['economy'].unique(),
    default=['USA', 'CHN', 'DEU']
)

# ------- 3b. create a new dataframe with filtered results ------------
#df_selection = df_gdp_w.query("economy in @economy")
gdp_list_selection = economy_gdp #['USA', 'CHN', 'DEU']

# ---------4. Create Mainpage ----------

st.title(":globe_with_meridians: Global Macro Dashboard")
st.write(""" 
        Created by: Matty C.
         This macro dashboard is built to provide a an introduction to the world's macro economy by
         1. Providing an interactive visuals of the top 3 markets
         2. Provide a forecast of the next critical dates 
         3. Provide implications for possible shocks @ critical dates (i.e. Growth, Inflation and Central Bank rates, Leadership changes, etc. )
         """)
#st.markdown("##")

#/////////////////////////////////////////////////////////////////////     A. (SR) GDP (Global, past 4 quarters, Next Target)
st.header("Part 1: GDP @ Global and Country level")
st.write("""
         These charts identify the largest economies by size and trend of top 30 economies. 
         - Aim to identify economy 'health' by matching growth to national targets
         - Aim to identify developmental issues through Real GDP growth
         """)

## Data Cleaning and mapping - Tree map (To convert into a function)
# Adjust for Billioons
df_treemap = df_gdp_c.head(30).copy()
df_treemap['YR2023_B'] = df_treemap['2023']/1000000000
df_treemap.reset_index(inplace=True, drop=True)
#df_treemap.info()

# Print treemap : Assuming df is your DataFrame
global_GDP = px.treemap(df_treemap,
                 path=['economy'],
                 values='YR2023_B',
                 title='GDP Treemap by Economy (YR2023) in Billions'
                )

## Data Cleaning - Global trend ( dataset : df_gdp_countries)

# Plot the line graph
global_GDP_trend = px.line(
    df_gdp_t,
    x=df_gdp_t['year'],
    y=gdp_list_selection,
    #color_discrete_map= df_selection, #{df_selection: 'blue'},  # Map a specific color to the selected column
    title='GDP Over Time <br> Source: XXX',
    labels={'GDP': 'GDP (Trillions)', 'Year': 'Year'},
    template='plotly_white'
)

global_GDP_trend.update_layout(
    legend_title_text="Economy",
    yaxis_title="GDP (Trillions)",
    xaxis_title="Year",
)

## Plotting - Nominal GDP growth (annual)
global_NomGDPgrowth_trend = px.line(
    df_nomGdpG_t,
    x=df_nomGdpG_t.index,
    y=gdp_list_selection,
    #color_discrete_map= df_selection, #{df_selection: 'blue'},  # Map a specific color to the selected column
    title='Nominal GDP Growth Over Time',
    #labels={'GDP': 'GDP (Trillions)', 'Year': 'Year'},
    template='plotly_white'
)

global_NomGDPgrowth_trend.update_layout(
    legend_title_text="Annual growth",
    yaxis_title="Percent, %",
    xaxis_title="Year",
)

# ## Data Cleaning - Real GDP growth
global_rgdp_trend = px.line(
    df_RgdpG_t,
    x=df_RgdpG_t.index,
    y=gdp_list_selection,
    #color_discrete_map= df_selection, #{df_selection: 'blue'},  # Map a specific color to the selected column
    title='REAL GDP growth (last 10 quarters), <br> i.e. Inflation adjusted growth',
    #labels={'GDP': 'GDP (Trillions)', 'Year': 'Year'},
    template='plotly_white'
)

global_rgdp_trend.update_layout(
    legend_title_text="Real GDP Growth",
    yaxis_title="Percent, %, YOY",
    xaxis_title="Quarters",
)

## A-1 Arranging charts with columns
left_column_A1, right_column_A1 = st.columns(2)
left_column_A1.plotly_chart(global_GDP, use_container_width=True)
right_column_A1.plotly_chart(global_GDP_trend, use_container_width=True)

## A-1 Arranging charts with columns
left_column_A1_2, middle_column_A1_2, right_column_A1_2 = st.columns(3)

left_column_A1_2.plotly_chart(global_NomGDPgrowth_trend, use_container_width=True)     #annual growth rate, non-inflation adjusted
middle_column_A1_2.plotly_chart(global_rgdp_trend, use_container_width=True)
# Add content to the first column
with right_column_A1_2:
    st.write("""
             ### Historical growth rates
             - US   : Growth rate: ? % / Real Growth rate 2%
             - CHN  : Growth rate: 4.5 - 5% / Real Growth rate ? %
             
             ### Projected
             - US   : Growth rate: ? % / Real Growth rate 2%
             - CHN  : Growth rate: 4.5 - 5% / Real Growth rate ? %
             """)
    
## A-1 Key dates and notes in columns
st.subheader("Notes & Upcoming Key dates:")
# Create two columns
gdp_col1, gdp_col2, gdp_col3 = st.columns(3)

# Add content to the first column
with gdp_col1:
    st.subheader("US")
    st.write("""
             KEY DATES:
             - Jan 20 : Trump Inauguration           -  What are Trump's policies, erasing for noise
             - Jan 30 : US GDP YOY quarterly updates -  where is this on the bell curve? is this above or below average and by how many std deviation?
             - **30th Jan**: US GDP Results for Q4 2024 (Actual: 2.3%, Forecast: 2.5%, Last: 3.1%)  
             - **XXth Apr**: US GDP Results for Q1 2025 (Actual: X %, Forecast: X%, Last: X%) 
             
             Note: Faster than average US GDP growth? **to investigate in stationarity of annual US growth data (Anyway, quarterly data is YOY growth anyway)**"""
             )

# Add content to the second column
with gdp_col2:
    st.subheader("CHINA:")
    st.write(""" 
             KEY DATES:
             
             Economic Agenda: Stagnant Chinese GDP in the last 3 years, reforms? **what has stagnated the Chinese economy and what are the next measures?**
             - Central Economic Work Conference (CEWC), held on December 11-12, 2024 (outlined China’s economic priorities and strategies for 2025)

             """)
  
# Add content to the second column
with gdp_col3:
    st.subheader("Rest of the world:")
    st.write(""" 
             KEY DATES:
             
             Economic Agenda:
             - EU (DEU): 
             - JPN : Japanese recession and negative GDP growth **What is the purpose of the japanese government driving the economy into recession?**
             - IND : Parallel growth of German and Indian markets
             - BRA : 
             """)  

#/////////////////////////////////////////////////////////////////////     B. (SR) Inflation (Global, past 4 quarters, Next Target)
st.header("Part 2: Inflation @ Global and Country level")
st.write("These charts identify the inflation situation globally and at national levels")

# Data Inflation
database_name = 'Data_inflation_timeIndexed_2025-02-10'
df_inf_t = manage_sqlite_db(relative_project_dir=project_directory ,db_name=database_name) 
df_inf_t = df_inf_t.set_index('year')

# side bar for inflation

# 3a. Sidebar for filtering data (Country)
st.sidebar.header("Select data for Inflation (Historical):")
economy_inf = st.sidebar.multiselect(           # output is a list
    "Select Economy:",
    options=df_inf_t.columns.unique(),
    default=['USA', 'CHN', 'DEU']
)

# ------- 3b-1. Inflation (world bank)------------
#df_selection = df_gdp_w.query("economy in @economy")
inf_list_selection = economy_inf #['USA', 'CHN', 'DEU']

# 3. Plot 

# Plot the line graph
global_inf_trend = px.line(
    df_inf_t,
    x=df_inf_t.index,
    y=inf_list_selection,
    #color_discrete_map= df_selection, #{df_selection: 'blue'},  # Map a specific color to the selected column
    title='Inflation Over Time',
    #labels={'GDP': 'GDP (Trillions)', 'Year': 'Year'},
    template='plotly_white'
)

global_inf_trend.update_layout(
    legend_title_text="Annual Inflation",
    yaxis_title="Percent, %",
    xaxis_title="Year",
)

st.plotly_chart(global_inf_trend)

# ------- 3b-2. Inflation (last 4 quarters)------------


#/////////////////////////////////////////////////////////////////////     C. (SR) Employment 



#/////////////////////////////////////////////////////////////////////     D. (LR) Fiscal stability (Non-current Debt **)


#/////////////////////////////////////////////////////////////////////     G. Central bank targets 
st.header("Part 3: Interest rate targets for Major central banks (FED, PBC, ECB + MAS)")
st.write("These charts identify the interest rate targets for the major central banks and impact (Price stability, Demand and Employment stability and Fiscal sustainability)")
#
# ---------7. styling and removing watermarks ----------

st.header("Annex: Notes and References:")
st.write(""" 
         The data is extracted and transfromed from World Bank and OCED sources. 
         
         Data chosen is motivated from the Real Business Cycle (RBC) model 
         (i.e. income(y), Investment(I), consumption(c), interest rates(i), capital(k), tax(t), wage(w), rent(r) )
         """)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
