from construct.AbstractVMServer import AbstractVMServer as AVMS
import asyncio, asyncpg, os
from dotenv import load_dotenv
from prettytable import PrettyTable

load_dotenv()
HOST = os.environ['DB_HOST']
USER = os.environ['DB_USER']
PASSWORD = os.environ['DB_PWD']
DATABASE = os.environ['DB_DATABASE']


class VMServer(AVMS):

    def __init__(self) -> None:
        self.vm_id = None

    async def connect(self, login: str, pwd: str, vm_id: int):
        print(f"args: ", login, pwd, vm_id)
        conn = await asyncpg.connect(user=USER, password=PASSWORD,
                                    database=DATABASE, host=HOST)
        
        q = '''SELECT * from virtual_machines where id = $1 and vm_pass = $2'''

        try:
            result = await conn.fetch(q, vm_id, pwd)
            print(result)
            if len(result)!= 0:
                q1 = '''UPDATE virtual_machines SET is_authored = true, vm_user = $1 where id = $2 RETURNING id'''
                res = await conn.fetchval(q1, login, vm_id)
                self.vm_id = res
                print(f"Welcome aboard VM: {res}")
            else:
                print("Your login or password is wrong. Try again!")
        except Exception as e:
            return {"error": e}
        finally:
            await conn.close()

    async def disconnect(self):
        if self.vm_id is None:
            print("Nothing to disconnect")
            return

        conn = await asyncpg.connect(user=USER, password=PASSWORD,
                                    database=DATABASE, host=HOST)
        
        q = '''UPDATE virtual_machines SET is_authored = false, vm_user = $2 where id = $1'''
        res = await conn.fetchval(q, self.vm_id, None)
        self.vm_id = None
        print("Succesfully disconnected!")
        

    async def create_vm(self, ram: int, cpu_cores: int, vinchester: list[int]):
        conn = await asyncpg.connect(user=USER, password=PASSWORD,
                                     database=DATABASE, host=HOST)

        print(ram, cpu_cores, vinchester)
        try:
            # Создаем ВМ
            async with conn.transaction():
                q1 = '''INSERT INTO virtual_machines (allocated_ram, allocated_cpu, is_connected) VALUES ($1, $2, true) RETURNING id'''
                vm_id = await conn.fetchval(q1, ram, cpu_cores)

                q2 = """INSERT INTO hard_disks (vm_id, disk_volume) VALUES ($1, $2)"""

                await conn.executemany(q2, [(vm_id, volume) for volume in vinchester])

        finally:
            # Закрываем соединение
            await conn.close()

    async def list_vm_authored(self):
        conn = await asyncpg.connect(user=USER, password=PASSWORD,
                                database=DATABASE, host=HOST)
        
        q = '''SELECT v.id, v.allocated_ram, v.allocated_cpu, array_agg(h.disk_volume) as hard_disks, vm_user
                FROM virtual_machines v
                LEFT JOIN hard_disks h ON h.vm_id = v.id
                WHERE v.is_authored = true
                GROUP BY v.id, v.allocated_ram, v.allocated_cpu;'''
        res = await conn.fetch(q)

        table = PrettyTable()
        table.field_names = ["VM ID", "RAM", "CPU Cores", "Hard Disks", "User"]

        for row in res:
            table.add_row([row['id'], row['allocated_ram'], row['allocated_cpu'], row['hard_disks'], row['vm_user']])

        print(table)

    async def list_vm_connected(self):
        conn = await asyncpg.connect(user=USER, password=PASSWORD,
                                database=DATABASE, host=HOST)
        
        q = '''SELECT v.id, v.allocated_ram, v.allocated_cpu, array_agg(h.disk_volume) as hard_disks
                FROM virtual_machines v
                LEFT JOIN hard_disks h ON h.vm_id = v.id
                WHERE v.is_connected = true
                GROUP BY v.id, v.allocated_ram, v.allocated_cpu;'''
        res = await conn.fetch(q)

        table = PrettyTable()
        table.field_names = ["VM ID", "RAM", "CPU Cores", "Hard Disks"]

        for row in res:
            table.add_row([row['id'], row['allocated_ram'], row['allocated_cpu'], row['hard_disks']])

        print(table)

    async def list_vm_all(self):
        conn = await asyncpg.connect(user=USER, password=PASSWORD,
                                database=DATABASE, host=HOST)
        
        q = '''SELECT v.id, v.allocated_ram, v.allocated_cpu, array_agg(h.disk_volume) as hard_disks, vm_user
                FROM virtual_machines v
                LEFT JOIN hard_disks h ON h.vm_id = v.id
                GROUP BY v.id, v.allocated_ram, v.allocated_cpu;'''
        res = await conn.fetch(q)

        table = PrettyTable()
        table.field_names = ["VM ID", "RAM", "CPU Cores", "Hard Disks", "User"]

        for row in res:
            table.add_row([row['id'], row['allocated_ram'], row['allocated_cpu'], row['hard_disks'], row['vm_user'] if row['vm_user'] else ""])

        print(table)