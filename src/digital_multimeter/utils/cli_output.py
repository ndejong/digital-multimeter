import json
import sys

from digital_multimeter.exceptions import MultimeterException


def cli_output(data, format="json", output="stdout", count=0):
    if format.lower() == "json":
        out = _json_format(data)
    elif format.lower() == "csv":
        out = _csv_format(data, delimiter="_", row=count)
    else:
        raise MultimeterException("Unsupported output format, permitted formats; json, csv")

    if output.lower() == "stdout":
        print(out, file=sys.stdout, flush=True, end="")
    elif output.lower() == "stderr":
        print(out, file=sys.stderr, flush=True, end="")
    else:
        try:
            file = open(output, "a")
        except Exception as e:
            raise MultimeterException(e)
        file.write(out)
        file.close()


def _json_format(data, indent="  "):
    return "{}\n".format(json.dumps(data, indent=indent))


def _csv_format(data, delimiter=".", row=0):
    flat_data = __flatten_data(data=data, delimiter=delimiter)
    output = ""
    if row == 0:
        output = "{}{}".format(output, __csv_row(list(flat_data.keys())))
    output = "{}{}".format(output, __csv_row(list(flat_data.values())))
    return output


def __csv_row(list_items, char="", end="\n"):
    return char + "{char},{char}".format(char=char).join(str(x) for x in list_items) + char + end


def __flatten_data(data, parent_key="", delimiter="."):
    items = []
    if type(data) is list:
        for list_index, value in enumerate(data):
            new_key = "{}{}{}".format(parent_key, delimiter, str(list_index)) if parent_key else str(list_index)
            if type(value) in (str, int, float, bool):
                items.append((new_key, value))
            else:
                items.extend(__flatten_data(value, new_key, delimiter=delimiter).items())
    elif type(data) is dict:
        for key, value in data.items():
            new_key = "{}{}{}".format(parent_key, delimiter, key) if parent_key else key
            if type(value) in (str, int, float, bool) or value is None:
                items.append((new_key, value))
            else:
                items.extend(__flatten_data(value, new_key, delimiter=delimiter).items())
    else:
        raise MultimeterException("Unsupported data type encountered while attempting to __flatten_data()")
    return dict(items)
