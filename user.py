from pydoc import describe
from flask_restful import Resource, reqparse
import pymysql
from flask import jsonify
import util
from flask_apispec import doc,use_kwargs,MethodResource,marshal_with
from user_route_model import UserGetResponse,UserCommonResponse,UserPatchRequest,UserPostRequests,LoginRequests,SearchProduct
from flask_jwt_extended import create_access_token,jwt_required
from datetime import timedelta 

def db_init():
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        db='market'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor

def get_access_token(account):
    token = create_access_token(
        identity={"account": account},
        expires_delta=timedelta(days=1)
    )
    return token

class Car(MethodResource):
    @doc(description='Get',tags=['Car'])
    @marshal_with(UserGetResponse,code=200)
    @jwt_required()
    def get(self):
        db, cursor = db_init()

        sql = "SELECT * FROM market.product "
        cursor.execute(sql)
        

        users = cursor.fetchall()
        db.close()
        return util.success(users)

    @doc(description='Post',tags=['Car'])
    @use_kwargs(UserPostRequests,location="json")
    @marshal_with(UserCommonResponse,code=200)
    def post(self,**kwargs):
        db, cursor = db_init()
        

        user = {
            'name': kwargs['name'],
            'price': kwargs['price'],
            'amount': kwargs['amount'],
        }
        sql = """

        INSERT INTO `market`.`product` (`name`,`price`,`amount`)
        VALUES ('{}','{}','{}');

        """.format(
            user['name'], user['price'] ,user['amount'])
            
        result = cursor.execute(sql)
        
        db.commit()
        db.close()

        if result==1:
            return util.success()
        
        return util.failure()
        
        


class car1(MethodResource):
    @doc(description='Update',tags=['Car'])
    @use_kwargs(UserPatchRequest,location="json")
    @marshal_with(UserGetResponse,code=200)
    def patch(self, name,**kwargs):
        db, cursor = db_init()
        
        user = {
            'name': kwargs.get('name'),
            'price': kwargs.get('price'),
            'amount': kwargs.get('amount')
            
        }

        query = []
        print(user)
        for key, value in user.items():
            if value is not None:
                query.append(f"{key} = {value}")
        query = ",".join(query)
        print(query)
        '''
        UPDATE table_name
        SET column1=value1, column2=value2, column3=value3···
        WHERE some_column=some_value;

        '''
        sql = """
            UPDATE market.product
            SET {}
            WHERE name = "{}";
        """.format(query, name)
        sql_total="SELECT SUM(CONVERT(price,SIGNED)* CONVERT(amount,SIGNED)) AS total_price FROM product;"

        result = cursor.execute(sql)
        result2 = cursor.execute(sql_total)


        db.commit()
        users = cursor.fetchall()
        db.close()

        if result  ==1:
            return util.success(users)
        
        return util.failure()
        

    @doc(description='Delete',tags=['Car'])
    @marshal_with(UserGetResponse,code=200)
    def delete(self, name):
        db, cursor = db_init()
        sql = f'DELETE FROM `market`.`product` WHERE name = "{name}";'
        sql_total="SELECT SUM(CONVERT(price,SIGNED)* CONVERT(amount,SIGNED)) AS total_price FROM product;"
        result = cursor.execute(sql)
        result2 = cursor.execute(sql_total)

        db.commit()
        users = cursor.fetchall()
        db.close()

        if result==1:
            return util.success(users)
        
        return util.failure()

class Login(MethodResource):
    @doc(description='User Login', tags=['Login'])
    @use_kwargs(LoginRequests, location="json") #要改
    #@marshal_with(user_router_model.UserGetResponse, code=200)
    def post(self, **kwargs):
        db, cursor = db_init()
        account, password = kwargs["account"], kwargs["password"]
        sql = f"SELECT * FROM market.member WHERE account = '{account}' AND password = '{password}';"
        cursor.execute(sql)
        user = cursor.fetchall()
        db.close()

        if user != ():
            token = get_access_token(account)
            data = {
                "message": f"Welcome back {user[0]['name']}",
                "token": token}
            return util.success(data)
        
        return util.failure({"message":"Account or password is wrong"})


class search(MethodResource):
    @doc(description='Search',tags=['Search'])
    @marshal_with(UserGetResponse,code=200)
    @jwt_required()
    def get(self, name):
        db, cursor = db_init()
        sql = f'select * FROM `market`.`product` WHERE name like "%{name}%";'
        result = cursor.execute(sql)

        db.commit()

        users = cursor.fetchall()
        db.close()
        return util.success(users)

