# coding:utf8
import sys
import pymysql

class TransferMoney(object):
    def __init__(self,conn):
        self.conn=conn

    def check_acct_available(self,acctid):
        cursor = self.conn.cursor()
        try:
            sql="select * from account where acctid=%s" % acctid
            cursor.execute(sql)
            print ("check_acct_available:" + sql)
            rs = cursor.fetchall()
            if len(rs) ! = 1:
                raise Exception("账号%s不存在"% acctid)
        finally:
            cursor.close()



    def has_enough_money(self,acctid,money):
        cursor = self.conn.cursor()
        try:
            sql="select * from account where acctid=%s and money>%s" % (acctid,money)
            cursor.execute(sql)
            print ("has_enough_money:"+sql)
            rs = cursor.fetchall()
            if len(rs) ! = 1:
                raise Exception("账号%s余额不足"% acctid)
        finally:
            cursor.close()


    def reduce_money(self,acctid,money):
        cursor = self.conn.cursor()
        try:
            sql = "update account set money=money-%s where acctid=%s" % (money,acctid)
            cursor.execute(sql)
            print ("reduce_money:"+sql)
            if cursor.rowcount ! = 1:
                raise Exception("账号%s减款失败" % acctid)
        finally:
            cursor.close()

    def add_money(self,acctid,money):
        cursor = self.conn.cursor()
        try:
            sql="update account set money=money+%s where acctid=%s" % (money,acctid)
            cursor.execute(sql)
            print ("add_money:"+sql)
            if cursor.rowcount ! = 1:
                raise Exception("账号%s加款失败" % acctid)
        finally:
            cursor.close()


    def transfer(self,source_acctid,target_acctid,money):
        try:
            self.check_acct_available(source_acctid)
            self.check_acct_available(target_acctid)
            self.has_enough_money(source_acctid,money)
            self.reduce_money(source_acctid,money)
            self.add_money(target_acctid,money)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e


if __name__ == "__main__":
    source_acctid = sys.argv[1]
    target_acctid = sys.argv[2]
    money = sys.argv[3]


    conn = pymysql.Connect(
                       host = 'localhost',
                       unix_socket = "..mysql/mysql.sock",
                       port = 3306,
                       user = 'root',
                       passwd = '',
                       db = 'python_db',
                                        )
    tr_money = TransferMoney(conn)

    try:
        tr_money.transfer(source_acctid,target_acctid,money)
    except Exception as e:
        print ("出现问题" + str(e))
    finally:
        conn.close()
