from clickhouse_driver import Client
client = Client('localhost', user='blcklptn', password='Mjolnir123', database='refferall')
l = client.execute('SHOW TABLES')
print(l)