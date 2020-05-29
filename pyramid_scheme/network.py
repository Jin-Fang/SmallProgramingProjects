class NetworkNode():
    """An node that represents a person in the pyramid network containing his
    name, asset, mentor, sponsor, and chilren.

    === Attributes ===
    :param name: Person's name
    :type name: str
    :param asset: Person's asset
    :type asset: int
    """
    def __init__(self, name, asset):
        """Initialize a NetworkNode instance.

        :param self: An node representing person
        :type self: NetworkNode
        :param name: person's name
        :type name: str
        :param asset: Person's asset
        :type asset: int
        :return: None
        :rtype: NoneType

        >>> Lisa = NetworkNode('Lisa', 20)
        >>> Mason = NetworkNode('Mason', 25)
        >>> Lisa.asset
        20
        >>> Lisa.name
        'Lisa'
        >>> Mason.children
        []
        >>> Mason.asset
        25

        # Author: Pai Peng and Jin Fang
        """
        self.name = name
        self.asset = int(asset)
        self.mentor = 'None'
        self.sponsor = 'None'
        self.children = []

    def __eq__(self, other):
        """
        Return whether NetworkNode self is equivalent to other.

        :param self: NetworkNode self
        :type self: NetworkNode
        :param other: object to compare to NetworkNode self
        :type other: object | NetworkNode
        :return: True if NetworkNode self equal to other; False if not
        :rtype: bool

        >>> person1 = NetworkNode('Jack', 80)
        >>> person2 = NetworkNode('Jack', 80)
        >>> person3 = NetworkNode('Tom', 60)
        >>> person1.__eq__(person2)
        True
        >>> person1.__eq__(person3)
        False

        # Author: Pai Peng and Jin Fang
        """
        return (type(self) == type(other) and self.name == other.name and
                self.asset == other.asset and self.sponsor == other.sponsor and
                self.mentor == other.mentor and self.children == other.children)


