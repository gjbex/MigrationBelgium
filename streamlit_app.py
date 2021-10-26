#!/usr/bin/env python

import altair as alt
import altair_saver
import pandas as pd
import streamlit as st

BE_GEO_URL = 'https://gist.githubusercontent.com/jandot/ba7eff2e15a38c6f809ba5e8bd8b6977/raw/eb49ce8dd2604e558e10e15d9a3806f114744e80/belgium_municipalities_topojson.json'
BE_MUNICIPALITIES_FEATURE = 'BE_municipalities'
DATA_URL = 'https://github.com/gjbex/MigrationBelgium/raw/main/data/mia_2021.xlsx'
MISSING_COLOR = 'white'
SCHEME = 'lightgreyteal'

def create_topo_data(url, feature):
    return alt.topo_feature(url, feature)

def create_plot(topo_data, data, column_name, data_type, tooltip_columns=None,
                stroke='darkgrey', strokeWidth=0.9, legend_title=None,
                scheme='reds', scale_type='linear', missing_color='white'):
    lookup_columns = [column_name]
    if tooltip_columns is not None:
        lookup_columns.extend(tooltip_columns)
    if legend_title is None:
        legend_title = column_name
    base = alt.Chart(topo_data) \
            .mark_geoshape() \
            .encode(
                color=alt.Color(f'{column_name}:{data_type}',
                                legend=alt.Legend(title=legend_title), 
                                scale=alt.Scale(scheme=scheme, type=scale_type)),
                tooltip=[f'{tooltip_columns[0]}:N', alt.Tooltip(f'{tooltip_columns[1]}:N', format='.2%')],
            ).transform_lookup(
                lookup='properties.CODE_INS',
                from_=alt.LookupData(data, 'niscode', lookup_columns)
            ).properties(
                width=600,
                height=450,
            )
    return alt.Chart(topo_data).mark_geoshape(stroke=stroke, strokeWidth=strokeWidth) \
            .encode(
                color=alt.value(missing_color),
                opacity=alt.value(0.9),
            ) + base

if __name__ == '__main__':
    st.title('Migratie achtergrond in Belgie')
    st.markdown('Gegevens verzameld door Jan Hertogen 1 januari 2021.')
    topo_data = create_topo_data(BE_GEO_URL, BE_MUNICIPALITIES_FEATURE)
    data = pd.read_excel(DATA_URL)
    countries = data.columns[5:]
    left_column, right_column = st.columns(2)
    with left_column:
        column_name = st.selectbox('Land van herkomst', countries)
    with right_column:
        scale_type = st.selectbox('weergave', ['linear', 'log'])
    data_type='Q'
    tooltip_names = ['Gemeente', column_name]
    plot = create_plot(topo_data=topo_data, data=data,
                       column_name=column_name, data_type=data_type,
                       tooltip_columns=tooltip_names, scheme=SCHEME,
                       scale_type=scale_type, missing_color=MISSING_COLOR)
    st.write(plot)
