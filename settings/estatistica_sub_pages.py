# ======================================
# IMPORTS
# ======================================

from nicegui import ui

# SciCalcs internal files
from .gui_components import page_title, header_layout, TabsCreator
from .state_classes import IncertezasManager, UploadManager, PyplotManager
from .defining_functions import visibility_management, convert_to_csv, convert_to_excel

# ======================================
# SUBCATEGOY INCERTEZAS PAGE's LAYOUTS
# ======================================

def incertezas():
    # Seting page title
    page_title('Incertezas')
    calculadoras = ["Incertezas", "Planilha de Incertezas"]
    
    # Custom header layout
    header_layout()
    

    # ======================================
    # TAB 1 INCERTEZAS
    # ======================================

    def tab1():

        # ======================================
        # CONSTANTS
        # ======================================
        
        incerteza = IncertezasManager()
        

        # ======================================
        # STATE FUNCTIONS
        # ======================================
        
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

        # ======================================
        # LAYOUT
        # ======================================

        with ui.column().classes('w-full px-2 md:px-52'):
            ui.markdown("""
            ## Incertezas Associadas
            Calcular as incertezas associadas de uma lista de números.
            
            ---
            """)
            ui.label("Inserir Medidas:").classes('text-xl')

            # Input of values
            medidas_input = ui.input(label="Calcular Incertezas:", 
                                     placeholder="1.42, 1.52, 2.25, 3.42, ...").classes('w-full')
            
            # Input of the Incerteza B
            b_value = ui.input(label="Incerteza Instrumental", 
                               value="0.0")
            
            # Calculation Button
            ui.button('Calcular', 
                      on_click=lambda: execute(medidas_input, 
                                               b_value.value, 
                                               labels=label_hand)).classes('w-full')
            
            # Results DIV Container
            with ui.element('div') as div:
                # Div custom Tailwind CSS classes
                div.classes('w-full grid grid-cols-1 md:grid-cols-2 gap-4 justify-items-center')
                
                # Titles for the cards
                titles = ["**MÉDIA**", "**DESVIO PADRÃO**", "**INCERTEZA A**", "**INCERTEZA B**", "**INCERTEZA C**"]
                
                # Results cards creation
                for i in range(5):
                    with ui.card() as card:
                        card.classes('w-full m-2')
                        ui.markdown(titles[i])
                        label_hand[i].move(card)
    


    # ======================================
    # TAB 2 INCERTEZAS WITH SPREADSHEETS
    # ======================================

    def tab2():

        # ======================================
        # CONSTANTS
        # ======================================
        
        upload_manager = UploadManager()

        # ======================================
        # State functions
        # ======================================
        
        def uihandler(**elements):
            manager: UploadManager = elements['manager']
            old_table: ui.aggrid = elements['old_table']
            old_label: ui.label = elements['old_label']
            new_table: ui.aggrid = elements['new_table']
            new_label: ui.label = elements['new_label']
            result_div: ui.element = elements['result_div']

            old_label.set_text(f'Conteúdo original de {manager.file_name}')
            new_label.set_text(f'Novo Conteúdo de {manager.file_name}')

            df = manager.original_dataframe
            old_data = df.to_dict(orient='records')
            old_columns = [{'headerName': col, 'suppressMovable': True, 'field': col} for col in df.columns]

            old_table.options['rowData'] = old_data
            old_table.options['columnDefs'] = old_columns
            old_table.update()

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
        
        
        # ======================================
        # LAYOUT
        # ======================================

        with ui.column().classes('w-full px-2 md:px-52'):
            ui.markdown("""
            ## Incertezas Associadas com planilhas
            Calcular as incertezas associadas a partir de dados inseridos em uma planilha.
            
            ---
            """)
            
            # Element container for the input of the file, input of the Uncertainty B and the confirmation button
            with ui.element('div').classes('w-full grid justify-items-center'):

                # File upload component
                file_uploaded = ui.upload(label="Insira o arquivo (.CSV ou . XLSX)",
                                on_upload=lambda e: (upload_manager.dataframer(e), visibility_management(True, calcular, inc_b_input), calcular.enable()),
                                on_rejected=lambda: ui.notify('Formato não reconhecido, tente novamente!'),
                                max_files=1,
                                max_file_size=5_000_000,
                                auto_upload=True
                                ).props('accept=".csv, .xlsx" flat bordered').classes('w-full')

            # Uncertainty input
            inc_b_input = ui.input(label='Insira o valor da Incerteza B', placeholder='0.05', on_change=lambda e: upload_manager.set_incerteza_b(e.value))
            
            # Confirmation button
            calcular = ui.button("Calcular", on_click=lambda:uihandler(
                manager = upload_manager, 
                old_table = og_table, 
                old_label = og_label, 
                new_table = new_table,
                new_label = new_label,
                result_div = result,
                inc_b = inc_b_input
                )).classes('w-full')
            
            # Set to not visible the elements in the *args
            visibility_management(False, calcular, inc_b_input)

            # Element container for the original table, resulting table and download buttons
            with ui.element('div') as container:

                # Container custom Tailwind CSS classes
                container.classes('w-full my-10')
                
                # ======================================
                # Original table section
                # ======================================

                og_label = ui.label().classes(replace='text-xl mb-2')
                og_table = ui.aggrid({
                                'columnDefs': [],
                                'rowData': []
                            }).classes('w-full max-h-52')
                visibility_management(False, og_table)


                # ======================================
                # New table section
                # ======================================

                # Element container for the new table
                with ui.element('div') as result:

                    # Container custom Tailwind CSS classes
                    result.classes('w-full mt-10 rounded-md ring ring-slate-200 ring-offset-8')

                    # Sets to not visible the elements in the *args
                    visibility_management(False, result)
                
                    # New table elements
                    new_label = ui.label().classes(replace='text-xl mb-2')
                    new_table = ui.aggrid({
                                'columnDefs': [],
                                'rowData': []
                            }).classes('w-full max-h-52')

                    # Element row container for the download buttons
                    with ui.row().classes('flex justify-around'):
                        
                        # Download as CSV the generated dataframe
                        download_as_csv = ui.button('Download .CSV',
                                                    on_click=lambda: ui.download(src=convert_to_csv(upload_manager.new_dataframe), 
                                                                                 filename="output.csv")).classes('w-[45%]')
                        # Download as EXCEL the generated dataframe
                        download_as_excel = ui.button('Download .XLSX',
                                                      on_click=lambda: ui.download(src=convert_to_excel(upload_manager.new_dataframe),
                                                                                   filename='output.xlsx')).classes('w-[45%]')

                    
    # ======================================
    # TABS CREATION AND MANAGEMENT
    # ======================================

    tabber = TabsCreator(calculadoras)
    tabber.create_tabs_header()
    tabber.create_tabs_panel(tab1, tab2)


