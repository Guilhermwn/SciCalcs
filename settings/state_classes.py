"""
Module containing classes for managing calculations and variable states in the SciCalcs applications.

Classes:
- ResistorState:
    Manage the state of variables used in calculations for amplifier gain.
    Methods include setting resistor values and units, calculating gain, and unit conversion.
    
- IncertezasManager:
    Handle calculations and variable states related to uncertainties in measurements.
    Methods include setting measurement values and uncertainties, calculating mean, standard deviation,
    Type A uncertainty, and combined uncertainty.

Examples:
    # Example usage of ResistorState class
    state = ResistorState()
    state.set_r1_value(100, ganho_label)
    state.set_r2_value(220, ganho_label)
    state.calculate_ganho(ganho_label)
    ganho_label = ui.label("Ganho: 0.00")
    
    # Example usage of IncertezasManager class
    manager = IncertezasManager()
    manager.set_values('10.1, 10.5, 9.8, 10.3', incerteza_b=0.1)
    media = manager.media()
    desvio_padrao = manager.desvio_padrao()
    incertezaA = manager.incertezaA()
    incerteza_combinada = manager.incerteza_combinada()
    print(f'Mean: {media:.2f}')
    print(f'Standard Deviation: {desvio_padrao:.2f}')
    print(f'Type A Uncertainty: {incertezaA:.2f}')
    print(f'Combined Uncertainty: {incerteza_combinada:.2f}')

Notes:
- These classes assume functionalities are provided by the 'ui' module for UI updates.
- Error handling is implemented where applicable, such as handling insufficient measurements or zero resistance.
"""


# ======================================
# IMPORTS
from nicegui import events ,ui
import re
import pandas as pd
import io

# ======================================
# CLASSES

# SUBCATEGORYS > GANHO AMPLIFICADOR
# ADMINISTRATE THE STATE OF THE VARIABLES USED IN THE CALCULATIONS OF AMPLIFIER'S GAIN
class ResistorState:
    """
    Manage the state of variables used in calculations for amplifier gain in the SciCalcs application.

    This class facilitates setting and updating resistor values and units, and calculates the amplifier gain accordingly.

    Attributes:
    - r1_value : float
        Value of resistor R1.
    - r1_unit : str
        Unit of resistor R1 ('ohms', 'kilohms', 'megaohms').
    - r2_value : float
        Value of resistor R2.
    - r2_unit : str
        Unit of resistor R2 ('ohms', 'kilohms', 'megaohms').
    - ganho : float or str
        Amplifier gain value or error message.

    Methods:
    - __init__():
        Initialize with default values for R1, R2, and gain.
    - set_r1_value(value, ui_label: ui.label):
        Set the value of resistor R1 and update UI label.
    - set_r1_unit(unit, ui_label: ui.label):
        Set the unit of resistor R1 and update UI label.
    - set_r2_value(value, ui_label: ui.label):
        Set the value of resistor R2 and update UI label.
    - set_r2_unit(unit, ui_label: ui.label):
        Set the unit of resistor R2 and update UI label.
    - calculate_ganho(ui_label: ui.label):
        Calculate the amplifier gain based on current R1 and R2 values and update UI label.
    - convert_to_ohms(value, unit):
        Convert resistor value to ohms based on specified unit ('ohms', 'kilohms', 'megaohms').

    Notes:
    - This class assumes UI functionalities are provided by the 'nicegui.ui' module.
    - Error handling is implemented for zero resistance and other potential exceptions during calculations.
    """

    def __init__(self):
        """
        Initialize ResistorState with default values.

        Sets initial values for R1 and R2 resistors to 0 ohms,
        sets their units to 'ohms', and initializes ganho (gain) to 0.
        """
        self.r1_value = 0
        self.r1_unit = 'ohms'
        self.r2_value = 0
        self.r2_unit = 'ohms'
        self.ganho = 0

    def set_r1_value(self, value, ui_label: ui.label):
        """
        Set the value of resistor R1 and update the UI label.

        Parameters
        ----------
        value : float
            The new value for resistor R1.
        ui_label : ui.label
            UI label to display updated information.
        """
        self.r1_value = value
        self.ui_label = ui_label
        self.calculate_ganho(self.ui_label)

    def set_r1_unit(self, unit, ui_label: ui.label):
        """
        Set the unit of resistor R1 and update the UI label.

        Parameters
        ----------
        unit : str
            The new unit for resistor R1 ('ohms', 'kilohms', 'megaohms').
        ui_label : ui.label
            UI label to display updated information.
        """
        self.r1_unit = unit
        self.ui_label = ui_label
        self.calculate_ganho(self.ui_label)

    def set_r2_value(self, value, ui_label: ui.label):
        """
        Set the value of resistor R2 and update the UI label.

        Parameters
        ----------
        value : float
            The new value for resistor R2.
        ui_label : ui.label
            UI label to display updated information.
        """
        self.r2_value = value
        self.ui_label = ui_label
        self.calculate_ganho(self.ui_label)

    def set_r2_unit(self, unit, ui_label: ui.label):
        """
        Set the unit of resistor R2 and update the UI label.

        Parameters
        ----------
        unit : str
            The new unit for resistor R2 ('ohms', 'kilohms', 'megaohms').
        ui_label : ui.label
            UI label to display updated information.
        """
        self.r2_unit = unit
        self.ui_label = ui_label
        self.calculate_ganho(self.ui_label)

    def calculate_ganho(self, ui_label: ui.label):
        """
        Calculate the amplifier gain based on current R1 and R2 values and update the UI label.

        Parameters
        ----------
        ui_label : ui.label
            UI label to display the calculated gain information.
        """
        try:
            r1 = self.convert_to_ohms(self.r1_value, self.r1_unit)
            r2 = self.convert_to_ohms(self.r2_value, self.r2_unit)
            if r1 == 0:
                self.ganho = "Erro: R1 não pode ser zero"
            else:
                self.ganho = - (r2 / r1)
        except Exception as e:
            self.ganho = f"Erro: {str(e)}"
        ui_label.set_text(f"Ganho: {self.ganho:.2f}")

    def convert_to_ohms(self, value, unit):
        """
        Convert resistor value to ohms based on specified unit.

        Parameters
        ----------
        value : float
            Resistor value to be converted.
        unit : str
            Unit of the resistor ('ohms', 'kilohms', 'megaohms').

        Returns
        -------
        float
            Equivalent resistor value in ohms.
        """
        if unit == 'kilohms':
            return value * 1e3
        elif unit == 'megaohms':
            return value * 1e6
        return value


