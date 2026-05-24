import time
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Fraud Monitoring System",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    h1, h2, h3 {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title(
    "Real-Time Fraud Detection Dashboard"
)

placeholder = st.empty()

while True:
    try:
        df = pd.read_csv("live_transactions.csv")
        fraud_df = df[df["prediction"] == 1]
        normal_df = df[df["prediction"] == 0]
        total_transactions = len(df)
        fraud_count = len(fraud_df)
        fraud_rate = round((fraud_count /total_transactions) * 100,2)
        avg_risk = round(df["fraud_probability"].mean(),4)
        recent_frauds = len(df.tail(20)[df.tail(20)["prediction"] == 1])
        risky_users = (df.groupby("user_id")["fraud_probability"].mean().sort_values(ascending=False).head(5))

        with placeholder.container():
            if recent_frauds > 0:
                st.error(f"🚨 {recent_frauds} HIGH RISK TRANSACTIONS DETECTED")
            else:
                st.success("✅ System Operating Normally")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Transactions",total_transactions)
            col2.metric("Fraud Alerts",fraud_count)
            col3.metric("Average Risk Score",avg_risk)
            st.markdown("---")
            chart_col1, chart_col2 = st.columns(2)
            pie_df = pd.DataFrame({
                "Category": [
                    "Fraud",
                    "Normal"
                ],
                "Count": [
                    fraud_count,
                    len(normal_df)
                ]
            })
            pie_chart = px.pie(
                pie_df,
                names="Category",
                values="Count",
                title="Fraud vs Normal Transactions"
            )
            chart_col1.plotly_chart(
                pie_chart,
                use_container_width=True
            )
            trend_df = df.tail(50)
            trend_chart = px.line(trend_df,
                y="fraud_probability",
                title="Fraud Probability Trend"
            )
            chart_col2.plotly_chart(trend_chart,
                use_container_width=True
            )
            st.markdown("---")
            st.subheader("Recent Transactions")
            recent_df = df.tail(20)[[
                "user_id",
                "amount",
                "merchant",
                "location",
                "fraud_probability",
                "prediction"
            ]]
            recent_df["prediction"] = recent_df["prediction"].map({0: "NORMAL",1: "FRAUD"})
            st.dataframe( recent_df, use_container_width=True)
            st.markdown("---")
            st.subheader("Detected Fraud Transactions")
            fraud_display = fraud_df[[
                "user_id",
                "amount",
                "merchant",
                "location",
                "fraud_probability",
                "risk_level"
            ]].tail(10)
            st.dataframe(fraud_display,use_container_width=True)
            st.markdown("---")
            st.subheader( "Normal Transactions")
            normal_display = normal_df[[
                "user_id",
                "amount",
                "merchant",
                "location",
                "fraud_probability"
            ]].tail(10)
            st.dataframe(
                normal_display,
                use_container_width=True
            )
            st.markdown("---")
            st.subheader( "Most Suspicious Users" )
            risky_users_df = pd.DataFrame({
                "user_id": risky_users.index,
                "average_risk_score": risky_users.values
            })
            st.dataframe( risky_users_df,use_container_width=True)
    except Exception as e:
        st.error(
            f"Error: {e}"
        )
    time.sleep(2)