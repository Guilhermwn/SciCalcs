# ======================================
# IMPORTS

from nicegui import ui, app
import pandas as pd

# SciCalcs internal files
from .gui_components import page_title, header_layout, TabsCreator
from .state_classes import IncertezasManager, UploadManager
from .defining_functions import visibility_management, convert_to_csv, convert_to_excel

# ======================================
# SUBCATEGOY PAGES LAYOUT

def incertezas():
    page_title('Incertezas')
    calculadoras = ["Incertezas", "Planilha de Incertezas"]
    header_layout()
    
    # TAB INCERTEZAS
    def tab1():
        # CONSTANTES
        incerteza = IncertezasManager()
        
        def labels_incerteza(num):
            return [ui.label('0.0') for i in range(num)]
        label_hand = labels_incerteza(5)

        def execute(e, incerteza_b: str = '0', labels: list[ui.label] = None):
            if incerteza_b == '':
                incerteza_b = "0"
            incerteza_b = float(incerteza_b)
            
            # Inset values in the class
            incerteza.set_values(e.value, incerteza_b)
            
            # Execute the last function, that will set all other values
            incerteza.incerteza_combinada(incerteza_b)
            inc_list = [
                f"{incerteza._media:.6f}",
                f"{incerteza._desvio_padrao:.6f}",
                f"{incerteza._incertezaA:.6f}",
                f"{incerteza.incerteza_b:.6f}",
                f"{incerteza._incerteza_combinada:.6f}"
            ]

            for lab, inc in zip(labels, inc_list):
                lab.set_text(inc)

        # LAYOUT
        
        with ui.column().classes('w-full px-2 md:px-52'):
            ui.markdown("""
            ## Incertezas Associadas
            Calcular as incertezas associadas de uma lista de números.
            
            ---
            """)
            ui.label("Inserir Medidas:").classes('text-xl')
            medidas_input = ui.input(label="Calcular Incertezas:", placeholder="1.42, 1.52, 2.25, 3.42, ...").classes('w-full')
            b_value = ui.input(label="Incerteza Instrumental", value="0.0")
            ui.button('Calcular', on_click=lambda: execute(medidas_input, b_value.value, labels=label_hand)).classes('w-full')
            
            with ui.element('div') as div:
                div.classes('w-full grid grid-cols-1 md:grid-cols-2 gap-4 justify-items-center')
                titles = ["**MÉDIA**", "**DESVIO PADRÃO**", "**INCERTEZA A**", "**INCERTEZA B**", "**INCERTEZA C**"]
                for i in range(5):
                    with ui.card() as card:
                        card.classes('w-full m-2')
                        ui.markdown(titles[i])
                        label_hand[i].move(card)
    
    # TAB INCERTEZAS THROUGH SPREADSHEETS
    def tab2():
        upload_manager = UploadManager()
        with ui.column().classes('w-full px-2 md:px-52'):
            ui.markdown("""
            ## Incertezas Associadas com planilhas
            Calcular as incertezas associadas a partir de dados inseridos em uma planilha.
            
            ---
            """)

            def uihandler(**elements):
                manager = elements['manager']
                old_table = elements['old_table']
                old_label = elements['old_label']
                new_table = elements['new_table']
                new_label = elements['new_label']
                button = elements['button']
                result_div = elements['result_div']

                button.disable()
                old_label.set_text('Conteúdo original')
                new_label.set_text('Novo Conteúdo')

                df = manager.dataframe
                old_data = df.to_dict(orient='records')
                old_columns = [{'headerName': col, 'suppressMovable': True, 'field': col} for col in df.columns]

                old_table.options['rowData'] = old_data
                old_table.options['columnDefs'] = old_columns
                if df.shape[0] <= 8:
                    old_table.options['domLayout'] = 'autoHeight'
                old_table.update()

                manager.incertezas_lists()
                colunas = manager.df_cols
                df.set_index(colunas[0], inplace=True)
                df.index.name = 'Medidas'
                df.loc['Média'] = manager.list_media
                df.loc['Desvio Padrão'] = manager.list_desv_pad
                df.loc['Incerteza A'] = manager.list_inc_a
                df.loc['Incerteza B'] = manager.incerteza_b
                df.loc['Incerteza C'] = manager.list_inc_a
                df_tail = df.tail()
                df_tail.reset_index(inplace=True)
                new_data = df_tail.to_dict(orient='records')
                new_columns = [{'headerName': col, 'suppressMovable': True, 'field': col} for col in df_tail.columns]
                new_table.options['rowData'] = new_data
                new_table.options['columnDefs'] = new_columns
                new_table.options['domLayout'] = 'autoHeight'
                new_table.update()
                visibility_management(True, old_table, result_div)

            def reset_ui_elements():
                og_label.set_text('')
                og_table.options['rowData'] = []
                og_table.options['columnDefs'] = []
                og_table.update()

                new_label.set_text('')
                new_table.options['rowData'] = []
                new_table.options['columnDefs'] = []
                new_table.update()

                visibility_management(False, og_table, result)

            with ui.element('div').classes('w-full grid justify-items-center'):
                file_uploaded = ui.upload(label="Insira o arquivo (.CSV ou . XLSX)",
                                on_upload=lambda e: (upload_manager.dataframer(e), reset_ui_elements(), visibility_management(True, calcular), calcular.enable()),
                                on_rejected=lambda: ui.notify('Formato não reconhecido, tente novamente!'),
                                max_files=1,
                                max_file_size=5_000_000,
                                auto_upload=True
                                ).props('accept=".csv, .xlsx" flat bordered').classes('w-full')


            calcular = ui.button("Calcular", on_click=lambda:uihandler(
                manager = upload_manager, 
                old_table = og_table, 
                old_label = og_label, 
                new_table = new_table,
                new_label = new_label,
                button = calcular,
                result_div = result
                ))
            calcular.classes('w-full')
            visibility_management(False, calcular)

            with ui.element('div') as container:
                container.classes('w-full my-10')
                
                og_label = ui.label().classes(replace='text-xl mb-2')
                og_table = ui.aggrid({
                                'columnDefs': [],
                                'rowData': []
                            }).classes('w-full max-h-52')
                visibility_management(False, og_table)

                with ui.element('div') as result:
                    result.classes('w-full mt-10 rounded-md ring ring-slate-200 ring-offset-8')
                    visibility_management(False, result)

                    new_label = ui.label().classes(replace='text-xl mb-2')
                    new_table = ui.aggrid({
                                'columnDefs': [],
                                'rowData': []
                            }).classes('w-full max-h-52')

                    with ui.row().classes('flex justify-around'):
                        
                        download_as_csv = ui.button('Download .CSV',
                                                    on_click=lambda: ui.download(src=convert_to_csv(upload_manager.dataframe), 
                                                                                 filename="output.csv")).classes('w-[45%]')
                        download_as_excel = ui.button('Download .XLSX',
                                                      on_click=lambda: ui.download(src=convert_to_excel(upload_manager.dataframe),
                                                                                   filename='output.xlsx')).classes('w-[45%]')

                    

    tabber = TabsCreator(calculadoras)
    tabber.create_tabs_header()
    tabber.create_tabs_panel(tab2, tab1)