from db.mysql import MySQL
import os
mysql = MySQL(host='localhost', username='root', password='root', database='sakila', port='3306')

def verific_databases():
    result = mysql.query("select TABLE_SCHEMA from information_schema.tables where TABLE_SCHEMA not in ('information_schema','performance_schema', 'sys','mysql') group by TABLE_SCHEMA")
    return result

database = verific_databases()

diretorio = fr'C:\Users\Rafael Carvalho\Desktop\Automatizacao'

ambientes = ['0 - DEVELOPER', '2 - HOMOLOGATION', '5 - PRODUCTION', '6 - DECLINEDS','7 - EMERGENCY','8 - ROLLBACK']
tables_actions = ['0 - ALTER TABLE', '1 - CREATE TABLE', '2 - DROP TABLE','3 - ALTER FUNCTION','4 - CREATE FUNCITON','5 - ALTER VIEW','6 - CREATE VIEW','7 - ALTER PROCEDURE','8 - CREATE PROCEDURE','9 - TRUNCATE TABLE']
table_mody = ['ADD COLUMN', 'ADD COMMENT','DROP COLUMN', 'MODIFY COLUMN']
table_increments = ['FOREING KEY', 'INDEX']
positions_scripts = [ '1 - REVIEW HOMOLOGATION','3 - REVIEW PRODUCTION','4 - FOR PRODUCTION',]
tipy_object = ['TABLE', 'VIEW', 'FUNCTION', 'PROCEDURE', 'EVENT', 'TRIGGER', 'INDEX']


def folder_is_exists(diretorio):
    if not os.path.exists(diretorio):
        os.mkdir(diretorio)
    return diretorio

for folder_ambientes in ambientes:
    folder_ambientes = f'{diretorio}\{folder_ambientes}'
    folder_is_exists(folder_ambientes)
    ambiente = folder_ambientes
    if folder_ambientes.find('DEVELOPER') > -1 or folder_ambientes.find('HOMOLOGATION') > -1:
        for folder_action in tables_actions:
            folder = f'{folder_ambientes}\{folder_action}'
            folder_is_exists(folder)
            if folder.find('ALTER TABLE') > -1:
                for folder_mody in table_mody:
                    folder_1 = f'{folder}\{folder_mody}'
                    folder_is_exists(folder_1)
                    folder_1 = folder
            if folder.find('CREATE TABLE') > -1:
                for folder_increments in table_increments:
                    folder_1 = f'{folder}\{folder_increments}'
                    folder_is_exists(folder_1)
                    folder_1 = folder
    if folder_ambientes.find('PRODUCTION') > -1:
            for obj in tipy_object:
                folder = f'{folder_ambientes}\{obj}'
                folder_is_exists(folder)
    

for folder_status in positions_scripts:
    folder_status = f'{diretorio}\{folder_status}'
    folder_is_exists(folder_status)

def tables_struture(data):
    result = mysql.query(f"select TABLE_NAME from information_schema.tables where TABLE_SCHEMA = '{data}' and TABLE_TYPE = 'BASE TABLE';")
    return result

def view_struture(data):
    result = mysql.query(f"SELECT TABLE_NAME FROM information_schema.VIEWS WHERE TABLE_SCHEMA IN ('{data}');")
    return result

def trigges_struture(data):
    result = mysql.query(f"select TRIGGER_NAME from information_schema.TRIGGERS where TRIGGER_SCHEMA in ('{data}');")
    return result

def functions_struture(data):
    result = mysql.query(f"SELECT ROUTINE_NAME FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA IN ('{data}') AND ROUTINE_TYPE = 'FUNCTION';")
    return result

def procedures_struture(data):
    result = mysql.query(f"SELECT ROUTINE_NAME FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA IN ('{data}') AND ROUTINE_TYPE = 'PROCEDURE';")
    return result

def event_struture(data):
    result = mysql.query(f"SELECT EVENT_NAME FROM information_schema.EVENTS WHERE EVENT_SCHEMA IN ('{data}');")
    return result

