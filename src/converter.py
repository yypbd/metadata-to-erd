def get_column_type_name(column_type):
    # if hasattr(column_type, "data_type"):
    #     name = column_type.data_type.python_type.__name__
    # elif hasattr(column_type, "python_type"):

    name = column_type.python_type.__name__
    if name == "str":
        return "text"
    elif name == "int":
        return "number"
    elif name == "datetime":
        return "datetime"

    return name
