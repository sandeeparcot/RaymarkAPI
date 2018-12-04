from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
import pyodbc
from DBClass import dbconnect

app = Flask(__name__)
api = Api(app)


class Quantity(Resource):
    def get(self,scode,pcode):
        v_dbobj = dbconnect()
        conn = v_dbobj.sqlconnect("HK-KWN-RPTST01\IZ_UAT", "ELHK_UAT", "abc", "pwd")

        query = "select rtrim(store_code) StoreCode,rtrim(product_code) ProductCode,cast(sum(isnull(quantity_received,0) - isnull(quantity_sold,0) -isnull(quantity_return_vendor,0) + isnull(qty_distributed_in, 0) - isnull(qty_distributed_out, 0) + isnull(qty_transfered_in, 0) - isnull(qty_transfered_out, 0) + isnull(qty_adj_inv_atl, 0 ) + isnull(quantity_returned,0) + isnull(shrink_qty, 0) + isnull(qty_adj_inv_btl, 0 ))as int) QtyOnHand from ELHK_UAT..product_now pn (nolock) inner join ELHK_UAT..store s (nolock)on pn.store_code_id = s.store_code_id inner join ELHK_UAT..product p (nolock) on p.Product_id = pn.product_id where s.store_code = '%s' and p.product_code = '%s'group by store_code, product_code" % (str(scode), str(pcode))

        cursor = v_dbobj.getdata(conn,query)

        for i in cursor.fetchall():
            result = {'Store Code': [i[0]],'6 digit SKU': [i[1]], 'Quantity': [i[2]]}

        print(result)
        return jsonify(result)

api.add_resource(Quantity, '/qtyonhand/<scode>/<pcode>')  # Route_1


if __name__ == '__main__':
    app.run(port='5007')

