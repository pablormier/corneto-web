def render_dot(dot_input, container_id=None):
    import base64
    import uuid
    from IPython.display import display, HTML

    # Generate a random container ID if none is provided
    if container_id is None:
        container_id = f"container-{uuid.uuid4()}"

    dot_string = ""
    
    # Determine if input is a file path or a Graphviz object
    if isinstance(dot_input, str):
        # Assume it's a file path
        try:
            with open(dot_input, 'r') as file:
                dot_string = file.read()
        except IOError as e:
            print(f"Error reading DOT file: {e}")
            return
    else:
        # Assume it's a Graphviz object
        try:
            dot_string = dot_input.source
        except AttributeError as e:
            print("Provided object is not a valid Graphviz object.")
            return

    # Base64 encode the DOT content to safely embed it in HTML/JavaScript
    dot_string_base64 = base64.b64encode(dot_string.encode()).decode('utf-8')

    # Create the HTML code to display the graph
    html_code = f"""
    <div id='{container_id}'></div>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/viz.js/2.1.2/viz.js'></script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/viz.js/2.1.2/full.render.js'></script>
    <script>
    (function() {{
        var viz = new Viz();
        var encodedDot = "{dot_string_base64}";
        var dotString = atob(encodedDot);
        viz.renderSVGElement(dotString)
            .then(function(element) {{
                document.getElementById('{container_id}').appendChild(element);
            }})
            .catch(function(error) {{
                console.error('Error rendering graph:', error);
            }});
    }})();
    </script>
    """

    display(HTML(html_code))
