# SOURCE: https://www.newtoncbraga.com.br/matematica-na-eletronica/4653-formulas-para-amplificadores-operacionais-m251.html
from settings.settings import *
from settings.functions import *
from settings.strings import *

# CONFIGURAÇÕES DA PÁGINA
st.set_page_config(
    page_title="SciCalcs - Elétrico",
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
    tipo_amplificador = st.selectbox(
        "Escolha qual tipo:",
        options=["Inversor[R1,R2]",
                "Inversor[G]",
                "Não Inversor[R1, R2]"],
        index=0,
        label_visibility="collapsed"
    )

    if tipo_amplificador == "Inversor[R1,R2]":
        st.title("Amplificador Inversor")
        st.write("Insira os valores de resistores e o ganho resultante será exibido.")

        with st.form("Inversor via Rs",clear_on_submit=True):
            left, center= st.columns(2)

            # ==============================================================
            # SETOR DE INPUT DO RESISTOR 1
            
            with left:
                with st.container(border=True):
                    r1_value = st.number_input("Valor do Resistor 1", min_value=1,key="r1_value")
                    r1_unit = st.selectbox("Unidade do Resistor 1",["ohms", "kilohms","megaohms"], key="r1_unit")
                    if r1_unit == "ohms":
                        r1 = r1_value
                        r1_latex = "\Omega"
                    if r1_unit == "kilohms":
                        r1 = r1_value * 1000
                        r1_latex = "K\Omega"
                    if r1_unit == "megaohms":
                        r1 = r1_value * 1000 * 1000
                        r1_latex = "M\Omega"

            # ==============================================================
            # SETOR DE INPUT DO RESISTOR 2

            with center:
                with st.container(border=True):
                    r2_value = st.number_input("Valor do Resistor 2", min_value=0,key="r2_value")
                    r2_unit = st.selectbox("Unidade do Resistor 2",["ohms", "kilohms","megaohms"], key="r2_unit")
                    if r2_unit == "ohms":
                        r2 = r2_value
                        r2_latex = "\Omega"
                    if r2_unit == "kilohms":
                        r2 = r2_value * 1000
                        r2_latex = "K\Omega"
                    if r2_unit == "megaohms":
                        r2 = r2_value * 1000 * 1000
                        r2_latex = "M\Omega"
            
            # ==============================================================
            # BOTÃO DE CONFIRMAÇÃO

            st.form_submit_button(use_container_width=True)
                
                        
        # ==============================================================

        
        g_value = - (r2/r1)
        show_l, show_c, show_r = st.columns(3)
        with show_l:
            st.metric("Resistor 1",f"{r1_value} {r1_unit}")
        with show_c:
            st.metric("Resistor 2",f"{r2_value} {r2_unit}")
        with show_r:
            st.metric("Ganho",f"{g_value:.2f}")

        # EXIBIÇÃO DA IMAGEM DO CIRCUITO

        # FORMATAÇÃO DAS LABELS DOS RESISTORES
        r1_label = f"{r1_value} {r1_latex}"
        r2_label = f"{r2_value} {r2_latex}"

        # == DESENHO DO AMPLIFICADOR ==
        amp_drawing = amp_inversor_draw(r1_label, r2_label, 'white','#0e1117')
        st.image(amp_drawing)
        # == DESENHO DO AMPLIFICADOR ==

        st.divider()
        st.markdown(eletrico_amplifier_strings[0])
    
    # ==============================================================
    # CÁLCULO DOS RESISTORES A PARTIR DO GANHO

    if tipo_amplificador == "Inversor[G]":
        st.title("Amplificador Inversor")
        st.write("Insira um valor de ganho desejado, e será exibido as combinações de resistores compatíveis.")

        with st.form("Inversor via G"):
            gain_value = st.number_input("Valor do Ganho", value=0, key="g_val")
            precision_value = st.number_input("Tolerância de Resultados", 
                                              value=20,
                                              min_value=0, 
                                              max_value=100,
                                              help="Quanto menor o valor, mais próximo da combinação perfeita",
                                              key="calc_precision")
            st.form_submit_button("Calcular", use_container_width=True)

        calculated_resistors = inv_r_combination(gain_value, precision_value)
        resistors_df = pd.DataFrame(calculated_resistors, columns=['R1', 'R2'])
        
        r1 = f"{resistors_df['R1'][0]} \Omega"
        r2 = f"{resistors_df['R2'][0]} \Omega"
        st.image(amp_inversor_draw(r1,r2))
        
        table_space = st.empty()
        if gain_value == 0:
            table_space.empty()
        else:
            table_space.dataframe(resistors_df, use_container_width=True)
        
        st.divider()
        st.markdown(eletrico_amplifier_strings[0])
    
    if tipo_amplificador == "Não Inversor[R1, R2]":
        st.title("Amplificador Não Inversor")
        st.write("Insira os valores de resistores e o ganho resultante será exibido.")

        with st.form("Não Inversor via Rs",clear_on_submit=True):
            left, center= st.columns(2)

            # ==============================================================
            # SETOR DE INPUT DO RESISTOR 1
            
            with left:
                with st.container(border=True):
                    r1_value = st.number_input("Valor do Resistor 1", min_value=1,key="r1_value")
                    r1_unit = st.selectbox("Unidade do Resistor 1",["ohms", "kilohms","megaohms"], key="r1_unit")
                    if r1_unit == "ohms":
                        r1 = r1_value
                        r1_latex = "\Omega"
                    if r1_unit == "kilohms":
                        r1 = r1_value * 1000
                        r1_latex = "K\Omega"
                    if r1_unit == "megaohms":
                        r1 = r1_value * 1000 * 1000
                        r1_latex = "M\Omega"

            # ==============================================================
            # SETOR DE INPUT DO RESISTOR 2

            with center:
                with st.container(border=True):
                    r2_value = st.number_input("Valor do Resistor 2", min_value=0,key="r2_value")
                    r2_unit = st.selectbox("Unidade do Resistor 2",["ohms", "kilohms","megaohms"], key="r2_unit")
                    if r2_unit == "ohms":
                        r2 = r2_value
                        r2_latex = "\Omega"
                    if r2_unit == "kilohms":
                        r2 = r2_value * 1000
                        r2_latex = "K\Omega"
                    if r2_unit == "megaohms":
                        r2 = r2_value * 1000 * 1000
                        r2_latex = "M\Omega"
            
            # ==============================================================
            # BOTÃO DE CONFIRMAÇÃO

            st.form_submit_button(use_container_width=True)
                
                        
        # ==============================================================

        
        g_value = 1 + (r2/r1)
        show_l, show_c, show_r = st.columns(3)
        with show_l:
            st.metric("Resistor 1",f"{r1_value} {r1_unit}")
        with show_c:
            st.metric("Resistor 2",f"{r2_value} {r2_unit}")
        with show_r:
            st.metric("Ganho",f"{g_value:.2f}")

        # EXIBIÇÃO DA IMAGEM DO CIRCUITO

        # FORMATAÇÃO DAS LABELS DOS RESISTORES
        r1_label = f"{r1_value} {r1_latex}"
        r2_label = f"{r2_value} {r2_latex}"

        # == DESENHO DO AMPLIFICADOR ==
        amp_drawing = amp_non_inversor_draw(r1_label, r2_label, 'white','#0e1117')
        st.image(amp_drawing)
        # == DESENHO DO AMPLIFICADOR ==

        st.divider()
        st.markdown(eletrico_amplifier_strings[1])