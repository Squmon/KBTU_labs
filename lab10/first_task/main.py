import psycopg2
import csv
def del_this_function():

    with open('temp_contacts.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['first_name', 'phone'])  # Заголовок
        writer.writerow(['Alice', '123-45-67'])
        writer.writerow(['Bob', '987-65-43'])
    quit()

'''
DROP TABLE contacts;
CREATE TABLE contacts(
	contact_id SERIAL NOT NULL,
	contact_name VARCHAR(100),
	phone VARCHAR(20),
	PRIMARY KEY(contact_id)
);
'''
        
class connection:
    def __init__(self, config):
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            self.conn = conn
        self.config = config

    def insert_contact(self, name, phone):
        if hasattr(self, 'conn'):
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
    
    def print(self, contacts = None):
        if contacts is None:
            contacts = self.get_contacts()
        print('contact_id', 'contact_name', 'phone')
        for c in contacts:
            print(*c)

    def insert_from_csv(self, csv_filename:str):
        with open(csv_filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                self.insert_contact(*row)
            self.conn.commit()

    def delete_contact(self, name):
        cur = self.conn.cursor()
        query = f"DELETE FROM contacts WHERE contact_name = %s"
        cur.execute(query, (name, ))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def insert_from_console(self):
        print("\c to cancel")
        name, phone = input("enter name:"), input("enter phone:")
        if not( '\c' in (name, phone)):
            self.insert_contact(name, phone)
        else:
            print('canceled')

config = {
    'host':'localhost',
    'database':'phonebook',
    'user':'postgres',
    'password':'12345678'
}
c = connection(config)
#c.insert_contact('Ellipsis', '77472006150')
#c.insert_from_csv("lab10/temp_contacts.csv")
#c.print()
#c.delete_contact('Ellipsis')
#c.insert_contact('cura', '111')
#c.insert_from_console()
#c.print(c.get_contacts({'contact_name':"B%"}))
c.print()
c.close()