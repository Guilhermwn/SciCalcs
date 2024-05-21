# ------------------------------------------------
# IMPORTAÇÕES

# Importação de outros módulos
import re

# Importação Streamlit
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import show_pages_from_config, hide_pages
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

# Importação de módulos internas
import settings.functions as func

# ------------------------------------------------
# CONFIGURAÇÕES

# hide_st_styles = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# header {visibility: hidden;}
# [data-testid="collapsedControl"] {display: none;}
# </style>
# """

hide_st_styles = ""

# Páginas a esconder na sidebar
pages_to_hide = ["Home", "Estatisticas"]

# ------------------------------------------------
# EXPLICAÇÕES USADAS NA PÁGINA "ESTATÍSTICAS"
estatisticas_markdown_definitions = [
    r"""
    ### Média
    A média aritmética, frequentemente referida apenas como "média", é uma medida estatística utilizada para representar um conjunto de dados por um valor central típico. O cálculo da média é feito somando todos os valores de um conjunto de dados e, em seguida, dividindo essa soma pelo número total de valores. A fórmula matemática para a média é representada como:            

    $$
    \overline{x} = \frac{\Sigma x_{i} }{n}
    $$

    Onde:
    - $\overline{x}$ representa a média aritmética. 
    - $\Sigma x_{i}$​ indica a soma de todos os valores individuais $(x_{i})​$ no conjunto de dados.
    - $n$ é o número total de valores no conjunto.
    """,

    r"""
    ### Desvio padrão
    O desvio padrão é uma medida estatística que quantifica a quantidade de variação ou dispersão dos valores em um conjunto de dados. Em outras palavras, ele indica o quão espalhados os valores estão em relação à média. A fórmula para calcular o desvio padrão de uma amostra é:

    $$
    S = \sqrt{\frac{\Sigma (x_{i} - \overline{x})^2}{n-1}}
    $$
                
    Onde:
    - $S$ representa o desvio padrão da amostra.
    - $\Sigma (x_{i} - \overline{x})^2$ é a soma dos quadrados das diferenças entre cada valor $(x_{i})$ e a média $(\overline{x})$.
    - $n$ é o número total de valores na amostra.
    """,

    r"""
    ### Incerteza Tipo A
    A incerteza do tipo A está associada à dispersão de valores obtidos através de múltiplas medições repetidas sob condições idênticas. Ela é determinada pelo desvio padrão da amostra e pelo número de medições realizadas.

    Por exemplo, considere um experimento em que foram realizadas quatro medições do diâmetro do mesmo pedaço de cano sob as mesmas condições.

    A incerteza do Tipo A($\sigma_{a}$) é obtida através do seguinte cálculo:

    $$
    \sigma_{a} = \frac{S}{\sqrt{n}}
    $$

    Onde:
    - $\sigma_{a}$ é a incerteza do tipo A.
    - $S$ é o desvio padrão da amostra
    - $n$ é o número de medições ou valores na amostra.
    """,

    r"""
    ### Incerteza Instrumental
    A **Incerteza B** ou **Incerteza Instrumental**($\sigma_b$), é a incerteza associada às limitações e precisão de um instrumento de medição. Ela reflete a margem de erro intrínseca do dispositivo, que pode ser devido a fatores como a resolução do instrumento, desgaste, calibração inadequada, ou variações ambientais. Este valor é geralmente fornecido pelo fabricante do instrumento e indica o grau de confiança que se pode ter nas medições realizadas com aquele equipamento. Por exemplo, um termômetro com uma incerteza instrumental de $\pm 0,5°\text{C}$ significa que as leituras podem variar em até $0,5°\text{C}$ acima ou abaixo do valor real.
    """,

    r"""
    ### Incerteza Combinada
    A **Incerteza do Tipo C** ou **Incerteza Combinada**, a combinação de incerteza do tipo A (estatística), incerteza do tipo B (instrumental ou sistemática), e outras possíveis contribuições, para determinar a incerteza total associada a uma medição, utilizando o método de propagação de incerteza, como a regra da soma quadrática para combinar as incertezas de diferentes fontes. A fórmula da incerteza combinada geralmente é expressa como:

    $$
    \sigma_{c} = \sqrt{(\sigma_{a})^2 + (\sigma_{b})^2 + \dots}
    $$

    """
]

# ------------------------------------------------
# FUNÇÕES EXTRAS

# Função para verificar caso haja um caractere errado na string
def contains_invalid_characters(values_str):
    # Expressão regular para permitir apenas números, vírgulas e pontos
    pattern = re.compile(r'^[0-9.,]+$')
    
    # Verifica se a string corresponde ao padrão
    if pattern.match(values_str):
        return False
    else:
        return True