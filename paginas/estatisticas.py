from settings.settings import *

# CONFIGURAÇÕES DA PÁGINA
st.set_page_config(
    page_title="SciCalcs - Estatísticas",
    initial_sidebar_state="collapsed",
    layout="centered"
)

st.markdown(hide_st_styles, unsafe_allow_html=True)
show_pages_from_config()
hide_pages(pages_to_hide)

# CONTEÚDO DA PÁGINA
menu = option_menu(
    menu_title=None,
    options=["Home", "Estatisticas"],
    icons=["house-fill", "calculator"],
    orientation="horizontal",
    default_index=1
)
if menu == "Home":
    switch_page("Home")
st.header("Estatísticas")

# INPUT DOS DADOS
values_list_example = "1.4, 2.43, 3.52..."
values_list = st.text_input("Insira uma lista dos valores da seguinte maneira", placeholder=values_list_example, help=f"Números decimais: (1.0).")

# VERIFICANDO SE O INPUT ESTÁ VAZIO
if values_list == "":
    label_media = 0.0
    label_dp = 0.0
    label_incertezaA = 0.0
else:
    try:
        float_list = [float(value) for value in values_list.split(",")]
        label_media = func.media(float_list)
        label_dp = func.desvio_padrao(float_list)
        label_incertezaA = func.incertezaA(float_list)
    except:
        pass

# CRIAÇÃO DAS COLUNAS
top_container = st.container()
left, center, right = st.columns(3)
left_container = left.container(border=True)
center_container = center.container(border=True)
right_container = right.container(border=True)

try:
    # Ambiente Left
    with left_container:
        st.markdown("<h4 style='text-align: center; color: white;'>Média</h1>", unsafe_allow_html=True)
        if st.button(label=str(label_media), use_container_width=True, key=1):
            copy_to_clipboard(label_media)
            st.toast("Média copiada para a área de transferência!")

    # Ambiente Center
    with center_container:
        st.markdown("<h4 style='text-align: center; color: white;'>Desvio Padrão</h1>", unsafe_allow_html=True)
        if st.button(label=str(label_dp), use_container_width=True, key=2, help="O número de elementos precisa ser maior que 1"):
            copy_to_clipboard(label_dp)
            st.toast("Desvio Padrão copiado para a área de transferência!")
    
    # Ambiente Center
    with right_container:
        st.markdown("<h4 style='text-align: center; color: white;'>Incerteza Tipo A</h1>", unsafe_allow_html=True)
        if st.button(label=str(label_incertezaA), use_container_width=True, key=3, help="O número de elementos precisa ser maior que 1"):
            copy_to_clipboard(label_incertezaA)
            st.toast("Incerteza Tipo A copiada para a área de transferência!")
    
    # Ambiente Last
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; color: white;'>Incerteza Combinada</h1>", unsafe_allow_html=True)
        last_col1, last_col2 = st.columns(2)
        last_col1.text_input(label="", value=str(label_incertezaA), disabled=True)
        with last_col2:
            inc_comb_value = st.text_input(label="", placeholder="Incerteza Instrumental", help="Um único valor19")    
            if inc_comb_value == "":
                label_incerteza_combinada = 0.0
            else:
                label_incerteza_combinada = func.incerteza_combinada(float_list, float(inc_comb_value))
        if st.button(label=str(label_incerteza_combinada), use_container_width=True, key=4, help="O número de elementos precisa ser maior que 1"):
            copy_to_clipboard(label_incerteza_combinada)
            st.toast("Incerteza Combinada copiada para a área de transferência!")
except:
    with top_container:
        st.markdown("""
                    Valores inválidos, escreva uma lista de números da seguinte maneira:
                    - Números decimais com ponto: 1.8 ...
                    - Números separados por vírgula: 1,2,1.6 ...
                    - Exemplo 1: 1,2,3,4,5,6,7,8,9,10 ..
                    - Exemplo 2: 1.2, 0.5, -0.98 ...
                    """)