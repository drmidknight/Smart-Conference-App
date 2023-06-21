# PROJECT DESCRIPTION

## Ready to setup the project:
    git clone https://github.com/Catalyst-OTU/Smart_Conference_App.git


## Installing Packages for Windows
- Run the following commad
    > pip install -r app/requirements.txt

## Installing Packages for Linux
- Run the following commad
    - pip install pipenve
    - pipenv shell
    - pipenv install



## CREATION AND MIGRATION OF DATABASE
>  Create a database name: **smart_conference_app**


- Database Migration and Data Seeding
Run the following command
    - python app/migrate.py


## RUNNING OR STARTING APPLICATON
- Running FastAPI Service Locally
    - uvicorn main:app --reload

    - OR

    - python run.py


- Running FastAPI Service On Docker 
    - Start Docker Service
    - Docker-compose build
    - Docker-compose up






Setup environment variables; allowed environment variables `KEYWORDS`=`VALUES`:

| KEYWORDS | VALUES | DEFAULT VALUE | VALUE TYPE | 
| :------------ | :---------------------: | :------------------: | :------------------: |
| DB_TYPE | | Mysql | string 
| DB_NAME | | smart_conference_app | string 
| DB_USER | | root | string 
| DB_PASSWORD | |  | string 
| DB_PORT | | 3131 | integer   
| BASE_URL | | http://localhost:8000/ | string  
| ADMIN_EMAIL | | admin@admin.com | string 
| ADMIN_PASSWORD | | openforme | string 
| EMAIL_CODE_DURATION_IN_MINUTES | | 15 | integer 
| ACCESS_TOKEN_DURATION_IN_MINUTES | | 60 | integer 
| REFRESH_TOKEN_DURATION_IN_MINUTES | | 600 | integer 
| PASSWORD_RESET_TOKEN_DURATION_IN_MINUTES | | 15 | integer 
| ACCOUNT_VERIFICATION_TOKEN_DURATION_IN_MINUTES | | 15 | integer 
| MAIL_USERNAME | | | string 
| MAIL_PASSWORD | | | string 
| MAIL_FROM | | | string 
| MAIL_PORT | | | string 
| MAIL_SERVER | | | string 
| MAIL_FROM_NAME | | | string 
| MAIL_TLS |  boolean 
| MAIL_SSL | | false | boolean 
| USE_CREDENTIALS |  boolean 
| VALIDATE_CERTS |  boolean 
| DEFAULT_MAIL_SUBJECT | | | string 





For more info on Fastapi: [Click here](https://fastapi.tiangolo.com/)
