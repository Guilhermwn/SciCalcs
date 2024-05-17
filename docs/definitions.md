## Como linkar outras páginas internas

Primeiro é preciso adicionar o caminho relativo da página no arquivo `.streamlit/pages.toml`:

```toml
[[pages]]
path = "paginas/eletrical.py"
name = "Eletrical"
icon = ":smile:"
```

Após definida a página no arquivo de definições, pode-se criar um botão linkando para a página

```python
# importar biblioteca extras do stramlit para trocar de página
from streamlit_extras.switch_page_button import switch_page

if st.button("Go to Eletrical"):
    switch_page("Eletrical")
```
