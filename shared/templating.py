import json

def render_workflow(workflow: dict, params: dict) -> dict:
    """
    Sustituye placeholders {{campo}} por valores reales.
    """
    text = json.dumps(workflow)

    for key, value in params.items():
        placeholder = "{{" + key + "}}"
        text = text.replace(placeholder, str(value))

    return json.loads(text)