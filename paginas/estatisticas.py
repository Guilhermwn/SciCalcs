from settings.settings import *
from settings.functions import *
from settings.strings import *
# from settings.functions import contains_invalid_characters, render_latex

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

option = st.selectbox("Label",
                                options=["Incertezas Associadas",
                                         "Geração de Gráficos",
                                         "Planilha Incertezas"],
                                placeholder="Escolha o que fazer:",
                                index=0, 
                                label_visibility="collapsed")
st.divider()

# =====================================================
# PÁGINA CÁLCULO DE INCERTEZAS

if option == "Incertezas Associadas":
    
    st.title("Incertezas Associadas")
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
            label_media = f"{media(medidas=float_list):.8f}".rstrip('0').rstrip('.')
            label_dp = f"{desvio_padrao(medidas=float_list):.8f}".rstrip('0').rstrip('.')
            label_incertezaA = f"{incertezaA(medidas=float_list):.5f}".rstrip('0').rstrip('.')
            
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
                
                label_inceteza_combinada = f"{incerteza_combinada(float_list, float(inc_inst_value)):.8f}"
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
                    render_latex(media_latex(values_list))
    with st.expander("Visualização da fórmula do Desvio Padrão"):
        if contains_invalid_characters(values_list):
            pass
        else:
            if values_list:
                with st.container(border=True):
                    st.markdown("<h5 style='text-align: center; color: white;'>Desvio Padrão</h1>", unsafe_allow_html=True)
                    render_latex(std_dev_latex(values_list, float_list))
    with st.expander("Visualização da fórmula da Incerteza Combinada"):
        if contains_invalid_characters(values_list):
            pass
        else:
            if float(label_incertezaA)>0:
                if inc_inst_value:
                    with st.container(border=True):
                        st.markdown("<h5 style='text-align: center; color: white;'>Incerteza Combinada</h1>", unsafe_allow_html=True)
                        render_latex(inc_comb_latex(label_incertezaA, inc_inst_value))


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


# =====================================================
# PÁGINA DE GERAÇÃO DE GRÁFICOS

if option == "Geração de Gráficos":

    color_map = {
        "Padrão": "#1f77b4",
        "Laranja": "#ff7f0e",
        "Verde": "#2ca02c",
        "Vermelho": "#d62728",
        "Roxo": "#9467bd",
        "Marrom": "#8c564b",
        "Rosa": "#e377c2" ,
        "Cinza": "#7f7f7f",
        "Verde Claro": "#bcbd22",
        "Azul Claro": "#17becf",
    }
    line_style_map = {
        "Sólido": "-",
        "Tracejada": "--",
        "Tracejada + Ponto": "-.",
        "Pontuada": ":"
    }
    markers_style_map = {
        "Padrão": "o",
        "Ponto": ".",
        "Triângulo": "^",
        "Tri": "2",
        "Quadrado" : "s",
        "Mais": "P",
        "Estrela": "*",
    }

    st.title("Geração de Gráficos")

    graph_type = st.selectbox("Tipo de gráfico",["Linha","Dispersão"])
    
    # =====================================================
    # TIPOS DE GRÁFICO SELECIONADOS

    # =====================================================
    # GRÁFICO DE LINHA
    if graph_type == "Linha":

        # FORMULÁRIO DE GERAÇÃO
        with st.form("Line Chart Generator"):
            st.write("Insira os valores dos eixos **X** e **Y**:")
            
            # DEFINIÇÃO DOS VALORES DOS EIXOS
            x_axes = st.text_area("Valores do Eixo X")
            y_axes = st.text_area("Valores do Eixo Y")
            
            # CUSTOMIZAÇÕES
            with st.expander("Customizações", expanded=False):
                title_graph = st.text_input("Título do Gráfico")
                title_x_axis = st.text_input("Título do eixo X")
                title_y_axis = st.text_input("Título do eixo Y")
                
                line_color = st.selectbox("Cor da linha",list(color_map.keys()))
                line_style_set = st.selectbox("Estilo da Linha", list(line_style_map.keys()))
                
                graph_theme = st.selectbox("Tema do Gráfico", index=5,options=plt.style.available)
            
            # BOTÃO DE GERAÇÃO
            st.form_submit_button("Gerar", use_container_width=True)

    # =====================================================
    # GRÁFICO DE DISPERSÃO
    if graph_type == "Dispersão":

        # FORMULÁRIO DE GERAÇÃO
        with st.form("Scatter Chart Generator"):
            st.write("Insira os valores dos eixos **X** e **Y**:")
            
            # DEFINIÇÃO DOS VALORES DE DOS EIXOS
            x_axes = st.text_area("Valores do Eixo X")
            y_axes = st.text_area("Valores do Eixo Y")
            
            # CUSTOMIZAÇÕES
            with st.expander("Customizações", expanded=False):
                title_graph = st.text_input("Título do Gráfico")
                title_x_axis = st.text_input("Título do eixo X")
                title_y_axis = st.text_input("Título do eixo Y")
                
                dot_color = st.selectbox("Cor dos pontos",list(color_map.keys()))
                markers_style_set = st.selectbox("Estilo de marcadores", list(markers_style_map.keys()))

                graph_theme = st.selectbox("Tema do Gráfico", index=5,options=plt.style.available)
            
            # BOTÃO DE GERAÇÃO
            st.form_submit_button("Gerar", use_container_width=True)
        
       
    # =====================================================
    # GERAÇÃO DO GRÁFICO COM BASE NAS INFORMAÇÕES DO FORMULÁRIO
    
    # VALIDANDO CARACTERES CORRETOS
    if validar_string_numerica(x_axes):
        x_nums = [float(num) for num in x_axes.split(',')]
        y_nums = [float(num) for num in y_axes.split(',')]
    else:
        x_nums = [0]
        y_nums = [0]

    # PLOT DO GRÁFICO
    plt.style.use(graph_theme)
    fig, ax = plt.subplots()

    # CASO GRÁFICO SELECIONADO FOR UM GRÁFICO DE LINHA
    if graph_type == "Linha":
        ax.plot(x_nums,
                y_nums,
                color=color_map[line_color],
                linestyle=line_style_map[line_style_set],)

        font_size = 20
        ax.set_xlabel(title_x_axis, fontsize=font_size)
        ax.set_ylabel(title_y_axis, fontsize=font_size)
        ax.set_title(title_graph, fontsize=font_size)

    
    ## CASO GRÁFICO SELECIONADO FOR UM GRÁFICO DE DISPERSÃO
    elif graph_type == "Dispersão":    
        ax.scatter(
            x_nums,
            y_nums,
            color=color_map[dot_color],
            marker=markers_style_map[markers_style_set])
        
        font_size = 14
        ax.set_xlabel(title_x_axis, fontsize=font_size)
        ax.set_ylabel(title_y_axis, fontsize=font_size)
        ax.set_title(title_graph, fontsize=font_size)

    
    # EXIBIÇÃO DO GRÁFICO
    with st.container(border=True):
        st.pyplot(fig)
        plot_generated_pdf = BytesIO()
        plot_generated_jpg = BytesIO()
        
        # GERAÇÃO DO NOME DO ARQUIVO
        if title_graph == "":
            file_name = [f"graph_scicalcs.pdf",f"graph_scicalcs.jpg"]
        else:
            file_name = [f"{title_graph}.pdf", f"{title_graph}.jpg"]
        
        plt.savefig(plot_generated_pdf, dpi=300,format='pdf')
        plt.savefig(plot_generated_jpg, dpi=300,format='jpg')

        # BOTÕES DE DOWNLOAD DO GRÁFICO GERADO
        donwload_slot_l, donwload_slot_r = st.columns(2)
        with donwload_slot_l:
            st.download_button(
                label="Baixar Gráfico PDF",
                data=plot_generated_pdf,
                file_name=file_name[0],
                mime="application/pdf",
                use_container_width=True
            )
        with donwload_slot_r:
            st.download_button(
                label="Baixar Gráfico JPG",
                data=plot_generated_jpg,
                file_name=file_name[1],
                mime="image/jpeg",
                use_container_width=True
            )

