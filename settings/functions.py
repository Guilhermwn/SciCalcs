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
# FUNÇÕES ESTATÍSTICAS

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
    mean = f"{media(medidas)}".rstrip('0').rstrip('.')
    
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
def combined_uncertainty_latex(*uncertainties):
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