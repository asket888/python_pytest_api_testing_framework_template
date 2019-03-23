from db.sql_queries import account_sql
from db.db_executor import execute_non_select_sql_query, execute_select_sql_query


# selects
def select_account_by_name(conn, account_name):
    return execute_select_sql_query(conn, account_sql.SELECT_ACCOUNT_BY_NAME
                                    .format(account_name=account_name))


# inserts
def insert_account(conn, account_name, param_1, param_2, param_3):
    delete_account_by_name(conn, account_name)
    execute_non_select_sql_query(conn, account_sql.INSERT_ACCOUNT
                                 .format(account_name=account_name,
                                         param_1=param_1,
                                         param_2=param_2,
                                         param_3=param_3))
    if not bool(select_account_by_name(conn, account_name=account_name)):
        raise AssertionError(f"Account with '{account_name}' name wasn't created in DB")


# deletes
def delete_account_by_name(conn, account_name):
    execute_non_select_sql_query(conn, account_sql.DELETE_ACCOUNT_BY_NAME
                                 .format(account_name=account_name))
    if bool(select_account_by_name(conn, account_name=account_name)):
        raise AssertionError(f"Account with '{account_name}' name wasn't deleted from DB")
