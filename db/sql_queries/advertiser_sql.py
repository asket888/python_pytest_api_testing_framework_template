INSERT_ADVERTISER = """"""

SELECT_ADVERTISER_BY_NAME = """
            SELECT *
            FROM advertiser
            WHERE name = '{advertiser_name}';
            """

DELETE_ADVERTISER_BY_NAME = """
            DELETE
            FROM advertiser
            WHERE name LIKE '{advertiser_name}%';
            """
