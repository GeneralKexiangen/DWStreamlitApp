import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="DATA.ER",
    page_icon="🐬",
    layout="wide",
    initial_sidebar_state= 'collapsed'
)
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("# Page 3 🎉")
st.sidebar.markdown("# Page 3 🎉")
# embed streamlit docs in a streamlit app
# components.iframe("https://docs.streamlit.io/en/latest", width=1000, height=1000, scrolling=True)

