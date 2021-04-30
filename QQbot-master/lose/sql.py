import pymysql

def gg(base, id, user_id, x, y):  #更改 x为需要更改的属性，y为改后的值
	sql = f"update {base} set {x}={y} where {id}={user_id}"
	con = pymysql.connect(host='localhost', user='root', password='282610', database='qqbot', charset='utf8')
	cur = con.cursor()
	print(sql)
	cur.execute(sql)
	con.commit()
	cur.close()
	con.close()

def select(base, x, a, b):
	con = pymysql.connect(host='localhost', user='root', password='282610', database='qqbot', charset='utf8')
	cur = con.cursor()
	cur.execute(f'select {x} from {base} where {a} = {b}')
	res = str(cur.fetchone())
	cur.close()
	con.close()
	return res




