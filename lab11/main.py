import psycopg2
import csv

class connection:
    def __init__(self, config):
        self.conn = psycopg2.connect(**config)
        print('Connected to the PostgreSQL server.')
        self.config = config

    def insert_contact(self, name, phone):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO contacts (contact_name, phone) VALUES (%s, %s)",
                (name, phone)
            )
            self.conn.commit()
            print("Контакт успешно добавлен.")
        except psycopg2.Error as e:
            print(f"Ошибка при добавлении контакта: {e}")

    def update_contact(self, contact_id, new_contact_name=None, new_phone=None):
        cur = self.conn.cursor()
        updates = []
        if new_contact_name:
            updates.append(f"contact_name = '{new_contact_name}'")
        if new_phone:
            updates.append(f"phone = '{new_phone}'")
        if updates:
            set_clause = ", ".join(updates)
            query = f"UPDATE contacts SET {set_clause} WHERE contact_id = %s"
            cur.execute(query, (contact_id,))
            self.conn.commit()
            print("Контакт успешно обновлен.")
        else:
            print("Нечего обновлять.")

    def get_contacts(self, filter_criteria=None):
        cur = self.conn.cursor()
        query = f"SELECT * FROM contacts"
        if filter_criteria:
            where_clauses = []
            for key, value in filter_criteria.items():
                where_clauses.append(f"{key} LIKE '{value}'")
            query += " WHERE " + " AND ".join(where_clauses)
        cur.execute(query)
        return cur.fetchall()

    def print(self, contacts=None):
        if contacts is None:
            contacts = self.get_contacts()
        print('contact_id', 'contact_name', 'phone')
        for c in contacts:
            print(*c)

    def insert_from_csv(self, csv_filename: str):
        with open(csv_filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                self.insert_contact(*row)
        self.conn.commit()

    def delete_contact(self, name):
        cur = self.conn.cursor()
        query = f"DELETE FROM contacts WHERE contact_name = %s"
        cur.execute(query, (name,))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def insert_from_console(self):
        print("\c to cancel")
        name, phone = input("enter name:"), input("enter phone:")
        if not ('\c' in (name, phone)):
            self.insert_contact(name, phone)
        else:
            print('canceled')



    def find_contacts_by_pattern(self, pattern):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM find_contacts(%s);", (pattern,))
        return cur.fetchall()

    def insert_or_update(self, name, phone):
        cur = self.conn.cursor()
        cur.execute("CALL insert_or_update_user(%s, %s);", (name, phone))
        self.conn.commit()

    def insert_many_users(self, user_list):
        cur = self.conn.cursor()
        pg_array = [[name, phone] for name, phone in user_list]
        cur.execute("CALL insert_many_users(%s, %s);", (pg_array, None))
        self.conn.commit()

    def get_contacts_paginated(self, limit, offset):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
        return cur.fetchall()

    def delete_by_name_or_phone(self, name=None, phone=None):
        cur = self.conn.cursor()
        cur.execute("CALL delete_by_name_or_phone(%s, %s);", (name, phone))
        self.conn.commit()


config = {
    'host': 'localhost',
    'database': 'phonebook',
    'user': 'postgres',
    'password': '12345678'
}





c = connection(config)
c.insert_or_update('John', '555-55-55')
c.print()
c.close()

c = connection(config)
results = c.find_contacts_by_pattern("Ali")
c.print(results)
c.close()

c = connection(config)
c.insert_or_update("Alice", "123-45-67")
c.print()
c.close()

c = connection(config)
user_list = [
    ["Ivan", "777-12-34"],
    ["Sara", "1234567890"],
    ["Oleg", "bad-number"]
]
c.insert_many_users(user_list) 
c.print()
c.close()

c = connection(config)
page1 = c.get_contacts_paginated(2, 0)
page2 = c.get_contacts_paginated(2, 2)
print("Page 1:")
c.print(page1)
print("Page 2:")
c.print(page2)
c.close()