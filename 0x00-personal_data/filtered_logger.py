#!/usr/bin/env python3
"""contains the filter datum function"""
from typing import List
import logging
import re
import os
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    pattern = r'(' + '|'.join(fields) + r')=(.*?)(' + separator + '|$)'
    return re.sub(pattern, r'\1=' + redaction + r'\3', message)


def get_logger() -> logging.Logger:
    """a logger function"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to a mysql db"""
    return mysql.connector.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST', "localhost"),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', "root"),
        passwd=os.getenv('PERSONAL_DATA_DB_PASSWORD', ""),
        database=os.getenv('PERSONAL_DATA_DB_NAME', ""),
        port=3306
    )


def main() -> None:
    """
    obtain a database connection using get_db and retrieve all
    rows in the users table and display each row under a filtered format
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    logger = get_logger()
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT {} FROM users;".format(fields))
        rows = cur.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
                )
            msg = '{}'.format(';'.join(list(record)))
            log_record = logging.LogRecord("user_data", logging.INFO,
                                           None, None, msg, None, None)
            logger.handle(log_record)
    db.close()


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initializes an instance"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats a record"""
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


if __name__ == "__main__":
    main()
