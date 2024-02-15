from dotenv import load_dotenv
from os import environ

config_bbdd = {
  'host': environ.get('DB_HOST'),
  'user': environ.get('DB_USER'),
  'pass': environ.get('DB_PASS'),
  'database': environ.get('DB_DATABASE'),
  'port': environ.get('DB_PORT'),
}