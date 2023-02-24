import pyodbc

class AccessDB:
    def __init__(self, db_file_path):
        self.db_file_path = db_file_path
        self.conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + db_file_path)
    
    def add_record(self, table_name, values_dict):
        columns = ', '.join(values_dict.keys())
        placeholders = ', '.join('?' * len(values_dict))
        values = tuple(values_dict.values())
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.conn.execute(sql, values)
        self.conn.commit()

    def add_record_no_id(self, table_name, values_dict):
        columns = ', '.join(values_dict.keys())
        placeholders = ', '.join('?' * len(values_dict))
        values = tuple(values_dict.values())
        cursor = self.conn.execute(f"SELECT MAX(code) FROM {table_name}")
        max_code = cursor.fetchone()[0] or 0
        values_dict["code"] = max_code + 1
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.conn.execute(sql, values)
        self.conn.commit()
    
    def find_record(self, table_name, column_name, value):
        sql = f"SELECT * FROM {table_name} WHERE {column_name} = ?"
        cursor = self.conn.execute(sql, value)
        row = cursor.fetchone()
        return row
    
    def get_table(self, table_name, filter_str=None):
        if filter_str:
            sql = f"SELECT * FROM {table_name} WHERE {filter_str}"
        else:
            sql = f"SELECT * FROM {table_name}"
        cursor = self.conn.execute(sql)
        rows = cursor.fetchall()
        return rows
    
    def get_colums_from_table(self, table_name, columns=None, filter_str=None):
        if columns is None:
            columns_str = "*"
        else:
            columns_str = ", ".join(columns)
        if filter_str:
            sql = f"SELECT {columns_str} FROM {table_name} WHERE {filter_str}"
        else:
            sql = f"SELECT {columns_str} FROM {table_name}"
        cursor = self.conn.execute(sql)
        rows = cursor.fetchall()
        return rows

    def update_record(self, table_name, column_name, value, new_values_dict):
        set_str = ', '.join([f"{key} = ?" for key in new_values_dict.keys()])
        values = tuple(new_values_dict.values())
        sql = f"UPDATE {table_name} SET {set_str} WHERE {column_name} = ?"
        values = values + (value,)
        self.conn.execute(sql, values)
        self.conn.commit()
    
    def delete_record(self, table_name, column_name, value):
        sql = f"DELETE FROM {table_name} WHERE {column_name} = ?"
        self.conn.execute(sql, value)
        self.conn.commit()
