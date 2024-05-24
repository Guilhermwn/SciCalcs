# SOURCE: https://www.newtoncbraga.com.br/matematica-na-eletronica/4653-formulas-para-amplificadores-operacionais-m251.html
from settings.settings import *
from settings.functions import *

# CONFIGURAÇÕES DA PÁGINA
st.set_page_config(
    page_title="SciCalcs - Estatísticas",
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
    options=["Home", "Elétricas"],
    icons=["house-fill", "lightning-charge-fill"],
    orientation="horizontal",
    default_index=1
)

# CASO PRESSIONAR "HOME" ELE VAI PARA A PÁGINA INICIAL
if menu == "Home":
    switch_page("Home")
st.header("Elétricas")


# SELETOR DE CALCULADORA
option = st.selectbox(
    "Escolha o que fazer:",
    ["Ganho de amplificador",],
    index=None,
    placeholder="Escolha o que fazer:",
    label_visibility="collapsed")

st.divider()

# ==============================================================
# PÁGINA GANHO AMPLIFICADOR

# SELETOR
if option == 'Ganho de amplificador':
    st.title("Amplificador Inversor")

    # COLUNAS DE INSERÇÃO DE DADOS
    left, center, right = st.columns(3)
    
    # ==============================================================
    # SETOR DE INPUT DO RESISTOR 2

    with left:
        r1_container = st.container(border=True, height=190)
        with r1_container:
            # INPUT DO VALOR DO RESISTOR 1
            r1 = st.number_input("R1", min_value=1)

            # INPUT DA UNIDADE DO RESISTOR 1
            r1_unit_select = st.selectbox("Unidade R1", ["ohms", "kilohms", "megaohms"], key=1)

            # FORMATAÇÃO DA UNIDADE NUMÉRICA PARA CÁLCULO E UNIDADE TEXTUAL PARA VISUALIZAÇÃO 
            if r1_unit_select == "ohms":
                r1_calc = r1
                r1_unit = "\Omega"
            if r1_unit_select == "kilohms":
                r1_calc = r1*1000
                r1_unit = "K\Omega"
            if r1_unit_select == "megaohms":
                r1_calc = r1*1000000
                r1_unit = "M\Omega"

    # ==============================================================
    # SETOR DE INPUT DO RESISTOR 2

    with center:
        r2_container = st.container(border=True, height=190)
        with r2_container:
            # INPUT DO VALOR DO RESISTOR 2
            r2 = st.number_input("R2", min_value=0)

            # INPUT DA UNIDADE DO RESISTOR 2
            r2_unit_select = st.selectbox("Unidade R2", ["ohms", "kilohms", "megaohms"], key=2)
            
            # FORMATAÇÃO DA UNIDADE NUMÉRICA PARA CÁLCULO E UNIDADE TEXTUAL PARA VISUALIZAÇÃO 
            if r2_unit_select == "ohms":
                r2_calc = r2
                r2_unit = "\Omega"
            if r2_unit_select == "kilohms":
                r2_calc = r2*1000
                r2_unit = "K\Omega"
            if r2_unit_select == "megaohms":
                r2_calc = r2*1000000
                r2_unit = "M\Omega"
    
    # ==============================================================
    # SETOR DE EXIBIÇÃO DO GANHO

    with right:
        ganho_container = st.container(border=True, height=190)
        with ganho_container:
            # CÁLCULO DO GANHO 
            ganho = -(r2_calc/r1_calc)
            st.markdown(f"<h3 style='text-align: center; color: white;'>Ganho</h1>", unsafe_allow_html=True)
            st.number_input("ganho", value=ganho,label_visibility="collapsed")
            # st.metric("Ganho do amplificador", value=ganho)

    # ==============================================================
    # EXIBIÇÃO DA IMAGEM DO CIRCUITO

    # FORMATAÇÃO DAS LABELS DOS RESISTORES
    r1_label = f"{r1}" + f"{r1_unit}"
    r2_label = f"{r2}" + f"{r2_unit}"

    # == DESENHO DO AMPLIFICADOR ==
    schemdraw.config(bgcolor='#0e1117')
    schemdraw.config(color='white')
    with schemdraw.Drawing(show=False,) as d:
        op = elm.Opamp(leads=True)
        elm.Line().down(d.unit/4).at(op.in2)
        elm.Ground(lead=False)
        Rin = elm.Resistor().at(op.in1).left().idot().label(f'${r1_label}$', loc='bot').label('$v_{in}$', loc='left')
        elm.Line().up(d.unit/2).at(op.in1)
        elm.Resistor().tox(op.out).label(f'${r2_label}$')
        elm.Line().toy(op.out).dot()
        elm.Line().right(d.unit/4).at(op.out).label('$v_{o}$', loc='right')

    image_bytes = d.get_imagedata('png')
    st.image(image_bytes)
    # == DESENHO DO AMPLIFICADOR ==

