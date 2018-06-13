import csv
from datetime import datetime
from collections import namedtuple
import itertools


def csv_parser(fname, *, delimiter=',', quotechar='"', include_header=False):
    with open(fname) as f:
        reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
        if not include_header:
            next(f)
        yield from reader


def parse_date(value, *, fmt='%Y-%m-%dT%H:%M:%SZ'):
    return datetime.strptime(value, fmt)


def extract_field_names(fname):
    reader = csv_parser(fname, include_header=True)
    return next(reader)


def create_named_tuple_class(fname, class_name):
    fields = extract_field_names(fname)
    return namedtuple(class_name, fields)


def iter_file(fname, class_name, parser):
    nt_class = create_named_tuple_class(fname, class_name)
    reader = csv_parser(fname, include_header=False)
    for row in reader:
        parsed_data = (parse_fn(value) for value, parse_fn in zip(row, parser))
        yield nt_class(*parsed_data)


def create_combo_named_tuple_class(fnames, compress_fields):
    # need to create an overarching named tuple that contains
    # all the fields from each file, but suppressing some

    # put all the compress fields into a single iterable
    compress_fields = itertools.chain.from_iterable(compress_fields)

    # put all the field names into a single iterable
    field_names = itertools.chain.from_iterable(extract_field_names(fname) for fname in fnames)

    # compress the field names
    compressed_field_names = itertools.compress(field_names, compress_fields)

    # return the named tuple class
    return namedtuple('Data', compressed_field_names)


def iter_combined_plain_tuple(fnames, class_names, parsers, compress_fields):
    # We'll need to combine all the field compression booleans in one iterable
    compress_fields = tuple(itertools.chain.from_iterable(compress_fields))

    # We need to iterate all the iterators in parallel
    # First we can zip them up - but this will result in an iterator containing a tuple of (named) tuples
    # i.e. zip -->  row = (Personal(...), Employment(...), Vehicle(...), UpdateStatus(...)),
    #               row = (Personal(...), Employment(...), Vehicle(...), UpdateStatus(...)),
    #               row = (Personal(...), Employment(...), Vehicle(...), UpdateStatus(...)),
    #               etc
    # What we really want is a row that is a **single** iterable, not a tuple of iterables
    # so we need to chain them together as well
    zipped_tuples = zip(*(iter_file(fname, class_name, parser)
                          for fname, class_name, parser in zip(fnames, class_names, parsers)))

    merged_iter = (itertools.chain.from_iterable(zipped_tuple) for zipped_tuple in zipped_tuples)

    for row in merged_iter:
        compressed_row = itertools.compress(row, compress_fields)
        yield tuple(compressed_row)


def iter_combined(fnames, class_names, parsers, compress_fields):
    # Create the named tuple to use for returning data rows
    combo_nt = create_combo_named_tuple_class(fnames, compress_fields)

    # We'll need to combine all the field compression booleans in one iterable
    compress_fields = tuple(itertools.chain.from_iterable(compress_fields))

    # We need to iterate all the iterators in parallel
    # First we can zip them up - but this will result in an iterator containing a tuple of (named) tuples
    # i.e. zip -->  row = (Personal(...), Employment(...), Vehicle(...), UpdateStatus(...)),
    #               row = (Personal(...), Employment(...), Vehicle(...), UpdateStatus(...)),
    #               row = (Personal(...), Employment(...), Vehicle(...), UpdateStatus(...)),
    #               etc
    # What we really want is a row that is a **single** iterable, not a tuple of iterables
    # so we need to chain them together as well
    zipped_tuples = zip(*(iter_file(fname, class_name, parser)
                        for fname, class_name, parser in zip(fnames, class_names, parsers)))

    merged_iter = (itertools.chain.from_iterable(zipped_tuple) for zipped_tuple in zipped_tuples)

    for row in merged_iter:
        compressed_row = itertools.compress(row, compress_fields)
        yield combo_nt(*compressed_row)


def filtered_iter_combined(fnames, class_names, parsers, compress_fields, *, key=None):
    iter_combo = iter_combined(fnames, class_names, parsers, compress_fields)
    yield from filter(key, iter_combo)


def group_data(fnames, class_names, parsers, compress_fields, cutoff_date, group_key, gender):
    data_iter = filtered_iter_combined(fnames,
                                       class_names,
                                       parsers,
                                       compress_fields,
                                       key=lambda x: x.last_updated >= cutoff_date)

    groups = sorted((row for row in data_iter if row.gender == gender), key=lambda x: group_key(x))
    groups = itertools.groupby(groups, key=group_key)
    group_counts = ((g[0], len(list(g[1]))) for g in groups)
    return sorted(group_counts, key=lambda x: x[1], reverse=True)
