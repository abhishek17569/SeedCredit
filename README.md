# SeedCredit

SeedCredit is a platform that provides investment cum crowdfunding opportunities in startups and lending money to others.
## About
- SeedCredit help startup to raise money(crowdfunding) and also help to lend money to people who need quick cash.  
- SeedCredit reduce gaps between small investors and startup geeks. Thus help in raising funding for startups and in-return provide high income opportunity for investors(from startups)

Video Link:
https://youtu.be/sHMWXwST_No  
Phase 1 video: https://www.youtube.com/watch?v=4rba4jOZCHE

PPT:
https://docs.google.com/presentation/d/1LfYYbnq19DWPbbBmHVkbk9rO4j1VJRn5/edit?usp=sharing&ouid=113446019009218061225&rtpof=true&sd=true

Other Links(Scrrenshots):
https://drive.google.com/drive/folders/1Vq_MxaLZoRMpszAyqP-_eIKUPgsVKgX4

## Tech Stack
- Flask
- Jinja
- HTML/CSS/JS
- Mongo
## Set Up
Before setup please install mongodb.
- Mongo Window set up: ```https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/```  
- Mongo Linux set up: ```https://docs.mongodb.com/manual/administration/install-on-linux/```  
- After installation, please import the provided database under folder ```Mongo Connection``` or ```Mongo Connection.zip```  
- Note: Our database name is ```test_database``` and  files are in json format. (Please go to end of readme to know more about importing data)
It requires ```python``` and ```pip``` to run the web app.  
Please run below command to install all the dependencies.

```bash
pip install -r requirements.txt
```

## Usage

```python
flask run
```

## Database File
```Mongo connection.zip``` and it is also in folder ```Mongo connection```

## Credentials
Use the below credential on the login page.
```
Email: demo@gmail.com
Password: demo
```
## Steps to use web-appp
- By default server run on port 5000
- Go to URL ```127.0.0.1:5000/``` (or ```localhost:5000```)
- Login to the side using above credential(i.e email: demo@gmail.com & password: demo)

## Screenshot
Also we have included the screenshot of web-app under ```Screenshot``` Folder

## Possible error while initial setup
```
ImportError: cannot import name 'abc' from 'bson.py3compat' 
(/zeta_hack/env/lib/python3.9/site-packages/bson/py3compat.py)
```
#### Solution
- Solution: ```https://stackoverflow.com/questions/53441445/flask-app-broken-after-bson-update-in-heroku```  
- Solution: ```https://stackoverflow.com/questions/60149801/import-error-importerror-cannot-import-name-abc-from-bson-py3compat```

### Importing Mongo data
- We are using Studio3T for all the mongo operations. So, importing from there is quite handly/easy (https://studio3t.com/download/). In the Screenshot folder, we have included a screenshot which display strcutre of our database
- Alternative, ```mongoimport --db dbName --collection collectionName < fileName.json``` from command line
- Below is the database structure
![Database structure](https://raw.githubusercontent.com/tusharkeshav/zeta_hack/main/Screenshots/Mongo_db_structure.png)
