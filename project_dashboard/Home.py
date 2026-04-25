import streamlit as st
from dataloader import load_project_data


st.set_page_config(page_title="KKM Dashboard")
st.title("KKM Dashboard")
st.markdown("""Welcome. Use the sidebar to navigate between pages


1. **Data Explorer** - Explore data
2. **Visualisation** - Charts
3. **ML Model** - Predict future COVID Cases that may arise in the nation.
4. **Region Mapping** - Model doing  
---
""")
