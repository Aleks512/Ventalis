from pytest_factoryboy import register

from .factories import NewUserFactory, ConsultantFactory, CustomerFactory, OrderItemFactory

register(NewUserFactory) # access with 'new_user_factory'
register(ConsultantFactory) # access with 'consultant_factory'
register(CustomerFactory) # access with 'customer_factory'
register(OrderItemFactory) # access with 'order_item_factory'
