from customer import Customer

class Restaurant(object):
    """A Restaurant.

    This class represents a restaurant in the simulation. This is the base
    class for different restaurant approaches. The main purpose of this
    class to define common interfaces for different approaches. If there
    are common tasks for all approaches that did not depend on a specific
    management style, they should be implemented here. Otherwise, they should
    be implemented in the subclasses.

    This class is abstract; subclasses must implement add_customer and
    process_turn functions.

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL approaches, and not just a particular
    approach.

    """

    # === Private Attributes ===
    #:param _wait_customer: a dictionary storing all waiting customer
    #:type _wait_cusotmer: dict
    #:param _current_serving: current serving customer
    #:type _current_serving: Customer
    #:param _current_due: record the exit turn of the customer
    #:type _current_due: int  
    #:param _total_profit: total profit of resaurant
    #:type _total_profit: float
    #:param _customer_served: number of customers have served
    #:type _customer_served: int
    #:param _impatience_turn: the turn when customers are about to leave if 
    #                         they are not served
    #:type _impatience_turn: int
    
    
    
    def __init__(self):
        """Initialize a new restaurant instance.
        """
        self._total_profit = 0
        self._customer_served = 0        
        self._wait_customer = {}
        self._current_serving = []
        self._current_due = 0
        self._impatience_turn = 0


    def add_customer(self, new_customer):
        """Add a new entering customer to the restaurant.

        :type new_customer: Customer
            The new customer that is entering the restaurant
        :rtype: None
        """
        raise NotImplementedError()
    
        
    def process_turn(self, current_turn):
        """Process the current_turn.

        This function will process the current turn. If the restaurant is not
        serving any customer now, and there are waiting customers, it should
        select one of them to serve.

        You can assume that all customers who entered the restaurant before or
        during this turn were already passed to the restaurant by simulator via
        calling the AddCustomer function.

        :type self: Restaurant
        :type current_turn: int
            The number of current turn
        :rtype: None
        """
        raise NotImplementedError()
        
        
    def remove_impatient_customer(self, current_turn):
        """remove all impatient customers from a collection of waiting customers

        :return: None
        :rtype: NoneType
        
        >>>a = Customer('1 23215 13.00 20 8')
        >>>b = Customer('2 58923 5.99 6 9')
        >>>c = PatApproach()
        >>>PatApproach.add_customer(c,a)
        >>>PatApproach.add_customer(c,b)
        >>>PatApproach.process_turn(c, 1)
        >>>PatApproach.remove_impatient_customer(c,3)
        >>>c._wait_customer
        {}
        """
        #remove impatient customers from wait_customer
        print('before remove:',self._wait_customer)
        if self._current_serving != []:
            temp = []
            for key in self._wait_customer:
                for customer in self._wait_customer[key]:
                    self._impatience_turn = customer.patience() + customer.entry_turn()
                    
                    if self._impatience_turn <= self._current_due:
                        self._wait_customer[key].remove(customer)
                        temp.append(key)
            for item in temp:
                if self._wait_customer[item] == []:
                    self._wait_customer.pop(item)  



    def write_report(self, report_file):
        """Write the final report of this restaurant approach in the report_file.

        :type self: Restaurant
        :type report_file: File
            This is an open file that this restaurant will write the report into.
        :rtype: None
        """
        template = 'Total profit: ${}\nCustomer served: {}\n'.format(self._total_profit, self._customer_served)
        report_file.write(template)
        


