# ------------------------------------------------
# IMPORTAÇÕES

# Importação de outros módulos
import re
import os
import schemdraw
from io import BytesIO
from pathlib import Path
import matplotlib.pyplot as plt
import schemdraw.elements as elm
from decimal import Decimal, getcontext
import pandas as pd

# IMPORTAÇÕES STREAMLIT
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# ------------------------------------------------
# FUNÇÕES STREAMLIT

# CRIAÇÃO DA GRID DE PÁGINAS DA PÁGINA INICIAL
def grid_creator(pages):

    # CRIAÇÃO DAS COLUNAS
    l1, c1, r1 = st.columns(3)

    # COLUNAS REUNIDAS
    cols = [l1, c1, r1]

    # QUANTIDADE DE PÁGINAS
    pages_amount = len(pages)
    
    # VETOR DE POSIÇÕES
    pos = [0,1,2]

    # VETOR FIXO DE ATUALIZAÇÃO
    updater  = [3,3,3]
    
    # ELE SABE A QUANTIDADE DE PÁGINAS QUE TEM
    for i in range(pages_amount):
        # CASO A POSIÇÃO SEJA MAIOR QUE O ÚLTIMO NÚMERO DA SEQUÊNCIA DE POSIÇÕES ATUAIS
        if i > pos[-1]:
            pos = [pos[j]+updater[j] for j in range(3)]
        
        # SE O INDICE DA PAGINA ATUAL É IGUAL À POSIÇÃO DESIGNADA
        if pages.index(pages[i]) == pos[0]:
            
            # NA COLUNA ESQUERDA
            with cols[0]:
                with st.container(border=True):
                    st.markdown(f"<h2 style='text-align: center; color: white;'>{pages[i]}</h1>", unsafe_allow_html=True)
                    st.image(f"img/{pages[i]}.png")
                    if st.button("ABRIR", use_container_width=True, key=pages[i]):
                        switch_page(pages[i])

        # SE O INDICE DA PAGINA ATUAL É IGUAL À POSIÇÃO DESIGNADA
        if pages.index(pages[i]) == pos[1]:
            
            # NA COLUNA DO MEIO
            with cols[1]:
                with st.container(border=True):
                    st.markdown(f"<h2 style='text-align: center; color: white;'>{pages[i]}</h1>", unsafe_allow_html=True)
                    st.image("img/" + f"{pages[i]}" + ".png")
                    if st.button("ABRIR", use_container_width=True, key=pages[i]):
                        switch_page(pages[i])

        # SE O INDICE DA PAGINA ATUAL É IGUAL À POSIÇÃO DESIGNADA
        if pages.index(pages[i]) == pos[2]:
            
            # NA COLUNA DA ESQUERDA
            with cols[2]:
                with st.container(border=True):
                    st.markdown(f"<h2 style='text-align: center; color: white;'>{pages[i]}</h1>", unsafe_allow_html=True)
                    st.image("img/" + f"{pages[i]}" + ".png")
                    if st.button("ABRIR", use_container_width=True, key=pages[i]):
                        switch_page(pages[i])


# ------------------------------------------------
# FUNÇÕES ESTATÍSTICAS

# MÉDIA
def media(medidas):
    media = sum(medidas) / len(medidas)
    return media

# DESVIO PADRÃO
def desvio_padrao(medidas):
    if len(medidas) < 2:
        return False
    else:
        media = sum(medidas) / len(medidas)
        acoplamento = []
        for amostra in medidas:
            sum_diff = (amostra - media) ** 2
            acoplamento.append(sum_diff)
        div = sum(acoplamento) / (len(medidas) - 1)
        dp = div ** 0.5
        return dp

# INCERTEZA ESTATÍSTICA, INCERTEZA TIPO A
def incertezaA(medidas):
    if len(medidas) < 2:
        return False
    else:
        # calculo da média
        media = sum(medidas) / len(medidas)
        acoplamento = []
        # calculo do desvio padrão
        for amostra in medidas:
            sum_diff = (amostra - media) ** 2
            acoplamento.append(sum_diff)
        div = sum(acoplamento) / (len(medidas) - 1)
        dp = div ** 0.5
        # calculo da incerteza do tipo A
        incerteza = dp / (len(medidas)) ** 0.5
        return incerteza

# INCERTEZA COMBINADA, COMBINAÇÃO DA INCERTEZA ESTATÍSTICA E INSTRUMENTAL
def incerteza_combinada(medidas, incerteza_b):
    if len(medidas) < 2:
        return False
    else:
        # calculo da média
        media = sum(medidas) / len(medidas)
        acoplamento = []
        # calculo do desvio padrão
        for amostra in medidas:
            sum_diff = (amostra - media) ** 2
            acoplamento.append(sum_diff)
        div = sum(acoplamento) / (len(medidas) - 1)
        dp = div ** 0.5
        # calculo da incerteza do tipo A
        incerteza_a = dp / (len(medidas)) ** 0.5

        combinada = ( (incerteza_a ** 2) + (incerteza_b ** 2) ) ** 0.5
        return combinada

# ------------------------------------------------

# VERIFICADOR DE STRING
def contains_invalid_characters(values_str):
    # Expressão regular para permitir apenas números, vírgulas e pontos
    pattern = re.compile(r'^[0-9.,]+$')
    
    # Verifica se a string corresponde ao padrão
    if pattern.match(values_str):
        return False
    else:
        return True

# ------------------------------------------------
# FUNÇÕES DE FORMATAÇÃO LATEX

