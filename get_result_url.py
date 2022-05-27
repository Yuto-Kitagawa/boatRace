#コード内では使用していないが、書かないとエラーがでる
#this module wasn't used in this codes,but if you don't write this,you catch some error
from re import M
import chromedriver_binary

#selenuim関連のモジュールインポート文
#selenuim-related module import statement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from time import sleep


import MySQLdb


#スクレイピングする際、seleniumはオプションをつけることができます
#エラーが出ないように・プラグインなどを使用してスクレイピングを行ってください。
#you can attach any options with selenium.if you cought some error,you should attach some options.
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches',['enable-logging'])
# options.add_argument('--headless')
options.use_chromium = True
driver = webdriver.Chrome(options=options)


"""
https://www1.mbrace.or.jp/od2/K/pmenu.html
ここのページからhtmlを作成している。
ソースを見れば、ヘッドの中に関数があり、ここの関数がhtmlを返している。
この通りにURLを作成すると、結果のhtmlが表示される
圧縮ファイルがダウンロードできる。
you can find js in the page.
You can look about results page

注意
url = "https://www1.mbrace.or.jp/od2/K/pindex.html"
このurlではできないので注意
the url doesn't use
"""


"""
ソースの中にselectタグなどがあるか
check sources of the page. if you can find some select tag, it's OK
frameタグしかない場合はURLが違います
if you find only frame tags,it's wrong
"""

class GetResultURL():
        
    def getMonthURL(self):
        url = "https://www1.mbrace.or.jp/od2/K/pmenu.html"
        driver.get(url)

        # 配列初期化
        j = []
        
        # selectタグを取得・選択
        dropdown = driver.find_element(by=By.NAME,value='JYOU')
        select = Select(dropdown)

        # すべてのoptionタグを取得
        select_options = select.options

        for option in select_options:
            # 配列に追加
            j.append(option.get_attribute('value'))

        # 配列初期化
        m = []

        # selectタグを取得・選択
        dropdown = driver.find_element(by=By.NAME,value='MONTH')
        select = Select(dropdown)
        
        # すべてのoptionタグを取得
        select_options = select.options

        for option in select_options:
            # 配列に追加
            m.append(option.get_attribute('value'))
        
        # print(j)
        # print(m)

        month_url = []
        url_base = "http://www1.mbrace.or.jp/od2/K/"

        day_page_param="day.html"

        # 日付を選択するページのURLを作成
        # 選択されていないときのvalueがXなのでそれを排除
        for i in range(len(j)):
            if(j[i] != "X"):
                for k in range(len(m)):
                    if(m[k] != "X"):
                        url_param = str(m[k]) + "/" + str(j[i]) + "/"
                        month_url.append(url_base + url_param + day_page_param)
                        
        #0~100番目を返す
        # 100番以降を返す時は[100:200]など
        return month_url[100:400]

    
    def getDayURL(self,month_url):

        print(month_url)
        
        # 結果のページのURLを作成
        day_url = []

        # 月にURLにアクセス
        for l in range(len(month_url)):
            driver.get(month_url[l])
            # すべての日付を取得
            days = driver.find_elements(By.NAME,'MDAY')

            for n in days:
                print(n.get_attribute('value'))
                url = str(month_url[l]).replace('day',n.get_attribute('value'))
                day_url.append(url)

        # すべてのレース結果のページが作成される        
        return day_url

    
    def insertDB(self,day_url):

        connection = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='',
            db='boat')
        cursor = connection.cursor()

        for s in range(len(day_url)):
            cursor.execute("INSERT INTO boat_results_url (url) VALUE (\"" + day_url[s] + "\");")

        print('successed')

        # 保存を実行
        connection.commit()
        # 接続を閉じる
        connection.close()


getresult = GetResultURL()

month_array = getresult.getMonthURL()
day_array = getresult.getDayURL(month_array)
getresult.insertDB(day_array)