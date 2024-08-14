import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.header('Analysis of Air Crashes from 1908 to 2024')
st.divider()
st.subheader('Air Crashes Data')
def load_data():
    data_file = 'aircrahesFullDataUpdated_2024.csv'
    df = pd.read_csv(data_file)
    # rename all columns in the dataset and save the changes back to the dataframe
    df = df.rename({'Year': 'year', 
                'Quarter': 'quarter', 
                'Month': 'month', 
                'Day': 'day', 
                'Country/Region': 'country/region',
                'Aircraft Manufacturer':'aircraft manufacturer', 
                'Aircraft': 'aircraft', 
                'Location': 'location', 
                'Operator': 'operator', 
                'Ground': 'ground',
                'Fatalities (air)' :'fatalities (air)', 
                'Aboard' : 'aboard'},axis=1
              )
       
    # Replaces all characters with values and empty string as applicable
    df['country/region'] = df['country/region'].str.replace('N/A', 'Other Region').str.replace('?', '').str.replace("'-",'Other Region')
    # Replace NaN with Other Region
    df['country/region'] = df['country/region'].fillna('Other Region', inplace=False)
    # Replaces all characters with values and empty string as applicable
    df['aircraft manufacturer'] = df['aircraft manufacturer'].str.replace('N/A', 'Other manufacturer').str.replace('?', '').str.replace('+', '')
    # Replace NaN with Other manufacturer
    df['aircraft manufacturer'] = df['aircraft manufacturer'].fillna('Other manufacturer', inplace=False)
    # Replace N/A with Other Aircraft
    # Replace question mark with an empty string
    df['aircraft'] = df['aircraft'].str.replace('N/A', 'Other Aircraft').str.replace('?', '')
    # Replace NaN with Other Aircraft
    df['aircraft'] = df['aircraft'].fillna('Other Aircraft', inplace=False)
    # Replace question mark with an empty string
    df['location'] = df['location'].str.replace('?', '')
    # Replace NaN with Others
    df['location'] = df['location'].fillna('Others', inplace=False)
    # To avoid comma on the year column, convert it so string
    df['year'] = df['year'].astype(str) 
    # Replace question mark with an empty string * Replace N/A with 'Other operator'
    # Trim white spaces
    df['operator'] = df['operator'].str.replace('?', '').str.replace('N/A', 'Other operator').str.strip()
    # Replace NaN with Other operator
    df['operator'] = df['operator'].fillna('Other operator', inplace=False)

    
    return df
df = load_data()

st.dataframe(df)

st.divider()
# select and display specific aircraft
# add a filter 
Aircraft = df['aircraft'].unique()
select_aircraft = st.sidebar.multiselect(
                    'Filter by Aircraft',
                    Aircraft)
filtered_table = df[df['aircraft'].isin(select_aircraft)]

# Variables for first metrics
if len(filtered_table) > 0:
    highest_ground_fatalities = filtered_table['ground'].max()
else:
    highest_ground_fatalities = df['ground'].max()
if len(filtered_table) > 0:
    highest_air_fatalities = filtered_table['fatalities (air)'].max()
else:
     highest_air_fatalities = df['fatalities (air)'].max()
if len(filtered_table) > 0:
    highest_no_aboard = filtered_table['aboard'].max()
else:
    highest_no_aboard = df['aboard'].max()

st.subheader('Metrics')

# Create first set of metrics (Highest Values)
col_1, col_2, col_3 = st.columns(3)

col_1.metric('Highest Ground Fatalities',f"{highest_ground_fatalities:,}")
col_2.metric('Highest Air Fatalities',highest_air_fatalities)
col_3.metric('Highest Number Aboard',highest_no_aboard)
# End of first metrics

# Variables for second metrics
if len(filtered_table) > 0:
    Avg_ground_fatalities = filtered_table['ground'].mean()
else:
    Avg_ground_fatalities = df['ground'].mean()
if len(filtered_table) > 0:
    Avg_air_fatalities = filtered_table['fatalities (air)'].mean()
