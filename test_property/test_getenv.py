from dotenv import load_dotenv
import os
load_dotenv()

key_value = os.getenv('GOOGLE_CSE_ID')
print(key_value)