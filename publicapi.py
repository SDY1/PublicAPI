import requests
import pandas as pd
import numpy as np
import sqlalchemy as db
from flask import Flask
from flask.templating import render_template


 # api데이터를 가져와서 원하는 값만 뽑기--------------------------------------------
url = '''
http://openapi.seoul.go.kr:8088/6d424f64706765743730746d476f47/json/RealtimeCityAir/1/5?END_INDEX=1
'''

response = requests.get(url)
responseDict = response.json()
RealtimeCityAirs = responseDict["RealtimeCityAir"]["row"]

RealtimeCityAir = RealtimeCityAirs[0]
# MSRDT = RealtimeCityAir["MSRDT"]
# MSRSTE_NM = RealtimeCityAir["MSRSTE_NM"]
# PM10 = RealtimeCityAir["PM10"]
# IDEX_NM = RealtimeCityAir["IDEX_NM"]

# 리스트로 만들기-------------------------------------------------------------
list_r = []
for RealtimeCityAir in RealtimeCityAirs:
    list_c = [RealtimeCityAir["MSRDT"], RealtimeCityAir["MSRSTE_NM"] ,RealtimeCityAir["PM10"], RealtimeCityAir["IDEX_NM"]]
    list_r.append(list_c)

# print(list_r)

# 데이터프레임으로 변환해서 db에 저장-----------------------------------------------
engine = db.create_engine("mariadb+mariadbconnector://python:python1234@127.0.0.1:3306/pythondb")

dataFrame = pd.DataFrame(list_r, columns=["MSRDT", "MSRSTE_NM", "PM10","IDEX_NM"])
# print(dataFrame)

def insert():
    dataFrame.to_sql("weather", engine, index=False, if_exists="replace")

insert()

# csv파일로 저장---------------------------------------------------------------
dataFrame.to_csv('weather.csv')

# db에 저장된 데이터를 select하여 Flask로 웹화면에 table형태로 시각화-------------------------
def select():
    weathers = pd.read_sql(con=engine, sql="select * from weather")
    weathers = weathers.values.tolist()
    return weathers

# weathers = select()
# print(weathers)
# print(type(weathers))
app = Flask(__name__)

@app.route("/")
def hello():                            
    return render_template("index.html", weathers=select())

if __name__ == "__main__":
    app.run(debug=True)
