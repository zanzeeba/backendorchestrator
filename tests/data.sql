INSERT INTO commissions (date, vendor_id, rate)
VALUES
('2019-08-01', 1, '0.29'),
('2019-08-01', 2, '0.07');

INSERT INTO orders (id, created_at, vendor_id, customer_id)
VALUES (2, '2019-08-01 18:43:57.052767', 3, 1398),
(3, '2019-08-01 11:51:07.349383', 2, 7449);