# ======================================
# GRAPH GENERATION PAGE 
# ======================================
def graph_generation():
    
    page_title('Geração de Gráfico')
    header_layout()
    with ui.column().classes('w-full px-2 md:px-52'):
        
        # ======================================
        # CONSTANTES
        # ======================================
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

        # Plot type selection 
        graph_type = ui.select(label='Escolha o tipo de gráfico', 
                               value=pyplot_manager.graph_options[0],
                               options=pyplot_manager.graph_options, 
                               on_change=lambda e: (pyplot_manager.set_graph_type(e.value), show_style())
                               ).classes('w-full')
        
        # Expansion element containing the axes inputs
        with ui.expansion('Dados', icon='analytics', value=True).classes('w-full'):
            
            # X Axis text input
            x_axes = ui.input(label='Eixo X', 
                              on_change=lambda e: pyplot_manager.set_x_axes(e.value)
                              ).classes('w-full')
            
            # Y Axis text input
            y_axes = ui.input(label='Eixo Y', 
                              on_change=lambda e: pyplot_manager.set_y_axes(e.value)
                              ).classes('w-full')
        
        # Expansion element containing customization inputs
        with ui.expansion('Customização', icon='tune').classes('w-full'):

            # Line style selection Input 
            line_style = ui.select(label='Estilo da linha', 
                                   options=list(pyplot_manager.line_style_map.keys()), 
                                   value=list(pyplot_manager.line_style_map.keys())[0], 
                                   on_change=lambda e: pyplot_manager.set_line_style(e.value)
                                   ).classes('w-full')
            
            # Marker style selection input
            marker_style = ui.select(label='Estilo do marcador', 
                                     options=list(pyplot_manager.markers_style_map.keys()), 
                                     value=list(pyplot_manager.markers_style_map.keys())[0], 
                                     on_change=lambda e: pyplot_manager.set_marker_style(e.value)
                                     ).classes('w-full')
            
            # Sets to not visible the elements in the *args
            visibility_management(False, marker_style)

            # Title of the plot text input
            graph_title = ui.input(label='Título do gráfico', 
                                   on_change=lambda e: pyplot_manager.set_title(e.value)
                                   ).classes('w-full')
            
            # X Axis label text input
            x_label = ui.input(label='Título do Eixo X', 
                               on_change=lambda e: pyplot_manager.set_x_label(e.value)
                               ).classes('w-full')
            
            # Y Axis label text input
            y_label = ui.input(label='Título do Eixo Y', 
                               on_change=lambda e: pyplot_manager.set_y_label(e.value)
                               ).classes('w-full')
            
            # Color of the data selection input
            data_color = ui.select(label='Cor dos dados', 
                                   options=list(pyplot_manager.color_map.keys()), 
                                   on_change=lambda e: pyplot_manager.set_data_color(e.value)
                                   ).classes('w-full')
        
        # Confirmation and generation button
        ui.button('Gerar', on_click=lambda: pyplot_manager.update_plot()).classes('w-full')
       
        
        # ======================================
        # GRAPH SHOW RESULT
        # ======================================

        # Element container for the plot element
        with ui.element('div').classes('w-full my-5'):

            # NiceGUI's Matplotlib Pyplot element 
            with ui.pyplot(close=False) as plot:

                # Instance methods of the PyplotManager Class
                # Seting NiceGUI's plot element as the plot element in the class
                pyplot_manager.set_pyplot(plot)

                # Updating the plot data using the values of the inputs 
                pyplot_manager.download_plot()
            
            # Updating the plot properties so that the plot fits the parent element width
            plot._props['innerHTML'] = plot._props['innerHTML'].replace('<svg', '<svg style="width:100%;height:100%"')
            plot.update()
        
        # Element DIV Container for the plot download buttons 
        with ui.element('div').classes('w-full flex flex-col items-center'):     
            
            # Row element container for the download buttons
            with ui.row():
                
                # Download the plot as JPG image file
                ui.button('Baixar JPEG', 
                            on_click=lambda: ui.download(
                                filename=f'{pyplot_manager.file_name}.jpg', 
                                src=pyplot_manager.jpg_plot, 
                                media_type='image/jpeg'))
                
                # Download the plot as a PDF file
                ui.button('Baixar PDF', 
                            on_click=lambda: ui.download(
                                filename=f'{pyplot_manager.file_name}.pdf', 
                                src=pyplot_manager.pdf_plot, 
                                media_type='application/pdf'))