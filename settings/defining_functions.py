"""
Module for functions
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
    """
    Manage the visibility state of multiple NiceGUI elements.

    Parameters
    ----------
    state : bool
        The desired visibility state. If `True`, elements will be visible.
        If `False`, elements will be hidden.
    *nicegui_elements : tuple
        A variable number of NiceGUI elements whose visibility will be managed.

    Returns
    -------
    None
        This function does not return any value. It modifies the visibility state of the provided elements.

    Examples
    --------
    >>> element1 = ui.label('Some Text')
    >>> element2 = ui.input('Input some data')
    >>> with ui.header() as element3:
        ...
    >>> visibility_management(False, element1, element2, element3)
    Both element1 and element2 will be hidden.
    """
    for element in nicegui_elements:
        element.set_visibility(state)


# ======================================
# CONVERTE UM DATAFRAME INSERIDO EM UM ARQUIVO CSV
# ======================================

def convert_to_csv(df: pd.DataFrame):
    """
    Convert a pandas DataFrame to a CSV format and encode it as UTF-8.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be converted to CSV.

    Returns
    -------
    bytes
        The CSV representation of the DataFrame, encoded as UTF-8.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    >>> csv_bytes = convert_to_csv(df)
    >>> print(csv_bytes.decode('utf-8'))
    ,A,B
    0,1,4
    1,2,5
    2,3,6
    """
    return df.to_csv(index=True).encode('utf-8')


# ======================================
# CONVERTE UM DATAFRAME INSERIDO EM UM ARQUIVO EXCEL
# ======================================

def convert_to_excel(df: pd.DataFrame):
    """
    Convert a pandas DataFrame to an Excel file and encode it as a base64 string.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be converted to an Excel file.

    Returns
    -------
    str
        A base64-encoded string of the Excel file content, suitable for use in data URLs.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    >>> excel_data_url = convert_to_excel(df)
    >>> print(excel_data_url)
    data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,...

    Notes
    -----
    This function uses an in-memory buffer to store the Excel file content and encodes the content 
    as a base64 string. The result is returned as a data URL.
    """
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=True)
    buffer.seek(0)
    excel_data = buffer.getvalue()
    b64_excel = base64.b64encode(excel_data).decode()
    return f"data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_excel}"