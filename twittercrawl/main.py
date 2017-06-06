# encoding = utf-8
import crawl_raw
import mysql.connector
import time

cnx = mysql.connector.connect(user='root', password='xxxx',
                              host='127.0.0.1',
                              database='xxxx')
cursor = cnx.cursor()
usr_id_list = [
    '25073877',
    '759251',
    '813286',
    '492532196',
    '1338951085',
    '1390077032',
    '279118291',
    '2319610428',
    '1318094264',
    '2299466747'
]

status_id_list = [
    '869753367299600384',
    '869753371510546432',
    '871145660036378624',
    '870586745468932096',
    '870709271477932032'
]

proxies = crawl_raw.Proxies

add_user = ("INSERT INTO user"
            "(name ,id, count,following, follower, favorite, list, location, join_date) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)") 
add_status = ("INSERT INTO status"
              "(status_id, user_id, text, time, reply, retweet, favorite) "
              "VALUES (%s, %s, %s, %s, %s, %s, %s)")

def craw_user():
    for user_id in usr_id_list:
        try:
            user_inf = []
            user_inf = crawl_raw.get_information(user_id, 1, proxies=proxies)
            data_user = (user_inf[0], user_id, user_inf[1], user_inf[2], user_inf[3], user_inf[4], user_inf[5], user_inf[6], user_inf[7])
            cursor.execute(add_user, data_user)
            cnx.commit()
        except Exception as err:
            print(err)
        time.sleep(1)

def craw_status():
    for status_id in status_id_list:
        try:
            status_inf = []
            status_inf = crawl_raw.get_status_information(status_id)
            data_status = (status_id, status_inf[0], status_inf[1], status_inf[2], status_inf[3], status_inf[4], status_inf[5])
            cursor.execute(add_status, data_status)
            cnx.commit()
        except Exception as err:
            print(err)

def main():
    craw_user()

if __name__ == '__main__':
    main()
