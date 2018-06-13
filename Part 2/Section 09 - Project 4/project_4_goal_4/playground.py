import constants
import parse_utils
import itertools
from datetime import datetime


# # see a sample of what is in each file
# for fname in constants.fnames:
#     print(fname)
#     with open(fname) as f:
#         print(next(f), end='')
#         print(next(f), end='')
#         print(next(f), end='')
#     print()

# # sample of what's in each file using csv parser
# for fname in constants.fnames:
#     print(fname)
#     reader = parse_utils.csv_parser(fname, include_header=True)
#     print(next(reader))
#     print(next(reader))
#     print()

# # Test the individual file iterators
# for fname, class_name, parser in zip(constants.fnames, constants.class_names, constants.parsers):
#     file_iterator = parse_utils.iter_file(fname, class_name, parser)
#     print(fname)
#     for row in itertools.islice(file_iterator, 2):
#         print(row)
#     print()

# # Test iter_combined_plain_tuple
# iterator = parse_utils.iter_combined_plain_tuple(constants.fnames,
#                                                  constants.class_names,
#                                                  constants.parsers,
#                                                  constants.compress_fields)
# for row in iterator:
#     print(row)

# # Test Combined Named Tuple Class creator
# print(parse_utils.create_combo_named_tuple_class(constants.fnames, constants.compress_fields)._fields)

# # Test iter_combined
# iterator = parse_utils.iter_combined(constants.fnames,
#                                      constants.class_names,
#                                      constants.parsers,
#                                      constants.compress_fields)
# for row in iterator:
#     print(row)

# # Test filtered iterator
# cutoff_date = datetime(2018, 3, 1)
# iterator = parse_utils.filtered_iter_combined(constants.fnames,
#                                               constants.class_names,
#                                               constants.parsers,
#                                               constants.compress_fields,
#                                               key=lambda x: x.last_updated >= cutoff_date)
# for row in iterator:
#     print(row)


# # Develop Algorithm for grouping results
cutoff_date = datetime(2017, 3, 1)


def group_key(item):
    return item.vehicle_make


data_iter = parse_utils.filtered_iter_combined(constants.fnames,
                                               constants.class_names,
                                               constants.parsers,
                                               constants.compress_fields,
                                               key=lambda x: x.last_updated >= cutoff_date)

# we need to use data_iter twice, once for each gender, so let's tee it
iter_1, iter_2 = itertools.tee(data_iter, 2)

# Before we group, the data has to be sorted by the same group key
groups_f = sorted((row for row in iter_1 if row.gender == 'Female'), key=group_key)
groups_m = sorted((row for row in iter_2 if row.gender == 'Male'), key=group_key)

# Now we can group each one by the group key and count the number of data rows for each group
groups_f = itertools.groupby(groups_f, key=group_key)
groups_m = itertools.groupby(groups_m, key=group_key)

# g[0] is the grouping key, g[1] is the sub-iterator
group_f_counts = ((g[0], len(list(g[1]))) for g in groups_f)
group_m_counts = ((g[0], len(list(g[1]))) for g in groups_m)

# Finally print results sorted descending by the counts
sorted_group_f_counts = sorted(group_f_counts, key=lambda x: x[1], reverse=True)
sorted_group_m_counts = sorted(group_m_counts, key=lambda x: x[1], reverse=True)

print(sorted_group_f_counts)
print(sorted_group_m_counts)


