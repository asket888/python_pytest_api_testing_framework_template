import psycopg2
from psycopg2 import extras

from utils.logging_util import logger
import logging

logger = logging.getLogger(__name__)


def execute_non_select_sql_query(conn, sql_query):
    try:
        with conn.cursor() as cur:
            cur.execute(sql_query)
            conn.commit()
            logger.debug('Query to execute: ' + str(cur.query.decode('utf-8')))
            logger.debug('DB output: ' + str(cur.statusmessage))
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)


def execute_select_sql_query(conn, sql_query):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(sql_query)
            result = cur.fetchone()
            logger.debug('Query to execute: ' + str(cur.query.decode('utf-8')))
            logger.debug('DB output: ' + str(cur.statusmessage))
            logger.debug('Query result set: ' + str(result))
            return result
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
