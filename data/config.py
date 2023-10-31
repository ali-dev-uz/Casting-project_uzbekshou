from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
CHECKER_ADMIN = env.list("CHECKER_ADMIN")  # adminlar ro'yxati
SEND_CHANNELS = env.list("SEND_CHANNELS")  # adminlar ro'yxati
PAYME_ID = env.int("PAYME_ID")  # adminlar ro'yxati
PAY_USERS = env.int("PAY_USERS")  # adminlar ro'yxati
IP = env.str("IP")  # Xosting ip manzili
DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
