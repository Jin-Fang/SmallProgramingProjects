from customer import Customer
from restaurant import PatApproach, MatApproach, MaxApproach, PacApproach

class Simulator:
    """A Simulator.

    This class represents the simulator which initiates different approaches,
    load scenario from the file, and call restaurant function for new customer
    arrivals and at each turn.

    Of course, you may add whatever private attributes and methods you want.
    But because you should not change the interface, you may not add any public
    attributes or methods.

    This is the entry point into your program, and in particular is used for
    auto-testing purposes. This makes it ESSENTIAL that you do not change the
    interface in any way!
    """

    # === Managed Attributes ===
    # :type _scenario: List[Customer]
    #     The simulation scenario, which consists of a list of customers that
    #     will enter the restaurant.
    # :type _approaches: List[Restaurant]
    #     All approaches that will be simulated

    def __init__(self):
        """Initialize a Simulation.
        """

        # Initialize the scenario to an empty list
        self._scenario = []

        # Initialize different approaches that will be simulated
        self._approaches = []
        self._approaches.append(PatApproach())
        self._approaches.append(MatApproach())
        self._approaches.append(MaxApproach())
        self._approaches.append(PacApproach())

    def load_scenario(self, scenario_file_name):
        """Load a scenario from the scenario_file_name and store it in _scenario

        :param scenario_file_name: Name of the scenario file
        :type scenario_file_name: str
        :rtype: None
        """
        scenario_file = open(scenario_file_name)

        for current_line in scenario_file:
            new_customer = Customer(current_line.strip())
            self._scenario.append(new_customer)

        scenario_file.close()


    def simulate(self, report_file_name):
        """Run the simulation and write resutls in report_file_name.

        This function runs the actual simulation by running a turn by turn
        simulation and writes the result in report_file_name.

        :param report_file_name: Name of the report file
        :type report_file_name: str
        :rtype: None
        """

        current_turn = 1
        last_turn = 0

        # Process all customers entry
        for next_customer in self._scenario:
            # While we did not reach the turn that this customer enters the
            # restaurant, process turns one by one
            while current_turn < next_customer.entry_turn():
                # Ask all approaches to process this turn
                for approach in self._approaches:
                    approach.process_turn(current_turn)

                current_turn += 1

            # Ask all approaches to add this customer
            for approach in self._approaches:
                approach.add_customer(next_customer)

            # Update the last turn that we should simulate based on when
            # this customer may leave the restaurant
            next_customer_exit_turn = next_customer.entry_turn() + next_customer.serve_time()
            if (next_customer_exit_turn > last_turn):
                last_turn = next_customer_exit_turn

        # Continue simulation until we are sure that no customer may remains
        # in a restaurant waiting
        while current_turn <= last_turn:
            # Ask all approaches to process this turn
            for approach in self._approaches:
                approach.process_turn(current_turn)

            current_turn += 1

        # Now write report of all approaches in report_file_name
        report_file = open(report_file_name, "w")

        for approach in self._approaches:
            approach.write_report(report_file)

        report_file.close()


if __name__ == "__main__":
    # A sample example of how to create and use simulator class
    simulator = Simulator()
    simulator.load_scenario("scenario1.txt")
    simulator.simulate("report1.txt");