class PatApproach(Restaurant):
    """A Restaurant with Pat management style.

    This class represents a restaurant that uses the Pat management style,
    in which customers are served based on their arrival time. This class is
    a subclass of Restaurant and implements two functions: add_customer and
    process_turn.

    """
    
    def add_customer(self, new_customer):
        """Add a new entering customer to the restaurant.

        :type new_customer: Customer
            The new customer that is entering the restaurant
        :rtype: None

        >>>a = Customer('1 23215 13.00 4 8')
        >>>b = Customer('2 58923 5.99 6 9')
        >>>c = PatApproach()
        >>>PatApproach.add_customer(c,a)
        >>>c._wait_customer
        {1: [<customer.Customer instance at 0x10531a7e8>]}
        >>>PatApproach.add_customer(c,b)
        >>>c._wait_customer
        {1: [<customer.Customer instance at 0x10531a7e8>], 2: }
        """
        
        #the key of the dictionary is each customer's entry turn
        if new_customer.entry_turn() not in self._wait_customer:
            self._wait_customer[new_customer.entry_turn()] = [new_customer]
        else:
            self._wait_customer[new_customer.entry_turn()].append(new_customer)



    def process_turn(self, current_turn):
        """Process the current_turn.

        This function will process the current turn. If the restaurant is not
        serving any customer now, and there are waiting customers, it should
        select one of them to serve.

        You can assume that all customers who entered the restaurant before or
        during this turn were already passed to the restaurant by simulator via
        calling the AddCustomer function.

        :type self: Restaurant
        :type current_turn: int
            The number of current turn
        :rtype: None
        
        >>>a = Customer('1 23215 13.00 4 8')
        >>>b = Customer('2 58923 5.99 6 9')
        >>>c = PatApproach()
        >>>PatApproach.add_customer(c, a)
        >>>PatApproach.add_customer(c, b)
        >>>PatApproach.process_turn(c, 1)
        >>>c._current_serving
        [<customer.Customer instance at 0x10541ef80>]
        >>>c._wait_customer
        {2: [<customer.Customer instance at 0x10f9a1050>]}
        """
        #remove impatient customers from wait_customer
        Restaurant.remove_impatient_customer(self, current_turn)
        print('after remove:',self._wait_customer)
        #check if current turn is finished
        
        if self._current_due == current_turn:           
            self._current_serving.pop()
            
        #pick a new customer
        if not self._wait_customer == {} and self._current_serving == []:
            new_customer_picked = self._wait_customer[min(self._wait_customer.keys())][0]
            print('picking:', new_customer_picked)
            self._current_serving.append(new_customer_picked)
            self._customer_served += 1
            print('customer served:', self._customer_served)
            self._total_profit += self._current_serving[0].profit()
            print('profit:', self._total_profit)
            self._current_due = current_turn + self._current_serving[0].serve_time() 
            print('current due:', self._current_due)
        #delete picked customer
            temp_entry_turn = self._current_serving[0].entry_turn()
            self._wait_customer[temp_entry_turn].pop(0)
            if self._wait_customer[temp_entry_turn] == []:
                self._wait_customer.pop(temp_entry_turn)
        
    def write_report(self, report_file):
        """Write the final report of this restaurant approach in the report_file.
        
        extend write_report method of super class

        :type self: Restaurant
        :type report_file: File
            This is an open file that this restaurant will write the report into.
        :rtype: None
        """
        temp = "Result for the serving approach using Pat's suggestion:\n"
        report_file.write(temp)
        Restaurant.write_report(self, report_file)

class MatApproach(Restaurant):
    """A Restaurant with Mat management style.

    This class represents a restaurant that uses the Mat management style,
    in which customers are served based on their arrival time. This class is
    a subclass of Restaurant and implements two functions: add_customer and
    process_turn.

    """
    
    def add_customer(self, new_customer):
        """Add a new entering customer to the restaurant.

        :type new_customer: Customer
            The new customer that is entering the restaurant
        :rtype: None
        
        >>>a = Customer('1 23215 13.00 4 8')
        >>>b = Customer('2 58923 5.99 6 9')
        >>>c = MatApproach()
        >>>MatApproach.add_customer(c,a)
        >>>c._wait_customer
        {1: [<customer.Customer instance at 0x10531a7e8>]}
        >>>MatApproach.add_customer(c,b)
        >>>c._wait_customer
        {1: [<customer.Customer instance at 0x10531a7e8>], 2: }
        """
        if new_customer.entry_turn() not in self._wait_customer:
            self._wait_customer[new_customer.entry_turn()] = [new_customer]
        else:
            self._wait_customer[new_customer.entry_turn()].append(new_customer)

    def process_turn(self, current_turn):
        """Process the current_turn.

        This function will process the current turn. If the restaurant is not
        serving any customer now, and there are waiting customers, it should
        select one of them to serve.

        You can assume that all customers who entered the restaurant before or
        during this turn were already passed to the restaurant by simulator via
        calling the AddCustomer function.

        :type self: Restaurant
        :type current_turn: int
            The number of current turn
        :rtype: None
        
        >>>a = Customer('1 23215 13.00 4 8')
        >>>b = Customer('2 58923 5.99 6 9')
        >>>c = MatApproach()
        >>>MatApproach.add_customer(c, a)
        >>>MatApproach.add_customer(c, b)
        >>>MatApproach.process_turn(c, 1)
        >>>c._current_serving
        [<customer.Customer instance at 0x10541ef80>]
        >>>c._wait_customer
        {1: [<customer.Customer instance at 0x10f9a1050>]}
        """
        #remove impatient customers from wait_customer
        Restaurant.remove_impatient_customer(self, current_turn)
        print('after remove:',self._wait_customer)
        #check if current turn is finished
        
        if self._current_due == current_turn:
            self._current_serving.pop()
            
            
            
        #pick a new customer
        if not self._wait_customer == {} and self._current_serving == []:
            new_customer_picked = self._wait_customer[max(self._wait_customer.keys())][0]
            print('picking:', new_customer_picked)
            self._current_serving.append(new_customer_picked)
            self._total_profit += self._current_serving[0].profit()
            print('profit:', self._total_profit)
            self._customer_served += 1
            print('customer served:', self._customer_served)
            self._current_due = current_turn + self._current_serving[0].serve_time() 
            print('current due:', self._current_due)
        #delete picked customer
            temp_entry_turn = self._current_serving[0].entry_turn()
            self._wait_customer[temp_entry_turn].pop(0)
            if self._wait_customer[temp_entry_turn] == []:
                self._wait_customer.pop(temp_entry_turn)
        
    def write_report(self, report_file):
        """Write the final report of this restaurant approach in the report_file.
        
        extend write_report method of super class

        :type self: Restaurant
        :type report_file: File
            This is an open file that this restaurant will write the report into.
        :rtype: None
        """
        temp = "Result for the serving approach using Mat's suggestion:\n"
        report_file.write(temp)
        Restaurant.write_report(self, report_file)       
        
    
