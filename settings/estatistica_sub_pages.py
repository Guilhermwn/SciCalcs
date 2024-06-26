# ======================================
# IMPORTS
# ======================================

from nicegui import ui, events
import numpy as np
# import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import base64

# SciCalcs internal files
from .gui_components import page_title, header_layout, TabsCreator
from .state_classes import IncertezasManager, UploadManager, PyplotManager
from .defining_functions import visibility_management, convert_to_csv, convert_to_excel

# ======================================
# SUBCATEGOY INCERTEZAS PAGE's LAYOUTS
# ======================================

def incertezas():
    page_title('Incertezas')
    calculadoras = ["Incertezas", "Planilha de Incertezas"]
    header_layout()
    


    # ======================================
    # TAB 1 INCERTEZAS
    # ======================================

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
    


    # ======================================
    # TAB 2 INCERTEZAS THROUGH SPREADSHEETS
    # ======================================

    def tab2():
        upload_manager = UploadManager()
        with ui.column().classes('w-full px-2 md:px-52'):
            ui.markdown("""
            ## Incertezas Associadas com planilhas
            Calcular as incertezas associadas a partir de dados inseridos em uma planilha.
            
            ---
            """)

            def uihandler(**elements):
                manager: UploadManager = elements['manager']
                old_table: ui.aggrid = elements['old_table']
                old_label: ui.label = elements['old_label']
                new_table: ui.aggrid = elements['new_table']
                new_label: ui.label = elements['new_label']
                button: ui.button = elements['button']
                result_div: ui.element = elements['result_div']

                # button.disable()
                old_label.set_text(f'Conteúdo original de {manager.file_name}')
                new_label.set_text(f'Novo Conteúdo de {manager.file_name}')

                df = manager.original_dataframe
                old_data = df.to_dict(orient='records')
                old_columns = [{'headerName': col, 'suppressMovable': True, 'field': col} for col in df.columns]

                old_table.options['rowData'] = old_data
                old_table.options['columnDefs'] = old_columns
                old_table.update()

                # manager.incertezas_lists()
                manager.incerteza_dataframe()

                new_df = manager.new_dataframe

                df_tail = new_df.tail()

                new_data = df_tail.to_dict(orient='records')
                new_columns = [{'headerName': col, 'suppressMovable': True, 'field': col} for col in df_tail.columns]
                new_table.options['rowData'] = new_data
                new_table.options['columnDefs'] = new_columns
                new_table.options['domLayout'] = 'autoHeight'
                new_table.update()
                visibility_management(True, old_table, result_div)

            with ui.element('div').classes('w-full grid justify-items-center'):
                file_uploaded = ui.upload(label="Insira o arquivo (.CSV ou . XLSX)",
                                on_upload=lambda e: (upload_manager.dataframer(e), visibility_management(True, calcular, inc_b_input), calcular.enable()),
                                on_rejected=lambda: ui.notify('Formato não reconhecido, tente novamente!'),
                                max_files=1,
                                max_file_size=5_000_000,
                                auto_upload=True
                                ).props('accept=".csv, .xlsx" flat bordered').classes('w-full')

            inc_b_input = ui.input(label='Insira o valor da Incerteza B', placeholder='0.05', on_change=lambda e: upload_manager.set_incerteza_b(e.value))
            calcular = ui.button("Calcular", on_click=lambda:uihandler(
                manager = upload_manager, 
                old_table = og_table, 
                old_label = og_label, 
                new_table = new_table,
                new_label = new_label,
                button = calcular,
                result_div = result,
                inc_b = inc_b_input
                ))
            calcular.classes('w-full')
            visibility_management(False, calcular, inc_b_input)

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
                                                    on_click=lambda: ui.download(src=convert_to_csv(upload_manager.new_dataframe), 
                                                                                 filename="output.csv")).classes('w-[45%]')
                        download_as_excel = ui.button('Download .XLSX',
                                                      on_click=lambda: ui.download(src=convert_to_excel(upload_manager.new_dataframe),
                                                                                   filename='output.xlsx')).classes('w-[45%]')

                    

    tabber = TabsCreator(calculadoras)
    tabber.create_tabs_header()
    tabber.create_tabs_panel(tab1, tab2)

