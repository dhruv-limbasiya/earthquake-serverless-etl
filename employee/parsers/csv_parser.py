import csv
import io


def parse_csv(file_content):
    """
    Parse CSV into a list of dictionaries.
    """

    csv_reader = csv.DictReader(
        io.StringIO(file_content)
    )

    return list(csv_reader)