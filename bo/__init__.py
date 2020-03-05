import os

from flask import Flask
from bo.db import get_db

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
    @app.route('/hello')
    def hello():
        tacrs_arr = []
        db = get_db()
        cpids = db.execute(
            'SELECT COUNT(product_id) AS cpid FROM order_lines '
            'JOIN orders ON order_lines.order_id = orders.id '
            'WHERE created_at LIKE "2019-08-11%"'
        ).fetchall()
        for cpid in cpids:
            print(f"items:- ", cpid['cpid'])

        cids = db.execute(
            'SELECT COUNT(customer_id) AS cid FROM orders WHERE created_at LIKE "2019-08-11%"'
        ).fetchall()
        for cid in cids:
            print(f"customers:- ", cid['cid'])

        sumdas = db.execute(
            'SELECT SUM(discounted_amount) AS sumda FROM order_lines '
            'JOIN orders ON order_lines.order_id = orders.id '
            'WHERE created_at LIKE "2019-08-11%"'
        ).fetchall()
        for sumda in sumdas:
            print(f"total_discount_amount:- ", sumda['sumda'])

        avgdrs = db.execute(
            'SELECT AVG(discount_rate) AS avgdr FROM order_lines '
            'JOIN orders ON order_lines.order_id = orders.id '
            'WHERE created_at LIKE "2019-08-11%"'
        ).fetchall()
        for avgdr in avgdrs:
            print(f"discount_rate_avg:- ", avgdr['avgdr'])

        avgtas = db.execute(
            'SELECT AVG(total_amount) AS avgta FROM order_lines '
            'JOIN orders ON order_lines.order_id = orders.id '
            'WHERE created_at LIKE "2019-08-11%"'
        ).fetchall()
        for avgta in avgtas:
            print(f"order_total_avg:- ", avgta['avgta'])

        sumtars = db.execute(
            'SELECT SUM(order_lines.total_amount * commissions.rate) AS sumtar '
            'FROM orders JOIN order_lines ON orders.id = order_lines.order_id '
            'JOIN commissions on orders.vendor_id = commissions.vendor_id '
            'WHERE created_at LIKE "2019-08-11%" AND commissions.date = "2019-08-11"'
        ).fetchall()
        for sumtar in sumtars:
            print(f"sumtar:- ", sumtar['sumtar'])

        averageperorders = db.execute(
            'SELECT orders.id AS orderid, order_lines.product_id, order_lines.total_amount, '
            'commissions.rate, AVG(order_lines.total_amount * commissions.rate) as averageperorder '
            'FROM orders LEFT JOIN order_lines ON orders.id = order_lines.order_id '
            'LEFT JOIN commissions on orders.vendor_id = commissions.vendor_id '
            'WHERE created_at LIKE "2019-08-12%" AND commissions.date = "2019-08-12"'
        ).fetchall()
        for averageperorder in averageperorders:
            print(f"order_average:- ", averageperorder['averageperorder'])


        tacrs = db.execute(
            'SELECT order_lines.product_id, order_lines.total_amount, product_promotions.promotion_id, '
            'SUM(order_lines.total_amount * commissions.rate) AS tacr FROM orders JOIN order_lines '
            'ON orders.id = order_lines.order_id LEFT JOIN product_promotions '
            'ON order_lines.product_id = product_promotions.product_id LEFT JOIN commissions '
            'ON orders.vendor_id = commissions.vendor_id WHERE created_at LIKE "2019-08-12%"'
            ' AND product_promotions.promotion_id IS NOT null '
            'AND commissions.date = "2019-08-12" '
            'AND product_promotions.date = "2019-08-12" GROUP BY product_promotions.promotion_id'
        ).fetchall()
        for tacr in tacrs:
            tacrs_arr.append(tacr['tacr'])

        print(f"commissions-promotions:- ", tacrs_arr)

        return 'results'

    return app
