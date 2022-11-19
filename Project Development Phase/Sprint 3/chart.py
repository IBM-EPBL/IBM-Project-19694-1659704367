from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE

class Chart:

    fig = figure(
            title="Your Expenses Chart",
            sizing_mode="stretch_width",
        )
    fig.line(
            [1, 2, 3, 4],
            [1.7, 2.2, 4.6, 3.9],
            color='navy',
            line_width=1
        )

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)   