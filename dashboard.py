import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# --- Page Configuration ---
# Layout is set to "wide" to use the full screen width
st.set_page_config(
    page_title="Oilfield Operations Dashboard",
    page_icon="",  # A drill icon
    layout="wide"
)

# --- Database Connection & Data Loading ---
DB_PATH = 'oilfield_data.db'
TABLE_NAME = 'drilling_metrics'


# We use st.cache_data to cache the data loading.
# This means the database is only queried once when the data is needed,
# and subsequent interactions with the dashboard will use the cached data.
@st.cache_data
def load_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        # Read the entire table into a pandas DataFrame
        df = pd.read_sql(f'SELECT * FROM {TABLE_NAME}', conn)
        conn.close()

        # Convert timestamp column to datetime objects
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        # If the table doesn't exist (e.g., ETL notebook hasn't been run)
        st.error(
            f"Error loading data: {e}. "
            "Have you run the `etl_pipeline.ipynb` notebook to create the database?"
        )
        return pd.DataFrame()  # Return empty dataframe


# Load the data
df = load_data()

if not df.empty:

    # --- Sidebar Filters ---
    st.sidebar.header("ð%C2%9B%C2%9Bï¸%C2%8F Filters")

    # Get unique values for filters
    all_rigs = df['rig_id'].unique()

    # Create a multiselect filter for Rig ID
    # The 'default=all_rigs' means all rigs are selected by default.
    selected_rigs = st.sidebar.multiselect(
        "Select Rig(s):",
        options=all_rigs,
        default=all_rigs
    )

    # Create a slider to filter by depth
    min_depth, max_depth = float(df['depth_m'].min()), float(df['depth_m'].max())
    depth_range = st.sidebar.slider(
        "Select Depth Range (m):",
        min_value=min_depth,
        max_value=max_depth,
        value=(min_depth, max_depth)  # Default is the full range
    )

    # Filter the DataFrame based on user selections
    # The .query() method is a powerful way to filter pandas DataFrames
    df_selection = df.query(
        "rig_id == @selected_rigs & depth_m >= @depth_range[0] & depth_m <= @depth_range[1]"
    )

    # --- Main Page ---
    st.title("ð%C2%93%C2%9A Oilfield Operations Dashboard")
    st.markdown("Live sensor data from drilling operations.")

    # --- Key Performance Indicators (KPIs) ---
    st.header("Key Performance Indicators (KPIs)")

    # Create 3 columns for our KPIs
    kpi1, kpi2, kpi3 = st.columns(3)

    # Calculate KPIs from the filtered data
    # Use f-strings for formatting
    avg_rop = df_selection['rop_m_hr'].mean()
    kpi1.metric(
        label="Average ROP (m/hr)",
        value=f"{avg_rop:.2f}"
    )

    avg_efficiency = df_selection['drilling_efficiency'].mean()
    kpi2.metric(
        label="Avg. Drilling Efficiency",
        value=f"{avg_efficiency:.3f}"
    )

    total_depth = df_selection.groupby('rig_id')['depth_m'].max().sum()
    kpi3.metric(
        label="Total Depth Drilled (m)",
        value=f"{total_depth:.0f}"
    )

    # --- Charts ---
    st.header("Drilling Performance Analysis")

    # Create two columns for our charts
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.subheader("ROP vs. Depth")
        # Create a line chart using Plotly Express
        fig_rop_depth = px.line(
            df_selection,
            x='depth_m',
            y='rop_m_hr',
            color='rig_id',  # Different color line for each rig
            title="Rate of Penetration vs. Depth",
            labels={'depth_m': 'Depth (m)', 'rop_m_hr': 'ROP (m/hr)'}
        )
        # Display the chart in Streamlit
        st.plotly_chart(fig_rop_depth, use_container_width=True)

    with fig_col2:
        st.subheader("Efficiency over Time")
        fig_eff_time = px.line(
            df_selection,
            x='timestamp',
            y='drilling_efficiency',
            color='rig_id',
            title="Drilling Efficiency over Time",
            labels={'timestamp': 'Time', 'drilling_efficiency': 'Efficiency'}
        )
        st.plotly_chart(fig_eff_time, use_container_width=True)

    st.header("Parameter Correlation")
    st.markdown("How do different parameters relate to ROP? (Select from dropdown)")

    # Let user select which parameter to plot against ROP
    param_options = ['wob_tons', 'torque_kNm', 'mud_pressure_psi']
    selected_param = st.selectbox("Select Parameter:", param_options)

    # Create a scatter plot
    fig_scatter = px.scatter(
        df_selection,
        x=selected_param,
        y='rop_m_hr',
        color='rig_id',
        title=f"ROP vs. {selected_param}",
        labels={selected_param: selected_param, 'rop_m_hr': 'ROP (m/hr)'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # --- Raw Data Table ---
    st.header("Raw Data Explorer")
    st.markdown("View the filtered data table (last 50 rows).")
    # Display the filtered dataframe
    # .tail(50) shows just the most recent data
    st.dataframe(df_selection.tail(50))

else:
    st.warning("Dataframe is empty. Please run the ETL pipeline first.")