import pyodbc

class dbconnect:
    def __init__(self):
        pass

#function for creating a database connection to SQL Server. The arguments are server name, database name , username and password.

    def sqlconnect(self,server,dbname,uname,pwd):
        try:
            cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                              "Server=%s;"
                              "Database=%s;"
                              "Trusted_Connection=yes;"  % (str(server),str(dbname)))
            return cnxn
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            #if sqlstate == '08001':
            print ex.args[1]



#function returns query result in a cursor. The arguments are connection and sql query

    def getdata(self,cnxn,query):
        cursor = cnxn.cursor()
        try:
            cursor.execute(query)
            return cursor
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            # if sqlstate == '08001':
            print ex.args[1]

    def validatestoreCode(self,cnxn,scode):
            try:
                cursor = cnxn.cursor()
                cursor.execute("Select rtrim(store_code) StoreCode from ELHK_UAT..store s where s.store_code = '%s'" % str(scode))
                results = cursor.fetchall()
                if results == []:
                    return False
                else:
                    return True
            except pyodbc.Error as ex:
                    print ex.args[1]