# FORMATAÇÃO DE STRING LATEX DA MÉDIA
def media_latex(values_str):
    values = values_str.split(',')
    
    if len(values) > 2:
        # Se há mais de 3 elementos, pegue apenas o primeiro e o último, com ... no meio
        values_adjusted = f"{values[0]}+...+{values[-1]}"
    else:
        # Caso contrário, junte todos os elementos
        values_adjusted = '+'.join(values)
    
    expr = f"\\overline{{x}} = \\frac{{{values_adjusted}}}{{{len(values)}}}"
    return expr

# FORMATAÇÃO DE STRING LATEX DO DESVIO PADRÃO
def std_dev_latex(values_str, medidas):
    values = list(map(float, values_str.split(',')))
    n = len(values)
    
    # Calcula a média dos valores
    # mean = sum(values) / n
    mean = f"{media(medidas):.4f}".rstrip('0').rstrip('.')
    
    # Cria a string dos termos individuais (x_i - \overline{x})^2
    terms = [f"({x} - {mean})^2" for x in values]
    
    if len(terms) > 2:
        # Se há mais de 3 elementos, pegue apenas o primeiro e o último, com ... no meio
        terms_adjusted = f"{terms[0]} + ... + {terms[-1]}"
    else:
        # Caso contrário, junte todos os elementos
        terms_adjusted = ' + '.join(terms)
    
    # Cria a expressão final em LaTeX
    expr = f"S = \\sqrt{{\\frac{{{terms_adjusted}}}{{{n-1}}}}}"
    return expr

# FORMATAÇÃO DE STRING LATEX DA INCERTEZA COMBINADA
def inc_comb_latex(*uncertainties):
    # Cria a string dos termos individuais (\sigma_{i})^2
    terms = [f"({sigma})^2" for sigma in uncertainties]
    
    if len(terms) > 2:
        # Se há mais de 2 incertezas, ajuste para incluir ... no meio
        terms_adjusted = f"{terms[0]} + ... + {terms[-1]}"
    else:
        # Caso contrário, junte todos os termos
        terms_adjusted = ' + '.join(terms)
    
    # Cria a expressão final em LaTeX
    expr = f"\\sigma_{{c}} = \\sqrt{{{terms_adjusted}}}"
    return expr

# RENDERIZAÇÃO DE LATEX EM IMAGEM
def render_latex(formula, fontsize=12, dpi=300):
    """Renders LaTeX formula into Streamlit."""
    fig = plt.figure()
    fig.patch.set_alpha(0)  # Define o fundo da figura como transparente
    text = fig.text(0, 0, f'${formula}$', fontsize=fontsize, color='white')  # Define a cor do texto como branco

    fig.savefig(BytesIO(), dpi=dpi)  # triggers rendering

    bbox = text.get_window_extent()
    width, height = bbox.size / float(dpi) + 0.05
    fig.set_size_inches((width, height))

    dy = (bbox.ymin / float(dpi)) / height
    text.set_position((0, -dy))

    buffer = BytesIO()
    fig.savefig(buffer, dpi=dpi, format='png', transparent=True)  # Salva a figura com fundo transparente
    plt.close(fig)

    st.image(buffer)

def amp_inversor_draw(r1_label: str, r2_label: str, line_color: str='white',bg_color: str='#0e1117'):
    schemdraw.config(bgcolor=bg_color)
    schemdraw.config(color=line_color)
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
    return image_bytes

def amp_non_inversor_draw(r1_label: str, r2_label: str, line_color: str='white',bg_color: str='#0e1117'):
    schemdraw.config(bgcolor=bg_color)
    schemdraw.config(color=line_color)
    with schemdraw.Drawing() as d:
        op = elm.Opamp(leads=True)
        out = elm.Line().at(op.out).length(.75)
        elm.Line().up().at(op.in1).length(1.5).dot()
        d.push()
        elm.Resistor().left().label(f'${r1_label}$')
        elm.Ground()
        d.pop()
        elm.Resistor().tox(op.out).label(f'${r2_label}$')
        elm.Line().toy(op.out).dot()
        elm.Line().left(d.unit/4).at(op.in2).label('$v_{in}$', loc='left')
    
    image_bytes = d.get_imagedata('png')
    return image_bytes

# ------------------------------------------------

# FUNÇÃO QUE RETORNA COMBINAÇÕES DE RESISTORES QUE ATINGEM O GANHO INSERIDO
def inv_r_combination(gain: int, precision: int):
    getcontext().prec = 10  # Definir precisão alta para evitar problemas de ponto flutuante
    resistors = []
    tolerance = precision/100  # Definir uma margem de tolerância (1%)

    e12_base_values = [Decimal('1.0'), Decimal('1.2'), Decimal('1.5'), Decimal('1.8'),
                       Decimal('2.2'), Decimal('2.7'), Decimal('3.3'), Decimal('3.9'),
                       Decimal('4.7'), Decimal('5.6'), Decimal('6.8'), Decimal('8.2')]
    # Gerar lista de valores comerciais para resistores com alta precisão
    resistor_values = [value * (Decimal(10) ** exp) for exp in range(-2, 7) for value in e12_base_values]

    for r1 in resistor_values:
        for r2 in resistor_values:
            # Verificar se os resistores estão dentro da faixa desejada
            if r1 > Decimal('9') and r1 < Decimal('1000000') and r2 > Decimal('9') and r2 < Decimal('1000000'):
                if abs((r2 / r1) - gain) <= tolerance:
                    resistors.append([r1, r2])
    
    # Ordenar os resistores pela soma dos seus valores, como uma forma de organização
    resistors.sort(key=lambda x: x[0] + x[1])
    return resistors