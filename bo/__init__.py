import os

from flask import Flask
from bo.db import get_db
from flask import request
import json

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='anastasia',
        DATABASE=os.path.join(app.instance_path, 'bo.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    # a simple page that says hello
    @app.route('/bonjour', methods=['GET'])
    def bonjour():
        if request.method == 'GET':
            return 'Bonjour, Matelot!'

    # the endpoint to create the json
    @app.route('/bo', methods=['GET'])
    def bo():
        if request.method == 'GET':
            args = request.args
            wdnt = args['date']  # working date - no time
            wd = args['date'] + "%"  # working date - with time
            tacrs_arr = []  # array for commissions and promotions
            db = get_db()
            json_output = {}

            cids = db.execute(
                'SELECT COUNT(customer_id) AS cid FROM orders WHERE created_at LIKE "' + wd + '"'
            ).fetchall()
            for cid in cids:
                json_output["customers"] = cid['cid']

            sumdas = db.execute(
                'SELECT SUM(discounted_amount) AS sumda FROM order_lines '
                'JOIN orders ON order_lines.order_id = orders.id '
                'WHERE created_at LIKE "' + wd + '"'
            ).fetchall()
            for sumda in sumdas:
                json_output["total_discount_amount"] = sumda['sumda']


            cpids = db.execute(
                'SELECT COUNT(product_id) AS cpid FROM order_lines '
                'JOIN orders ON order_lines.order_id = orders.id '
                'WHERE created_at LIKE "' + wd + '"'
            ).fetchall()
            for cpid in cpids:
                json_output["items"] = cpid['cpid']


            avgtas = db.execute(
                'SELECT AVG(total_amount) AS avgta FROM order_lines '
                'JOIN orders ON order_lines.order_id = orders.id '
                'WHERE created_at LIKE "' + wd + '"'
            ).fetchall()
            for avgta in avgtas:
                json_output["order_total_avg"] = avgta['avgta']


            avgdrs = db.execute(
                'SELECT AVG(discount_rate) AS avgdr FROM order_lines '
                'JOIN orders ON order_lines.order_id = orders.id '
                'WHERE created_at LIKE "' + wd + '"'
            ).fetchall()
            for avgdr in avgdrs:
                json_output["discount_rate_avg"] = avgdr['avgdr']


            tacrs = db.execute(
                'SELECT order_lines.product_id, order_lines.total_amount, product_promotions.promotion_id, '
                'SUM(order_lines.total_amount * commissions.rate) AS tacr FROM orders JOIN order_lines '
                'ON orders.id = order_lines.order_id LEFT JOIN product_promotions '
                'ON order_lines.product_id = product_promotions.product_id LEFT JOIN commissions '
                'ON orders.vendor_id = commissions.vendor_id WHERE created_at LIKE "' + wd + '"'
                ' AND product_promotions.promotion_id IS NOT null '
                'AND commissions.date = "' + wdnt + '" '
                'AND product_promotions.date = "2019-08-12" GROUP BY product_promotions.promotion_id'
            ).fetchall()
            comm_json = {}
            promo_json = {}
            cp_counter = 1
            for tacr in tacrs:
                promo_json[cp_counter] = tacr['tacr']
                cp_counter += 1
                tacrs_arr.append(tacr['tacr'])

            comm_json["promotions"] = promo_json
            json_output["commissions"] = comm_json

            sumtars = db.execute(
                'SELECT SUM(order_lines.total_amount * commissions.rate) AS sumtar '
                'FROM orders JOIN order_lines ON orders.id = order_lines.order_id '
                'JOIN commissions on orders.vendor_id = commissions.vendor_id '
                'WHERE created_at LIKE "' + wd + '" AND commissions.date = "' + wdnt + '"'
            ).fetchall()
            for sumtar in sumtars:
                json_output["total"] = sumtar['sumtar']

            averageperorders = db.execute(
                'SELECT orders.id AS orderid, order_lines.product_id, order_lines.total_amount, '
                'commissions.rate, AVG(order_lines.total_amount * commissions.rate) as averageperorder '
                'FROM orders LEFT JOIN order_lines ON orders.id = order_lines.order_id '
                'LEFT JOIN commissions on orders.vendor_id = commissions.vendor_id '
                'WHERE created_at LIKE "' + wd + '" AND commissions.date = "' + wdnt + '"'
            ).fetchall()
            for averageperorder in averageperorders:
                json_output["order_average"] = averageperorder['averageperorder']

            json_string = json.dumps(json_output)
            return json_string

    return app
