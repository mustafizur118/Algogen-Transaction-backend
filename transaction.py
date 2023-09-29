import psycopg2
from datetime import date

hostname = 'localhost'
database = 'transaction'
username = 'postgres'
pwd = '1234'
port_id = 5432

conn = psycopg2.connect(
    host=hostname,
    dbname=database,
    user=username,
    password=pwd,
    port=port_id

)

cur = conn.cursor()

create_script = ''' CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    transaction_date DATE NOT NULL,
    account_id INT NOT NULL,
    description TEXT,
    amount DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
)

 '''

query1 = """
    SELECT SUM(amount)
    FROM transactions
    WHERE account_id = %s AND transaction_date BETWEEN %s AND %s;
"""

query2 = """
            SELECT transaction_id, transaction_date, description, amount, category
            FROM transactions
            WHERE account_id = %s AND transaction_date BETWEEN %s AND %s;
        """

transactions = cur.fetchall()

if not transactions:
    print("No transactions found for the specified account and date range.")
else:
    # Print the transaction report
    print(f"Transaction Report for Account {account_id} ({start_date} to {end_date}):")
    print("{:<15} {:<12} {:<30} {:<15} {:<20}".format(
        "Transaction ID", "Date", "Description", "Amount ($)", "Category"))
    print("-" * 90)
    for transaction in transactions:
        transaction_id, transaction_date, description, amount, category = transaction
        print("{:<15} {:<12} {:<30} {:<15.2f} {:<20}".format(
            transaction_id, transaction_date, description, amount, category))

'''This is a Indexing part'''

'CREATE INDEX idx_transaction_date ON transactions (transaction_date)'
'CREATE INDEX idx_account_id ON transactions (account_id)'

account_id = 1
start_date = '2023-01-01'
end_date = '2023-12-31'

cur.execute(query1, (account_id, start_date, end_date))

total_amount = cur.fetchone()[0]

cur.execute(create_script)

insert_script = 'INSERT INTO  transactions (transaction_id, transaction_date, account_id, description, amount, category, created_at ) VALUES (%s, %s, %s, %s, %s, %s, %s)'
insert_value = [
    (111, '2023-01-01', '1', 'cityscape international limited', '80000', 'software engineer', '2023-09-29')]

cur.execute(insert_script, insert_value)

conn.commit()

cur.close()
conn.close()


def generate_transaction_report(account_id, start_date, end_date):
    pass


if __name__ == "__main__":
    account_id = 1
    start_date = date(2023, 1, 1)
    end_date = date(2023, 12, 31)

    generate_transaction_report(account_id, start_date, end_date)

print(f'Total amount for account {account_id} between {start_date} and {end_date}: ${total_amount:.2f}')
