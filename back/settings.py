import os


DB_HOST = os.getenv("DB_HOST", "database-1.csqwyiwvwe6r.eu-central-1.rds.amazonaws.com")
DB_PASS = os.getenv("DB_PASS", "0Password")
DB_USER = os.getenv("DB_USER", "postgres")
DB_SCHEME = os.getenv("DB_SCHEME", "postgres")
