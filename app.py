import streamlit as st

# Set up Streamlit page with enhanced design
st.set_page_config(page_title="CVP Analysis Tool", layout="centered", page_icon="📊")

# Sidebar for page navigation
page = st.sidebar.selectbox("Choose Analysis Type", ["CVP Analysis", "Sales Mix Analysis"])

# Importing relevant module based on selected analysis type
if page == "CVP Analysis":
    import backend.cvp_analysis as cvp_analysis
    cvp_analysis.run()
elif page == "Sales Mix Analysis":
    import backend.sales_mix_analysis as sales_mix_analysis
    sales_mix_analysis.run()
