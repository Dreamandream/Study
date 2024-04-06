# pip install pymysql
import  pymysql

# 创建数据库连接对象，db是链接数据库，此处用户名密码必须同mysql库里的。
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                       password='Study', db='stuDB')

# 获取一个用来操作数据库的游标对象
cursor = conn.cursor()

sql = 'select * from student where sno=10001'

# 执行sql语句
cursor.execute(sql)

# 读取结果
res = cursor.fetchone()

print(res)