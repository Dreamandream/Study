import  pymysql

# 创建数据库连接对象，db是链接数据库，此处用户名密码必须同mysql库里的。
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                       password='Study', db='stuDB')

# 获取一个用来操作数据库的游标对象
cursor = conn.cursor()

sql = 'insert into student values(10006, "张三", "男", 30, "cs")'

cursor.execute(sql)

# 哇哦
# 数据的增删改需要提交事务（类似保存）
conn.commit()
