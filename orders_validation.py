
import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user =  "root",
    password = "root",
    database = "etl_project"
)
cursor = conn.cursor()

print("===== ORDERS VALIDATION REPORT =====")

# 1. Record Count Validation
cursor.execute("SELECT COUNT(*) FROM orders")
source_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM orders_target")
target_count = cursor.fetchone()[0]

print(f"\nSource Count : {source_count}")
print(f"Target Count : {target_count}")

if source_count == target_count:
    print("Record Count Validation : PASS")
else:
    print("Record Count Validation : FAIL")

# 2. Null Validation
cursor.execute("""
SELECT COUNT(*)
FROM orders
WHERE customer_id IS NULL
""")

null_count = cursor.fetchone()[0]

print(f"\nNull Count : {null_count}")

if null_count == 0:
    print("Null Validation : PASS")
else:
    print("Null Validation : FAIL")

# 3. Duplicate Validation
cursor.execute("""
SELECT COUNT(*)
FROM (
    SELECT order_id
    FROM orders
    GROUP BY order_id
    HAVING COUNT(*) > 1
) a
""")

dup_count = cursor.fetchone()[0]

print(f"\nDuplicate Count : {dup_count}")

if dup_count == 0:
    print("Duplicate Validation : PASS")
else:
    print("Duplicate Validation : FAIL")

# 4. Aggregate Validation - Price
cursor.execute("SELECT SUM(price) FROM orders")
source_price = cursor.fetchone()[0]

cursor.execute("SELECT SUM(price) FROM orders_target")
target_price = cursor.fetchone()[0]

print(f"\nSource Price Sum : {source_price}")
print(f"Target Price Sum : {target_price}")

if source_price == target_price:
    print("Price Aggregate Validation : PASS")
else:
    print("Price Aggregate Validation : FAIL")

# 5. Aggregate Validation - Quantity
cursor.execute("SELECT SUM(quantity) FROM orders")
source_qty = cursor.fetchone()[0]

cursor.execute("SELECT SUM(quantity) FROM orders_target")
target_qty = cursor.fetchone()[0]

print(f"\nSource Quantity Sum : {source_qty}")
print(f"Target Quantity Sum : {target_qty}")

if source_qty == target_qty:
    print("Quantity Aggregate Validation : PASS")
else:
    print("Quantity Aggregate Validation : FAIL")

# 6. Data Comparison Validation
cursor.execute("""
SELECT COUNT(*)
FROM orders s
LEFT JOIN orders_target t
ON s.order_id = t.order_id
WHERE t.order_id IS NULL
""")

mismatch_count = cursor.fetchone()[0]

print(f"\nMismatch Records : {mismatch_count}")

if mismatch_count == 0:
    print("Data Comparison Validation : PASS")
else:
    print("Data Comparison Validation : FAIL")

conn.close()

print("\n===== VALIDATION COMPLETED =====")