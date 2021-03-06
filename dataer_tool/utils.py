# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/03_utils.ipynb (unless otherwise specified).

__all__ = ['get_count_data_datetime', 'fmt_str_in_file']

# Cell
from .imports import *

# Cell
def get_count_data_datetime(input_df, count_column, date_time_column:str=None, agg_method='sum', cumsum:bool=False, resample_mode:str='d', extra_meta_column:str=None):
    date_df = input_df
    extra_meta_keys = list(date_df[extra_meta_column].value_counts().index) if extra_meta_column is not None else None
    if date_time_column is not None:
        if 'int' in str(date_df[date_time_column].dtype).lower(): date_df[date_time_column] = date_df[date_time_column].astype("string")
        date_df[date_time_column] = pd.to_datetime(date_df[date_time_column])
        date_df = date_df.set_index(date_time_column)
    if date_time_column is None: date_time_column = date_df.index.name = "_index_column_title"
    if resample_mode in ['d', 'w', 'm', 'y']:
        date_df_iter = date_df.resample(resample_mode)
    else:
        date_df_iter = date_df.groupby(date_time_column)
    agg_row = date_df_iter[count_column].agg(agg_method)
    if cumsum: agg_row = agg_row.cumsum()
    count_data = agg_row.to_dict()
    if extra_meta_column is not None:
        extra_output_data = {k: [] for k in extra_meta_keys}
        for o in date_df_iter:
            extra_data_item = o[1].groupby(extra_meta_column)[count_column].sum().to_dict()
            for extra_meta_key in extra_meta_keys:
                extra_output_data[extra_meta_key].append(extra_data_item.get(extra_meta_key, 0))
    else:
        extra_output_data = None
    return (count_data, extra_output_data) if extra_output_data is not None else count_data

# Cell
def fmt_str_in_file(file_path, **kwargs):
    with open(file_path, 'r') as f:
        data = f.read()
    return data.format(**kwargs)