"""
This file contains functions to define the main pages for the SciCalcs application. 

Pages
-----
- Home: The home page layout (`home_layout`) sets up the initial view of the application,
  including a welcome message and navigation cards to different sections.

- Elétrica: The `eletrica_layout` function defines the layout for the electrical section 
  main page, displaying navigation cards for specific electrical subcategories like amplifier 
  gain, resistors, and inductors.

- Estatística: The `estatistica_layout` function sets up the layout for the statistics 
  section main page, showing navigation cards for statistical subcategories such as 
  uncertainties and graph generation.

- 404 Not Found: The `not_found_404` function defines the layout for the 404 error page, 
  which is displayed when a requested page is not found. It includes setting the page 
  title and displaying a "Not Found" message.

This file contributes to the organization and structure of the SciCalcs application by 
defining the visual and navigational elements of its main pages.

Functions
---------
- home_layout(): Layout for the Home Page.
- eletrica_layout(): Layout for the main page of Elétrica.
- estatistica_layout(): Layout for the main page of Estatística.
- not_found_404(): Layout for the 404 error, not found page.
"""

# ======================================
# IMPORTS

from nicegui import ui

# SciCalcs internal files
from .gui_components import  page_title, header_layout, cards
from .defining_functions import clear_text

# ======================================
# MAIN PAGE LAYOUT FUNCTIONS

# HOME PAGE LAYOUT
def home_layout():
    """
    Layout for the Home Page.

    This function sets up the layout for the home page of the SciCalcs application. It includes setting the 
    page title, adding a header, and displaying navigation cards for different sections.

    Examples
    --------
    >>> home_layout()
    """
    page_title('Home')
    header_layout()
    ui.markdown('## Bem vindo ao SciCalcs\n ---').classes('w-full')
    with ui.row().classes('w-full p-4'):
        cards("Elétrico", "img/Eletrico.png", '/eletrica')
        cards("Estatística", "img/Estatisticas.png", '/estatistica')


# ======================================
# ELETRICA PAGE LAYOUT

def eletrica_layout():
    """
    Layout for the main page of Elétrica.

    This function sets up the layout for the main page of the Elétrica section in the SciCalcs application. 
    It includes setting the page title, adding a header, and displaying navigation cards for various 
    electrical subcategories.

    Examples
    --------
    >>> eletrica_layout()
    """
    # Constantes
    subcategorias = ['Ganho de amplificador', "resistores", "indutores"]

    # página
    page_title('Elétrica')
    header_layout()
    with ui.row():
        for subcategory in subcategorias:
            cards(subcategory, 
                  "img/Eletrico.png", 
                  f'/eletrica/{clear_text(subcategory)}')


# ======================================
# ESTATISTICA PAGE LAYOUT

def estatistica_layout():
    """
    Layout for the main page of Estatistica.

    This function sets up the layout for the main page of the Estatistica section in the SciCalcs application. 
    It includes setting the page title, adding a header, and displaying navigation cards for various 
    statistical subcategories.

    Examples
    --------
    >>> estatistica_layout()
    """
    subcategorias = ['Incertezas', 'Geração de Gráfico']
    page_title('Estatistica')
    header_layout()
    with ui.row():
        for subcategory in subcategorias:
            cards(subcategory, 
                  "img/Estatisticas.png", 
                  f'/estatistica/{clear_text(subcategory)}')


# ======================================
# NOT FOUND PAGE LAYOUT

def not_found_404():
    """
    Layout for the 404 error, not found page.

    This function sets up the layout for the 404 error page, which is displayed when a requested page 
    cannot be found. It includes setting the page title and displaying a "Not Found" message.

    Examples
    --------
    >>> not_found_404()
    """
    page_title('Indisponível')
    ui.label("Not Found")

