import ujson

def check(input_account,input_password):
    with open('data/admin.json','r',encoding='utf-8') as f:
        admin=ujson.load(f)
        f.close()
    account=admin['account']
    password=str(admin['password'])
    if input_account==account:
        if input_password==password:
            return True
        else:
            return False
    else:
        return False

if __name__=='__main__':
    acc=str(input("account:"))
    pw=str(input("password:"))
    print(check(acc,pw))