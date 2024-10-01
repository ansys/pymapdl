"""Helper functions"""

from docutils import nodes
from docutils.parsers.rst import Directive


class HideObject(Directive):
    """HideObject Hide HTML elements.

    Hide or remove HTML elements. They can be selected using the class or the id.

    Directive arguments:

    * 'class' class to select to remove/hide. It has priority over 'id'
    * 'id': Element Id to remove or hide. Ignored if 'class' is given.
    * 'remove': If 'true', it removes the element(s), otherwise the visibility is
      set to 'hidden'.
    * 'adjustmargin': If 'true', the siblings of the selected elements get the
      attribute "'margin': true" which allow them to center themselves horizontally.
      This only makes a difference when 'remove' is 'true'.

    Parameters
    ----------
    Directive : docutils.parsers.rst.Directive
        Directive class from where it is subclassed from.
    """

    has_content = False
    required_arguments = 0
    optional_arguments = 4
    final_argument_whitespace = True
    option_spec = {
        "class": str,
        "id": str,
        "remove": str,
        "adjustmargin": str,
    }

    def run(self):
        remove = self.options.get("remove", "false")
        adjustmargin = self.options.get("adjustmargin", "false")

        remove = "true" if remove.lower() == "true" else "false"
        adjustmargin = "true" if adjustmargin.lower() == "true" else "false"

        if "class" in self.options:
            selecting = "class"
        elif "id" in self.options:
            selecting = "id"
        else:
            raise ValueError(f"Directive 'hideobject' has not enough arguments.")

        selector = self.options.get(selecting).lower()

        if selecting == "class":
            select_cmd = (
                f"""var elements = document.getElementsByClassName("{selector}");"""
            )
        else:
            select_cmd = f"""var element = document.getElementById("{selector}");"""

        js_code = f"""
<script>
// Injected using 'HideObject' directive
document.addEventListener("DOMContentLoaded", function() {{
    {select_cmd}
    if (elements.length > 0) {{

        // Get the parent of the selected element
        var parent = elements[0].parentNode;

        // Remove the selected element from the DOM

        for (var i = 0; i < elements.length; i++) {{
             if ({remove}){{
                // remove element
                elements[i].remove();
            }} else {{
                //Just hide
                elements[0].style.visibility = "hidden";
            }}
        }}

        // Loop through the remaining child elements (siblings)
        if ({adjustmargin}) {{
            var siblings = parent.children;
            for (var i = 0; i < siblings.length; i++) {{
                // Apply margin: auto to each sibling
                siblings[i].style.margin = 'auto';
            }}
        }}
    }}
}});
</script>
        """
        raw_node = nodes.raw("", js_code, format="html")
        return [raw_node]
