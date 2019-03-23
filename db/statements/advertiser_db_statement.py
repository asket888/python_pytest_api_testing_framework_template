from db.db_executor import execute_non_select_sql_query, execute_select_sql_query
from db.sql_queries import advertiser_sql


# selects
def select_advertiser_by_name(conn, advertiser_name):
    return execute_select_sql_query(conn, advertiser_sql.SELECT_ADVERTISER_BY_NAME
                                    .format(advertiser_name=advertiser_name))


# inserts
def insert_advertiser(conn, advertiser_name, param_1, param_2, param_3):
    delete_advertiser_by_name(conn, advertiser_name)
    execute_non_select_sql_query(conn, advertiser_sql.INSERT_ADVERTISER
                                 .format(advertiser_name=advertiser_name,
                                         param_1=param_1,
                                         param_2=param_2,
                                         param_3=param_3))
    if not bool(select_advertiser_by_name(conn, advertiser_name=advertiser_name)):
        raise AssertionError(f"Advertiser with '{advertiser_name}' name wasn't created in DB")


# deletes
def delete_advertiser_by_name(conn, advertiser_name):
    execute_non_select_sql_query(conn, advertiser_sql.DELETE_ADVERTISER_BY_NAME
                                 .format(advertiser_name=advertiser_name))
    if bool(select_advertiser_by_name(conn, advertiser_name=advertiser_name)):
        raise AssertionError(f"Advertiser with '{advertiser_name}' name wasn't deleted from DB")
