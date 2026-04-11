from uuid import uuid4
from pathlib import Path
from yaml import safe_load, YAMLError
from asyncpg import connect, Connection

# mock data
organizers_data = [
    {
        'id': uuid4().hex,
        'username': 'mafia',
        'password_hash': '123',
        'full_name': 'Зубенко Михаил Петрович',
        'is_admin': True
    },
    {
        'id': uuid4().hex,
        'username': 'kolbasa',
        'password_hash': '312',
        'full_name': 'Данил Колбасенко',
        'is_admin': False
    },
]
    
timeslots_data = [
    {'id': uuid4().hex, 'startt': '2026-06-01 10:00', 'endt': '2026-06-01 11:00', 'slotcnt': 3},
    {'id': uuid4().hex, 'startt': '2026-06-01 11:00', 'endt': '2026-06-01 12:00', 'slotcnt': 5},
]

activists_data = [
    {
        'id': uuid4().hex, 
        'username': 'vaspup', 
        'password_hash': 'pup', 
        'full_name': 'Василий Пупкин', 
        'sex': 'male', 
        'phone': '+79991234567',
        'department': 'smm', 
        'timeslotid': timeslots_data[0]['id']
     },
    {
        'id': uuid4().hex, 
        'username': 'peyta', 
        'password_hash': 'pet', 
        'full_name': 'Петрова Петра Ивановна', 
        'sex': 'female', 
        'phone': '+78005553535', 
        'department': 'cod', 
        'timeslotid': timeslots_data[1]['id']
     }
]

sessions_data = [
    {
        'id': uuid4().hex,
        'join_number': 1234,
        'startt': '2026-06-01 10:00',
        'endt': '2026-06-01 11:00',
        'created_by': organizers_data[0]['id']
    },
    {
        'id': uuid4().hex,
        'join_number': 4312,
        'startt': '2026-06-01 11:00',
        'endt': None,
        'created_by': organizers_data[0]['id']
    }
]

assessment_data = [
    {
        'id': uuid4().hex,
        'activistid': activists_data[0]['id'],
        'organizerid': organizers_data[0]['id'],
        'sessionid': sessions_data[0]['id'],
        'logic': 1,
        'charm': 2,
        'speech': 3,
        'resourcefulness': 4,
        'stressresilience': 3,
        'worthy': True,
        'comment': 'Хорошо',
    },
    {
        'id': uuid4().hex,
        'activistid': activists_data[0]['id'],
        'organizerid': organizers_data[1]['id'],
        'sessionid': sessions_data[0]['id'],
        'logic': 4,
        'charm': 5,
        'speech': 4,
        'resourcefulness': 4,
        'stressresilience': 4,
        'worthy': False,
        'comment': 'Плохо',
    },
    {
        'id': uuid4().hex,
        'activistid': activists_data[1]['id'],
        'organizerid': organizers_data[0]['id'],
        'sessionid': sessions_data[1]['id'],
        'logic': 2,
        'charm': 1,
        'speech': 3,
        'resourcefulness': 3,
        'stressresilience': 3,
        'worthy': True,
        'comment': 'Норм',
    }
]

sa_data = [
    {'id': uuid4().hex, 'sessionid': sessions_data[0]['id'], 'activistid': activists_data[0]['id']},
    {'id': uuid4().hex, 'sessionid': sessions_data[1]['id'], 'activistid': activists_data[1]['id']},
]

so_data = [
    {'id': uuid4().hex, 'sessionid': sessions_data[0]['id'], 'organizerid': organizers_data[0]['id']},
    {'id': uuid4().hex, 'sessionid': sessions_data[0]['id'], 'organizerid': organizers_data[1]['id']},
    {'id': uuid4().hex, 'sessionid': sessions_data[1]['id'], 'organizerid': organizers_data[0]['id']},
    {'id': uuid4().hex, 'sessionid': sessions_data[1]['id'], 'organizerid': organizers_data[1]['id']},
]


def load_config():
    config_path = Path(__file__).parent.parent / 'config/app.yaml'
    with open(config_path, 'r') as f:
        try:
            return safe_load(f)
        except YAMLError as e:
            print(f"Error parsing YAML: {e}")
            return


async def create_rows(conn: Connection, table: str, rows: list[dict]):
    columns = ', '.join(rows[0].keys())
    values = ', '.join(["'{}'" for _ in rows[0]]) 
    values = f" ({values}),"

    query = f"INSERT INTO {table} ({columns}) VALUES"
    for row in rows:
        query += values.format(*row.values()).replace("'None'", 'NULL').replace(
            "'True'", "true").replace("'False'", 'false')
    query = query[:-1] + ';'

    await conn.execute(query)
    

async def main():
    config = load_config()
    if config is None:
        return
    database_config = config['database']
    
    try:
        conn = await connect(
            user=database_config['user'],
            password=database_config['password'],
            database=database_config['database'],
            host=database_config['host'],
            port=database_config['port'],
        )
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return
    
    async with conn.transaction():
        try:
            await create_rows(conn, 'organizers', organizers_data)
            await create_rows(conn, 'timeslots', timeslots_data)
            await create_rows(conn, 'activists', activists_data)
            await create_rows(conn, 'sessions', sessions_data)
            await create_rows(conn, 'assessments', assessment_data)
            await create_rows(conn, 'sessions_activists', sa_data)
            await create_rows(conn, 'sessions_organizers', so_data)
        except Exception as e:
            print(f"Error creating mock data. Transaction will be rolled back. Error: {e}")
        else:
            print('Mock data created')
    
    await conn.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