class Network(object):
    """A pyramid network.

    This class represents a pyramid network. The network topology can be loaded
    from a file, and it can find the best arrest scenario to maximize the
    seized asset.

    === Attributes ===
    :param member_list: members listed by a list.
    :type member_list: list
    """

    def __init__(self):
        """Initialize a new member list.

        :param self: a pyramid network
        :type self: Network
        :param member_list: a member list containing all members
        :type member_list: list
        :return: None
        :rtype: NoneType

        >>> network = Network()
        >>> network.member_list
        []

        # Author: Pai Peng and Jin Fang
        """
        self.member_list = []

    def load_log(self, log_file_name):
        """Load the network topology from the log log_file_name.

        :param self: a pyramid network
        :type self: Network
        :param log_file_name: name of a file containing members' information
        :type log_file_name: str
        :return: None
        :rtype: NoneType

        # Author: Pai Peng and Jin Fang
        """
        f = open(log_file_name)
        # read each line per time
        for line in f:
            info = line.strip().split('#')
            # handle the great boss who does not have sponsor or mentor
            if len(info) == 2:
                member = NetworkNode(info[0], info[1])
            # handle members other than the great boss
            else:
                index = 0
                sponsor_name = info[1]
                for i in range(len(self.member_list)):
                    if self.member_list[i].name == sponsor_name:
                        index = i
                member = NetworkNode(info[0], info[2])
                member.sponsor = self.member_list[index]
                # if the sponsor does not have children, sponsor is the mentor
                if len(member.sponsor.children) == 0:
                    member.mentor = member.sponsor
                # if the sponsor has children, mentor is most recent children
                else:
                    member.mentor = member.sponsor.children[-1]
                member.sponsor.children += [member]
            self.member_list.append(member)
        f.close()

    def sponsor(self, member_name):
        """Return the sponsor name of member with name member_name.

        :param self: a pyramid network
        :type self: Network
        :param member_name: The name of a member
        :type member_name: str
        :return: memeber's sponsor's name
        :rtype : str

        >>> network = Network()
        >>> Liam = NetworkNode('Liam',20)
        >>> Mason = NetworkNode('Mason', 14)
        >>> Emma = NetworkNode('Emma', 32)
        >>> Jacob = NetworkNode('Jacob', 50)
        >>> Liam.children.append(Emma)
        >>> Liam.children.append(Jacob)
        >>> Emma.sponsor = Liam
        >>> Emma.mentor = Liam
        >>> Emma.children.append(Mason)
        >>> Jacob.sponsor = Liam
        >>> Jacob.mentor = Liam
        >>> Mason.sponsor = Emma
        >>> Mason.mentor = Emma
        >>> network.member_list.append(Liam)
        >>> network.member_list.append(Emma)
        >>> network.member_list.append(Jacob)
        >>> network.member_list.append(Mason)
        >>> network.sponsor('Emma')
        'Liam'
        >>> network.sponsor('Mason')
        'Emma'
        >>> network.sponsor('Liam')
        'None'

        # Author: Pai Peng and Jin Fang
        """
        # loop over the member_list to find the specific member
        for member in self.member_list:
            if member.name == member_name:
                if member.sponsor != 'None':
                    return member.sponsor.name
                else:
                    return member.sponsor

    def mentor(self, member_name):
        """Return the mentor name of member with name member_name.

        :param self: a pyramid network
        :type self: Network
        :param member_name: The name of a member
        :type member_name: str
        :return: member's member's name
        :rtype: str

        >>> network = Network()
        >>> Liam = NetworkNode('Liam',20)
        >>> Mason = NetworkNode('Mason', 14)
        >>> Emma = NetworkNode('Emma', 32)
        >>> Jacob = NetworkNode('Jacob', 50)
        >>> Liam.children.append(Emma)
        >>> Liam.children.append(Jacob)
        >>> Emma.sponsor = Liam
        >>> Emma.mentor = Liam
        >>> Emma.children.append(Mason)
        >>> Jacob.sponsor = Liam
        >>> Jacob.mentor = Liam
        >>> Mason.sponsor = Emma
        >>> Mason.mentor = Emma
        >>> network.member_list.append(Liam)
        >>> network.member_list.append(Emma)
        >>> network.member_list.append(Jacob)
        >>> network.member_list.append(Mason)
        >>> network.mentor('Emma')
        'Liam'
        >>> network.mentor('Mason')
        'Emma'
        >>> network.mentor('Liam')
        'None'

        # Author: Pai Peng and Jin Fang
        """
        # loop over the member_list to find the specific member
        for member in self.member_list:
            if member.name == member_name:
                if member.mentor != 'None':
                    return member.mentor.name
                else:
                    return member.mentor

    def assets(self, member_name):
        """Return the assets of member with name member_name.

        :param self: a pyramid network
        :type self: Network
        :param str member_name: The name of a member
        :return: member's asset
        :rtype: int

        >>> network = Network()
        >>> Liam = NetworkNode('Liam',20)
        >>> Mason = NetworkNode('Mason', 14)
        >>> Emma = NetworkNode('Emma', 32)
        >>> Jacob = NetworkNode('Jacob', 50)
        >>> Liam.children.append(Emma)
        >>> Liam.children.append(Jacob)
        >>> Emma.sponsor = Liam
        >>> Emma.mentor = Liam
        >>> Emma.children.append(Mason)
        >>> Jacob.sponsor = Liam
        >>> Jacob.mentor = Liam
        >>> Mason.sponsor = Emma
        >>> Mason.mentor = Emma
        >>> network.member_list.append(Liam)
        >>> network.member_list.append(Emma)
        >>> network.member_list.append(Jacob)
        >>> network.member_list.append(Mason)
        >>> network.assets('Emma')
        32
        >>> network.assets('Mason')
        14
        >>> network.assets('Liam')
        20

        # Author: Pai Peng and Jin Fang
        """
        # loop over the member_list to find the specific member
        for member in self.member_list:
            if member.name == member_name:
                return member.asset

    def children(self, member_name):
        """Return the name of all children of member with name member_name.

        :param self: a pyramid network
        :type self: Network
        :param member_name: The name of a member.
        :type member_name: str
        :return: a list of member's children
        :rtype: list

        >>> network = Network()
        >>> Liam = NetworkNode('Liam',20)
        >>> Mason = NetworkNode('Mason', 14)
        >>> Emma = NetworkNode('Emma', 32)
        >>> Jacob = NetworkNode('Jacob', 50)
        >>> Liam.children.append(Emma)
        >>> Liam.children.append(Jacob)
        >>> Emma.sponsor = Liam
        >>> Emma.mentor = Liam
        >>> Emma.children.append(Mason)
        >>> Jacob.sponsor = Liam
        >>> Jacob.mentor = Liam
        >>> Mason.sponsor = Emma
        >>> Mason.mentor = Emma
        >>> network.member_list.append(Liam)
        >>> network.member_list.append(Emma)
        >>> network.member_list.append(Jacob)
        >>> network.member_list.append(Mason)
        >>> network.children('Emma')
        ['Mason']
        >>> network.children('Mason')
        []
        >>> network.children('Liam')
        ['Emma', 'Jacob']

        # Author: Pai Peng and Jin Fang
        """
        # loop over the member_list to find the specific member
        for member in self.member_list:
            if member.name == member_name:
                acc = []
                for child in member.children:
                    acc.append(child.name)
                return acc

    def best_arrest_assets(self, maximum_arrest):
        """Search for the amount of seized assets in the best arrest scenario
        that maximizes the seized assets. Consider all members as target zero.

        :param self: a pyramid network
        :type self: Network
        :param maximum_arrest: maximum number of people that police can arrest
        :type maximum_arrest: int
        :return: the maximum asset the police can seize
        :rtype: int

        >>> network = Network()
        >>> Liam = NetworkNode('Liam',20)
        >>> Mason = NetworkNode('Mason', 14)
        >>> Emma = NetworkNode('Emma', 32)
        >>> Jacob = NetworkNode('Jacob', 50)
        >>> Liam.children.append(Emma)
        >>> Liam.children.append(Jacob)
        >>> Emma.sponsor = Liam
        >>> Emma.mentor = Liam
        >>> Emma.children.append(Mason)
        >>> Jacob.sponsor = Liam
        >>> Jacob.mentor = Liam
        >>> Mason.sponsor = Emma
        >>> Mason.mentor = Emma
        >>> network.member_list.append(Liam)
        >>> network.member_list.append(Emma)
        >>> network.member_list.append(Jacob)
        >>> network.member_list.append(Mason)
        >>> network.best_arrest_assets(1)
        50
        >>> network.best_arrest_assets(3)
        102

        # Author: Pai Peng and Jin Fang
        """
        def person_all_path(member, maximum_arrest, visited=[]):
            """Return a lis of all possible path start from a specific person
            in a pyramid network.

            :param member: a member in a pyramid network
            :type member: NetworkNode
            :param maximum_arrest: maximum number of people that police arrest
            :type maximum_arrest: int
            :param visited: a list recording visited people
            :type visited: list
            :return: a nested list of all possible path
            :rtype: list of list

            >>> network = Network()
            >>> Liam = NetworkNode('Liam',20)
            >>> Mason = NetworkNode('Mason', 14)
            >>> Emma = NetworkNode('Emma', 32)
            >>> Jacob = NetworkNode('Jacob', 50)
            >>> Liam.children.append(Emma)
            >>> Liam.children.append(Jacob)
            >>> Emma.sponsor = Liam
            >>> Emma.mentor = Liam
            >>> Emma.children.append(Mason)
            >>> Jacob.sponsor = Liam
            >>> Jacob.mentor = Liam
            >>> Mason.sponsor = Emma
            >>> Mason.mentor = Emma
            >>> network.member_list.append(Liam)
            >>> network.member_list.append(Emma)
            >>> network.member_list.append(Jacob)
            >>> network.member_list.append(Mason)
            >>> person_all_path(Jacob, 1, visited = [])
            [['Jacob']]
            >>> person_all_path(Liam, 2, visited = [])
            [['Liam', 'Emma'], ['Liam', 'Jacob']]

            #Author: Pai Peng and Jin Fang
            """
            # copy children, mentor, and sponsor
            children_copy = member.children[::-1]
            mentor_copy = [member.mentor]
            sponsor_copy = [member.sponsor]
            # base case 1: arrest the last person
            if maximum_arrest == 1:
                return [[member]]
            # develop a list of reachable person for each member
            reachable = []
            if sponsor_copy != ['None'] and mentor_copy != ['None']:
                # when mentor and sponsor for a member are different people
                if sponsor_copy != mentor_copy:
                    reachable = mentor_copy + sponsor_copy + children_copy
                # when mentor and sponsor for a member is the same person
                else:
                    reachable = mentor_copy + children_copy
            # when member is the great boss, reachables are his children
            else:
                reachable = children_copy
            # delete any visited member from reachable list
            i = 0
            while i < len(reachable):
                if reachable[i] in visited:
                    reachable.pop(i)
                else:
                    i += 1
            # base case 2: all people the member can reach have been arrested
            if reachable == []:
                return [[member]]
            # update the visited list to make sure the path does not go back
            visited += [member]
            # use recursion to split the problem and combine all paths
            total_path = []
            for person in reachable:
                for path in person_all_path(person, maximum_arrest-1, visited):
                    temp = [member]
                    temp.extend(path)
                    total_path.append(temp)
            return total_path

        if self.member_list == [] or maximum_arrest <= 0:
            return 0
        # use the helper function to get all possible paths
        allpath = []
        for member in self.member_list:
            allpath.extend(person_all_path(member, maximum_arrest, visited=[]))
        # find the maximum asset the best path can seize
        asset_lst = []
        for path in allpath:
            asset = 0
            for person in path:
                asset += person.asset
            asset_lst += [asset]
        return max(asset_lst)

    def best_arrest_order(self, maximum_arrest):
        """Search for list of member names in the best arrest scenario that
        maximizes the seized assets. Consider all members as target zero,
        and the order in the list represents the order that members are
        arrested.

        :param self: a pyramid network
        :type self: Network
        :param maximum_arrest: maximum number of people that police can arrest
        :type maximum_arrest: int
        :return: a list of people ino rder which is the best arrest order
        :rtype: list

        >>> network = Network()
        >>> Liam = NetworkNode('Liam',20)
        >>> Mason = NetworkNode('Mason', 14)
        >>> Emma = NetworkNode('Emma', 32)
        >>> Jacob = NetworkNode('Jacob', 50)
        >>> Liam.children.append(Emma)
        >>> Liam.children.append(Jacob)
        >>> Emma.sponsor = Liam
        >>> Emma.mentor = Liam
        >>> Emma.children.append(Mason)
        >>> Jacob.sponsor = Liam
        >>> Jacob.mentor = Liam
        >>> Mason.sponsor = Emma
        >>> Mason.mentor = Emma
        >>> network.member_list.append(Liam)
        >>> network.member_list.append(Emma)
        >>> network.member_list.append(Jacob)
        >>> network.member_list.append(Mason)
        >>> network.best_arrest_order(1)
        ['Jacob']
        >>> network.best_arrest_order(3)
        ['Emma', 'Liam', 'Jacob']

        # Author: Pai Peng and Jin Fang
        """

        def person_all_path(member, maximum_arrest, visited=[]):
            """Return a lis of all possible path start from a specific person
            in a pyramid network.

            :param member: a member in a pyramid network
            :type member: NetworkNode
            :param maximum_arrest: maximum number of people that police arrest
            :type maximum_arrest: int
            :param visited: a list recording visited people
            :type visited: list
            :return: a nested list of all possible path
            :rtype: list of list

            >>> network = Network()
            >>> Liam = NetworkNode('Liam',20)
            >>> Mason = NetworkNode('Mason', 14)
            >>> Emma = NetworkNode('Emma', 32)
            >>> Jacob = NetworkNode('Jacob', 50)
            >>> Liam.children.append(Emma)
            >>> Liam.children.append(Jacob)
            >>> Emma.sponsor = Liam
            >>> Emma.mentor = Liam
            >>> Emma.children.append(Mason)
            >>> Jacob.sponsor = Liam
            >>> Jacob.mentor = Liam
            >>> Mason.sponsor = Emma
            >>> Mason.mentor = Emma
            >>> network.member_list.append(Liam)
            >>> network.member_list.append(Emma)
            >>> network.member_list.append(Jacob)
            >>> network.member_list.append(Mason)
            >>> person_all_path(Jacob, 1, visited = [])
            [['Jacob']]
            >>> person_all_path(Liam, 2, visited = [])
            [['Liam', 'Emma'], ['Liam', 'Jacob']]

            # this helper function is identical to the previous helper function
            # Author: Pai Peng and Jin Fang
            """
            # copy children, mentor, and sponsor
            children_copy = member.children[::-1]
            mentor_copy = [member.mentor]
            sponsor_copy = [member.sponsor]
            # base case 1: arrest the last person
            if maximum_arrest == 1:
                return [[member]]
            # develop a list of reachable person for each member
            reachable = []
            if sponsor_copy != ['None'] and mentor_copy != ['None']:
                # when mentor and sponsor for a member are different people
                if sponsor_copy != mentor_copy:
                    reachable = mentor_copy + sponsor_copy + children_copy
                # when mentor and sponsor for a member is the same person
                else:
                    reachable = mentor_copy + children_copy
            # when member is the great boss, reachables are his children
            else:
                reachable = children_copy
            # delete any visited member from reachable list
            i = 0
            while i < len(reachable):
                if reachable[i] in visited:
                    reachable.pop(i)
                else:
                    i += 1
            # base case 2: all people the member can reach have been arrested
            if reachable == []:
                return [[member]]
            # update the visited list to make sure the path does not go back
            visited += [member]
            # use recursion to split the problem and combine all paths
            total_path = []
            for person in reachable:
                for path in person_all_path(person, maximum_arrest-1, visited):
                    temp = [member]
                    temp.extend(path)
                    total_path.append(temp)
            return total_path

        if self.member_list == [] or maximum_arrest <= 0:
            return []
        allpath = []
        # use the helper function to get all possible paths
        for member in self.member_list:
            allpath.extend(person_all_path(member, maximum_arrest, visited=[]))
        # find the path which can seize maximum assets
        ptr = 0
        asset = 0
        for i in range(len(allpath)):
            current_asset = 0
            for person in allpath[i]:
                current_asset += int(person.asset)
            if current_asset > asset:
                asset = current_asset
                ptr = i
        best_path = []
        for individual in allpath[ptr]:
            best_path += [individual.name]
        return best_path

if __name__ == "__main__":
    # A sample example of how to use a network object
    network = Network()
    network.load_log("topology1.txt")
    member_name = "Sophia"
    print(member_name + "'s sponsor is " + network.sponsor(member_name))
    print(member_name + "'s mentor is " + network.mentor(member_name))
    print(member_name + "'s asset is " + str(network.assets(member_name)))
    print(member_name + "'s childrens are " + str(network.children(member_name)))
    maximum_arrest = 4
    print("The best arrest scenario with the maximum of " + str(maximum_arrest)\
          + " arrests will seize " + str(network.best_arrest_assets(maximum_arrest)))
    print("The best arrest scenario with the maximum of " + str(maximum_arrest)\
          + " arrests is: " + str(network.best_arrest_order(maximum_arrest)))
