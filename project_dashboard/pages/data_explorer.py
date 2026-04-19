import streamlit as st
import seaborn as sns

st.title("Data Explorer")


@st.cache_data
def load_data():
    return sns.load_dataset("iris")


df = load_data()

species = st.multiselect(
    "Select species", options=df["species"].unique(), default=df["species"].unique()
)

filtered = df[df["species"].isin(species)]
st.session_state["filtered_df"] = filtered  # <-- share across pages

st.write(f"Showing **{len(filtered)}** rows")
st.dataframe(filtered)

st.subheader("Summary statistics")
st.write(filtered.describe())
