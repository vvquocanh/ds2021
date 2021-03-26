import socket
import threading
import mysql.connector
from tabulate import tabulate

s=socket.socket()
host = socket.gethostname()
port = 14
s.bind((host, port))
s.listen(5)
connections = []
print('Waiting for connection...')

def query_table(query):
    i = 0
    for words in query.split():
        if words.casefold() == 'from':
            i += 1
            return query.split()[i]
        i += 1
    return
    

def table_list(cursor):
    result = []
    cursor.execute('show tables')
    rows = cursor.fetchall()
    for row in rows:
        result.append(row[0])
    return result


def handler(conn, addr):
    exit = False
    while True:
        if exit == False:
            database = conn.recv(1024).decode()
            if database == 'exit':
                connections.remove(conn)
                print(addr, ' disconnected.')
                conn.close()
                exit = True
                break
            elif database == '?':
                database = ''
                print('Got {} from '.format(database),addr)
            else:
                print('Got {} from '.format(database),addr)  

                try:
                    sqlconn = mysql.connector.connect(host='localhost', user='root', password='password', database=database)
                    sqlconn1 = mysql.connector.connect(host='Cyen', user='cyen', password='password',database =database, port='3360')
                    conn.send('ok'.encode())
                    cursor = sqlconn.cursor()
                    cursor1 = sqlconn1.cursor()
                    tables = table_list(cursor)
                    print('tables: ',str(tables))
                    tables1 = table_list(cursor1)
                    print('tables1: ',str(tables1))
                    while True:
                        query = conn.recv(1024).decode()
                        if query.casefold() == 'exit' or query.casefold() == '':
                            connections.remove(conn)
                            conn.close()
                            print(addr, ' disconnected.')
                            exit = True
                            break
                        elif query.casefold() == 'back':
                            break
                        else:
                            print('Recieved query: '+ query)
                            query_tables = query_table(query)
                            cursor = sqlconn.cursor()
                            if query_tables in tables1:
                                cursor = sqlconn1.cursor()
                                print('From server 1')
                            else:
                                print('From server 0')
                            
                            try:
                                headers = []
                                cursor.execute(query)
                                if cursor.description != None:
                                    for cd in cursor.description:
                                        headers.append(cd[0])
                                    rows = cursor.fetchall()
                                    results = tabulate(rows, headers=headers, tablefmt='psql')
                                    conn.send(results.encode())
                                else:
                                    conn.send('?'.encode())
                                continue
                            except mysql.connector.Error as err:
                                conn.send(str(err).encode())
                                continue
                except mysql.connector.Error as err:
                    conn.send(str(err).encode())
                    continue
        else:
            return

while True:
    conn, addr = s.accept()
    print(addr, ' connected to server.')
    cThread = threading.Thread(target=handler, args=(conn, addr))   
    cThread.daemon = True
    cThread.start()
    connections.append(conn)
    
    
