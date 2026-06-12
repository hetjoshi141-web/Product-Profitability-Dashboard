import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Product Profitability Dashboard",
    layout="wide"
)

# ----------------------------------
# LOAD DATA
# ----------------------------------
product_summary = pd.read_csv("product_summary.csv")
division_summary = pd.read_csv("division_summary.csv")
cost_margin = pd.read_csv("cost_margin.csv")
pareto = pd.read_csv("pareto_revenue.csv")
data = pd.read_csv("processed_data.csv")

# ----------------------------------
# SIDEBAR FILTERS
# ----------------------------------
# Product Filter
product_filter = st.sidebar.multiselect(
    "Select Product",
    product_summary["Product Name"].unique()
)

# Apply Product Filter
filtered_product = product_summary.copy()

if product_filter:
    filtered_product = filtered_product[
        filtered_product["Product Name"].isin(product_filter)
    ]
# Division Filter
if "Division" in data.columns:
    divisions = data["Division"].unique()
    selected_divisions = st.sidebar.multiselect(
        "Select Division",
        divisions,
        default=divisions
    )
else:
    selected_divisions = []

# Margin Threshold
margin_threshold = st.sidebar.slider(
    "Margin Threshold %",
    0,
    100,
    20
)

# Date Range
if "Date" in data.columns:
    data["Date"] = pd.to_datetime(data["Date"])

    start_date = st.sidebar.date_input(
        "Start Date",
        data["Date"].min()
    )

    end_date = st.sidebar.date_input(
        "End Date",
        data["Date"].max()
    )

# ----------------------------------
# TITLE
# ----------------------------------
st.title("📊 Product Profitability Dashboard")

# ----------------------------------
# KPI CARDS
# ----------------------------------
st.subheader("Business KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Sales",
        f"{data['Sales'].sum():,.0f}"
    )

with c2:
    st.metric(
        "Total Profit",
        f"{data['Gross Profit'].sum():,.0f}"
    )

with c3:
    st.metric(
        "Total Units",
        f"{data['Units'].sum():,.0f}"
    )

with c4:
    st.metric(
        "Average Margin %",
        round(
            (data["Gross Profit"].sum() /
             data["Sales"].sum()) * 100,
            2
        )
    )

# ==================================
# PRODUCT PROFITABILITY OVERVIEW
# ==================================
st.header("Product Profitability Overview")

col1, col2 = st.columns(2)

with col1:

    top_products = product_summary.sort_values(
        by="Gross Profit",
        ascending=False
    ).head(10)

    fig1 = px.bar(
        top_products,
        x="Product Name",
        y="Gross Profit",
        title="Product-Level Margin Leaderboard"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col2:

    fig2 = px.pie(
        product_summary,
        names="Product Name",
        values="Gross Profit",
        title="Profit Contribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )
st.dataframe(filtered_product)
# ==================================
# DIVISION PERFORMANCE
# ==================================
st.header("Division Performance Dashboard")

col3, col4 = st.columns(2)

with col3:

    fig3 = px.bar(
        division_summary,
        x="Division",
        y=["Sales", "Gross Profit"],
        barmode="group",
        title="Revenue vs Profit Comparison"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with col4:

    if "Average Margin %" in division_summary.columns:

        fig4 = px.bar(
            division_summary,
            x="Division",
            y="Average Margin %",
            title="Margin Distribution by Division"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )
st.write("show data")
st.dataframe(division_summary)
# ==================================
# COST VS MARGIN
# ==================================
st.header("Cost vs Margin Diagnostics")

if "Margin %" in cost_margin.columns:

    fig5 = px.scatter(
        cost_margin,
        x="Cost",
        y="Margin %",
        title="Cost-Sales Scatter Plot"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    st.subheader("Margin Risk Flags")

    risk_products = cost_margin[
        cost_margin["Margin %"] < margin_threshold
    ]

    st.dataframe(risk_products)
    st.write("all data show:")
    st.dataframe(cost_margin)

# ==================================
# PARETO ANALYSIS
# ==================================
st.header("Profit Concentration Analysis")

if "Cumulative Revenue %" in pareto.columns:

    fig6 = px.line(
        pareto,
        x=pareto.index,
        y="Cumulative Revenue %",
        markers=True,
        title="Pareto Chart"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

    dependency_count = len(
        pareto[
            pareto["Cumulative Revenue %"] <= 80
        ]
    )

    st.metric(
        "Products Driving 80% Revenue",
        dependency_count
    )
st.dataframe(filtered_product)
st.dataframe(pareto)
# ==================================
# TABLES
# ==================================
st.header("Detailed Tables")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Products",
        "Divisions",
        "Cost Margin",
        "Pareto"
    ]
)

with tab1:
    st.dataframe(product_summary)

with tab2:
    st.dataframe(division_summary)

with tab3:
    st.dataframe(cost_margin)

with tab4:
    st.dataframe(pareto)

print(product_summary.columns.tolist())
print(division_summary.columns.tolist())
print(cost_margin.columns.tolist())
print(pareto.columns.tolist())