import streamlit as st
import pandas as pd
import geopandas as gpd
from io import StringIO

def to_geo(df: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Convert DataFrame with Geometry Strings (CRS=4326) to GeoDataFrame
    """
    geo = gpd.GeoSeries.from_wkt(df['geometry'].to_list(), crs=4326)
    gdf = gpd.GeoDataFrame(df, geometry=geo)
    return gdf

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)
    
    geo_col_name = st.text_input('Geometry Columns Name', 'geometry')
    geo_col_crs = st.text_input('Geometry Columns CRS', '4326')

    if st.button('Preview Data'):
        st.write(df.sample(3).T)

    if st.button('Convert Geo to Lat, Lon'):
        geo = gpd.GeoSeries.from_wkt(df[geo_col_name].to_list(), crs=geo_col_crs)
        df = gpd.GeoDataFrame(df, geometry=geo)
        df['lon'] = geo.x
        df['lat'] = geo.y
        st.map(df)

        csv = convert_df(pd.DataFrame(df))

        filename = uploaded_file.name
        f, ext = filename.split('.')
        new_filename = f"{f}-lat-lon.{ext}"

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=new_filename,
            mime='text/csv',
)