if option == "Planilha Incertezas":
    # =====================================================
    # CONSTANTES
    medias = list()
    desv_pad = list()
    incer_a = list()
    incer_c = list()

    # =====================================================
    # PÁGINA 
    
    # TÍTULO DA PÁGINA
    st.title("Incertezas calculadas a partir de um arquivo")
    
    # SEÇÃO DE UPLOAD DO ARQUIVO
    uploaded_file = st.file_uploader("Escolha um arquivo", type=["xlsx", "csv"])
    bytes_data  = uploaded_file
    
    if bytes_data is not None:
        data_name = uploaded_file.name
        data_name_split = data_name.split('.')
        
        if "xlsx" in data_name:
            df = pd.read_excel(bytes_data)
        elif "csv" in data_name:
            df = pd.read_csv(bytes_data)
        
        colunas = df.columns
        df.set_index(colunas[0], inplace=True)
        df.index.name = 'Medidas'

        incer_b = st.number_input('Insira a incerteza instrumental',placeholder='Incerteza Instrumental/Incerteza B')
        
        st.header('Planilha Inserida')
        st.dataframe(df, use_container_width=True)

        for col in colunas[1:]:
            medidas = df[col].tolist()
            medias.append(media(medidas))
            desv_pad.append(desvio_padrao(medidas))
            incer_a.append(incertezaA(medidas))
            incer_c.append(incerteza_combinada(medidas, incer_b))
        
        df.loc['Média'] = medias
        df.loc['Desvio Padrão'] = desv_pad
        df.loc['Incerteza A'] = incer_a
        df.loc['Incerteza B'] = incer_b
        df.loc['Incerteza C'] = incer_c

        st.header('Planilha calculada')
        with st.container(border=True):
            st.dataframe(df, use_container_width=True)
            
            # OPÇÃO DE BAIXAR A PLANILHA COMO CSV
            csv = convert_to_csv(df)
            download1 = st.download_button(
                label="Baixar como CSV",
                data=csv,
                file_name=f'{data_name_split[0]}.csv',
                mime='text/csv',
                use_container_width=True
            )
            # OPÇÃO DE BAIXAR A PLANILHA COMO EXCEL
            excel = convert_to_excel(df)
            download1 = st.download_button(
                label="Baixar como EXCEL",
                data=excel,
                file_name=f'{data_name_split[0]}.xlsx',
                mime='application/vnd.ms-excel',
                use_container_width=True
            )