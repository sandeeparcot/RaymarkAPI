import pyodbc

class dbconnect:
    def __init__(self):
        pass

#function for creating a database connection to SQL Server. The arguments are server name, database name , username and password.

    def sqlconnect(self,server,dbname,uname,pwd):
        cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                              "Server=%s;"
                              "Database=%s;"
                              "Trusted_Connection=yes;"  % (str(server),str(dbname)))
        return cnxn

#function returns query result in a cursor. The arguments are connection and sql query

    def getdata(self,cnxn,query):
        cursor = cnxn.cursor()
        cursor.execute(query)
        return cursor

C1 = dbconnect()

conn = C1.sqlconnect("HK-KWN-RPTST01\IZ_UAT","ELHK_UAT","abc","pwd")
query = "select rtrim(store_code) StoreCode,rtrim(product_code) ProductCode,sum(isnull(quantity_received,0) - isnull(quantity_sold,0) -isnull(quantity_return_vendor,0) + isnull(qty_distributed_in, 0) - isnull(qty_distributed_out, 0) + isnull(qty_transfered_in, 0) - isnull(qty_transfered_out, 0) + isnull(qty_adj_inv_atl, 0 ) + isnull(quantity_returned,0) + isnull(shrink_qty, 0) + isnull(qty_adj_inv_btl, 0 )) QtyOnHand from ELHK_UAT..product_now pn (nolock) inner join ELHK_UAT..store s (nolock)on pn.store_code_id = s.store_code_id inner join ELHK_UAT..product p (nolock) on p.Product_id = pn.product_id where s.store_code = 'CL52' and p.product_code = 'ZTPH02'group by store_code, product_code"
print (query)

cursor = C1.getdata(C1.sqlconnect("HK-KWN-RPTST01\IZ_UAT","ELHK_UAT","abc","pwd"),query)
for row in cursor:
    print('row = %r' % (row,))