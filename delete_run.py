#!python3.6
# -*- coding: utf-8 -*-

'''
指定されたworkflow IDのランのうち、run_statusが９（起動失敗）のものを削除（論理削除）する。
削除したランのinternal_run_idをrun_idとともにログとして残す
'''

import mysql.connector
import time
import sys, os

# 削除日時設定（本プログラム実行時）
time_stamp = time.strftime('%Y-%m-%d %H:%M:%S')
log_stamp = time.strftime('%Y%m%d_%H%M%S')
logfilename = "workflow_run_delete_%s.log"%log_stamp

# workflow idの確認
if len(sys.argv) == 1:
    print("user python <workflow_id>")
    sys.exit(1)
else:
    workflow_id = sys.argv[1]

print("workflow id is %s"%workflow_id)

db=mysql.connector.connect(host="127.0.0.1", user="root", password="P@ssw0rd")
cursor = db.cursor()
cursor.execute("use workflow")

# 対象workflow id の起動失敗ランと異常終了ランの取得
cursor.execute("""select run_id from run where workflow_id = '""" + workflow_id + """' and (run_status = "9" or run_status = "99") and deleted = 0;""")
# 対象workflow id の起動失敗ランの取得
#cursor.execute("""select run_id from run where workflow_id = '""" + workflow_id + """' and run_status = "9" and deleted = 0;""")
rows = cursor.fetchall()
print(len(rows))
counts = len(rows)
if counts == 0:
    print("削除対象のランがありません。")
    sys.exit(0)

count = 1

#last_id = str(rows[-1][0])
#print(last_id)

# ログファイル準備
outfile = open(logfilename, "w")

# 論理削除実行
for row in rows:
    last_id = str(row[0])
    sys.stdout.write("\r%06d/%06d(run_id = %s)"%(count, counts, last_id))
    sys.stdout.flush()
    count += 1

    #print(last_id)
    #time.sleep(0.1)
    #continue

    # internal_run_id取得
    cursor.execute("""select internal_run_id from run where run_id = '""" + last_id + """';""")
    items = cursor.fetchall()
    internal_run_id = str(items[-1][0])
    # creator取得
    cursor.execute("""select creator from run where run_id = '""" + last_id + """';""")
    items = cursor.fetchall()
    creator = str(items[-1][0])
    # 更新作業
    cursor.execute("""update run set deleted="1" where run_id = '""" + last_id + """';""")
    cursor.execute("""update run set deletion_time = '""" + time_stamp + """' where run_id = '""" + last_id + """';""")
    cursor.execute("""update run set deleted_by = '""" + creator + """' where run_id = '""" + last_id + """';""")
    db.commit()
    outfile.write("run_id = %s / internal_run_id = %s / deleted at %s\n"%(last_id, internal_run_id, time_stamp))
    time.sleep(0.1)

outfile.close()
print("")

# 終了処理
cursor.close()
db.close()