class MaxApproach(Restaurant):
    """A Restaurant with Pat management style.

    This class represents a restaurant that uses the Max management style,
    in which customers are served based on the profit they can bring. This class 
    is a subclass of Restaurant and implements two functions: add_customer and
    process_turn.

    """
    
    def add_customer(self, new_customer):
        """Add a new entering customer to the restaurant.

        :type new_customer: Customer
            The new customer that is entering the restaurant
        :rtype: None
        
        >>>a = Customer('1 23215 13.00 4 8')
        >>>b = Customer('2 58923 5.99 6 9')
        >>>c = MaxApproach()
        >>>MaxApproach.add_customer(c,a)
        >>>c._wait_customer
        {13.0: [<customer.Customer instance at 0x10531a7e8>]}
        >>>MaxApproach.add_customer(c,b)
        >>>c._wait_customer
        {13.0: [<customer.Customer instance at 0x10531a7e8>], 5.99: }
        """
        if new_customer.profit() not in self._wait_customer:
            self._wait_customer[new_customer.profit()] = [new_customer]
        else:
            self._wait_customer[new_customer.profit()].append(new_customer)


    def process_turn(self, current_turn):
        """Process the current_turn.

        This function will process the current turn. If the restaurant is not
        serving any customer now, and there are waiting customers, it should
        select one of them to serve.

        You can assume that all customers who entered the restaurant before or
        during this turn were already passed to the restaurant by simulator via
        calling the AddCustomer function.

        :type self: Restaurant
        :type current_turn: int
            The number of current turn
        :rtype: None
        
        >>>a = Customer('1 23215 13.00 4 8')
        >>>b = Customer('2 58923 5.99 6 9')
        >>>c = MaxApproach()
        >>>MaxApproach.add_customer(c, a)
        >>>MaxApproach.add_customer(c, b)
        >>>MaxApproach.process_turn(c, 1)
        >>>c._current_serving
        [<customer.Customer instance at 0x10541ef80>]
        >>>c._wait_customer
        {5.99: [<customer.Customer instance at 0x10f9a1050>]}
        """
        #remove impatient customers from wait_customer
        Restaurant.remove_impatient_customer(self, current_turn)
        print('after remove:',self._wait_customer)
        #check if current turn is finished
        
        if self._current_due == current_turn:
            self._current_serving.pop()
            
            
        #pick a new customer
        if not self._wait_customer == {} and self._current_serving == []:
            new_customer_picked = self._wait_customer[max(self._wait_customer.keys())][0]
            print('picking:', new_customer_picked)
            self._current_serving.append(new_customer_picked)
            self._total_profit += self._current_serving[0].profit()
            print('profit:', self._total_profit)
            self._customer_served += 1 
            print('customer served:', self._customer_served)
            self._current_due = current_turn + self._current_serving[0].serve_time()   
            print('current due:', self._current_due)
        #delete picked customer
            temp_profit = self._current_serving[0].profit()
            self._wait_customer[temp_profit].pop(0)
            if self._wait_customer[temp_profit] == []:
                self._wait_customer.pop(temp_profit)       
    
        
    def write_report(self, report_file):
        """Write the final report of this restaurant approach in the report_file.
        
        extend write_report method of super class

        :type self: Restaurant
        :type report_file: File
            This is an open file that this restaurant will write the report into.
        :rtype: None
        """
        temp = "Result for the serving approach using Max's suggestion:\n"
        report_file.write(temp)
        Restaurant.write_report(self, report_file)        
    
