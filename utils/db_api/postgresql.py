from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:

                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
        telegram_id BIGINT NOT NULL UNIQUE,
        language_db VARCHAR(10) NULL,
        name_db VARCHAR(100) NULL,
        city VARCHAR(100) NULL,
        nationality VARCHAR(60) NULL,
        birthday VARCHAR(30) NULL,
        age BIGINT NULL,
        height_length VARCHAR(50) NULL,
        hair_color VARCHAR(60) NULL,
        eye_color VARCHAR(60) NULL,
        dress_size VARCHAR(200) NULL,
        footwear_size VARCHAR(100) NULL,
        email VARCHAR(100) NULL,
        phone_number VARCHAR(30) NULL,
        telegram VARCHAR(100) NULL,
        facebook VARCHAR(100) NULL,
        instagram VARCHAR(100) NULL,
        breast_size VARCHAR(10) NULL,
        waist_size VARCHAR(10) NULL,
        footless_size VARCHAR(10) NULL,
        species VARCHAR(50) NULL,
        gender VARCHAR(50) NULL,
        photo VARCHAR(1000) NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, telegram_id, language_db, name_db, city, nationality, birthday, age, height_length,
                       hair_color, eye_color, dress_size, footwear_size, email, phone_number, telegram, facebook,
                       instagram, breast_size, waist_size, footless_size, species, gender, photo):
        sql = "INSERT INTO users (telegram_id, language_db, name_db, city, nationality, birthday, age, height_length, hair_color, eye_color, dress_size, footwear_size, email, phone_number, telegram, facebook, instagram, breast_size, waist_size, footless_size, species, gender, photo) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23) returning *"
        return await self.execute(sql, telegram_id, language_db, name_db, city, nationality, birthday, age,
                                  height_length,
                                  hair_color, eye_color, dress_size, footwear_size, email, phone_number, telegram,
                                  facebook,
                                  instagram, breast_size, waist_size, footless_size, species, gender, photo,
                                  fetchrow=True)

    async def select_users_one(self, telegram_id):
        sql = "SELECT * FROM users WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users"
        return await self.execute(sql, fetchval=True)

    async def update_language_db(self, language_db, telegram_id):
        sql = "UPDATE users SET language_db=$1 WHERE telegram_id=$2"
        return await self.execute(sql, language_db, telegram_id, execute=True)

    async def update_species(self, species, telegram_id):
        sql = "UPDATE users SET species=$1 WHERE telegram_id=$2"
        return await self.execute(sql, species, telegram_id, execute=True)

    async def update_all(self, name_db, city, nationality, birthday, age, height_length,
                         hair_color, eye_color, dress_size, footwear_size, email, phone_number, telegram, facebook,
                         instagram, breast_size, waist_size, footless_size, gender, telegram_id):
        sql = ("UPDATE users SET name_db=$1, city=$2, nationality=$3, birthday=$4, age=$5, height_length=$6, "
               "hair_color=$7, "
               "eye_color=$8, dress_size=$9, footwear_size=$10, email=$11, phone_number=$12, telegram=$13, facebook=$14,"
               "instagram=$15, breast_size=$16,"
               "waist_size=$17, footless_size=$18, gender=$19 WHERE telegram_id=$20")
        return await self.execute(sql, name_db, city, nationality, birthday, age,
                                  height_length,
                                  hair_color, eye_color, dress_size, footwear_size, email, phone_number, telegram,
                                  facebook,
                                  instagram, breast_size, waist_size, footless_size, gender, telegram_id, execute=True)

    async def update_photo(self, photo, telegram_id):
        sql = "UPDATE users SET photo=$1 WHERE telegram_id=$2"
        return await self.execute(sql, photo, telegram_id, execute=True)

    async def count_users_one(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

    async def update_user_photo(self, photo, telegram_id):
        sql = "UPDATE users SET photo=$1 WHERE telegram_id=$2"
        return await self.execute(sql, photo, telegram_id, execute=True)

    async def update_user_lavarge(self, Leverage, Telegram_id):
        sql = "UPDATE users SET Leverage=$1 WHERE Telegram_id=$2"
        return await self.execute(sql, Leverage, Telegram_id, execute=True)

    async def update_user_status(self, Ex_status, Telegram_id):
        sql = "UPDATE users SET Ex_status=$1 WHERE Telegram_id=$2"
        return await self.execute(sql, Ex_status, Telegram_id, execute=True)

    async def delete_users(self, Chat_id):
        sql = "DELETE FROM users WHERE Chat_id=$1"
        return await self.execute(sql, Chat_id, fetchrow=True)

    async def drop_users(self):
        await self.execute("DROP TABLE users", execute=True)

    async def create_data_static(self):
        sql = """
        CREATE TABLE IF NOT EXISTS data_stat (
        data_id BIGINT NOT NULL UNIQUE,
        monthly BIGINT NOT NULL,
        days BIGINT NOT NULL,
        weekly BIGINT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args2(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_data(self, data_id, monthly, days, weekly):
        sql = "INSERT INTO data_stat (data_id, monthly, days, weekly) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, data_id, monthly, days, weekly, fetchrow=True)

    async def update_day(self, days, data_id):
        sql = "UPDATE data_stat SET days=$1 WHERE data_id=$2"
        return await self.execute(sql, days, data_id, execute=True)

    async def update_monthly(self, monthly, data_id):
        sql = "UPDATE data_stat SET monthly=$1 WHERE data_id=$2"
        return await self.execute(sql, monthly, data_id, execute=True)

    async def update_weekly(self, weekly, data_id):
        sql = "UPDATE data_stat SET weekly=$1 WHERE data_id=$2"
        return await self.execute(sql, weekly, data_id, execute=True)

    async def select_static_one(self, data_id):
        sql = "SELECT * FROM data_stat WHERE data_id=$1"
        return await self.execute(sql, data_id, fetchrow=True)

    async def drop_static(self):
        await self.execute("DROP TABLE data_stat", execute=True)

    async def create_data_message(self):
        sql = """
        CREATE TABLE IF NOT EXISTS message (
        message_id BIGINT NOT NULL UNIQUE,
        telegram_id BIGINT NOT NULL,
        photo_id VARCHAR(1000) NULL,
        chat_id BIGINT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args3(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_data_message(self, message_id, telegram_id, photo_id, chat_id):
        sql = "INSERT INTO message (message_id, telegram_id, photo_id, chat_id) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, message_id, telegram_id, photo_id, chat_id, fetchrow=True)

    async def select_message_data(self, message_id):
        sql = "SELECT * FROM message WHERE message_id=$1"
        return await self.execute(sql, message_id, fetchrow=True)

    async def select_all_data(self, telegram_id):
        sql = "SELECT * FROM message WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetch=True)

    async def delete_data(self, telegram_id):
        sql = "DELETE FROM message WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetch=True)

    async def drop_data(self):
        await self.execute("DROP TABLE message", execute=True)

    async def create_data_pay_message(self):
        sql = """
        CREATE TABLE IF NOT EXISTS message_pay (
        message_id BIGINT NOT NULL UNIQUE,
        telegram_id BIGINT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args4(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_data_message_pay(self, message_id, telegram_id):
        sql = "INSERT INTO message_pay (message_id, telegram_id) VALUES($1, $2) returning *"
        return await self.execute(sql, message_id, telegram_id, fetchrow=True)

    async def select_message_data_pay(self, message_id):
        sql = "SELECT * FROM message_pay WHERE message_id=$1"
        return await self.execute(sql, message_id, fetchrow=True)

    async def delete_data_pay(self, telegram_id):
        sql = "DELETE FROM message_pay WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetch=True)

    async def drop_data_pay(self):
        await self.execute("DROP TABLE message_pay", execute=True)
