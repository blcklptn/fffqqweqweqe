from clickhouse_driver import Client
def get_referall_link(user_id):
    """Get referall link from database"""
    client = Client('localhost', user='default', password='Mjolnir123', database='refferall')
    l = client.execute(f"SELECT * FROM refferall.users WHERE user = '{user_id}'")
    try:
        print(l[0][1])
    except:
        print('None')

get_referall_link(4535345)