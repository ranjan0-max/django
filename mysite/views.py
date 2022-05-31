from pickle import FALSE, TRUE
from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse
import json
from pymongo import MongoClient

av_user=""

def login(request):       
    return render(request,'login.html')

def billing(request):
    global av_user
    try:
        client =MongoClient('mongodb+srv://ranjan:Ranjan123@cluster0.f5ahg2j.mongodb.net/test')  
        db = client.login # create database
        collection=db.allowed #create collection
        if request.method=="POST":
            uname=request.POST.get('username','none')
            pwrd=request.POST.get('password','none')
            info=collection.find({"name":uname},{"name":1,"_id":0,"password":1,"email":1,"pno":1})
            l1= list(info)
            if uname in l1[0]["name"] and pwrd in l1[0]["password"]:
                    av_user=uname
                    return render(request,'ranjan_trader.html')
            else:
                return render(request,'login.html')
        else:
            return render(request,'login.html')            
    except:
        return HttpResponse("Database is not working right now...")        

def data(request):
    global av_user
    if request.method=="POST":
        receivedata=json.loads(request.body)
        try:
            client =MongoClient('mongodb+srv://ranjan:Ranjan123@cluster0.f5ahg2j.mongodb.net/test')
            db = client[f'biling']  #create database
            collection=db[f"{av_user}data"]  # create collection
            post_id=collection.insert_many(receivedata)  #upload datain server
            print("data inserted")
        except:
            print("user is not define")
        return StreamingHttpResponse("done")

def createacc(request):
    return render(request,'acc.html')


def user_name_exist(name):
    client =MongoClient('mongodb+srv://ranjan:Ranjan123@cluster0.f5ahg2j.mongodb.net/test')
    db = client.login
    collection=db.allowed
    info=collection.find({"name":name},{"name":1,"_id":0,"password":1,"email":1,"pno":1})
    li= list(info)
    l1=[]
    if len(li)!=0:
        return TRUE
    else:
        return FALSE       

def newuser(request):
    data={}
    if request.method=="POST":
        name=request.POST.get('name',"none")
        pwd=request.POST.get('password',"none")
        email=request.POST.get('email','none')
        pno=int(request.POST.get('pno',"none"))
        n=user_name_exist(name)
        if n==TRUE:
            return render(request,'acc.html',{"n":TRUE})
        else:    
            data={"name":name,
                "password":pwd,
                "email":email,
                "pno":pno,
                }
            try:     
                client =MongoClient('mongodb+srv://ranjan:Ranjan123@cluster0.f5ahg2j.mongodb.net/test')    
                db = client.login
                collection=db.allowed
                post_id=collection.insert_one(data)
                print("new user created")
                return render(request,'login.html')
            except:
                print("Database is not working write now")    
    else:
        print("it's not a post method")    