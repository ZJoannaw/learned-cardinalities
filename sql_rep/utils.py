import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML
import time
import networkx as nx
import itertools
import hashlib
import psycopg2 as pg
import shelve
import pdb
import os
import errno
import getpass

import glob

import random
def execute_query(sql, user, db_host, port, pwd, db_name, pre_execs):
    '''
    @db_host: going to ignore it so default localhost is used.
    @pre_execs: options like set join_collapse_limit to 1 that are executed
    before the query.
    '''
    con = pg.connect(user=user, host=db_host, port=port,
            password=pwd, database=db_name)
    cursor = con.cursor()

    for setup_sql in pre_execs:
        cursor.execute(setup_sql)

    try:
        cursor.execute(sql)
    except Exception as e:
        print(e)
        try:
            # con.commit()
            cursor.close()
            con.close()
        finally:
            if not "timeout" in str(e):
                print("failed to execute for reason other than timeout")
                print(e)
                return e
            return "timeout"

    exp_output = cursor.fetchall()
    cursor.close()
    con.close()

    return exp_output