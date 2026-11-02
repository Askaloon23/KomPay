from repositories.base import BaseRepository

class UserRoleRepository(BaseRepository): table='user_roles'; pk='user_role_id'
class ServiceRepository(BaseRepository): table='services'; pk='service_id'
class PaymentMethodRepository(BaseRepository): table='payment_methods'; pk='method_id'
class UserRepository(BaseRepository): table='users'; pk='user_id'
class AccrualRepository(BaseRepository): table='accruals'; pk='accrual_id'
class PaymentRepository(BaseRepository): table='payments'; pk='payment_id'
class ReceiptRepository(BaseRepository): table='receipts'; pk='receipt_id'

roles = UserRoleRepository(); services = ServiceRepository(); methods = PaymentMethodRepository()
users = UserRepository(); accruals = AccrualRepository(); payments = PaymentRepository(); receipts = ReceiptRepository()
