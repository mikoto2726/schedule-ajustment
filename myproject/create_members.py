import re
import sqlite3

def extract_info(line):
    # 正規表現を使用してデータを抽出する
    match = re.match(r'(.+?),(.*),(.+)', line)
    if match:
        name = match.group(1)
        email = match.group(2)
        slack_id = match.group(3)
        return (name, email, slack_id)
    else:
        return None

# データベースに接続
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# members.txtファイルをオープン
with open('members.txt', 'r') as file:
    for line in file:
        # データを抽出
        data = extract_info(line)
        if data:
            name, email, slack_id = data
            # データをschedule_memberテーブルに挿入
            cursor.execute('INSERT INTO schedule_member (name, slack_id) VALUES (?, ?)', (name, slack_id))
        else:
            print(f"Invalid data format: {line}")

# コミットして接続を閉じる
conn.commit()
conn.close()