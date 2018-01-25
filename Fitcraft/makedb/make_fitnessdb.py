#!/usr/bin/env python3

import sys
import os
import logging
import json
import sqlite3
import datetime
import calendar


FORMAT = '%(created)s:%(levelno)s:%(message)s'
logging.basicConfig(stream = sys.stdout,
                    format = FORMAT,
                    level = logging.INFO)

def main(argv):
    if len(argv) < 2:
        logging.debug('We need argument for path')
        return
    dir_queue = list()

    for arg in argv:
        if os.path.isdir(arg) == True:
            dir_queue.append(arg)

    connector = connect_database('fitcraft.db')
    create_tables(connector)

    for file_path in get_file_list(dir_queue):
        try:
            insert_data(connector, file_path)
        except Exception as e:
            logging.critical((str(e) + file_path))
            with open(file_path, 'r') as f:
                logging.critical(f.read())

    close_database(connector)



def insert_data(connector, file_path):
    cursor = connector.cursor()
    db_data = list()
    data = get_data(file_path)
    user = file_path.split('/')[-1]
    user = user.split('.')[0]
    if 'activities-steps' in data:
        db_name = 'steps'
        date = data['activities-steps'][0]['dateTime']
        for values in data['activities-steps-intraday']['dataset']:
            timestr = (date + ' ' + values['time'] + ' +0900')
            timedt = datetime.datetime.strptime(timestr, 
                                                '%Y-%m-%d %H:%M:%S %z')
            timeepoch = calendar.timegm(timedt.utctimetuple())
            logging.debug(
                    (db_name, user, timeepoch, values['value']))
            db_data.append((timeepoch, user, values['value']))
    if 'sleep' in data:
        db_name = 'sleeps'
        date = data['sleep'][0]['dateOfSleep']
        for values in data['sleep'][0]['minuteData']:
            timestr = (date + ' ' + values['dateTime'] + ' +0900')
            timedt = datetime.datetime.strptime(timestr, 
                                                '%Y-%m-%d %H:%M:%S %z')
            timeepoch = calendar.timegm(timedt.utctimetuple())
            logging.debug(
                    (db_name, user, timeepoch, values['value']))
            db_data.append((timeepoch, user, values['value']))
    if 'activities-heart' in data:
        db_name = 'hearts'
        date = data['activities-heart'][0]['dateTime']
        for values in data['activities-heart-intraday']['dataset']:
            timestr = (date + ' ' + values['time'] + ' +0900')
            timedt = datetime.datetime.strptime(timestr, 
                                                '%Y-%m-%d %H:%M:%S %z')
            timeepoch = calendar.timegm(timedt.utctimetuple())
            logging.debug(
                    (db_name, user, timeepoch, values['value']))
            db_data.append((timeepoch, user, values['value']))
    cursor.executemany(('INSERT INTO '
                      + db_name
                      + ' VALUES (?, ?, ?)'), db_data)
        
    connector.commit()



def create_tables(connector):
    cursor = connector.cursor()
    # it contain ROWID INTEGER PRIMARY KEY defaults
    cursor.execute('''CREATE TABLE IF NOT EXISTS steps (
                        datetime INTEGER NOT NULL,
                        user TEXT NOT NULL,
                        value INTEGER NOT NULL)
                   ''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS hearts (
                        datetime INTEGER NOT NULL,
                        user TEXT NOT NULL,
                        value INTEGER NOT NULL)
                   ''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS sleeps (
                        datetime INTEGER NOT NULL,
                        user TEXT NOT NULL,
                        value INTEGER NOT NULL)
                   ''')
    connector.commit()


def connect_database(name = 'fitcraft.db'):
    connector = sqlite3.connect(name)
    return connector



def close_database(connector):
    connector.close()



def get_file_list(dir_queue):
    file_queue = list()

    while len(dir_queue) > 0:
        path = dir_queue.pop()
        with os.scandir(path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    yield entry.path
                else:
                    dir_queue.append(entry.path)

    return file_queue



def get_data(file_path):
    with open(file_path, 'r') as rfile:
        data = json.load(rfile)
        return data



# is it good thing, right?
if __name__ == '__main__':
    sys.exit(main(sys.argv))
