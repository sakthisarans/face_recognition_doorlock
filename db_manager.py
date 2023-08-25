import sys,sqlite3
sys.path.insert(0, '/home/pi/cam/telebot')
import dateandtime as dtm



def updater(name,auth_mod):
    try:
        conn=sqlite3.connect('/home/pi/cam/telebot/history.db')
        date=dtm.find_date()
        time=dtm.find_time()
        query=f"insert into history (date,time,name,auth_mode) values ('{date}','{time}','{name}','{auth_mod}')"
        o=conn.execute(query)
        conn.commit()
        conn.close()
        if(o.rowcount==1):
            print("updated successfully")
        else:
            print("not added")
    except Exception as ex:
        print(ex)
