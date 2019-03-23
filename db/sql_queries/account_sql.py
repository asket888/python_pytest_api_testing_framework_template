INSERT_ACCOUNT = """"""

SELECT_ACCOUNT_BY_NAME = """
            SELECT *
            FROM account
            WHERE name = '{account_name}';
            """

DELETE_ACCOUNT_BY_NAME = """
            DELETE
            FROM account
            WHERE name LIKE '{account_name}%';
            """
