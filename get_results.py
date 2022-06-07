import requests
from bs4 import BeautifulSoup
import time
import MySQLdb

class insertDetail():

    def getURL(serif):

        connection = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='',
            db='boat')

        cursor = connection.cursor()
        res = []

        cursor.execute("SELECT url FROM boat_results_url")
        for row in cursor:
            res.append(row[0])

        # 保存を実行
        connection.commit()
        # 接続を閉じる
        connection.close()

        return res
    
    def sraping(serif,url):
        # for i in range(url):
        response = requests.get(url=url)
        response.encoding = response.apparent_encoding
        print(response.text)


cl = insertDetail()
res = cl.getURL()
cl.sraping(res[0])
