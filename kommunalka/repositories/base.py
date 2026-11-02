from database.connection import get_connection

class BaseRepository:
    table = ''; pk = ''; fields = ()
    def _model(self, row):
        if row is None: return None
        from models.entities import UserRole, Service, PaymentMethod, User, Accrual, Payment, Receipt
        classes = {'user_roles': UserRole, 'services': Service, 'payment_methods': PaymentMethod,
                   'users': User, 'accruals': Accrual, 'payments': Payment, 'receipts': Receipt}
        return classes[self.table](**dict(row))
    def get_all(self):
        with get_connection() as c:
            rows = c.execute(f'SELECT * FROM {self.table} ORDER BY {self.pk}').fetchall()
            return [self._model(r) for r in rows]
    def get_by_id(self, item_id):
        with get_connection() as c:
            row = c.execute(f'SELECT * FROM {self.table} WHERE {self.pk}=?', (item_id,)).fetchone()
            return self._model(row)
    def create(self, **data):
        cols = ','.join(data); marks = ','.join('?' for _ in data)
        with get_connection() as c:
            cur = c.execute(f'INSERT INTO {self.table} ({cols}) VALUES ({marks})', tuple(data.values()))
            return cur.lastrowid
    def update(self, item_id, **data):
        if not data: return False
        sets = ','.join(f'{k}=?' for k in data)
        with get_connection() as c:
            cur = c.execute(f'UPDATE {self.table} SET {sets} WHERE {self.pk}=?', (*data.values(), item_id))
            return cur.rowcount > 0
    def delete(self, item_id):
        with get_connection() as c:
            cur = c.execute(f'DELETE FROM {self.table} WHERE {self.pk}=?', (item_id,))
            return cur.rowcount > 0
