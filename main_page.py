import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from urllib.error import URLError
from connectiondb import connection
# streamlit run app.py


st.markdown("# Spese ")
st.sidebar.markdown("# Main page ")

if __name__ == "__main__":
    
    
    try:
        df = pd.read_json("transaction.json")
        
        category  = st.multiselect(
            "Choose category ", list(df["categoria"].unique())
        )
        
        if category :
            df_category  = df[df["categoria"].isin(category )]
            
            expense = st.multiselect(
                "Choose expense", list(df_category ["spesa"].unique())
            )
        else:
            expense = st.multiselect(
                "Choose expense", list(df["spesa"].unique())
            )
        
        if not category  and not expense:
            st.dataframe(df)
        else:
            if category :
                filtered_df = df[df["categoria"].isin(category )]
            if expense:
                filtered_df = df[df["spesa"].isin(expense)]
            st.dataframe(filtered_df)
    
    except URLError as e:
        st.write(e.reason)

