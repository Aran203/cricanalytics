import streamlit as st
import pandas as pd
import altair as alt

def wagon_wheel(batter, ipl_data,seasons,venues):
    zones = [1,2,3,4,5,6,7,8] 
    values = getZones(batter, ipl_data,seasons, venues)  
    equal_angle = 45  
    source = pd.DataFrame({
        "Zone": zones, 
        "value": [equal_angle] * len(zones), 
        "shots": values,
        "angle": [i * equal_angle + equal_angle / 2 for i in range(len(zones))] ,
        "rads":[5,4,4,5,5,4,4,5]

    })

    chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
        color=alt.Color(field="shots", type="ordinal", legend = None), 
        theta=alt.Theta(field="value", type="quantitative"),  
        order = alt.Order(field="Zone"),
        tooltip=["Zone", "Zone"]
    )
    

    text = alt.Chart(source).mark_text(size=12, color='black').encode(
        theta=alt.Theta(field="angle", type="quantitative"), 
        radius=alt.value(100), 
        text=alt.Text(field="shots", type="quantitative"), 
    )
    

    final_chart = chart + text
    return final_chart

def getZones(playername, df, seasons=None, venues=None):
    batter = df.loc[df['bat'] == playername]  
    col = df.columns.get_loc('batruns')
    if seasons:
        batter = batter[batter['season'].isin(seasons)]  

    if venues:
        # venue_pattern = '|'.join(venues)
        # print(venue_pattern)
        batter = batter[batter['ground'].isin(venues)]

    zones = [0, 0, 0, 0, 0, 0, 0, 0]

    for row in batter.itertuples(index=True, name="Row"):
        zones[int(row.wagonZone) - 1] += row[col]

    return zones

