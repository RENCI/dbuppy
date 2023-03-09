import argparse
import logging
import sys

from renci.dbuppy.dbaccess.PostgreDBAccess import PostgreDBAccess
from renci.dbuppy.dbauppy import DBUppy
from renci.dbuppy.dbaccess.DBConnection import DBConnection
from renci.dbuppy.sqlscripts.SQLScriptProvider import SQLScriptProvider

VERSION = 20230308


def main():
    set_logging()
    logging.info(f'dbuppy v. {VERSION} started')


    parser = argparse.ArgumentParser(
        prog='dbuppy',
        description='This tool tracks and applies changes to a database')

    parser.add_argument('-path')
    parser.add_argument('-host')
    parser.add_argument('-port')
    parser.add_argument('-dbname')
    parser.add_argument('-username')
    parser.add_argument('-password')
    parser.add_argument('-action')

    args = parser.parse_args()

    db_connection = DBConnection()
    db_connection.HOST = args.host
    db_connection.PORT = int(args.port)
    db_connection.DB_NAME = args.dbname
    db_connection.USER = args.username
    db_connection.PASSWORD = args.password


    dba = PostgreDBAccess(db_connection)
    script_provider = SQLScriptProvider(args.path)

    dbu = DBUppy(dba, script_provider)

    if str.lower(args.action) == 'create':
        dbu.create()
    else:
        dbu.update()

    logging.info('dbuppy finished')


def set_logging():
    logFormatter = logging.Formatter("[%(levelname)-5.5s] %(asctime)s  %(message)s")
    logging.basicConfig(filename='dbuppy.log', level=logging.INFO)
    handler = logging.StreamHandler(sys.stdout) # setting logging to console
    handler.setFormatter(logFormatter)
    logging.getLogger().addHandler(handler)



if __name__ == '__main__':
    main()
