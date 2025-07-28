def get_column_type_name(column_type):
    # TODO : add types
    try:
        if hasattr(column_type, "data_type"):
            name = column_type.data_type.python_type.__name__
        elif hasattr(column_type, "python_type"):
            name = column_type.python_type.__name__
        else:
            name = type(column_type).__name__
    except:
        name = type(column_type).__name__

    if name == "str":
        return "text"
    elif name == "int" or name == "INTEGER" or name == "BIT":
        return "number"
    elif name == "datetime":
        return "datetime"

    return name
