def get_all_schema_sql():
    return """SELECT schema_name FROM information_schema.schemata;"""


def get_all_table_sql(schema):
    return f"""
        SELECT tablename
        FROM pg_catalog.pg_tables
        WHERE schemaname = '{schema}';"""


def get_all_int_attribute_sql(schema, table):
    return f"""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = '{schema}'
        AND table_name   = '{table}'"""


# TODO
def get_attribute_range_sql(schema, table, attribute):
    return ""


# TODO
def get_current_estimate_sql(schema, table, attribute_range):
    query_string = f"""
        SELECT COUNT(*) 
        FROM {schema}."{table}"
        WHERE TRUE"""
    for attr in attribute_range:
        query_string += f"""
            AND {attr} >= {attribute_range[attr][0]}
            AND {attr} <= {attribute_range[attr][1]}"""
    return query_string


def get_exception_information(e, sql):
    return f"{e} \nwhen executing \n{sql}"
