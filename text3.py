import  pymysql

# 创建数据库连接对象，db是链接数据库，此处用户名密码必须同mysql库里的。
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                       password='Study', db='stuDB')

# 获取一个用来操作数据库的游标对象
cursor = conn.cursor()

# 程序菜单
print('1.查询学生\n2.添加学生')
s = int(input('请输入功能序号：'))
if s == 1:
    num = int(input('请输入要查询的学生学号：'))

    sql = 'select * from student where sno=%d'%num
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        print(res)
    else:
        print('没找到啊')
elif s == 2:
    num = int(input('请输入学号：'))
    name = input('请输入姓名：')
    sex = input('请输入性别：')
    age = int(input('请输入年龄：'))
    dept = input('请输入专业：')
    # 双引号啊，双引号！
    sql = 'insert into student values(%d, "%s", "%s", %d, "%s")'%(num, name, sex, age, dept)
    cursor.execute(sql)
    conn.commit()