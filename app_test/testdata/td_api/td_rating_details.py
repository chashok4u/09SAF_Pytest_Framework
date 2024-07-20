class Product_Details_Mexico(object):
    def __init__(self, product_reference=None, product_name=None, quantity=None, first_name=None, surname=None,
                 customer_type=None, state=None, city=None, address=None, street=None):
        self.product_reference = product_reference
        self.product_name = product_name
        self.quantity = quantity
        self.first_name = first_name
        self.surname = surname
        self.customer_type = customer_type
        self.state = state
        self.city = city
        self.address = address
        self.street = street


td_Product_Details_Mexico = [Product_Details_Mexico
                             (product_reference='', product_name='', quantity='',
                              first_name='', surname='',
                              customer_type='',
                              state='', city='', address='', street='')]