class PacApproach(Restaurant):
    """A Restaurant with Pat management style.

    This class represents a restaurant that uses the Pac management style,
    in which customers are served based on their serve time. This class is
    a subclass of Restaurant and implements two functions: add_customer and
    process_turn.

    """
    
    def add_customer(self, new_customer):
        """Add a new entering customer to the restaurant.

        :type new_customer: Customer
            The new customer that is entering the restaurant
        :rtype: None
        
        >>>a = Customer('1 23215 13.00 4 8')
        >>>b = Customer('2 58923 5.99 6 9')
        >>>c = PacApproach()
        >>>PacApproach.add_customer(c,a)
        >>>c._wait_customer
        {4: [<customer.Customer instance at 0x10531a7e8>]}
        >>>PacApproach.add_customer(c,b)
        >>>c._wait_customer
        {4: [<customer.Customer instance at 0x10531a7e8>], 6: }
        """
        if new_customer.serve_time() not in self._wait_customer:
            self._wait_customer[new_customer.serve_time()] = [new_customer]
        else:
            self._wait_customer[new_customer.serve_time()].append(new_customer)


    def process_turn(self, current_turn):
        """Process the current_turn.

        This function will process the current turn. If the restaurant is not
        serving any customer now, and there are waiting customers, it should
        select one of them to serve.

        You can assume that all customers who entered the restaurant before or
        during this turn were already passed to the restaurant by simulator via
        calling the AddCustomer function.

        :type self: Restaurant
        :type current_turn: int
            The number of current turn
        :rtype: None
        
        >>>a = Customer('1 23215 13.00 4 8')
        >>>b = Customer('2 58923 5.99 6 9')
        >>>c = PacApproach()
        >>>PacApproach.add_customer(c, a)
        >>>PacApproach.add_customer(c, b)
        >>>PacApproach.process_turn(c, 1)
        >>>c._current_serving
        [<customer.Customer instance at 0x10541ef80>]
        >>>c._wait_customer
        {6: [<customer.Customer instance at 0x10f9a1050>]}
        """
        #remove impatient customers from wait_customer
        Restaurant.remove_impatient_customer(self, current_turn)
        print('after remove:',self._wait_customer)
        #check if current turn is finished
        
        if self._current_due == current_turn:
            self._current_serving.pop()
            
            
            
        #pick a new customer
        if not self._wait_customer == {} and self._current_serving == []:
            new_customer_picked = self._wait_customer[min(self._wait_customer.keys())][0]
            print('picking:', new_customer_picked)
            self._current_serving.append(new_customer_picked)
            self._total_profit += self._current_serving[0].profit()
            print('profit:', self._total_profit)
            self._customer_served += 1 
            print('customer served:', self._customer_served)
            self._current_due = current_turn + self._current_serving[0].serve_time()  
            print('current due:', self._current_due)
        #delete picked customer
            temp_serve_time = self._current_serving[0].serve_time()
            self._wait_customer[temp_serve_time].pop(0)
            if self._wait_customer[temp_serve_time] == []:
                self._wait_customer.pop(temp_serve_time)
        print('\n')
    def write_report(self, report_file):
        """Write the final report of this restaurant approach in the report_file.
        
        extend write_report method of super class

        :type self: Restaurant
        :type report_file: File
            This is an open file that this restaurant will write the report into.
        :rtype: None
        """
        temp = "Result for the serving approach using Pac's suggestion:\n"
        report_file.write(temp)
        Restaurant.write_report(self, report_file)        