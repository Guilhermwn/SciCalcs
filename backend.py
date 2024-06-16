from nicegui import ui
from frontend import *

@ui.page('/')
async def home_page():
    # home_layout()
    ui.button('ELÉTRICA', on_click=lambda: ui.navigate.to('/eletrica'))
    ui.button('ESTATÍSTICA', on_click=lambda: ui.navigate.to('/estatistica'))

@ui.page('/{category}')
async def category_selector(category):
    if category == 'eletrica':
        eletrica_layout()
    elif category == 'estatistica':
        estatistica_layout()
    else:
        not_found_404()

@ui.page('/{category}/{subcategory}')
async def subcatery_calculator(category, subcategory):
    if category == 'eletrica':
        if subcategory == 'Ganho de amplificador'.casefold():
            ganho_amplificador()
        

ui.run()