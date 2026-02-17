import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Bug Reports Analytics Dashboard",
    layout="wide"
)

# --------------------------------------------------
# Title & Description
# --------------------------------------------------
st.title("🐞 Bug Reports Analytics Dashboard")
st.markdown(
    "An interactive dashboard for exploring patterns in software bug reports."
)

# --------------------------------------------------
# Load Data (Cached)
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("bug_dataset_50k.csv")
    return df

df = load_data()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.markdown("## 🔍 Filters")
st.sidebar.markdown(
    "Use the filters below to explore specific subsets of bug reports."
)

selected_severity = st.sidebar.multiselect(
    "Select Severity Level",
    options=df['severity'].unique(),
    default=df['severity'].unique()
)

selected_domain = st.sidebar.multiselect(
    "Select Bug Domain",
    options=df['bug_domain'].unique(),
    default=df['bug_domain'].unique()
)

filtered_df = df[
    (df['severity'].isin(selected_severity)) &
    (df['bug_domain'].isin(selected_domain))
]

# --------------------------------------------------
# KPI Section
# --------------------------------------------------
st.markdown("### 📊 Dashboard Overview")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Bugs", f"{len(filtered_df):,}")
k2.metric("Critical Bugs", f"{(filtered_df['severity'] == 'Critical').sum():,}")
k3.metric("High Severity Bugs", f"{(filtered_df['severity'] == 'High').sum():,}")
k4.metric("Bug Domains", filtered_df['bug_domain'].nunique())

# --------------------------------------------------
# Bug Analysis Section
# --------------------------------------------------
st.markdown("---")
st.markdown("## 🐞 Bug Analysis")

left, right = st.columns(2)

# -------- Left: Bug Categories --------
with left:
    st.subheader("Most Common Bug Categories")

    bug_category_counts = (
        filtered_df['bug_category']
        .value_counts()
        .head(10)
        .reset_index()
    )
    bug_category_counts.columns = ['bug_category', 'bug_count']

    fig, ax = plt.subplots()
    sns.barplot(
        data=bug_category_counts,
        y='bug_category',
        x='bug_count',
        palette="viridis",
        ax=ax
    )
    ax.set_xlabel("Number of Bug Reports")
    ax.set_ylabel("Bug Category")
    st.pyplot(fig)

    st.caption(
        "💡 Memory, concurrency, and backend-related bugs dominate, "
        "highlighting persistent challenges in core system stability."
    )

# -------- Right: Severity Distribution --------
with right:
    st.subheader("Bug Severity Distribution")

    severity_counts = (
        filtered_df['severity']
        .value_counts()
        .reset_index()
    )
    severity_counts.columns = ['severity', 'bug_count']

    fig, ax = plt.subplots()
    sns.barplot(
        data=severity_counts,
        x='severity',
        y='bug_count',
        palette="rocket",
        ax=ax
    )
    ax.set_xlabel("Severity Level")
    ax.set_ylabel("Number of Bug Reports")
    st.pyplot(fig)

    st.caption(
        "⚠️ A significant proportion of bugs fall under High and Critical severity, "
        "indicating notable operational risk."
    )

# --------------------------------------------------
# Risk & Severity Insights Section
# --------------------------------------------------
st.markdown("---")
st.markdown("## 🚨 Risk & Severity Insights")

env_severity = (
    filtered_df.groupby(['environment', 'severity'])
    .size()
    .reset_index(name='bug_count')
)

env_pivot = env_severity.pivot(
    index='environment',
    columns='severity',
    values='bug_count'
).fillna(0)

fig, ax = plt.subplots()
env_pivot.plot(kind='bar', stacked=True, ax=ax)
ax.set_xlabel("Environment")
ax.set_ylabel("Number of Bug Reports")
ax.legend(title="Severity", bbox_to_anchor=(1.02, 1), loc="upper left")
st.pyplot(fig)

st.caption(
    "🚨 Although most bugs are detected during development and staging, "
    "critical issues still appear in production, suggesting gaps in pre-deployment testing."
)

# --------------------------------------------------
# Footer
# --------------------------------------------------
# --------------------------------------------------
# Final Report Section
# --------------------------------------------------
st.markdown("---")
st.markdown("## 📝 Analytical Report Summary")

st.markdown(
    """
### 📌 Overview
This dashboard analyzed **50,000 software bug reports** to identify patterns in bug categories,
severity levels, affected domains, environments, and risk areas. Interactive filters were used
to explore how bug behavior changes across different conditions.

---

### 🔍 Key Findings
- **Memory leaks, concurrency issues, and backend logic bugs** are the most frequently reported,
  indicating persistent challenges in core system stability.
- A **significant proportion of bugs are classified as High or Critical severity**, highlighting
  non-trivial operational risk.
- Although most bugs are detected during **development and staging**, critical issues still
  appear in **production environments**.
- Backend, cloud, and DevOps-related domains show a **higher concentration of severe bugs**,
  suggesting greater complexity and risk in infrastructure components.

---

### 💡 Recommendations
- Strengthen **pre-production testing and validation**, especially for backend and cloud systems.
- Introduce **automated monitoring and memory profiling tools** to reduce recurring bug types.
- Prioritize **high-risk domains and technologies** for code reviews and refactoring.
- Use dashboards like this regularly to support **data-driven quality improvement decisions**.

---

### ✅ Conclusion
This analysis demonstrates how **exploratory data analysis and visualization** can be used to
gain actionable insights from bug report data. The findings can help engineering teams improve
software quality, reduce production risk, and allocate resources more effectively.
"""
)
