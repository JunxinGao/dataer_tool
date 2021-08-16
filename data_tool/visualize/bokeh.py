# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_visualize.bokeh.ipynb (unless otherwise specified).

__all__ = ['count2colors', 'bar_figure', 'line_figure_datetime', 'get_count_data_datetime']

# Cell
from ..imports import *
from bokeh.palettes import Spectral, Category20, Viridis256, Cividis256, Turbo256, Set2
from bokeh.io import output_file, show
from bokeh.palettes import Spectral6, Spectral
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LabelSet, RangeTool, HoverTool, Label, Legend
from bokeh.transform import cumsum
from bokeh.plotting import figure
from bokeh.io import output_notebook, show
from bokeh.layouts import column
from bokeh.plotting.figure import get_range, get_scale

# Cell
def count2colors(count: int):
    """
    colors from `bokeh.palettes`
    range:
        1:12    -> Spectral,
        12:21   -> Category20,
        21:257  -> Viridis256,
        257:769 -> Turbo256+Cividis256+Viridis256
    """
    if count <= 0:
        raise ValueError(f"Invalid count={count}, must > 0")
    elif count <= 3:
        return Set2[3][:count]
    elif count <= 8:
        return Set2[count]
    elif count <= 20:
        return Category20[count]
    elif count <= 256:
        index = np.arange(256)
        return tuple(np.array(Viridis256)[np.isin(index, np.arange(0, 256, 256/count, dtype=np.uint8))])
    elif count <= 256 * 3:
        return tuple(np.random.choice(Turbo256 + Cividis256 + Viridis256, count))
    else:
        raise ValueError(f"Invalid count={count}, must <= 768")

# Cell
def bar_figure(data: dict, title="统计", with_label=True, y_log_multiple_thresh=100, eps=1e-1, toolbar_location=None, **kwargs):
    x = list(data.keys())
    y = list(data.values())

    source = ColumnDataSource(data=dict(x=x, y=y, color=count2colors(len(x))))

    p = figure(
        x_range=x, title=title,
        y_axis_type="log" if max(y)/(min(y)+eps) > y_log_multiple_thresh else 'linear',
        toolbar_location=toolbar_location, **kwargs)
    p.vbar(x='x', top='y', width=0.9, bottom=0.1, color='color', legend_field="x", source=source)
    p.legend.orientation = "vertical"
    p.legend.location = "top_right"

    if with_label:
        labels = LabelSet(
            x='x', y='y', text='y', level='glyph',
            x_offset=-10, y_offset=2, source=source, render_mode='canvas', text_font_size="9pt")
        p.add_layout(labels)
    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = math.pi/12
    return p

# Cell
def line_figure_datetime(
        data_list: list, fig_width=800, fig_height=500, x_dtype=np.datetime64,
        select_title:str=None, draw_circle=False, tooltips_metadata:list=None,
        x_name='x', y_name='y', legend_labels:list=None, tools='save,reset,pan', **kwargs
    ):
    if isinstance(data_list, dict): data_list = [data_list]
    if isinstance(tooltips_metadata, dict): tooltips_metadata = [tooltips_metadata]
    if not (isinstance(legend_labels, list) and len(legend_labels)) == len(data_list): legend_labels = None
    if not (isinstance(tooltips_metadata, list) and len(tooltips_metadata)) == len(data_list):
        tooltips_metadata = [{}]*len(data_list)
    p = figure(
        plot_height=int(0.65*fig_height), plot_width=fig_width,
        x_axis_type="datetime", x_axis_location="above",
        background_fill_color="#efefef", x_range=None,
        tools=tools, **kwargs
    )
    print(p.tools)
    colors = count2colors(len(data_list))
    p.yaxis.axis_label = y_name

    select_title = select_title if select_title is not None else f"拖动选择 {x_name} 区间"
    select = figure(
        title=select_title, tools=tools,
        plot_height=int(0.35*fig_height), plot_width=fig_width, y_range=p.y_range,
        x_axis_type="datetime", y_axis_type=None, background_fill_color="#efefef"
    )

    max_x = []
    for i, data in enumerate(data_list):
        if not isinstance(data, dict):
            logger.error(f"invalid data_list[{i}] data format, must be dict")
        x = [str(o) for o in data.keys()]
        if x_dtype: x = list(np.array(x, dtype=x_dtype))
        y = list(data.values())
        metadata = {}
        if isinstance(tooltips_metadata[i], dict):
            for k, v in tooltips_metadata[i].items():
                if isinstance(v, list) and len(v) == len(x):
                    metadata[k] = v
                else:
                    logger.warning(f"tooltips_metadata->{k} values invalid, type={type(v)} length={len(v)}")
        tooltips = [(x_name, "@{"f"{x_name}""}{%F}"),(y_name, "@{"f"{y_name}""}")]
        for k in metadata: tooltips.append((k, "@{"f"{k}""}"))
        column_data = {
            x_name: x,
            y_name: y
        }
        source = ColumnDataSource(data=dict(**column_data, **metadata))
        legend_kwargs = {} if legend_labels is None else {'legend_label': legend_labels[i]}
        p.line(x_name, y_name, source=source, line_color=colors[i], **legend_kwargs)
        if draw_circle: p.circle(x_name, y_name, fill_color='white', size=6, source=source, line_color=colors[i], **legend_kwargs)
        if len(x) > len(max_x): max_x = x
        p.add_tools(HoverTool(tooltips=tooltips, formatters={"@{"f"{x_name}""}": 'datetime'}))

        select.line(x_name, y_name, source=source, line_color=colors[i])
    p.x_range = get_range((max_x[len(max_x)//2-min(len(max_x)//8, 300)], max_x[len(max_x)//2+min(len(max_x)//8, 300)]))
    p.x_scale = get_scale(p.x_range, 'datetime')

    range_tool = RangeTool(x_range=p.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2

    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)
    select.toolbar.active_multi = range_tool
    return column(p, select)

# Cell
def get_count_data_datetime(date_df, count_column, resample_mode='d', extra_meta_column:str=None):
    resample_date_data = date_df.resample(resample_mode).sum()[count_column].to_dict()
    count_data = {}
    extra_output_data = {k: [] for k in date_df[extra_meta_column].value_counts().index} if isinstance(extra_meta_column, str) else None
    for i, k in enumerate(resample_date_data):
        if k not in date_df.index:
            continue
        count_data[k] = resample_date_data[k]
        if isinstance(extra_output_data, dict):
            day_df = date_df.loc[k]
            for extra_k in extra_output_data: extra_output_data[extra_k].append(0)
            try:
                if hasattr(day_df, 'iterrows'):
                    for j, row in day_df.iterrows():
                        extra_output_data[row[extra_meta_column]][-1] += row[count_column]
                else:
                    extra_output_data[day_df[extra_meta_column]][-1] += day_df[count_column]
            except Exception as e:
                logger.error(day_df)
                raise e
                break
    return (count_data, extra_output_data) if extra_output_data is not None else count_data