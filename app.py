import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/jobs.csv')
    return df

df = load_data()

# Title
st.title("📊 Skill Demand Dashboard")

# Dataset Overview
st.subheader("Dataset Preview")
st.write(df.head())

# Data Cleaning (example: drop missing skill entries)
df = df.dropna(subset=['Skills'])

# Skill Frequency
st.subheader("Top Skills in Demand")
all_skills = df['Skills'].str.lower().str.split(',').explode().str.strip()
top_skills = all_skills.value_counts().head(20)

fig1, ax1 = plt.subplots()
sns.barplot(x=top_skills.values, y=top_skills.index, ax=ax1)
ax1.set_xlabel("Frequency")
st.pyplot(fig1)

# Word Cloud
st.subheader("Skills Word Cloud")
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(all_skills))
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.imshow(wordcloud, interpolation='bilinear')
ax2.axis("off")
st.pyplot(fig2)

# Filter by location
st.subheader("Filter by Job Location")
locations = df['Location'].dropna().unique().tolist()
selected_location = st.selectbox("Select a location", ["All"] + locations)

if selected_location != "All":
    filtered_df = df[df['Location'] == selected_location]
else:
    filtered_df = df

st.write(f"Total jobs: {len(filtered_df)}")

# Skills in filtered data
filtered_skills = filtered_df['Skills'].str.lower().str.split(',').explode().str.strip()
filtered_skill_counts = filtered_skills.value_counts().head(10)

fig3, ax3 = plt.subplots()
sns.barplot(x=filtered_skill_counts.values, y=filtered_skill_counts.index, ax=ax3)
ax3.set_xlabel("Frequency")
st.pyplot(fig3)
