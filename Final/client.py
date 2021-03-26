
import socket


def recvall(sock):
    BUFF_SIZE = 1024
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    return data

s = socket.socket()
host = socket.gethostname()
port = 14
s.connect((host, port))
print('\nConnected to database coordinator!')
print('USAGE: Enter necessary fields to connect to a database. Enter \'exit\' to quit the program.')

exit = False
while True:
    if exit == False:
        print()
        database = input('>>>> Enter database to query: ')
        
        if database.casefold() == 'exit':
            s.send('exit'.encode())
            s.close()
            exit = True
            break
        elif database.casefold() == '':
            s.send('?'.encode())
        else:
            s.send(database.encode())

        status = s.recv(1024).decode()
        if status == 'ok':
            print('\nConnected to database server!')
            print('Using',database)
            print()
            print('>>>> To change to different database, enter \'back\'.')

        else:
            print(status)
            print('Please re-enter the fields.')
            continue
        while True:
            print()
            query = input('>>>> Enter query: ')
            if query.casefold() == 'exit':
                s.send(query.encode())
                s.close()
                exit = True
                break
            elif query.casefold() == 'back':
                s.send(query.encode())
                break
            else:
                s.send(query.encode())
                results = recvall(s).decode()
                if results.casefold() == '?':
                    pass
                else:
                    print(results)
                continue
    else:
        break