else: 
    Avg_air_fatalities = df['fatalities (air)'].mean()
if len(filtered_table) > 0:
    Avg_no_aboard = filtered_table['aboard'].mean()
else:
     Avg_no_aboard = df['aboard'].mean()

# Create second set of metrics (Highest Values)
colA, colB, colC = st.columns(3)

colA.metric('Average Ground Fatalities',Avg_ground_fatalities)
colB.metric('Average Air Fatalities',Avg_air_fatalities)
colC.metric('Average Number Aboard',Avg_no_aboard)
# End of scond metrics

st.divider()

# add a filter table to the app
st.subheader('Filtered Table')
st.dataframe(filtered_table[['year', 'quarter', 'month',
                            'aircraft manufacturer', 
                            'aircraft','operator', 'ground',
                            'fatalities (air)', 'aboard']])
st.divider()

# Add charts visualization to the app

st.subheader('Charts for Visualization')

st.divider()
# Monthly Aircrashes Analysis
try:
    st.write('Total Monthly Aircrashes')
    if len(filtered_table) > 0:
        monthly_aircrashes = filtered_table.groupby('month')['fatalities (air)'].count()
    else:
        monthly_aircrashes = df.groupby('month')['fatalities (air)'].count()

    monthly_aircrashes_df = monthly_aircrashes.reset_index()

    plt.figure(figsize=(10,6))
    st.bar_chart(monthly_aircrashes_df,
                x = 'month',
                y = 'fatalities (air)')
except ValueError as v:
    st.error(
        """Error""" % v.reason
    )


# Trend in the number of aircraft crashes over the years
try:
    st.write('Trend in the Number of Aircraft Crashes over the Years')
    if len(filtered_table) > 0:
        crashes_per_year = filtered_table.groupby('year')['fatalities (air)'].count()
    else:
        crashes_per_year = df.groupby('year')['fatalities (air)'].count()
    
    crashes_per_year_df = crashes_per_year.reset_index()

    st.line_chart(crashes_per_year_df,
                  x='year', 
                  y = 'fatalities (air)')
except ValueError as v:
    st.error(
        """Error""" % v.reason
    )


# quarter of the year has the highest number of aircraft crashes
try:
    st.write('Quarter with the Highest Number of Aircraft Crashes')
    if len(filtered_table) > 0:
        aircrashes_per_quarter = filtered_table.groupby('quarter')['fatalities (air)'].count()
    else:
        aircrashes_per_quarter = df.groupby('quarter')['fatalities (air)'].count()

    aircrashes_per_quarter_df = aircrashes_per_quarter.reset_index()

    st.bar_chart(aircrashes_per_quarter_df,
                    x='quarter', 
                    y = 'fatalities (air)')
except ValueError as v:
    st.error(
        """Error""" % v.reason
    )

# fatalities vary across different aircraft manufacturers
try:
    st.write('Analysis of Fatalities Across Different Aircraft Manufacturers')
    if len(filtered_table) > 0:
        fatalities_per_manufacturer = filtered_table.groupby('aircraft manufacturer')['fatalities (air)'].count().reset_index()
    else: 
        fatalities_per_manufacturer = df.groupby('aircraft manufacturer')['fatalities (air)'].count().reset_index()
    
    fatalities_per_manufacturer_df = fatalities_per_manufacturer.reset_index()

    st.line_chart(fatalities_per_manufacturer_df,
                 x='aircraft manufacturer', 
                 y = 'fatalities (air)')
except ValueError as v:
    st.error(
        """Error""" % v.reason
    )

# Correlation btw Air fatalities, ground and Aboard
st.write('Correlation Analysis for Air Fatalities, Ground Fatalities and Number of People Aboard')
Aircrashes = df[['ground', 'fatalities (air)', 'aboard']]
Aircrashes.corr()
fig, ax = plt.subplots()
sns.heatmap(Aircrashes.corr(), ax=ax, annot=True, cmap='BuGn', vmin=-1, vmax=1)
st.write(fig)