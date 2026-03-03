import firebase_admin
from firebase_admin import credentials, db
from config.env_variables import firebase_sdk, database_url


cred = credentials.Certificate(firebase_sdk)
firebase_admin.initialize_app(
    cred,
    {
        'databaseURL': database_url
    })

ref_users = db.reference('/users')
ref_roles = db.reference('/roles')
    