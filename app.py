import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Supplier Performance & Segmentation Dashboard", layout="wide")

st.title("📊 Strategic Supplier Performance & ABC Segmentation")

@st.cache_data
def load_data():
    return pd.read_csv('Final_Supplier_Analytics_Master.csv')

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Options")
selected_abc = st.sidebar.multiselect("ABC Spend Category", options=df['abc_category'].unique(), default=df['abc_category'].unique())
selected_cluster = st.sidebar.multiselect("Supplier Cluster ID", options=df['cluster_id'].unique(), default=df['cluster_id'].unique())

filtered_df = df[(df['abc_category'].isin(selected_abc)) & (df['cluster_id'].isin(selected_cluster))]

# Top Key Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Analyzed Suppliers", len(filtered_df))
col2.metric("Total Procurement Spend ($)", f"${filtered_df['total_spend'].sum():,.2f}")
col3.metric("Avg On-Time Delivery (%)", f"{filtered_df['on_time_delivery_pct'].mean():.2f}%")
col4.metric("Avg Quality Rating", f"{filtered_df['quality_rating'].mean():.2f} / 5.0")

st.markdown("---")

# Visualizations
c1, c2 = st.columns(2)

with c1:
    fig_abc = px.pie(filtered_df, names='abc_category', title='Spend Distribution by ABC Category', hole=0.4)
    st.plotly_chart(fig_abc, use_container_width=True)

with c2:
    fig_scatter = px.scatter(
        filtered_df, 
        x='on_time_delivery_pct', 
        y='composite_score', 
        color='abc_category',
        size='total_spend',
        hover_data=['supplier_name'],
        title='On-Time Delivery vs Composite Score'
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("📋 Master Supplier Performance Table")
st.dataframe(filtered_df[['supplier_name', 'abc_category', 'total_spend', 'on_time_delivery_pct', 'quality_rating', 'composite_score', 'cluster_id']])