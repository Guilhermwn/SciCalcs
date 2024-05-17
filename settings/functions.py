def is_zero(medidas):
    if sum(medidas) == 0:
        return True

def media(medidas):
    media = sum(medidas) / len(medidas)
    return media

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