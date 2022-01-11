import ujson

def check(input_account,input_password,datatype):
    flag=False
    if datatype=='Admin':
        data='data/admin.json'
    elif datatype=='user':
        data='data/user.json'
    with open(data,'r',encoding='utf-8') as f:
        database=ujson.load(f)
        f.close()
    for item in database:
        account=item['account'];
        password=str(item['password'])
        if input_account==account and input_password==password:
            flag=True
    return flag
            

if __name__=='__main__':
    acc=str(input("account:"))
    pw=str(input("password:"))
    print(check(acc,pw,"Admin"))