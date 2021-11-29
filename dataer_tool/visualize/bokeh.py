# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_visualize.bokeh.ipynb (unless otherwise specified).

__all__ = ['BOKEH_DEFAULT_TOOLS', 'BOKEH_DEFAULT_TOOLBAR_LOC', 'count2colors', 'bar_figure', 'line_figure_datetime',
           'boxplot_figure', 'histogram_figure', 'scatter_figure', 'bubble_figure', 'stacked_bar_figure',
           'stacked_area_figure', 'pie_figure', 'datatable_from_dataframe', 'bar_mixed_figure', 'text_figure']

# Cell
from ..imports import *
from bokeh.palettes import Spectral, Category20, Viridis256, Cividis256, Turbo256, Set2, brewer, Greys256, Inferno256, Magma256, Plasma256
from bokeh.io import output_file, show
from bokeh.palettes import Spectral6, Spectral
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange, LabelSet, RangeTool, HoverTool, Label, Legend, Paragraph
from bokeh.transform import cumsum, factor_cmap
from bokeh.plotting import figure
from bokeh.io import output_notebook, show
from bokeh.layouts import column
from bokeh.plotting.figure import get_range, get_scale
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn


BOKEH_DEFAULT_TOOLS = 'save,reset,pan'
BOKEH_DEFAULT_TOOLBAR_LOC = 'above' #'above', 'below', 'left', 'right', None


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
        cmp_256 = random.choice([Viridis256, Cividis256, Turbo256, Inferno256, Magma256, Plasma256])
        return tuple(np.array(cmp_256)[np.isin(index, np.arange(0, 256, 256/count, dtype=np.uint8))])
    elif count <= 256 * 3:
        return tuple(np.random.choice(Turbo256 + Cividis256 + Viridis256, count))
    else:
        raise ValueError(f"Invalid count={count}, must <= 768")

# Cell
def bar_figure(
    data: dict, title="统计", with_label=True, y_log_multiple_thresh=1000, eps=1e-1, hide_legend=False,
    toolbar_location=BOKEH_DEFAULT_TOOLBAR_LOC, legend_orientation = "vertical", legend_location = "top_right", vertical_bar=True,
    xaxis_major_label_orientation=math.pi/8, label_angle=0, bar_width=0.8, draw_line_circle=False,
    tools=BOKEH_DEFAULT_TOOLS, x_axis_label=None, y_axis_label=None, **kwargs):
    x = [str(o) for o in data.keys()]
    y = list(data.values())

    source = ColumnDataSource(data=dict(x=x, y=y, color=count2colors(len(x))))
    if vertical_bar:
        p = figure(
            x_range=x, title=title,
            y_axis_type="log" if max(y)/(min(y)+eps) > y_log_multiple_thresh else 'linear',
            toolbar_location=toolbar_location, tools=tools, **kwargs)
        p.vbar(x='x', top='y', width=bar_width, bottom=0.1, color='color', legend_field="x", source=source)
    else:
        p = figure(
            y_range=x, title=title,
            toolbar_location=toolbar_location, tools=tools, **kwargs)
        p.hbar(y='x', right='y', height=bar_width, color='color', legend_field="x", source=source)
    p.legend.orientation = legend_orientation
    p.legend.location = legend_location
    if hide_legend: p.legend.visible=False

    if with_label:
        if vertical_bar:
            labels = LabelSet(
                x='x', y='y', text='y', angle=label_angle,
                x_offset=-8, y_offset=2, source=source, render_mode='css', text_font_size="9pt")
            if draw_line_circle:
                p.line(x='x', y='y', source=source, line_color='#4292c6')
                p.circle(x='x', y='y', fill_color='white', size=6, source=source, line_color='black')
        else:
            labels = LabelSet(
                x='y', y='x', text='y', angle=label_angle,
                x_offset=2, y_offset=-8, source=source, render_mode='css', text_font_size="9pt")
        p.add_layout(labels)
    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = xaxis_major_label_orientation
    p.yaxis.axis_label = y_axis_label
    p.xaxis.axis_label = x_axis_label
    return p

