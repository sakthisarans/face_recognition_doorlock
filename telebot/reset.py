import os,sqlite3
def reset():
    path='/home/pi/cam/data/images'
    os.system(f'rm -r {path} && mkdir {path}')
    path='/home/pi/cam/model/saves/Dnn'
    os.system(f'rm -r {path} && mkdir {path}')
    path='/home/pi/cam/model/saves/lbp'
    os.system(f'rm -r {path} && mkdir {path}')
    print('dir over')
    conn = sqlite3.connect('/home/pi/cam/telebot/login.db')
    conn.execute('delete from login')
    conn.commit()
    print('login delete')
    conn.execute("insert into login (password) VALUES ('admin')")
    conn.commit()
    print('new table')
    conn.close()
    conn = sqlite3.connect('/home/pi/cam/telebot/history.db')
    conn.execute('delete from history')
    conn.commit()
    print('history delete')
    print('over')
    return True

# print(reset())