def show_table(base,table):
    result = mysql.query(f"SHOW CREATE TABLE {base}.{table};")
    return result

def show_view(base,table):
    result = mysql.query(f"SHOW CREATE VIEW  {base}.{table};")
    return result

def show_function(base,table):
    result = mysql.query(f"SHOW CREATE FUNCTION  {base}.{table};")
    return result

def show_procdure(base,table):
    result = mysql.query(f"SHOW CREATE PROCEDURE {base}.{table};")
    return result

def show_trigger(base,table):
    result = mysql.query(f"SHOW CREATE TRIGGER  {base}.{table};")
    return result

def show_event(base,table):
    result = mysql.query(f"show create EVENT {base}.{table};")
    return result

for data in database:
    
    for amb in ambientes:
        folder_database = folder_is_exists(fr'{diretorio}\{amb}')
        table = tables_struture(data[0])
        for tab in table:
            if amb.find('5 - PRODUCTION') > -1:
                if not os.path.isfile(folder_database+f'\TABLE\{data[0]}'):
                   folder_table = f"{folder_database}\TABLE\{data[0]}"
                   folder_is_exists(folder_table)
                   file_table = open(f"{folder_table}\{tab[0]}.sql", 'w+')
                   create_table = show_table(data[0],tab[0])
                   for cre in create_table:
                       file_table.write(cre[1])
        views = view_struture(data[0])
        for view in views:
            if amb.find('5 - PRODUCTION') > -1:
                if not os.path.isfile(folder_database+f'\VIEW\{data[0]}'):
                    folder_view = f"{folder_database}\VIEW\{data[0]}"
                    folder_is_exists(folder_view)
                    file_view = open(f"{folder_view}\{view[0]}.sql", 'w+')
                    create_view = show_view(data[0],view[0])
                    for cre in create_view:
                       file_view.write(cre[1])
        function = functions_struture(data[0])
        for func in function:
            if amb.find('5 - PRODUCTION') > -1:
                if not os.path.isfile(folder_database+f'\FUNCTION\{data[0]}'):
                    folder_func = f"{folder_database}\FUNCTION\{data[0]}"
                    folder_is_exists(folder_func)
                    file_func = open(f"{folder_func}\{func[0]}.sql", 'w+')
                    create_func = show_function(data[0],func[0])
                    for cre in create_func:
                       file_func.write(cre[1])
        procedure = procedures_struture(data[0])
        for proc in procedure:
            if amb.find('5 - PRODUCTION') > -1:
                if not os.path.isfile(folder_database+f'\PROCEDURE\{data[0]}'):
                    folder_proc = f"{folder_database}\PROCEDURE\{data[0]}"
                    folder_is_exists(folder_proc)
                    file_proc = open(f"{folder_proc}\{proc[0]}.sql", 'w+')
                    create_proc = show_procdure(data[0],proc[0])
                    for cre in create_proc:
                       file_proc.write(cre[2])
        trigger = trigges_struture(data[0])
        for trig in trigger:
            if amb.find('5 - PRODUCTION') > -1:
                if not os.path.isfile(folder_database+f'\TRIGGER\{data[0]}'):
                    folder_trig = f"{folder_database}\TRIGGER\{data[0]}"
                    folder_is_exists(folder_trig)
                    file_trig = open(f"{folder_trig}\{trig[0]}.sql", 'w+')
                    create_trig = show_trigger(data[0],trig[0])
                    for cre in create_trig:
                       file_trig.write(cre[2])
        event = event_struture(data[0])
        for even in event:
            if amb.find('5 - PRODUCTION') > -1:
                if not os.path.isfile(folder_database+f'\EVENT\{data[0]}'):
                    folder_even = f"{folder_database}\EVENT\{data[0]}"
                    folder_is_exists(folder_even)
                    file_even = open(f"{folder_even}\{even[0]}.sql", 'w+')
                    create_even = show_event(data[0],even[0])
                    for cre in create_trig:
                       file_even.write(cre[2])



            
            
    

