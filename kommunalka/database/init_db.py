from database.connection import get_connection

SCHEMA = '''
CREATE TABLE IF NOT EXISTS user_roles (
 user_role_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS services (
 service_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE,
 unit TEXT NOT NULL, tariff NUMERIC NOT NULL CHECK(tariff >= 0)
);
CREATE TABLE IF NOT EXISTS payment_methods (
 method_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS users (
 user_id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT NOT NULL UNIQUE,
 password TEXT NOT NULL, full_name TEXT NOT NULL, address TEXT,
 user_role INTEGER NOT NULL REFERENCES user_roles(user_role_id)
);
CREATE TABLE IF NOT EXISTS accruals (
 accrual_id INTEGER PRIMARY KEY AUTOINCREMENT,
 resident_id INTEGER NOT NULL REFERENCES users(user_id),
 service_id INTEGER NOT NULL REFERENCES services(service_id),
 accountant_id INTEGER NOT NULL REFERENCES users(user_id),
 period TEXT NOT NULL, volume NUMERIC NOT NULL CHECK(volume >= 0),
 amount NUMERIC NOT NULL CHECK(amount >= 0)
);
CREATE TABLE IF NOT EXISTS payments (
 payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
 accrual_id INTEGER NOT NULL REFERENCES accruals(accrual_id),
 method_id INTEGER NOT NULL REFERENCES payment_methods(method_id),
 amount NUMERIC NOT NULL CHECK(amount > 0), payment_date TEXT NOT NULL,
 status TEXT NOT NULL DEFAULT 'confirmed'
);
CREATE TABLE IF NOT EXISTS receipts (
 receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
 payment_id INTEGER NOT NULL UNIQUE REFERENCES payments(payment_id),
 number TEXT NOT NULL UNIQUE, issue_date TEXT NOT NULL
);
'''

def initialize():
    with get_connection() as conn:
        conn.executescript(SCHEMA)
        # Роли и справочники создаются только в пустой базе; названия можно изменить в меню.
        if conn.execute('SELECT COUNT(*) FROM user_roles').fetchone()[0] == 0:
            conn.executemany('INSERT INTO user_roles(user_role_id, name) VALUES (?, ?)',
                             [(0, 'Жилец'), (1, 'Бухгалтер'), (2, 'Администратор')])
        if conn.execute('SELECT COUNT(*) FROM payment_methods').fetchone()[0] == 0:
            conn.executemany('INSERT INTO payment_methods(method_id, name) VALUES (?, ?)',
                             [(0, 'Банковская карта'), (1, 'Наличные'), (2, 'Онлайн-банк')])
        if conn.execute('SELECT COUNT(*) FROM services').fetchone()[0] == 0:
            conn.executemany('INSERT INTO services(service_id, name, unit, tariff) VALUES (?, ?, ?, ?)', [
                (0, 'Холодная вода', 'м³', 45), (1, 'Горячая вода', 'м³', 210),
                (2, 'Электроэнергия', 'кВт·ч', 5), (3, 'Отопление', 'м²', 1300)])

if __name__ == '__main__':
    initialize()
    print('База данных инициализирована.')