# Cell
def line_figure_datetime(
        data_list: list, plot_width=800, plot_height=500, x_dtype=np.datetime64,
        select_title:str=None, draw_circle=False, tooltips_metadata:list=None,
        x_name='x', y_name='y', legend_labels:list=None, tools=BOKEH_DEFAULT_TOOLS,
        use_select_figure=True, toolbar_location=BOKEH_DEFAULT_TOOLBAR_LOC, legend_alpha=0.8,
        legend_orientation = "vertical", legend_location = "top_right",
        y_axis_label=None, x_axis_label=None, **kwargs
    ):
    if isinstance(data_list, dict): data_list = [data_list]
    if isinstance(tooltips_metadata, dict): tooltips_metadata = [tooltips_metadata]
    if not (isinstance(legend_labels, list) and len(legend_labels)) == len(data_list): legend_labels = None
    if not (isinstance(tooltips_metadata, list) and len(tooltips_metadata)) == len(data_list):
        tooltips_metadata = [{}]*len(data_list)
    p = figure(
        plot_height=int(0.65*plot_height), plot_width=plot_width,
        x_axis_type="datetime", x_axis_location="above" if use_select_figure else 'below',
        background_fill_color="#efefef", x_range=None,
        toolbar_location=toolbar_location,
        tools=tools, **kwargs
    )
    colors = count2colors(len(data_list))
    p.yaxis.axis_label = y_name if y_axis_label is None else y_axis_label
    p.xaxis.axis_label = x_name if x_axis_label is None else x_axis_label
    if use_select_figure:
        select_title = select_title if select_title is not None else f"拖动选择 {x_name} 区间"
        select = figure(
            title=select_title, tools=tools, toolbar_location=toolbar_location,
            plot_height=int(0.35*plot_height), plot_width=plot_width, y_range=p.y_range,
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

        if use_select_figure: select.line(x_name, y_name, source=source, line_color=colors[i])
    p.x_scale = get_scale(p.x_range, 'datetime')
    p.legend.background_fill_alpha = legend_alpha
    p.legend.orientation = legend_orientation
    p.legend.location = legend_location
    if use_select_figure:
        p.x_range = get_range((max_x[len(max_x)//2-min(len(max_x)//8, 300)], max_x[len(max_x)//2+min(len(max_x)//8, 300)]))
        range_tool = RangeTool(x_range=p.x_range)
        range_tool.overlay.fill_color = "navy"
        range_tool.overlay.fill_alpha = 0.2

        select.ygrid.grid_line_color = None
        select.add_tools(range_tool)
        select.toolbar.active_multi = range_tool
        return column(p, select)
    else:
        return p

# Cell
def boxplot_figure(
    data_df, group_column='group', value_column='value', toolbar_location=BOKEH_DEFAULT_TOOLBAR_LOC,
    tools=BOKEH_DEFAULT_TOOLS, y_axis_label=None, x_axis_label=None, **kwargs):
    # find the quartiles and IQR for each category
    groups = df.groupby(group_column)
    q1 = groups.quantile(q=0.25)
    q2 = groups.quantile(q=0.5)
    q3 = groups.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5*iqr
    lower = q1 - 1.5*iqr
        # find the outliers for each category
    def outliers(group):
        cat = group.name
        return group[(group.score > upper.loc[cat][value_column]) | (group.score < lower.loc[cat][value_column])][value_column]
    out = groups.apply(outliers).dropna()

    # prepare outlier data for plotting, we need coordinates for every outlier.
    if not out.empty:
        outx = list(out.index.get_level_values(0))
        outy = list(out.values)

    p = figure(tools=tools, background_fill_color="#efefef", x_range=cats, toolbar_location=toolbar_location, **kwargs)

    # if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
    qmin = groups.quantile(q=0.00)
    qmax = groups.quantile(q=1.00)
    upper.score = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,value_column]),upper.score)]
    lower.score = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,value_column]),lower.score)]

    # stems
    p.segment(cats, upper.score, cats, q3.score, line_color="black")
    p.segment(cats, lower.score, cats, q1.score, line_color="black")

    # boxes
    p.vbar(cats, 0.7, q2.score, q3.score, fill_color="#E08E79", line_color="black")
    p.vbar(cats, 0.7, q1.score, q2.score, fill_color="#3B8686", line_color="black")

    # whiskers (almost-0 height rects simpler than segments)
    p.rect(cats, lower.score, 0.2, 0.01, line_color="black")
    p.rect(cats, upper.score, 0.2, 0.01, line_color="black")

    # outliers
    if not out.empty:
        p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = "white"
    p.grid.grid_line_width = 2
    p.xaxis.major_label_text_font_size="16px"
    p.yaxis.axis_label = y_axis_label
    p.xaxis.axis_label = x_axis_label
    return p