# ======================================

# SUBCATEGORYS > INCERTEZA
# HANDLES THE CALCULATIONS AND VARIABLE STATE OF THE UNCERTAINTYS

class IncertezasManager:
    """
    Manage calculations and variable states related to uncertainties in measurements.

    This class handles operations for calculating statistical properties such as mean, standard deviation,
    Type A uncertainty, and combined uncertainty based on provided measurements and uncertainty sources.

    Attributes:
    - medidas : list[float]
        List of measurement values.
    - size : int
        Number of measurements.
    - sum : float
        Sum of measurement values.
    - incerteza_b : float
        Type B uncertainty value.
    - _media : float
        Calculated mean value of measurements.
    - _desvio_padrao : float
        Calculated standard deviation of measurements.
    - _incertezaA : float
        Calculated Type A uncertainty.
    - _incerteza_combinada : float
        Calculated combined uncertainty.

    Methods:
    - __init__():
        Initialize with default values for measurements and uncertainties.
    - set_values(medidas: str, incerteza_b: float = 0):
        Set measurement values and Type B uncertainty based on provided input string and value.
    - media():
        Calculate and return the mean of measurements.
    - desvio_padrao():
        Calculate and return the standard deviation of measurements.
    - incertezaA():
        Calculate and return the Type A uncertainty.
    - incerteza_combinada(incerteza_b: float = 0):
        Calculate and return the combined uncertainty considering Type A and Type B uncertainties.

    Examples:
        # Initialize and set measurement values
        manager = IncertezasManager()
        manager.set_values('10.1, 10.5, 9.8, 10.3', incerteza_b=0.1)
        
        # Calculate and print results
        media = manager.media()
        desvio_padrao = manager.desvio_padrao()
        incertezaA = manager.incertezaA()
        incerteza_combinada = manager.incerteza_combinada()
        print(f'Mean: {media:.2f}')
        print(f'Standard Deviation: {desvio_padrao:.2f}')
        print(f'Type A Uncertainty: {incertezaA:.2f}')
        print(f'Combined Uncertainty: {incerteza_combinada:.2f}')

    Notes:
    - This class assumes measurements are provided as a comma-separated string of numerical values.
    - Calculation methods handle cases where insufficient measurements are provided by returning default values.
    """

    def __init__(self):
        """
        Initialize IncertezasManager with default values.

        Sets initial values for measurements, size, sum, Type B uncertainty, and statistical properties.
        """
        self.medidas: list[float] = []
        self.size: int = 0
        self.sum: float = 0
        self.incerteza_b: float = 0
        self._media: float = 0
        self._desvio_padrao: float = 0
        self._incertezaA: float = 0
        self._incerteza_combinada: float = 0

    def set_values(self, medidas: str, incerteza_b:float = 0):
        """
        Set measurement values and Type B uncertainty based on provided input.

        Parameters
        ----------
        medidas : str
            Comma-separated string of numerical measurement values.
        incerteza_b : float, optional
            Type B uncertainty value (default is 0).
        """
        num_pattern = re.compile(r'[+-]?(?:\d+\.\d+|\d+\.\d*|\.\d+|\d+)')
        finder = re.findall(num_pattern, medidas)
        
        self.medidas = list(map(float, finder))
        self.size = len(self.medidas)
        self.sum = sum(self.medidas)
        self.incerteza_b = float(incerteza_b)
    
    def media(self):
        """
        Calculate the mean of measurements.

        Returns
        -------
        float
            Mean value of measurements, or 0.0 if fewer than 2 measurements.
        """
        if self.size < 2:
            return 0.0
        else:
            self._media = sum(self.medidas) / self.size
            return self._media
    
    def desvio_padrao(self):
        """
        Calculate the standard deviation of measurements.

        Returns
        -------
        float
            Standard deviation of measurements, or 0.0 if fewer than 2 measurements.
        """
        if self.size < 2:
            return 0.0
        else:
            self._media = self.media()
            acoplamento = []
            for amostra in self.medidas:
                sum_diff = (amostra - self._media) ** 2
                acoplamento.append(sum_diff)
            div = sum(acoplamento) / (self.size - 1)
            self._desvio_padrao = div ** 0.5
            return self._desvio_padrao
    
    def incertezaA(self):
            """
            Calculate the Type A uncertainty.

            Returns
            -------
            float
                Type A uncertainty value, or 0.0 if fewer than 2 measurements.
            """
            self._desvio_padrao = self.desvio_padrao()
            self._incertezaA =  self._desvio_padrao / self.size ** 0.5
            return self._incertezaA
    
    def incerteza_combinada(self, incerteza_b: float = 0):
        """
        Calculate the combined uncertainty considering Type A and Type B uncertainties.

        Parameters
        ----------
        incerteza_b : float, optional
            Type B uncertainty value (default is 0).

        Returns
        -------
        float
            Combined uncertainty value.
        """
        self.incerteza_b = incerteza_b
        self._incertezaA = self.incertezaA()
        self._incerteza_combinada = ( (self._incertezaA ** 2) + (self.incerteza_b ** 2) ) ** 0.5
        return self._incerteza_combinada
    def calculate_incertezas(self, incerteza_b: float = 0):
        """
        Calculates all the uncertainties
        """
        self.incerteza_combinada(incerteza_b=incerteza_b)


