#!/usr/bin/env python3
""" Module that target obfuscating log messages. """
import re
import logging
from os import getenv
import mysql.connector
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Return an obfuscated log message
    params:
        - field (list): list of strings identifying fields to obfuscate
        - redaction (str): what the field will be obfuscated to
        - message (str): log message too obfuscate
        - separator (str) character separating fields
    Return:
        - (str): obfuscated log message
    """
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize RedactingFormatter instance.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Redact sesnsitive data in LogRecord message.
        """
        redacted = filter_datum(self.fields, self.REDACTION,
                                super(RedactingFormatter, self).format(record),
                                self.SEPARATOR)
        return redacted


def get_logger() -> logging.Logger:
    """ Return logging.Logger object. """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PIL_FIELDS)
    handler.setFormatter(formatter)
    logging.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ create connection to database. """
    mydb = mysql.connector.connect(
        host=getenv('PERSONAL_DATA_DB_HOST') or 'localhost',
        user=getenv('PERSONAL_DATA_DB_USERNAME') or 'root',
        password=getenv('PERSONAL_DATA_DB_PASSWORD') or '',
        database=getenv('PERSONAL_DATA_DB_NAME')
    )
    return mydb


def main():
    """ Main entry point """
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users')
    logger = get_logger()
    fields = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
