"""
Module containing functions and a class for building elements of the SciCalcs application user interface.

Functions:
- page_title(title: str):
    Set the page title for a SciCalcs application.

- header_layout():
    Generate a header layout for the SciCalcs application.

- cards(title: str, image: Path, target: str):
    Generate a card element with title, image, and a link to a specified target.

Classes:
- TabsCreator:
    Helper class for creating tabs with headers and panels using nicegui ui module.
    Methods include:
    - __init__(tabs_list: list[str]): Initialize with a list of tab names.
    - create_tabs_header(): Create and return the tabs header with specified tab names.
    - create_tabs_panel(*ui_functions): Create tab panels associated with the tabs header
      using provided UI functions.

This module provides functionalities for structuring and styling components that are used in the SciCalcs application.
"""

# ======================================
# IMPORTS 
# ======================================

from nicegui import ui
from pathlib import Path


# ======================================
# PAGE TITLE UTILITY
# ======================================

def page_title(title: str):
    """
    Set the page title for the SciCalcs application.

    Parameters
    ----------
    title : str
        The title to be appended after 'SciCalcs - '.

    Notes
    -----
    This function uses the ui.page_title function from nicegui to set the page title
    with a specific format suitable for the SciCalcs application.
    """
    ui.page_title(f'SciCalcs - {title}')


# ======================================    
# MAIN HEADER LAYOUT
# ======================================    

def header_layout():
    """
    Generate a header layout for the SciCalcs application.

    Notes
    -----
    This function constructs a header layout using the nicegui ui module. It includes
    a link titled 'SciCalcs' with specific styling classes suitable for the application.
    """
    with ui.header():
        ui.link('SciCalcs', '/').classes(replace='p-3 text-lg text-white hover:bg-sky-700 rounded-md')


# ======================================
# GENERAL USAGE CARD
# ======================================

def cards(title:str, image:Path, target:str):
    """
    Generate a card element with title and image linked to a specified target.

    Parameters
    ----------
    title : str
        The title text to display in the card.
    image : Path
        The path to the image file to display in the card.
    target : str
        The URL target for the link associated with the card.

    Notes
    -----
    This function constructs a card element using the nicegui ui module. It includes
    a link with the specified target, a card with title and image, and applies styling
    classes for visual presentation.
    """
    with ui.link(target=target).classes(replace='text-center text-wrap text-3xl'):
        with ui.card().classes('no-shadow border-[3px] hover:scale-105'):
            ui.label(title).classes('w-64')
            ui.image(image).classes('w-64')


# ======================================
# CLASS TABS GENERATOR
# ======================================

class TabsCreator:
    """
    Helper class for creating tabs with headers and panels using nicegui ui module.

    Parameters
    ----------
    tabs_list : list[str]
        List of tab names to create.

    Attributes
    ----------
    tabs_list : list[str]
        List of tab names.
    tabs_iter : list
        List to store created tab objects.
    tabs_header : ui.tabs
        Object representing the tabs header.

    Methods
    -------
    create_tabs_header()
        Creates and returns the tabs header with specified tab names.
    
    create_tabs_panel(*ui_functions)
        Creates tab panels associated with the tabs header using provided UI functions.
    """
    def __init__(self, tabs_list: list[str]):
        self.tabs_list = tabs_list
        self.tabs_iter = list()
        self.tabs_header = None

    def create_tabs_header(self):
        """
        Create tabs header with names from self.tabs_list.

        Returns
        -------
        ui.tabs
            Object representing the tabs header.
        """
        with ui.tabs().classes('w-full') as self.tabs_header:
            for tab in self.tabs_list:
                self.tabs_iter.append(ui.tab(tab))
        return self.tabs_header

    def create_tabs_panel(self, *ui_functions):
        """
        Create tabs panels associated with the tabs header.

        Parameters
        ----------
        *ui_functions : callable
            UI functions to execute within each tab panel.
        """
        with ui.tab_panels(self.tabs_header, value=self.tabs_iter[0]).classes('w-full'):
            for i, func in zip(self.tabs_iter, ui_functions):
                with ui.tab_panel(i):
                    func()

# class GridManager:
#     def __init__(self):
#         self.columns = [
#             {'field': 'name', 'editable': True, 'sortable': True},
#             {'field': 'age', 'editable': True},
#             {'field': 'id'},
#         ]
#         self.rows = [
#             {'id': 0, 'name': 'Alice', 'age': 18},
#             {'id': 1, 'name': 'Bob', 'age': 21},
#             {'id': 2, 'name': 'Carol', 'age': 20},
#         ]
#         self.aggrid = ui.aggrid({
#             'columnDefs': self.columns,
#             'rowData': self.rows,
#             'rowSelection': 'multiple',
#             'stopEditingWhenCellsLoseFocus': True,
#         }).on('cellValueChanged', self.handle_cell_value_change)

#     def add_row(self):
#         new_id = max((dx['id'] for dx in self.rows), default=-1) + 1
#         self.rows.append({'id': new_id, 'name': 'New name', 'age': None})
#         ui.notify(f'Added row with ID {new_id}')
#         self.aggrid.update()

#     def handle_cell_value_change(self, e):
#         new_row = e.args['data']
#         ui.notify(f'Updated row to: {e.args["data"]}')
#         self.rows[:] = [row | new_row if row['id'] == new_row['id'] else row for row in self.rows]

#     async def delete_selected(self):
#         selected_id = [row['id'] for row in await self.aggrid.get_selected_rows()]
#         self.rows[:] = [row for row in self.rows if row['id'] not in selected_id]
#         ui.notify(f'Deleted row with ID {selected_id}')
#         self.aggrid.update()