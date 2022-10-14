import holoviews as hv
from holoviews import opts
from holoviews.streams import Buffer
from bokeh.models import Range1d, LinearAxis, VBar

def plot_secondary(plot, element):
    """
    Hook to plot data on a secondary (twin) axis on a Holoviews Plot with Bokeh backend.
    More info:
    - http://holoviews.org/user_guide/Customizing_Plots.html#plot-hooks
    - https://docs.bokeh.org/en/latest/docs/user_guide/plotting.html#twin-axes
    
    """
    fig: Figure = plot.state
    glyph_first: GlyphRenderer = fig.renderers[0]  # will be the original plot
    glyph_last: GlyphRenderer = fig.renderers[-1] # will be the new plot
    right_axis_name = "twiny"
    
    # Create both axes if right axis does not exist
    if right_axis_name not in fig.extra_y_ranges.keys():
        
        # Recreate primary axis (left)
        if isinstance(glyph_first.glyph, VBar):
            y_first_name = glyph_first.glyph.top
        else:
            y_first_name = glyph_first.glyph.y
        
        #y_first_min = glyph_first.data_source.data[y_first_name].min()
        y_first_min = 0
        y_first_max = glyph_first.data_source.data[y_first_name].max()
        y_first_offset = (y_first_max - y_first_min) * 0.1
        
        fig.y_range = Range1d(
            start=y_first_min - y_first_offset,
            end=y_first_max + y_first_offset)
        fig.y_range.name = glyph_first.y_range_name
        
        # Create secondary axis (right)
        if isinstance(glyph_last.glyph, VBar):
            y_last_name = glyph_last.glyph.top
        else:
            y_last_name = glyph_last.glyph.y        
        
        y_last_min = 0
        y_last_max = glyph_last.data_source.data[y_last_name].max()
        y_last_offset = (y_last_max - y_last_min) * 0.1
        
        fig.extra_y_ranges = {right_axis_name: Range1d(
            start=y_last_min - y_last_offset,
            end=y_last_max + y_last_offset
        )}
        fig.add_layout(LinearAxis(y_range_name=right_axis_name, axis_label=y_last_name), "right")
    
    # Set right axis for the last glyph added to the figure
    glyph_last.y_range_name = right_axis_name