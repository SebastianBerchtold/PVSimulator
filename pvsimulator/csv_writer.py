import csv

# Init csv writer
csvfile = open('logs/output.csv', 'w')
fieldnames = ['timestamp', 'meter_value', 'pv_value', 'sum']
writer = csv.DictWriter(csvfile,
                        fieldnames=fieldnames,
                        delimiter="\t")
writer.writeheader()


def format_float(value):
    """Truncates floats to 3 decimals. And convert to kW"""
    if isinstance(value, float):
        value = '{:.3f}'.format(value * 1e-3)
    return value


def write_row(row: dict):
    """Appends a row to `csvfile` according to `fieldnames`"""
    row = {k: format_float(v) for k, v in row.items()}
    writer.writerow(row)
    csvfile.flush()
