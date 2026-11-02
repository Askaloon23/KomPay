from database.database import get_connection

def initialize():
    conn = get_connection()
    cur = conn.cursor()

    # Роли
    cur.execute("""
    CREATE TABLE IF NOT EXISTS roles (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    )
    """)

    # Пользователи
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        address TEXT,
        role_id INTEGER NOT NULL,
        FOREIGN KEY (role_id) REFERENCES roles(id)
    )
    """)

    # Услуги
    cur.execute("""
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        unit TEXT,
        tariff REAL NOT NULL
    )
    """)

    # Начисления
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accruals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        service_id INTEGER NOT NULL,
        volume REAL,
        amount REAL NOT NULL,
        period TEXT NOT NULL,
        accountant_id INTEGER,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (service_id) REFERENCES services(id),
        FOREIGN KEY (accountant_id) REFERENCES users(id)
    )
    """)

    # Способы оплаты
    cur.execute("""
    CREATE TABLE IF NOT EXISTS payment_methods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    # Платежи
    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        accrual_id INTEGER,
        amount REAL NOT NULL,
        payment_method_id INTEGER,
        cashier_id INTEGER,
        paid_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (accrual_id) REFERENCES accruals(id),
        FOREIGN KEY (payment_method_id) REFERENCES payment_methods(id),
        FOREIGN KEY (cashier_id) REFERENCES users(id)
    )
    """)

    # Начальные роли
    cur.execute("INSERT OR IGNORE INTO roles (id, name) VALUES (1, 'Бухгалтер')")
    cur.execute("INSERT OR IGNORE INTO roles (id, name) VALUES (2, 'Администратор')")
    cur.execute("INSERT OR IGNORE INTO roles (id, name) VALUES (3, 'Жилец')")

    # Способы оплаты
    cur.execute("INSERT OR IGNORE INTO payment_methods (id, name) VALUES (1, 'Наличные')")
    cur.execute("INSERT OR IGNORE INTO payment_methods (id, name) VALUES (2, 'Карта')")
    cur.execute("INSERT OR IGNORE INTO payment_methods (id, name) VALUES (3, 'Перевод')")

    # Тестовые услуги
    cur.execute("INSERT OR IGNORE INTO services (id, name, unit, tariff) VALUES (1, 'Холодная вода', 'м³', 35.5)")
    cur.execute("INSERT OR IGNORE INTO services (id, name, unit, tariff) VALUES (2, 'Горячая вода', 'м³', 180.0)")
    cur.execute("INSERT OR IGNORE INTO services (id, name, unit, tariff) VALUES (3, 'Электричество', 'кВт·ч', 5.5)")
    cur.execute("INSERT OR IGNORE INTO services (id, name, unit, tariff) VALUES (4, 'Отопление', 'Гкал', 2500.0)")

    # Создаём администратора по умолчанию (логин: admin, пароль: admin)
    cur.execute("SELECT id FROM users WHERE login = 'admin'")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (login, password, full_name, address, role_id) VALUES (?, ?, ?, ?, ?)",
            ("admin", "admin", "Администратор Системы", "Офис", 2)
        )

    # Создаём бухгалтера по умолчанию (логин: buh, пароль: buh)
    cur.execute("SELECT id FROM users WHERE login = 'buh'")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (login, password, full_name, address, role_id) VALUES (?, ?, ?, ?, ?)",
            ("buh", "buh", "Иванова Мария Петровна", "Офис", 1)
        )

    conn.commit()
    conn.close()
    print("База данных успешно инициализирована.")
