import streamlit as st
import os
import pandas as pd
import plotly.express as px
from data_processing.analyze import load_dataframe
from plotly import graph_objects as go

st.title("📊 Dashboard")
uploaded_file = st.file_uploader("Upload your dataset (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ Uploaded: {uploaded_file.name}")

    df = load_dataframe(file_path)

    if 'report_figures' not in st.session_state:
        st.session_state['report_figures'] = []

    st.subheader("🖊️ Visualizations")

    # Bar Chart
    st.markdown("#### Bar Chart")
    bar_data = df[df.columns[0]].value_counts().nlargest(10)
    fig_bar = px.bar(x=bar_data.index, y=bar_data.values, labels={'x': df.columns[0], 'y': 'Count'})
    st.plotly_chart(fig_bar, use_container_width=True)
    st.session_state['report_figures'].append(fig_bar)

    # Pie Chart
    st.markdown("#### Pie Chart")
    pie_data = df[df.columns[0]].value_counts().nlargest(5)
    fig_pie = px.pie(names=pie_data.index, values=pie_data.values)
    st.plotly_chart(fig_pie, use_container_width=True)
    st.session_state['report_figures'].append(fig_pie)

    # Histogram
    if pd.api.types.is_numeric_dtype(df[df.columns[1]]):
        st.markdown("#### Histogram")
        fig_hist = px.histogram(df, x=df.columns[1])
        st.plotly_chart(fig_hist, use_container_width=True)
        st.session_state['report_figures'].append(fig_hist)
    else:
        st.warning(f"Histogram skipped: '{df.columns[1]}' must be numeric.")

    st.markdown("---")
    st.markdown("### ⚙️ Additional Visualizations")

    def validate_columns(n):
        return len(df.columns) >= n

    if st.checkbox("🔗 Sankey Diagram"):
        if validate_columns(3):
            src = df[df.columns[0]].astype(str)
            tgt = df[df.columns[1]].astype(str)
            val = df[df.columns[2]].fillna(1)
            nodes = list(set(src) | set(tgt))
            fig_sankey = go.Figure(data=[go.Sankey(
                node=dict(label=nodes),
                link=dict(
                    source=src.map(nodes.index),
                    target=tgt.map(nodes.index),
                    value=val
                )
            )])
            st.plotly_chart(fig_sankey, use_container_width=True)
            st.session_state['report_figures'].append(fig_sankey)
        else:
            st.warning("Sankey requires at least 3 columns.")

    if st.checkbox("🌞 Sunburst Chart"):
        if validate_columns(3):
            try:
                fig_sunburst = px.sunburst(df, path=[df.columns[0], df.columns[1], df.columns[2]], values=df[df.columns[2]])
                st.plotly_chart(fig_sunburst, use_container_width=True)
                st.session_state['report_figures'].append(fig_sunburst)
            except Exception as e:
                st.warning(f"Sunburst chart error: {e}")
        else:
            st.warning("Sunburst requires at least 3 columns.")

    if st.checkbox("📈 Line Chart"):
        if validate_columns(2) and pd.api.types.is_numeric_dtype(df[df.columns[1]]):
            fig_line = px.line(df, x=df.columns[0], y=df.columns[1])
            st.plotly_chart(fig_line, use_container_width=True)
            st.session_state['report_figures'].append(fig_line)
        else:
            st.warning("Line chart requires a categorical x-axis and numeric y-axis.")

    if st.checkbox("📊 Box Plot"):
        if validate_columns(2) and pd.api.types.is_numeric_dtype(df[df.columns[1]]):
            fig_box = px.box(df, x=df.columns[0], y=df.columns[1])
            st.plotly_chart(fig_box, use_container_width=True)
            st.session_state['report_figures'].append(fig_box)
        else:
            st.warning("Box plot requires a categorical x and numeric y column.")

    if st.checkbox("📉 Area Chart"):
        if validate_columns(2) and pd.api.types.is_numeric_dtype(df[df.columns[1]]):
            fig_area = px.area(df, x=df.columns[0], y=df.columns[1])
            st.plotly_chart(fig_area, use_container_width=True)
            st.session_state['report_figures'].append(fig_area)
        else:
            st.warning("Area chart requires a categorical x and numeric y column.")

    if st.checkbox("📊 Correlation Heatmap"):
        numeric_df = df.select_dtypes(include='number')
        if numeric_df.shape[1] >= 2:
            fig_heat = px.imshow(numeric_df.corr(), text_auto=True, aspect="auto", color_continuous_scale='RdBu')
            st.plotly_chart(fig_heat, use_container_width=True)
            st.session_state['report_figures'].append(fig_heat)
        else:
            st.warning("Heatmap requires at least 2 numeric columns.")

    if st.checkbox("🔍 Scatter Plot"):
        if validate_columns(2) and all(pd.api.types.is_numeric_dtype(df[col]) for col in df.columns[:2]):
            fig_scatter = px.scatter(df, x=df.columns[0], y=df.columns[1])
            st.plotly_chart(fig_scatter, use_container_width=True)
            st.session_state['report_figures'].append(fig_scatter)
        else:
            st.warning("Scatter plot requires two numeric columns.")

    if st.checkbox("📇 Violin Plot"):
        if validate_columns(2) and pd.api.types.is_numeric_dtype(df[df.columns[1]]):
            fig_violin = px.violin(df, x=df.columns[0], y=df.columns[1], box=True)
            st.plotly_chart(fig_violin, use_container_width=True)
            st.session_state['report_figures'].append(fig_violin)
        else:
            st.warning("Violin plot requires a categorical x and numeric y column.")

    if st.checkbox("🌲 Treemap"):
        if validate_columns(2):
            if pd.api.types.is_numeric_dtype(df[df.columns[1]]):
                try:
                    fig_tree = px.treemap(df, path=[df.columns[0]], values=df[df.columns[1]])
                    st.plotly_chart(fig_tree, use_container_width=True)
                    st.session_state['report_figures'].append(fig_tree)
                except Exception as e:
                    st.warning(f"Treemap error: {e}")
            else:
                st.warning(f"Treemap skipped: '{df.columns[1]}' must be numeric.")
        else:
            st.warning("Treemap requires at least 2 columns.")

    st.page_link("pages/Generate_report.py", label="➡️ Go to Generate PDF", icon="🧾")
