from settings.settings import *        
from settings.functions import *
from settings.classes import *

# CONFIGURAÇÕES DA PÁGINA
st.set_page_config(
    page_title="SciCalcs Home",
    initial_sidebar_state="collapsed",
    layout="centered"
)

st.markdown(hide_st_styles, unsafe_allow_html=True)
show_pages_from_config()
# hide_pages(pages_to_hide)

# CONTEÚDO DA PÁGINA

menu = option_menu(
    menu_title=None,
    options=["Home"],
    icons=["house-fill"],
    orientation="horizontal",
)


st.header("Página Inicial")
st.divider()

pages_list = Detector("paginas").list_pages()
grid_creator(pages_list)