def graph_generation():
    # ui.add_head_html('''
    #     <script>
    #     function emitSize() {
    #         emitEvent('resize', {
    #             width: document.body.offsetWidth,
    #             height: document.body.offsetHeight,
    #         });
    #     }
    #     window.onload = emitSize;
    #     window.onresize = emitSize;
    #     </script>
    # ''')
    
    page_title('Geração de Gráfico')
    header_layout()
    with ui.column().classes('w-full px-2 md:px-52'):
        
        # CONSTANTES
        pyplot_manager = PyplotManager()

        ui.markdown("""
        ## Geração de gráficos
        Gere gráficos de **linha** ou de **dispersão** e customize ao seu gosto
                    
        ---
        """)

        def show_style():
            if pyplot_manager.graph_type == pyplot_manager.graph_options[0]:
                visibility_management(True, line_style)
                visibility_management(False, marker_style)
            elif pyplot_manager.graph_type == pyplot_manager.graph_options[1]:
                visibility_management(True, marker_style)
                visibility_management(False, line_style)
        
        # ======================================
        # GRAPH SETTINGS FORM
        # ======================================

        # SELEÇÃO DO TIPO DE GRÁFICO
        graph_type = ui.select(label='Escolha o tipo de gráfico', 
                               value=pyplot_manager.graph_options[0],
                               options=pyplot_manager.graph_options, 
                               on_change=lambda e: (pyplot_manager.set_graph_type(e.value), show_style())
                               ).classes('w-full')
        
        with ui.expansion('Dados', icon='analytics', value=True).classes('w-full'):
            x_axes = ui.input(label='Eixo X', 
                              on_change=lambda e: pyplot_manager.set_x_axes(e.value)
                              ).classes('w-full')
            
            y_axes = ui.input(label='Eixo Y', 
                              on_change=lambda e: pyplot_manager.set_y_axes(e.value)
                              ).classes('w-full')
        
        with ui.expansion('Customização', icon='tune').classes('w-full'):

            line_style = ui.select(label='Estilo da linha', 
                                   options=list(pyplot_manager.line_style_map.keys()), 
                                   value=list(pyplot_manager.line_style_map.keys())[0], 
                                   on_change=lambda e: pyplot_manager.set_line_style(e.value)
                                   ).classes('w-full')
            
            marker_style = ui.select(label='Estilo do marcador', 
                                     options=list(pyplot_manager.markers_style_map.keys()), 
                                     value=list(pyplot_manager.markers_style_map.keys())[0], 
                                     on_change=lambda e: pyplot_manager.set_marker_style(e.value)
                                     ).classes('w-full')
            
            visibility_management(False, marker_style)

            graph_title = ui.input(label='Título do gráfico', 
                                   on_change=lambda e: pyplot_manager.set_title(e.value)
                                   ).classes('w-full')
            
            x_label = ui.input(label='Título do Eixo X', 
                               on_change=lambda e: pyplot_manager.set_x_label(e.value)
                               ).classes('w-full')
            
            y_label = ui.input(label='Título do Eixo Y', 
                               on_change=lambda e: pyplot_manager.set_y_label(e.value)
                               ).classes('w-full')
            
            data_color = ui.select(label='Cor dos dados', 
                                   options=list(pyplot_manager.color_map.keys()), 
                                   on_change=lambda e: pyplot_manager.set_data_color(e.value)
                                   ).classes('w-full')
        
        
        ui.button('Gerar', on_click=lambda: pyplot_manager.update_plot(plot_image)).classes('w-full')
        
        # ======================================
        # GRAPH SETTINGS FORM
        # ======================================
       
        # ui.on('resize', lambda e: print(f'resize: {e.args}'))
        
        # ======================================
        # GRAPH SHOW RESULT
        # ======================================

        # with ui.element('div').classes('w-full flex flex-col items-center bg-red-300'): 
        # with ui.element('div').classes('flex flex-col items-center my-5 bg-green-500'):
        with ui.element('div').classes('w-full my-5'):
            with ui.pyplot(close=False) as plot:
                # plot.style('max-width: 100%; max-height: 100%;')
                visibility_management(False, plot)
                pyplot_manager.set_pyplot(plot)
                pyplot_manager.download_plot()
            
            
            plot_image = ui.image(pyplot_manager.plot_image)
                    
        with ui.element('div').classes('w-full flex flex-col items-center'):     
            with ui.row():
                
                ui.button('Baixar JPEG', 
                            on_click=lambda: ui.download(
                                filename=f'{pyplot_manager.file_name}.jpg', 
                                src=pyplot_manager.jpg_plot, 
                                media_type='image/jpeg'))
                
                ui.button('Baixar PDF', 
                            on_click=lambda: ui.download(
                                filename=f'{pyplot_manager.file_name}.pdf', 
                                src=pyplot_manager.pdf_plot, 
                                media_type='application/pdf'))

        
        # ======================================
        # GRAPH SHOW RESULT
        # ======================================



                    
