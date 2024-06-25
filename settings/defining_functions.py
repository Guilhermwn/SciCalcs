"""
Module for text processing and schematic drawing generation.

This module provides functions for text cleaning and generating
schematic drawings of inverting amplifiers.

Functions
---------
clear_text(text)
    Convert the given text to lowercase, replace spaces with underscores,
    and remove any non-ASCII characters.

amp_inversor_draw(line_color='white', bg_color='#0e1117')
    Generate a schematic drawing of an inverting amplifier and return it
    as a base64 encoded PNG image.

Examples
--------
>>> clear_text("Hello World!")
'hello_world'

>>> clear_text("Café com leite")
'cafe_com_leite'

>>> amp_inversor_draw(line_color='black', bg_color='white')
'data:image/png;base64,...'
"""

# ======================================
############### IMPORTS ################
# ======================================

import schemdraw 
import schemdraw.elements as elm
from io import BytesIO
import base64
import unidecode as uni
import pandas as pd


# ======================================
############# FUNCTIONS ################
# ======================================


# ======================================
# CLEAR TEXT OF DECORATIONS AND UNCOMMON CARACTERS
# ======================================
def clear_text(text):
    """
    Convert the given text to lowercase, replace spaces with underscores, and remove any non-ASCII characters.

    Parameters
    ----------
    text : str
        The input string to be cleaned.

    Returns
    -------
    str
        The cleaned string with spaces replaced by underscores and non-ASCII characters removed.

    Examples
    --------
    >>> clear_text("Hello World!")
    'hello_world'
    
    >>> clear_text("Café com leite")
    'cafe_com_leite'
    """
    return uni.unidecode(text.casefold().replace(" ", "_"))


# ======================================
# INVERTER AMPLIFIER DRAWING GENERATOR
# ======================================

def amp_inversor_draw(line_color: str='white',bg_color: str='#0e1117'):
        """
        Generate a schematic drawing of an inverting amplifier and return it as a base64 encoded PNG image.

        Parameters
        ----------
        line_color : str, optional
            Color of the lines in the schematic, by default 'white'.
        bg_color : str, optional
            Background color of the schematic, by default '#0e1117'.

        Returns
        -------
        str
            Base64 encoded PNG image data URI of the inverting amplifier schematic.

        Examples
        --------
        >>> amp_inversor_draw(line_color='black', bg_color='white')
        'data:image/png;base64,...'
        """
        # r1_label: str, r2_label: str, 
        schemdraw.config(bgcolor=bg_color)
        schemdraw.config(color=line_color)
        with schemdraw.Drawing(show=False,) as d:
            op = elm.Opamp(leads=True)
            elm.Line().down(d.unit/4).at(op.in2)
            elm.Ground(lead=False)
            Rin = elm.Resistor().at(op.in1).left().idot().label(f'$R_1$', loc='bot').label('$v_{in}$', loc='left')
            elm.Line().up(d.unit/2).at(op.in1)
            elm.Resistor().tox(op.out).label(f'$R_2$')
            elm.Line().toy(op.out).dot()
            elm.Line().right(d.unit/4).at(op.out).label('$v_{o}$', loc='right')
            
            # Salvar a imagem em um buffer
            buffer = BytesIO()
            d.save(buffer)
            buffer.seek(0)
        
        # Converter a imagem para base64
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        # image_bytes = d.get_imagedata('png')
        # return image_bytes
        return f"data:image/png;base64,{image_base64}"


# ======================================
# VISIBILITY MANAGEMENT OF NICEGUI FUNCTION
# ======================================

def visibility_management(state: bool ,*nicegui_elements):
    for element in nicegui_elements:
        element.set_visibility(state)


# ======================================
# CONVERTE UM DATAFRAME INSERIDO EM UM ARQUIVO CSV
# ======================================

def convert_to_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=True).encode('utf-8')


# ======================================
# CONVERTE UM DATAFRAME INSERIDO EM UM ARQUIVO EXCEL
# ======================================

def convert_to_excel(df):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=True)
    buffer.seek(0)
    excel_data = buffer.getvalue()
    b64_excel = base64.b64encode(excel_data).decode()
    return f"data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_excel}"