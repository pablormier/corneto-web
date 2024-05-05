def render_dot(dot_input, container_id=None, vizjs_version="2.1.2"):
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

    html_code = f"""
    <div id='{container_id}'></div> <!-- Container to display the graph -->
    <script src='https://cdnjs.cloudflare.com/ajax/libs/viz.js/{vizjs_version}/viz.js'></script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/viz.js/{vizjs_version}/full.render.js'></script>
    <script>
    function renderGraph(encodedDot) {{
        var viz = new Viz();
        // Decode the base64 string to get the DOT format
        var dotString = atob(encodedDot);
        
        viz.renderSVGElement(dotString)
            .then(function(element) {{
                document.getElementById('{container_id}').appendChild(element);
            }})
            .catch(error => {{
                console.error('Error rendering graph:', error);
            }});
    }}

    // Execute the rendering function with the base64-encoded DOT string
    renderGraph("{dot_string_base64}");
    </script>
    """

    display(HTML(html_code))
