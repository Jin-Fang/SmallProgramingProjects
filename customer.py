
class Customer:
    """A Customer.

    This class represents a customer in the simulation. Each customer will
    enter the simulation at _entry_time, will wait at most _patience turns.
    The restaurant need _prepare_time turns to prepare this customer order,
    and will receive _profit if can serve this customer on time.
    
    Your main task is to implement the remaining methods.
    """

    # === Private Attributes ===
    

    def __init__(self, customer_info):
        """Initialize a new Customer class
        
        :param customer_info: a string containing a customer's entry turn, unique
        id, profit, serving time, and max waiting time.
        :type: str
        
        >>> a = Customer('1 23215 13.00 4 8')
        >>> a.customer_info
        ['1', '23215', '13.00', '4', '8']
        >>> b = Customer('1 58923 5.99 6 9')
        >>> b.customer_info
        ['1', '58923', '5.99', '6', '9']
        """
        self.customer_info = customer_info.split()


    def id(self):
        """get the unique customer id from Customer self
        
        :return: the unique customer id
        :rtype: int
        
        >>> a = Customer('1 23215 13.00 4 8')
        >>> b = Customer('1 58923 5.99 6 9')
        >>> a.id()
        23215
        >>> b.id()
        58923
        """
        return int(self.customer_info[1])
        
    def entry_turn(self):
        """get the customer's entry turn from Customer self
        
        :return: the customer's entry turn
        :rtype: int
        
        >>> a = Customer('1 23215 13.00 4 8')
        >>> b = Customer('1 58923 5.99 6 9')
        >>> a.entry_turn()
        1
        >>> b.entry_turn()
        1
        """
        return int(self.customer_info[0])
    
    def patience(self):
        """get the customer's maximum waiting time from Customer self
        
        :return: the customer's maximum waiting time
        :rtype: int
        
        >>> a = Customer('1 23215 13.00 4 8')
        >>> b = Customer('1 58923 5.99 6 9')
        >>> a.patience()
        8
        >>> b.patience()
        9
        """
        
        return int(self.customer_info[4])
    
    def profit(self):
        """get the profit that the customr can bring from Customer self
        
        :return: the profit that the customr can bring
        :rtype: float
        
        >>> a = Customer('1 23215 13.00 4 8')
        >>> b = Customer('1 58923 5.99 6 9')
        >>> a.profit()
        13.0
        >>> b.profit()
        5.99
        """
        return float(self.customer_info[2])
    
    def serve_time(self):
        """get the customer's serving time from Customer self
        
        :return: the customer's serving time
        :rtype: int
        
        >>> a = Customer('1 23215 13.00 4 8')
        >>> b = Customer('1 58923 5.99 6 9')
        >>> a.serve_time()
        4
        >>> b.serve_time()
        6
        """
        return int(self.customer_info[3])
        
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    

