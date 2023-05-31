# PROJECT DESCRIPTION

## Ready to setup the project:
    git clone https://github.com/Catalyst-OTU/Smart_Conference_App.git


## Installing Packages
- Run the following commad
    > pip install -r app/requirements.txt



## CREATION AND MIGRATION OF DATABASE
>  Create a database name: **smart_conference_app**


- Database Migration and Data Seeding
Run the following command
    - python app/migrate.py


## RUNNING OR STARTING APPLICATON
- Running FastAPI Service 
    - uvicorn app.main:app --reload

    - OR

    - python run.py






Setup environment variables; allowed environment variables `KEYWORDS`=`VALUES`:

| KEYWORDS | VALUES | DEFAULT VALUE | VALUE TYPE | IS REQUIRED | 
| :------------ | :---------------------: | :------------------: | :------------------: | :------------------: |
| DB_TYPE | | Mysql | string | true |
| DB_NAME | | smart_conference_app | string | true |
| DB_USER | | root | string | true |
| DB_PASSWORD | |  | string | true |
| DB_PORT | | 3306 | integer | true |  
| BASE_URL | | http://localhost:8000/ | string | true | 
| ADMIN_EMAIL | | admin@admin.com | string | true |
| ADMIN_PASSWORD | | openforme | string | true |
| EMAIL_CODE_DURATION_IN_MINUTES | | 15 | integer | true |
| ACCESS_TOKEN_DURATION_IN_MINUTES | | 60 | integer | true |
| REFRESH_TOKEN_DURATION_IN_MINUTES | | 600 | integer | true |
| PASSWORD_RESET_TOKEN_DURATION_IN_MINUTES | | 15 | integer | true |
| ACCOUNT_VERIFICATION_TOKEN_DURATION_IN_MINUTES | | 15 | integer | true |
| MAIL_USERNAME | | | string | true |
| MAIL_PASSWORD | | | string | true |
| MAIL_FROM | | | string | true |
| MAIL_PORT | | | string | true |
| MAIL_SERVER | | | string | true |
| MAIL_FROM_NAME | | | string | true |
| MAIL_TLS | | true | boolean | true |
| MAIL_SSL | | false | boolean | true |
| USE_CREDENTIALS | | true | boolean | true |
| VALIDATE_CERTS | | true | boolean | true |
| DEFAULT_MAIL_SUBJECT | | | string | true |





For more info on Fastapi: [Click here](https://fastapi.tiangolo.com/)
