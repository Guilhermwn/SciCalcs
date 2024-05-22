from settings.settings import *

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

left, center, right = st.columns([1,1,1])

with left:
    left_container = st.container(border=True)
    with left_container:
        st.markdown("<h2 style='text-align: center; color: white;'>Estatística</h1>", unsafe_allow_html=True)
        # st.header("Estatística")
        st.image("img/estatistics.png")
        if st.button("ABRIR", use_container_width=True, key=1):
            switch_page("Estatisticas")

with center:
    center_container = st.container(border=True)
    with center_container:
        st.markdown("<h2 style='text-align: center; color: white;'>Elétricas</h1>", unsafe_allow_html=True)
        # st.header("Estatística")
        st.image("img/eletric.jpg")
        if st.button("ABRIR", use_container_width=True, key=2):
            switch_page("Eletricas")