# Cell
def histogram_figure(
       hist, edges, title='histogram', x_axis_label='x', y_axis_label='y',
       fill_color='navy', toolbar_location=BOKEH_DEFAULT_TOOLBAR_LOC,
       tools=BOKEH_DEFAULT_TOOLS, **kwargs):
    p = figure(title=title, tools=tools, background_fill_color="#fafafa", toolbar_location=toolbar_location, **kwargs)
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color=fill_color, line_color="white", alpha=0.5)
    p.y_range.start = 0
    p.xaxis.axis_label = x_axis_label
    p.yaxis.axis_label = y_axis_label
    p.grid.grid_line_color="white"
    return p

# Cell
def scatter_figure(
        x, y, x_axis_label='x', y_axis_label='y', title='scatter',
        toolbar_location=BOKEH_DEFAULT_TOOLBAR_LOC, tools=BOKEH_DEFAULT_TOOLS, **kwargs
    ):
    assert len(x) == len(y)
    p = figure(title=title, tools=tools, toolbar_location=toolbar_location, **kwargs)
    p.xaxis.axis_label = x_axis_label
    p.yaxis.axis_label = y_axis_label

    p.circle(x, y, fill_alpha=0.2, size=10)
    return p

# Cell
def bubble_figure(
    x, y, z=None, title='bubble', tools=BOKEH_DEFAULT_TOOLS, toolbar_location=BOKEH_DEFAULT_TOOLBAR_LOC,
    y_axis_label=None, x_axis_label=None, **kwargs):
    p = figure(tools=tools, title=title, toolbar_location=toolbar_location, **kwargs)
    if z is not None:
        z = np.array(z)
        z -= np.mean(z)
        z /= np.std(z)
        z /= ((max(z) - min(z))/2)
        z -= min(z)
        z /= 5
        z += 0.1
        p.scatter(x, y, fill_alpha=0.6, radius=z)
    else:
        p.scatter(x, y, fill_alpha=0.6)
    p.yaxis.axis_label = y_axis_label
    p.xaxis.axis_label = x_axis_label

    return p

# Cell
def stacked_bar_figure(
    data:dict, x_key, y_keys:list, title='stacked bar',
    toolbar_location=BOKEH_DEFAULT_TOOLBAR_LOC, tools=BOKEH_DEFAULT_TOOLS,
    y_axis_label=None, x_axis_label=None, **kwargs
):
    p = figure(title=title, toolbar_location=toolbar_location, tools=tools, x_range=data[x_key], **kwargs)

    p.vbar_stack(y_keys, x=x_key, width=0.9, color=colors, source=data, legend_label=y_keys)

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    p.yaxis.axis_label = y_axis_label
    p.xaxis.axis_label = x_axis_label
    return p

# Cell
def stacked_area_figure(
    df, stackers:list, title='stacked_area', tools=BOKEH_DEFAULT_TOOLS,
    toolbar_location=BOKEH_DEFAULT_TOOLBAR_LOC,
    y_axis_label=None, x_axis_label=None, **kwargs):
    p = figure(x_range=(0, len(df)-1), title=title, tools=tools, toolbar_location=toolbar_location, **kwargs)
    p.grid.minor_grid_line_color = '#eeeeee'
    if df.index.name is None: df.index.name = '_index_col'

    p.varea_stack(stackers=stackers, x=df.index.name, color=count2colors(len(stackers)), legend_label=stackers, source=df)

    # reverse the legend entries to match the stacked order
    p.legend.items.reverse()
    p.yaxis.axis_label = y_axis_label
    p.xaxis.axis_label = x_axis_label
    return p

