# ======================================
# IMPORTS
# ======================================
from nicegui import ui, app

# SciCalcs Internal Modules
from settings.mainpages import home_layout, eletrica_layout, estatistica_layout, not_found_404
from settings.eletrica_sub_pages import ganho_amplificador
from settings.estatistica_sub_pages import incertezas, graph_generation
from settings.defining_functions import clear_text

# ======================================
# ROUTES HANDLING
# ======================================

app.add_static_files('/img', 'img')


@ui.page('/')
async def home_page():
    home_layout()

@ui.page('/{category}')
async def category_selector(category):
    if category == 'eletrica':
        eletrica_layout()
    elif category == 'estatistica':
        estatistica_layout()
    # else:
    #     not_found_404()

@ui.page('/{category}/{subcategory}')
async def subcatery_calculator(category, subcategory):
    if category == 'eletrica':
        if subcategory == clear_text('Ganho de amplificador'):
            ganho_amplificador()
        # else:
        #     not_found_404()
    
    if category == 'estatistica':
        if subcategory == clear_text('Incertezas'):
            incertezas()
        if subcategory == clear_text('Geração de Gráfico'):
            graph_generation()
        # else:
        #     not_found_404()
        

ui.run(reload=False)
# ui.run(host='192.168.1.10')