# ======================================

# SUBCATEGORYS > INCERTEZA
# HANDLES THE CALCULATIONS AND VARIABLE STATE OF THE UNCERTAINTYS
class UploadManager(IncertezasManager):
    def __init__(self):
        super().__init__()
        self.dataframe: pd.DataFrame = None
        self.df_cols: list[str] = []
        self.list_media: list[float] = []
        self.list_desv_pad: list[float] = []
        self.list_inc_a: list[float] = []
        self.list_inc_c: list[float] = []

    def dataframer(self, event: events.UploadEventArguments):
                """Generates and updates the Aggrid"""
                if ".csv" in event.name: 
                    with io.StringIO(event.content.read().decode()) as f:
                        self.dataframe = pd.read_csv(f)
                elif ".xlsx" in event.name:
                    with io.BytesIO(event.content.read()) as f:
                        self.dataframe = pd.read_excel(f)
    def incertezas_lists(self):
        self.df_cols = self.dataframe.columns

        for col in self.df_cols[1:]:
            medidas = self.dataframe[col].tolist()
            medidas = str(medidas)

            self.set_values(medidas)
            self.calculate_incertezas()

            self.list_media.append(float(f'{self._media:.6f}'))
            self.list_desv_pad.append(float(f'{self._desvio_padrao:.6f}'))
            self.list_inc_a.append(float(f'{self._incertezaA:.6f}'))
            self.list_inc_c.append(float(f'{self._incerteza_combinada:.6f}'))