# Cell
def pie_figure(data, title='pie', tools=BOKEH_DEFAULT_TOOLS, toolbar_location=BOKEH_DEFAULT_TOOLBAR_LOC,
                min_pct=0.01, others_name='OTHERS', legend_orientation="horizontal", legend_location="top_center",
                radius=0.8, pct_text_pad=100, **kwargs):
    x = list(data.keys())
    y = list(data.values())
    df = pd.Series(data).reset_index(name='y').rename(columns={'index':'x'})
    df["percentage"] = df["y"] / df["y"].sum()
    if isinstance(min_pct, float) and 0<min_pct<1 and len(df[df["percentage"] < min_pct]) > 0:
        others_y = df[df["percentage"] < min_pct]['y'].sum()
        others_pct = df[df["percentage"] < min_pct]['percentage'].sum()
        df = df[df["percentage"] >= min_pct]
        df = df.append({'x': others_name, 'y': others_y, 'percentage': others_pct}, ignore_index=True)
    df['percentage'] = df['percentage'].astype(float).map(lambda n: '{:.1%}'.format(n))
    df["percentage"] = df['percentage'].astype(str)
    df["percentage"] = df["percentage"].str.pad(pct_text_pad, side="left")
    df['angle'] = df['y']/df['y'].sum() * 2 * math.pi
    df['color'] = count2colors(len(df))
    tooltips = [("category", "@x"), ("count", "@y"), ("percentage", "@percentage")

]
    p = figure(title=title, tools=tools, tooltips=tooltips, toolbar_location=toolbar_location, **kwargs)

    p.wedge(x=0, y=1, radius=radius,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='x', source=df)
    # labels = LabelSet(x="cos", y="sin", y_offset=0, text='percentage', text_align="center", angle=0, source=ColumnDataSource(df), render_mode='canvas')
    labels = LabelSet(x=0, y=1, y_offset=0, text='percentage', text_align="center", angle=cumsum('angle', include_zero=True), source=ColumnDataSource(df), render_mode='css')
    p.add_layout(labels)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None
    p.legend.orientation = legend_orientation
    p.legend.location = legend_location
    return p

# Cell
def datatable_from_dataframe(df, **kwargs):
    df = df.fillna('nan')
    columns = [TableColumn(field=o, title=o) for o in df.columns]
    data_table = DataTable(columns=columns, source=ColumnDataSource(df), **kwargs)
    return data_table


# Cell
def bar_mixed_figure(df, group_keys:list, y_column_name, label_angle=0,
                    agg_method='sum', tools=BOKEH_DEFAULT_TOOLS, title='mixed bar',
                    toolbar_location=BOKEH_DEFAULT_TOOLBAR_LOC, draw_mean_line=False, line_alpha=0.8,
                    legend_orientation = "vertical", legend_location = "top_center",
                    label_offset_kwargs={'x_offset':-8, 'y_offset':2}, y_axis_label=None, x_axis_label=None,
                    line_legend_label="平均值", line_color="#4292c6", hide_legend=True, **kwargs):
    bar_group_keys = list(df[group_keys[-1]].unique())
    palette = count2colors(len(bar_group_keys))
    grouped_df = df.groupby(group_keys).agg(agg_method)
    bar_legend_values = list(grouped_df.reset_index()[group_keys[-1]].values)
    x = list(grouped_df.index)
    counts = list(grouped_df[y_column_name].values)

    source = ColumnDataSource(data=dict(x=x, counts=counts, bar_legend=bar_legend_values))

    p = figure(x_range=FactorRange(*x), title=title, toolbar_location=toolbar_location, tools=tools, **kwargs)

    p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white", legend_field='bar_legend',
        fill_color=factor_cmap('x', palette=palette, factors=bar_group_keys, start=len(group_keys)-1, end=len(group_keys)))
    labels = LabelSet(
                x='x', y='counts', text='counts', angle=label_angle,
                source=source, render_mode='css', text_font_size="9pt", **label_offset_kwargs)
    p.add_layout(labels)
    if draw_mean_line:
        line_data = df.groupby(group_keys[0])[y_column_name].mean().to_dict()
        p.line(
            x=list(line_data.keys()), y=list(line_data.values()),
            color=line_color, line_width=2, legend_label=line_legend_label, alpha=line_alpha
        )
        p.circle(
            x=list(line_data.keys()), y=list(line_data.values()),
            fill_color='white', size=6, line_color='black', legend_label=line_legend_label, alpha=line_alpha
        )
        p.add_tools(HoverTool(tooltips=[('mean', '@y')]))
    p.legend.orientation = legend_orientation
    p.legend.location = legend_location
    if hide_legend: p.legend.visible = False

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    p.yaxis.axis_label = y_axis_label
    p.xaxis.axis_label = x_axis_label
    return p

# Cell
def text_figure(text, plot_width=600, plot_height=200, **kwargs):
    p = Paragraph(text=text, width=plot_width, height=plot_height, **kwargs)
    return p
