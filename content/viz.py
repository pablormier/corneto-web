def render_dot(dot_file_path):
    import base64
    from IPython.display import display, HTML

    # Read the DOT file
    try:
        with open(dot_file_path, 'r') as file:
            dot_string = file.read()
    except IOError as e:
        print(f"Error reading file: {e}")
        return

    # Base64 encode the DOT content to safely embed it in HTML/JavaScript
    dot_string_base64 = base64.b64encode(dot_string.encode()).decode('utf-8')

    # Create the HTML code to display the graph
    html_code = f"""
    <div id='graph-container'></div> <!-- Container to display the graph -->
    <script src='https://cdnjs.cloudflare.com/ajax/libs/viz.js/2.1.2/viz.js'></script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/viz.js/2.1.2/full.render.js'></script>
    <script>
    function renderGraph(encodedDot) {{
        var viz = new Viz();
        // Decode the base64 string to get the DOT format
        var dotString = atob(encodedDot);
        
        viz.renderSVGElement(dotString)
            .then(function(element) {{
                document.getElementById('graph-container').appendChild(element);
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

