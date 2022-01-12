import ujson

def register_acc(new_account,new_password):
    new_account=str(new_account)
    new_password=str(new_password)
    isexist=False
    with open('data/user.json','r',encoding='utf-8') as f:
        database=ujson.load(f)
        f.close()
    for item in database:
        account=item['account'];
        if new_account==account:
            isexist=True
    if isexist==True:
        return "account is exist!"
    else:
        new_user={
            "account":new_account,
            "password":new_password
        }
        with open('data/user.json','r',encoding='utf-8')as f:
            database = ujson.load(f)
            f.close()
        database.append(new_user)
        with open('data/user.json','w',encoding='utf-8')as f:
            ujson.dump(database,f)
            f.close()
        return "Success!"

if __name__=='__main__':
    print(register_acc("123","456"))