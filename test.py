import pandas as pd


def summary_csv(self):
    # Initialize an empty list to hold records
    records = []
    details = [
        'name',
        'dispersive',
        'material_path',
        'material_n_k',
        'pattern',
        'description',
        'thickness',
        'thickness_sub'
    ]

    # Loop through each layer and create a record for it
    for layer in self._layers:
        record = {}
        for detail in details:
            # Use getattr to safely get the attribute
            record[detail] = getattr(layer, detail, None)
        records.append(record)

    # Create DataFrame from the list of records
    summary = pd.DataFrame(records, columns=details)

    return summary
