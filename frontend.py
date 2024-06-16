# ======================================
# IMPORTS

from pathlib import Path
from nicegui import ui

# ======================================
# LAYOUT FUNCTIONS

# MAIN HEADER LAYOUT
def header_layout():
    with ui.header():
        ui.link('SciCalcs', '/').classes(replace='p-3 text-lg text-white hover:bg-sky-700 rounded-md')

# HOME PAGE CARD LAYOUT
def cards(title:str, image:Path, target:str):
    with ui.link(target=target).classes(replace='text-center text-wrap text-3xl'):
        with ui.card().classes('no-shadow border-[3px] hover:scale-105'):
            ui.label(title).classes('w-64')
            ui.image(image).classes('w-64')

# ======================================
# MAIN PAGE LAYOUT FUNCTIONS

# HOME PAGE LAYOUT
def home_layout():
    ui.page_title('Scicalcs - Home')
    header_layout()
    ui.markdown('## Bem vindo ao SciCalcs\n ---').classes('w-full')
    cards("Elétrico", "img/Eletrico.png", '/eletrica')

# ELETRICA PAGE LAYOUT
def eletrica_layout():
    # Constantes
    subcategorias = ['Ganho de amplificador', "resistores", "indutores"]
    
    # página
    ui.page_title('Scicalcs - Elétrica')
    header_layout()
    for subcategory in subcategorias:
        cards(subcategory, "img/Eletrico.png", f'/eletrica/{subcategory.casefold()}')

# ESTATISTICA PAGE LAYOUT
def estatistica_layout():
    pass

# NOT FOUND PAGE LAYOUT
def not_found_404():
    ui.label("Not Found")

# ======================================
# SUBCATEGOY PAGES LAYOUT

def ganho_amplificador():

    header_layout()
    calculadoras = ['Inversor [R1,R2]', 'Inversor [G]', 'Não Inversor [R1, R2]']
    with ui.tabs().classes('w-full') as tabs:
        tabs_iter = []
        for tab in calculadoras:
            tabs_iter.append(
                ui.tab(tab)
            )
    with ui.tab_panels(tabs, value=tabs_iter[0]).classes('w-full'):
        
        # Página do Amplificador Inversor [R1, R2]
        with ui.tab_panel(tabs_iter[0]):

            class ResistorState:
                def __init__(self):
                    self.r1_value = 0
                    self.r1_unit = 'ohms'
                    self.r2_value = 0
                    self.r2_unit = 'ohms'
                    self.ganho = 0

                def set_r1_value(self, value):
                    self.r1_value = value
                    self.calculate_ganho()

                def set_r1_unit(self, unit):
                    self.r1_unit = unit
                    self.calculate_ganho()

                def set_r2_value(self, value):
                    self.r2_value = value
                    self.calculate_ganho()

                def set_r2_unit(self, unit):
                    self.r2_unit = unit
                    self.calculate_ganho()

                def calculate_ganho(self):
                    try:
                        r1 = self.convert_to_ohms(self.r1_value, self.r1_unit)
                        r2 = self.convert_to_ohms(self.r2_value, self.r2_unit)
                        if r1 == 0:
                            self.ganho = "Erro: R1 não pode ser zero"
                        else:
                            self.ganho = - (r2 / r1)
                    except Exception as e:
                        self.ganho = f"Erro: {str(e)}"
                    ganho_label.set_text(f"Ganho: {self.ganho}")

                def convert_to_ohms(self, value, unit):
                    if unit == 'kilohms':
                        return value * 1e3
                    elif unit == 'megaohms':
                        return value * 1e6
                    return value

            state = ResistorState()
            
            ui.markdown("""
            ## Amplificador Inversor
            Calcular o valor do ganho, de um circuito de **amplificador inversor** a partir do valor dos resistores 1 e 2 inseridos.
            """)
            unidades = ['ohms', 'kilohms', 'megaohms']
            ui.number(label="Valor do Resistor 1", on_change=lambda e: state.set_r1_value(e.value))
            ui.select(label="Unidade do Resistor 1", options=['ohms', 'kilohms', 'megaohms'], value='ohms', on_change=lambda e: state.set_r1_unit(e.value))
            ui.number(label="Valor do Resistor 2", on_change=lambda e: state.set_r2_value(e.value))
            ui.select(label="Unidade do Resistor 2", options=['ohms', 'kilohms', 'megaohms'], value='ohms', on_change=lambda e: state.set_r2_unit(e.value))
            global ganho_label
            ganho_label = ui.label("Ganho: 0.00").classes('text-xl mt-4')


        # Página do Amplificador Inversor [G]
        with ui.tab_panel(tabs_iter[1]):
            ui.markdown("""
            ## Amplificador Inversor
            Gerar sugestão de combinação de resistores para o valor de ganho inserido.
            """)
            ui.number(label="Ganho")
        
        # Página do Amplificador Não Inversor [R1, R2]
        with ui.tab_panel(tabs_iter[2]):
            pass