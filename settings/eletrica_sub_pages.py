# ======================================
# IMPORTS

# NICEGUI IMPORTS 
from nicegui import ui

# SciCalcs Internal Modules
from .gui_components import page_title, header_layout, TabsCreator
from .state_classes import ResistorState
from .defining_functions import amp_inversor_draw


# ======================================
# SUBPAGES FUNCTION DEFINITIONS

# ELÉTRICA'S PAGE "GANHO DE AMPLIFICADOR"
def ganho_amplificador():
    # Page title
    page_title('Ganho de Amplificador')

    # Base Header layout creation
    header_layout()
    
    # "Ganho de Amplificador" subpages
    calculadoras = ['Inversor [R1,R2]', 'Inversor [G]', 'Não Inversor [R1, R2]', 'Não Inversor [G]']
    
    def tab1():
        
        # CONSTANTS
        state = ResistorState()
        unidades = ['ohms', 'kilohms', 'megaohms']
        global ganho_label
        
        # PRESENTATION TEXT
        ui.markdown("""
        ## Amplificador Inversor
        Calcular o valor do ganho, de um circuito de **amplificador inversor** a partir do valor dos resistores 1 e 2 inseridos.
        
        ---
        """)

        # LAYOUT
        with ui.row().classes('w-full'):
            with ui.grid(columns=2).classes('w-full h-1/2 md:w-2/5'):
                ui.number(label="Valor do Resistor 1", on_change=lambda e: state.set_r1_value(e.value, ganho_label))
                ui.select(label="Unidade do Resistor 1", options=unidades, value='ohms', on_change=lambda e: state.set_r1_unit(e.value, ganho_label))
                
                ui.number(label="Valor do Resistor 2", on_change=lambda e: state.set_r2_value(e.value, ganho_label))
                ui.select(label="Unidade do Resistor 2", options=unidades, value='ohms', on_change=lambda e: state.set_r2_unit(e.value, ganho_label))
                
                ganho_label = ui.label("Ganho: 0.00").classes('text-xl mt-4')
            
            image = amp_inversor_draw(line_color='black',bg_color='#0e1117')
            ui.image(image).classes('w-full h-1/2 md:w-1/2')

    tabber = TabsCreator(calculadoras)
    tabber.create_tabs_header()
    tabber.create_tabs_panel(tab1)