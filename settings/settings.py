# IMPORTAÇÕES

# Importação Streamlit
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import show_pages_from_config, hide_pages
from streamlit_option_menu import option_menu
# Importação Streamlit

# Importação de funções internas
import settings.functions as func

# CONFIGURAÇÕES
hide_st_styles = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="collapsedControl"] {display: none;}
</style>
"""

# hide_st_styles = ""

pages_to_hide = ["Home", "Estatisticas"]

