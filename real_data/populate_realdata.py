import psycopg2
import csv

# Connect to the PostgreSQL database
conn = psycopg2.connect(database="tool_tracking", user="postgres", password="postgres")

# Create a cursor object
cur = conn.cursor()

# Open the spreadsheet file
with open("products.csv", "r") as f:
    reader = csv.reader(f)

    # Iterate over the rows in the spreadsheet
    for row in reader:
        product_id = row[1]  # Assuming the "product_id" is in the second column
        # Check if a record with the same "product_id" already exists
        cur.execute("SELECT COUNT(*) FROM inlet_product WHERE product_id = %s", (product_id,))
        count = cur.fetchone()[0]
        if count == 0:
            # Insert the data into the Product table
            cur.execute("INSERT INTO inlet_product (name, product_id, supplier_name, supplier_gstin, description) VALUES (%s, %s, %s, %s, 'none')", row)
        else:
            # Handle the case where the record already exists (e.g., update or skip)
            pass

# Commit the changes
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
