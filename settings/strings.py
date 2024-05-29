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

eletrico_amplifier_strings = [
    r"""
    ### Explicação
    Um amplificador operacional (amp op) inversor é um circuito amplificador que utiliza um amplificador operacional para amplificar um sinal de entrada com inversão de fase. Isso significa que a saída é um sinal amplificado que é 180 graus fora de fase em relação ao sinal de entrada. A configuração básica inclui um resistor de entrada ($R_{\text{in}}$) e um resistor de realimentação ($R_f$) conectados ao amplificador operacional.

    ### Funcionamento
    1. **Entrada de Sinal (Vin):** O sinal de entrada é aplicado ao terminal inversor ($V_{-}$) do amplificador operacional através do resistor de entrada ($R_{\text{in}}$). O terminal não inversor ($V_{+}$) é geralmente conectado ao terra (0V).
    2. **Realimentação:** O resistor de realimentação ($R_f$) é conectado entre a saída do amplificador operacional e o terminal inversor ($V_{-}$). Esse resistor fornece uma realimentação negativa ao circuito.
    3. **Amplificação:** O amplificador operacional ajusta a saída ($V_{\text{out}}$) para manter a tensão no terminal inversor ($V_{-}$) igual à do terminal não inversor ($V_{+}$), que está em 0V (terra). Devido à alta impedância de entrada e ao ganho infinito ideal do amplificador operacional, a corrente que entra no terminal inversor é desprezível, fazendo com que a corrente através de $R_{\text{in}}$ seja igual à corrente através de $R_f$.

    ### Fórmula
    A relação entre a tensão de entrada ($V_{\text{in}}$) e a tensão de saída ($V_{\text{out}}$) é dada pela fórmula do ganho do amplificador inversor:
    
    $$ V_{\text{out}} = -\left(\frac{R_f}{R_{\text{in}}}\right) V_{\text{in}} $$

    ### Explicação da Fórmula
    - **Ganho ($-\frac{R_f}{R_{\text{in}}}$):** O ganho do amplificador inversor é determinado pela razão entre o resistor de realimentação ($R_f$) e o resistor de entrada ($R_{\text{in}}$). O sinal negativo indica que a saída está em fase oposta à entrada (inversão de fase).
    - **Corrente:** A corrente que flui através de $R_{\text{in}}$ (devido a $V_{\text{in}}$) é a mesma que flui através de $R_f$ (devido a $V_{\text{out}}$) porque a corrente de entrada do amplificador operacional é praticamente zero.
    - **Realimentação Negativa:** O amplificador operacional ajusta sua saída para manter o terminal inversor em um potencial próximo ao terra (0V), garantindo que a tensão de entrada seja proporcionalmente amplificada e invertida.

    ### Exemplo Prático
    Se você deseja um ganho de 50, você precisa escolher $R_f$ e $R_{\text{in}}$ de forma que:
    
    $$ 50 = \frac{R_f}{R_{\text{in}}} $$

    Por exemplo, se $R_{\text{in}}$ é 1kΩ, então $R_f$ deve ser 50kΩ para obter o ganho desejado de -50.
    """,
    r"""
    ### Explicação
    Um amplificador operacional (amp op) não inversor é um circuito que amplifica um sinal de entrada sem inverter sua fase. A configuração básica inclui dois resistores ($R_1$ e $R_f$) e um amplificador operacional.

    ### Funcionamento
    1. **Entrada de Sinal (Vin):** O sinal de entrada é aplicado ao terminal não inversor ($V_{+}$) do amplificador operacional.
    2. **Realimentação:** O resistor $R_f$ é conectado entre a saída ($V_{\text{out}}$) e o terminal inversor ($V_{-}$), e o resistor $R_1$ é conectado entre o terminal inversor ($V_{-}$) e o terra.
    3. **Amplificação:** O amplificador operacional ajusta a saída para manter $V_{-}$ igual a $V_{+}$.

    ### Fórmula
    A relação entre a tensão de entrada ($V_{\text{in}}$) e a tensão de saída ($V_{\text{out}}$) é dada pela fórmula do ganho do amplificador não inversor:

    $$ V_{\text{out}} = \left(1 + \frac{R_f}{R_1}\right) V_{\text{in}} $$

    ### Explicação da Fórmula
    - **Ganho ($1 + \frac{R_f}{R_1}$):** O ganho do amplificador não inversor é determinado pela razão entre $R_f$ e $R_1$, mais 1.
    - **Realimentação Negativa:** O amplificador operacional ajusta a saída para manter $V_{-}$ igual a $V_{+}$, resultando em uma amplificação proporcional sem inversão de fase.

    ### Exemplo Prático
    Se você deseja um ganho de 11, você pode escolher $R_f$ como 10kΩ e $R_1$ como 1kΩ:

    $$ 11 = 1 + \frac{10kΩ}{1kΩ} $$

    Assim, o sinal de entrada é amplificado 11 vezes sem inversão de fase.
    """
]