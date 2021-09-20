import MySQLdb

username = "' OR 1=1 #"# sql语句注入
password = ""
conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root", db="mxonline", charset="utf8")
cursor = conn.cursor()
sql = "select * from users_userprofile where username='{}' and password='{}'".format(username, password)
cursor.execute(sql)
for row in cursor.fetchall():
    print(row)

# 1. 表单验证
# 2. 查询用户逻辑
# 3. django的orm会对特殊字符转义