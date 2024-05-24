# ------------------------------------------------
# IMPORTAÇÕES

# Importação Streamlit
import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from st_pages import show_pages_from_config, hide_pages
from streamlit_extras.switch_page_button import switch_page

# ------------------------------------------------
# CONFIGURAÇÕES

# CSS PARA ESCONDER COMPONENTES INÚTEIS DA PÁGINA STREAMLIT
# hide_st_styles = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# header {visibility: hidden;}
# [data-testid="collapsedControl"] {display: none;}
# </style>
#"""

hide_st_styles = ""

# PÁGINAS A ESCONDER NA SIDEBAR
pages_to_hide = ["Home", "Estatisticas"]


