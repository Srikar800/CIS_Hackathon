import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Patch & Update Risk Management Dashboard",
    layout="wide"
)

st.title("🛡️ Patch and Update Management with Risk Analysis")

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload Patch Data CSV",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Risk calculation function
    def calculate_risk(severity, exposure, cvss):

        severity_score = {
            "Low": 2,
            "Medium": 5,
            "High": 10
        }

        exposure_score = {
            "Internal": 2,
            "Internet": 5
        }

        sev = severity_score.get(severity, 1)
        exp = exposure_score.get(exposure, 1)

        return (sev * exp) + cvss

    # Calculate Risk Score
    df["Risk Score"] = df.apply(
        lambda row: calculate_risk(
            row["Severity"],
            row["Exposure"],
            row["CVSS Score"]
        ),
        axis=1
    )

    # Sort by Risk
    df = df.sort_values(
        by="Risk Score",
        ascending=False
    )

    # Sidebar Filters
    st.sidebar.header("🔎 Filter Systems")

    severity_filter = st.sidebar.selectbox(
        "Select Severity",
        ["All", "High", "Medium", "Low"]
    )

    exposure_filter = st.sidebar.selectbox(
        "Select Exposure",
        ["All", "Internet", "Internal"]
    )

    filtered_df = df.copy()

    if severity_filter != "All":
        filtered_df = filtered_df[
            filtered_df["Severity"] == severity_filter
        ]

    if exposure_filter != "All":
        filtered_df = filtered_df[
            filtered_df["Exposure"] == exposure_filter
        ]

    # Show Data
    st.subheader("📋 Patch Risk Table")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    # High Risk Alerts
    st.subheader("🚨 High Risk Alerts")

    high_risk = filtered_df[
        filtered_df["Risk Score"] > 40
    ]

    if not high_risk.empty:
        st.error(
            f"{len(high_risk)} High Risk Systems Need Immediate Patching!"
        )
        st.dataframe(high_risk)

    else:
        st.success(
            "No Critical Risk Systems Found ✅"
        )

    # Risk Distribution Chart
    st.subheader("📊 Risk Distribution")

    severity_counts = filtered_df[
        "Severity"
    ].value_counts()

    st.bar_chart(severity_counts)

    # Exposure Chart
    st.subheader("🌐 Exposure Distribution")

    exposure_counts = filtered_df[
        "Exposure"
    ].value_counts()

    st.bar_chart(exposure_counts)

    # Top Risk Systems
    st.subheader("🔥 Top Priority Patch Systems")

    top5 = filtered_df.head(5)

    st.table(top5)

else:
    st.info(
        "Upload a CSV file to begin analysis."
    )