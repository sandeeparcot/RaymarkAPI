from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from DBClass import dbconnect
from datetime import datetime

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False

class Quantity(Resource):
    def get(self,scode,pcode):

        # Creating the instance of the dbconnect class from DBClass.py
        v_dbobj = dbconnect()
        conn = v_dbobj.sqlconnect("HK-KWN-RPTST01\IZ_UAT", "ELHK_UAT", "abc", "pwd")

        # Validating the length of SKU
        if len(pcode) <> 6:
            return {'Error':['6 digit SKU only allowed']}

        # Validating the Store Code
        if (v_dbobj.validatestoreCode(conn,scode)):
            pass
        else:
            return {'Error': ['Not a Valid StoreCode']}

        #forming the raymark db query to query the on hand quantity
        strqtyquery = "select rtrim(store_code) StoreCode,rtrim(product_code) ProductCode,cast(sum(isnull(quantity_received,0) - isnull(quantity_sold,0) -isnull(quantity_return_vendor,0) + isnull(qty_distributed_in, 0) - isnull(qty_distributed_out, 0) + isnull(qty_transfered_in, 0) - isnull(qty_transfered_out, 0) + isnull(qty_adj_inv_atl, 0 ) + isnull(quantity_returned,0) + isnull(shrink_qty, 0) + isnull(qty_adj_inv_btl, 0 ))as int) QtyOnHand from ELHK_UAT..product_now pn (nolock) inner join ELHK_UAT..store s (nolock)on pn.store_code_id = s.store_code_id inner join ELHK_UAT..product p (nolock) on p.Product_id = pn.product_id where s.store_code = '%s' and p.product_code = '%s'group by store_code, product_code" % (str(scode), str(pcode))
        cursor = v_dbobj.getdata(conn,strqtyquery) #call the get data function from sqlconnect class
        now = datetime.now()
        print (now.strftime('%Y-%m-%d %H:%M:%S'))
        if cursor.rowcount == -1:
            for i in cursor.fetchall():
                return {"Error": [],"InventoryQty": i[2], "Store Code": i[0], "SKU": i[1], "Last_Polled_Date": now.strftime('%Y-%m-%d %H:%M:%S') ,"Hist_Day_Date":'null',"status": 'success',"type": 'success',"code": '200'}
        else:
            return {'Error': ['No Data']}



api.add_resource(Quantity, '/onhandinventory/<scode>/<pcode>')  # Route_1


if __name__ == '__main__':
    app.run(port='5007')

