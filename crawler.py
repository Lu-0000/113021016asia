import os
import sqlite3
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver. common.by import By
import time

# 啟動瀏覽器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://csie.asia.edu.tw/zh_tw/TeacherIntroduction/Full_time_faculty")
time.sleep(2)

# 抓取網頁文字（以第一個 <p> 為例）
tags=driver.find_elements(By.CLASS_NAME, "member-data-value-7")
for tag in tags:
  print(tag.text)
# 使用者輸入資料夾
folder_path = input("請輸入要儲存的資料夾路徑：")
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 儲存為 txt 檔案
file_path = os.path.join(folder_path, "professors_expertise.txt")
with open(file_path, "w", encoding="utf-8") as f:
    for tag in tags:
        f.write(tag.text + "\n")  # 每行寫一筆
print(f" 已儲存文字到 {file_path}")

print(f"已儲存文字到 {file_path}")

# 儲存到 SQLite 資料庫
db_path = os.path.join(folder_path, "data.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 建立資料表（如果不存在）
cursor.execute('''
CREATE TABLE IF NOT EXISTS scraped_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    saved_time TEXT
)
''')

# 插入資料
saved_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cursor.execute('INSERT INTO scraped_data (content, saved_time) VALUES (?, ?)', (tag.text, saved_time))

conn.commit()
conn.close()

print(f"已儲存資料到 SQLite 資料庫：{db_path}")
