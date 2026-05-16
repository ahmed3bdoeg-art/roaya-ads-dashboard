import streamlit as st
import pandas as pd

st.set_page_config(page_title="ROAYA Ads Intelligence Dashboard", layout="wide")
st.title("📊 ROAYA Ads Intelligence Dashboard")
st.write("ارفع تقارير Meta Ads أو TikTok Ads بصيغة CSV أو Excel وسيتم تحليلها تلقائيًا.")

uploaded_files = st.file_uploader(
    "Upload Reports",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

def read_file(file):
    if file.name.lower().endswith(".csv"):
        try:
            return pd.read_csv(file)
        except Exception:
            file.seek(0)
            return pd.read_csv(file, encoding="utf-8-sig")
    return pd.read_excel(file)

if uploaded_files:
    dfs = []
    for f in uploaded_files:
        try:
            df = read_file(f)
            df["Source File"] = f.name
            dfs.append(df)
        except Exception as e:
            st.error(f"Error reading {f.name}: {e}")

    if dfs:
        data = pd.concat(dfs, ignore_index=True)
        st.success(f"Loaded {len(uploaded_files)} file(s) successfully.")
        st.dataframe(data.head(50), use_container_width=True)

        numeric_candidates = [
            "Amount spent (EGP)", "Amount spent", "Cost", "Spend",
            "Results", "Conversions", "Impressions", "Reach", "Clicks"
        ]

        metrics = {}
        for col in numeric_candidates:
            if col in data.columns:
                metrics[col] = pd.to_numeric(data[col], errors="coerce").fillna(0).sum()

        if metrics:
            st.subheader("Executive Summary")
            cols = st.columns(min(4, len(metrics)))
            for i, (k, v) in enumerate(metrics.items()):
                cols[i % len(cols)].metric(k, f"{v:,.0f}")

        csv = data.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "Download Clean Data",
            csv,
            file_name="cleaned_ads_data.csv",
            mime="text/csv"
        )
else:
    st.info("ابدأ برفع ملفات CSV أو Excel من Meta Ads أو TikTok Ads.")