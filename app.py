from flask import Flask,render_template,request
from flask_cors import CORS,cross_origin
import pymongo
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import logging
import requests
import os
logging.basicConfig(filename='img_scrap.log',level=logging.INFO)
app=Flask(__name__)
@app.route('/',methods=['GET'])
def homepage():
    return render_template('index.html')
@app.route('/review',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        try:
            query=request.form['content'].replace(" ","")
            save_dir='images1/'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
            response=requests.get(f'https://www.google.com/search?q={query}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjLmJ-Py6v-AhXaSGwGHfYLBrYQ_AUoAnoECAEQBA&biw=1536&bih=746&dpr=1.25')
            soup=bs(response.content,'html.parser')
            img_tags=soup.find_all('img')
            del(img_tags[0])
            img_data=[]
            for index,image_tag in enumerate(img_tags):
                image_url=image_tag['src']      
                image_data=requests.get(image_url).content
                mydict={"index":index,"image":image_data}
                img_data.append(mydict)
                with open(os.path.join(save_dir,f"{query}_{img_tags.index(image_tag)}.jpg"),'wb') as f:
                    f.write(image_data)
            
            client=pymongo.MongoClient('mongodb+srv://aqibansari72a:aqib7860@cluster0.1tmwbzz.mongodb.net/test')
            db=client['image_scrap']
            coll=db['image_data_scrap']
            coll.insert_many(img_data)
            
            return "something is wrong"
        except Exception as e:
            logging.info(e)
            return "something is wrong"
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)