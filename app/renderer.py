import os
import re
from fastapi.responses import HTMLResponse

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")

def render_template(template_name: str, context: dict = None) -> HTMLResponse:
    """
    Renderiza um template HTML simples, substituindo {{ chave }} por valores.
    Não depende de Jinja2 - resolve o bug do Python 3.13.
    """
    if context is None:
        context = {}
    
    filepath = os.path.join(TEMPLATES_DIR, template_name)
    
    if not os.path.exists(filepath):
        return HTMLResponse(content=f"<h1>Template não encontrado: {template_name}</h1>", status_code=404)
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Substituir variáveis {{ chave }}
    for key, value in context.items():
        content = content.replace(f"{{{{ {key} }}}}", str(value))
    
    # Processar {% extends "base.html" %}
    if '{% extends "base.html" %}' in content:
        # Extrair nome do template base
        base_match = re.search(r'{% extends "(.*?)" %}', content)
        if base_match:
            base_name = base_match.group(1)
            base_path = os.path.join(TEMPLATES_DIR, base_name)
            if os.path.exists(base_path):
                with open(base_path, "r", encoding="utf-8") as f:
                    base_content = f.read()
                
                # Extrair bloco de conteúdo
                block_match = re.search(r'{% block content %}(.*?){% endblock %}', content, re.DOTALL)
                if block_match:
                    block_content = block_match.group(1)
                    content = base_content.replace('{% block content %}{% endblock %}', block_content)
    
    # Limpar tags Jinja2 restantes
    content = re.sub(r'{% extends ".*?" %}', '', content)
    content = re.sub(r'{% block content %}', '', content)
    content = re.sub(r'{% endblock %}', '', content)
    content = re.sub(r'{% for .*? %}', '', content)
    content = re.sub(r'{% endfor %}', '', content)
    content = re.sub(r'{% if .*? %}', '', content)
    content = re.sub(r'{% endif %}', '', content)
    
    return HTMLResponse(content=content)