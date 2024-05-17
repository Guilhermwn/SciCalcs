# IMPORTAÇÕES
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import show_pages_from_config, hide_pages
from streamlit_option_menu import option_menu
import settings.functions as func
import pyperclip

hide_st_styles = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="collapsedControl"] {display: none;}
</style>
"""

pages_to_hide = ["Home", "Estatisticas"]

def copy_to_clipboard(text):
    pyperclip.copy(text)

