import flask
import ujson 

def ticketjson_gen(account):
    account=str(account)
    name=flask.request.values.get('name',type=str)
    birthday=flask.request.values.get('birthday',type=str)
    ID_card=flask.request.values.get('ID',type=str)
    cellphone=flask.request.values.get('cellphone',type=str)
    email=flask.request.values.get('email',type=str)
    choose_movie=flask.request.values.get('choose_movie',type=str)
    movie_type=flask.request.values.get('op',type=str)
    cinema=flask.request.values.get('cinema',type=str)
    session=flask.request.values.get('session',type=str)
    seat_row=flask.request.values.get('seat_row',type=str)
    seat_num=flask.request.values.get('seat_num',type=str)
    food=flask.request.values.get('food',type=str)
    flag=True
    reason=0
    new_ticket={"account":account,"name":name,"birthday":birthday,"ID_card":ID_card,"cellphone":cellphone,"email":email,"choose_movie":choose_movie,"movie_type":movie_type,"cinema":cinema,"session":session,"seat_row":seat_row,"seat_num":seat_num,"food":food}
    if len(ID_card)!=4:
        flag=False
        reason=1
    if len(cellphone)!=10 or not cellphone.startswith('09'):
        flag=False
        reason=2
    if choose_movie=='0' or cinema=='0' or session=='0' or seat_row=='0' or seat_num=='0' or food=='0':
        flag=False
        reason=3
    if flag==False:
        new_error={"account":account,"reason":reason}
        with open('data/error.json','r',encoding='utf-8')as f:
            database = ujson.load(f)
            f.close()
        database.append(new_error)
        with open('data/error.json','w',encoding='utf-8')as f:
            ujson.dump(database,f)
            f.close()
    else:
        with open('data/ticket.json','r',encoding='utf-8')as f:
            database = ujson.load(f)
            f.close()
        database.append(new_ticket)
        with open('data/ticket.json','w',encoding='utf-8')as f:
            ujson.dump(database,f,ensure_ascii=False)
            f.close()
    

