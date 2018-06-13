import constants
from parse_utils import group_data
from datetime import datetime


def group_key(item):
    return item.vehicle_make


cutoff_date = datetime(2017, 3, 1)

for gender in ('Female', 'Male'):
    group = group_data(constants.fnames,
                       constants.class_names,
                       constants.parsers,
                       constants.compress_fields,
                       cutoff_date,
                       group_key,
                       gender)
    print(f'***** {gender} *****')
    print(group[0:5], end='\n\n')


