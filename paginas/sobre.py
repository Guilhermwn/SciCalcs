from settings.settings import *
from settings.functions import *

# CONFIGURAÇÕES DA PÁGINA
st.set_page_config(
    page_title="SciCalcs - Sobre",
    initial_sidebar_state="collapsed",
    layout="centered"
)

# EDIÇÃO DO CSS
st.markdown(hide_st_styles, unsafe_allow_html=True)
show_pages_from_config()
# hide_pages(pages_to_hide)

# CONTEÚDO DA PÁGINA
menu = option_menu(
    menu_title=None,
    options=["Home", "Sobre"],
    icons=["house-fill", "person-circle"],
    orientation="horizontal",
    default_index=1
)

# CASO PRESSIONAR "HOME" ELE VAI PARA A PÁGINA INICIAL
if menu == "Home":
    switch_page("Home")
st.header("Sobre")
centering = st.columns([2,3,1])
with centering[1]:
    st.image("./img/Sobre.png", "Logo Guilhermwn Enterprise", width=250)

st.markdown("""
## Motivação
Esse projeto surgiu como uma ideia de automatizar os cálculos repetitivos de incerteza necessários para elaboração de relatórios na matéria de **Laboratório de Física**. A ideia inicial seria projetar um aplicativo desktop, mas essa abordagem demandaria um tempo que eu não tinha na época e nem no momento em que essa página foi concebida. 

Enquanto eu participo do projeto de extensão disponibilizado pelo meu departamento na **Universidade Federal de Sergipe**, o DEL(Departamento de Engenharia Elétrica e Eletrônica), com o intuito de resolver questões e disponibilizar uma video-aula explicativa para os diversos alunos da universidade, eu fiquei responsável por gerenciar e responder questões justamente de Laboratório de Física.
            
Então tomei essa oportunidade para juntar o conhecimento que eu tenho obtido na universidade, e atualizar a minha gama de conhecimento sobre criação de interfaces gráfica, páginas web, dashboards e páginas dinâmicas. Assim optei por usar a biblioteca Streamlit do Python para criação de páginas web, para dar vida ao projeto SciCalcs.
""")

st.markdown("""
## Roadmap
Aqui se encontra os passos futuros da página SciCalcs

[Página do Projeto | Plane](https://sites.plane.so/guilhermwn-enterprise/91fc4bb2-f3e4-464e-a607-3cbad0ceb8be)
""")