from settings.settings import *
from settings.settings import contains_invalid_characters, render_latex

# CONFIGURAÇÕES DA PÁGINA
st.set_page_config(
    page_title="SciCalcs - Estatísticas",
    initial_sidebar_state="collapsed",
    layout="centered"
)

st.markdown(hide_st_styles, unsafe_allow_html=True)
show_pages_from_config()
# hide_pages(pages_to_hide)

# CONTEÚDO DA PÁGINA
menu = option_menu(
    menu_title=None,
    options=["Home", "Estatísticas"],
    icons=["house-fill", "calculator"],
    orientation="horizontal",
    default_index=1
)

# CASO PRESSIONAR "HOME" ELE VAI PRA PÁGINA INICIAL
if menu == "Home":
    switch_page("Home")
st.header("Estatísticas")

# INPUT DOS DADOS
values_list = st.text_input(
    label="Insira uma lista dos valores da seguinte maneira", 
    placeholder="1.4, 2.43, 3.52..." , 
    help=f"Números decimais: (1.0)."
    )

# VERIFICANDO SE O INPUT ESTÁ VAZIO
try:
    # Se o input está vazio
    if values_list == "":
        float_list = [0,0]
        label_media = 0.0
        label_dp = 0.0
        label_incertezaA = 0.0
    
    # Se o input recebe algum valor
    else:
        # Fazendo a criação da lista de valores float
        float_list = [float(value) for value in values_list.split(",")]
        label_media = f"{func.media(medidas=float_list):.8f}".rstrip('0').rstrip('.')
        label_dp = f"{func.desvio_padrao(medidas=float_list):.8f}".rstrip('0').rstrip('.')
        label_incertezaA = f"{func.incertezaA(medidas=float_list):.5f}".rstrip('0').rstrip('.')
        
        # Incerteza combinada, inicialmente em 0.0

# caso ocorra algum erro de conversão da lista para float
except ValueError:
    float_list = [0,0]
    label_media = 0.0
    label_dp = 0.0
    label_incertezaA = 0.0

    top_container = st.container()
    with top_container:
        st.error("""
                    Valores inválidos, escreva uma lista de números da seguinte maneira:
                    - Números decimais com ponto: 1.8 ...
                    - Números separados por vírgula: 1,2,1.6 ...
                    - Exemplo 1: 1,2,3,4,5,6,7,8,9,10 ..
                    - Exemplo 2: 1.2, 0.5, -0.98 ...
                    """)

# CRIAÇÃO DAS COLUNAS
left, center, right = st.columns(3)
left_container = left.container(border=True)
center_container = center.container(border=True)
right_container = right.container(border=True)

# Ambiente Left
with left_container:
    st.markdown("<h4 style='text-align: center; color: white;'>Média</h1>", unsafe_allow_html=True)
    st.code(body=label_media, line_numbers=False)

# Ambiente Center
with center_container:
    st.markdown("<h4 style='text-align: center; color: white;'>Desvio Padrão</h1>", unsafe_allow_html=True)
    st.code(body=label_dp, line_numbers=False)

# Ambiente Right
with right_container:
    st.markdown("<h4 style='text-align: center; color: white;'>Incerteza Tipo A</h1>", unsafe_allow_html=True)
    st.code(body=label_incertezaA, line_numbers=False)

# Ambiente Last
with st.container(border=True):
    st.markdown("<h4 style='text-align: center; color: white;'>Incerteza Combinada</h1>", unsafe_allow_html=True)

    last_col1, last_col2 = st.columns(2)
    with last_col1:
        st.code(body=label_incertezaA, line_numbers=False)

    with last_col2:
        inc_inst_value = st.text_input(
            label=" ", 
            placeholder="Incerteza Instrumental", 
            help="Um único valor19", 
            label_visibility="collapsed"
        )

    try:
        if inc_inst_value == "":
            label_inceteza_combinada = 0.0
        else:
            
            label_inceteza_combinada = f"{func.incerteza_combinada(float_list, float(inc_inst_value)):.8f}"
    except ValueError:
        label_inceteza_combinada = 0.0
        st.error("Insira um número válido!!")

    st.code(body=label_inceteza_combinada)


# FÓRMULAS

with st.expander("Visualização da fórmula da Média"):
    if contains_invalid_characters(values_list):
        pass
    else:
        if values_list:
            with st.container(border=True):
                st.markdown("<h5 style='text-align: center; color: white;'>Média</h1>", unsafe_allow_html=True)
                render_latex(func.media_latex(values_list))
with st.expander("Visualização da fórmula do Desvio Padrão"):
    if contains_invalid_characters(values_list):
        pass
    else:
        if values_list:
            with st.container(border=True):
                st.markdown("<h5 style='text-align: center; color: white;'>Desvio Padrão</h1>", unsafe_allow_html=True)
                render_latex(func.std_dev_latex(values_list, float_list))
with st.expander("Visualização da fórmula da Incerteza Combinada"):
    if contains_invalid_characters(values_list):
        pass
    else:
        if float(label_incertezaA)>0:
            if inc_inst_value:
                with st.container(border=True):
                    st.markdown("<h5 style='text-align: center; color: white;'>Incerteza Combinada</h1>", unsafe_allow_html=True)
                    render_latex(func.combined_uncertainty_latex(label_incertezaA, inc_inst_value))


st.divider()

# EXPLICAÇÕES 
# Explicação da média
st.markdown(estatisticas_markdown_definitions[0])

# Explicação do Desvio padrão
st.markdown(estatisticas_markdown_definitions[1])

# Explicação da Incerteza do Tipo A
st.markdown(estatisticas_markdown_definitions[2])

# Explicação da Incerteza Instrumental
st.markdown(estatisticas_markdown_definitions[3])

# Explicação da Incerteza Combinada
st.markdown(estatisticas_markdown_definitions[4])