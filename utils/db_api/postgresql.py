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
        species VARCHAR(50) NULL
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
                       instagram, breast_size, waist_size, footless_size, species):
        sql = "INSERT INTO users (telegram_id, language_db, name_db, city, nationality, birthday, age, height_length, hair_color, eye_color, dress_size, footwear_size, email, phone_number, telegram, facebook, instagram, breast_size, waist_size, footless_size, species) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21) returning *"
        return await self.execute(sql, telegram_id, language_db, name_db, city, nationality, birthday, age,
                                  height_length,
                                  hair_color, eye_color, dress_size, footwear_size, email, phone_number, telegram,
                                  facebook,
                                  instagram, breast_size, waist_size, footless_size, species, fetchrow=True)

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

    async def update_user_answers(self, Answers, Chat_id):
        sql = "UPDATE users SET Answers=$1 WHERE Chat_id=$2"
        return await self.execute(sql, Answers, Chat_id, execute=True)

    async def update_user_secret(self, secret, Telegram_id):
        sql = "UPDATE users SET secret=$1 WHERE Telegram_id=$2"
        return await self.execute(sql, secret, Telegram_id, execute=True)

    async def count_users_one(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

    async def update_user_ammount(self, Ammaount, Telegram_id):
        sql = "UPDATE users SET Ammaount=$1 WHERE Telegram_id=$2"
        return await self.execute(sql, Ammaount, Telegram_id, execute=True)

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
