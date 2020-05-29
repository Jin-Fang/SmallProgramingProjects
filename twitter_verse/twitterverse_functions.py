"""
Type descriptions of Twitterverse and Query dictionaries
(for use in docstrings)

Twitterverse dictionary:  dict of {str: dict of {str: object}}
    - each key is a username (a str)
    - each value is a dict of {str: object} with items as follows:
        - key "name", value represents a user's name (a str)
        - key "location", value represents a user's location (a str)
        - key "web", value represents a user's website (a str)
        - key "bio", value represents a user's bio (a str)
        - key "following", value represents all the usernames of users this 
          user is following (a list of str)
       
Query dictionary: dict of {str: dict of {str: object}}
   - key "search", value represents a search specification dictionary
   - key "filter", value represents a filter specification dictionary
   - key "present", value represents a presentation specification dictionary

Search specification dictionary: dict of {str: object}
   - key "username", value represents the username to begin search at (a str)
   - key "operations", value represents the operations to perform (a list of str)

Filter specification dictionary: dict of {str: str}
   - key "following" might exist, value represents a username (a str)
   - key "follower" might exist, value represents a username (a str)
   - key "name-includes" might exist, value represents a str to match (a case-insensitive match)
   - key "location-includes" might exist, value represents a str to match (a case-insensitive match)

Presentation specification dictionary: dict of {str: str}
   - key "sort-by", value represents how to sort results (a str)
   - key "format", value represents how to format results (a str)

"""

# Write your Twitterverse functions here
def find_END_index(lines):
    ''' (list of str) -> list

    Return a list
    '''
    END_index_list = []
    for i in range(len(lines)):
        if lines[i] == 'END':
            END_index_list.append(i)
    return END_index_list


def find_ENDBIO_index(lines):
    ''' (list of str) -> list

    Return a list of intagers, each one refers to the index in the list of str 'ENDBIO'.

    >>>find_ENDBIO_index(['a', 'ENDBIO', 'END', 'b'])
    [1]
    >>>find_ENDBIO_index(['ENDBIO', 'a', 'end', 'ENDBIO', 'Y'])
    [1, 3]
    '''
    ENDBIO_index_list = []
    for i in range(len(lines)):
        if lines[i] == 'ENDBIO':
            ENDBIO_index_list.append(i)
    return ENDBIO_index_list


def process_data(data_file):
    ''' (file open for reading) -> dict of {str: dict of {str: obeject}}
    '''
    Twitterverse_dictionary = {}
    lines = data_file.readlines()
    lines = [line.strip() for line in lines]
    END_index_list = find_END_index(lines)
    END_index_list.insert(0, -1)
    ENDBIO_index_list = find_ENDBIO_index(lines)

    for i in range(len(END_index_list)-1):
        sub_twitterverse_dict = {}

        username = lines[END_index_list[i] + 1]
        Twitterverse_dictionary[username] = sub_twitterverse_dict
        
        name_info = lines[END_index_list[i] + 2]
        sub_twitterverse_dict['name'] = name_info
        
        location_info = lines[END_index_list[i] + 3]
        sub_twitterverse_dict['location'] = location_info
        
        web_info = lines[END_index_list[i] + 4]
        sub_twitterverse_dict['web'] = web_info

        bio_info = lines[END_index_list[i] + 5 : ENDBIO_index_list[i]]
        bio_info_str = ''
        for j in range(len(bio_info)):
            bio_info_str += bio_info[j]
        sub_twitterverse_dict['bio'] = bio_info_str
        
        following_info = lines[ENDBIO_index_list[i] + 1 : END_index_list[i+1]]
        sub_twitterverse_dict['following'] = following_info

    return Twitterverse_dictionary


def process_query(query_file):
    ''' (file open for reading) -> dict of {str: dict of {str: obeject}}

    Return query dictioanry containing all the information in the query file. 
    '''
    
    lines = query_file.readlines()
    #lines = [line.strip() for line in lines]
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    FILTER_index = lines.index('FILTER')
    PRESENT_index = lines.index('PRESENT')
    query_dictionary = {}
    search_dictionary = {}
    filter_dictionary = {}
    present_dictionary = {}
    
    query_dictionary['search'] = search_dictionary
    search_dictionary['username'] = lines[1]
    search_dictionary['operations'] = lines[2 : FILTER_index]
    
    query_dictionary['filter'] = filter_dictionary
    for i in range(FILTER_index + 1, PRESENT_index):
        filter_dictionary_key = lines[i].split()[0]
        filter_dictionary_value = lines[i].split()[1]
        filter_dictionary[filter_dictionary_key] = filter_dictionary_value
    
    query_dictionary['present'] = present_dictionary
    for i in range(PRESENT_index + 1, len(lines)):
        if lines[i].split()[0] == 'sort-by':
            present_dictionary['sort-by'] = lines[i].split()[1]
        elif lines[i].split()[0] == 'format':
            present_dictionary['format'] = lines[i].split()[1]

    return query_dictionary


def all_followers(Twitterverse_dictionary, chosen_username):
    ''' (Twitterverse dictionary, str) -> list of str
    '''
    all_followers_list = []
    for username in Twitterverse_dictionary:
        if chosen_username in Twitterverse_dictionary[username]['following']:
            all_followers_list.append(username)
            
    return all_followers_list


def get_search_results(Twitterverse_dictionary, search_specification_dictionary):
    '''(Twitterverse dictionary, search specification dictionary) -> list of str

    Return a list of str containing the research result from the Twitterverse dictionary. Search specifications are indicated in search specification dictionary.  

    >>> Twitterverse_dictionary = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['c', 'a']}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['a']}}
    >>> search_specification_dictionary = {\
    'username': 'a', 'operations': ['following', 'following']}
    >>> get_search_results(Twitterverse_dictionary, search_specification_dictionary)
    ['c', 'a']
    >>> search_specification_dictionary = {\
    'username': 'a', 'operations': ['following', 'follower']}
    >>> get_search_results(Twitterverse_dictionary, search_specification_dictionary)
    ['a']
    '''
                      
    chosen_username = search_specification_dictionary['username']
    chosen_operations = search_specification_dictionary['operations']
    result = [chosen_username]
    for i in range(len(chosen_operations)):
        result_2 = []
        for j in range(len(result)):
            if chosen_operations[i] == 'following':
                result_2.extend(Twitterverse_dictionary[result[j]]['following'])
            elif chosen_operations[i] == 'followers':
                result_2.extend(all_followers(Twitterverse_dictionary, result[j]))
        i = 0
        while i < len(result_2):
            if result_2[i] in result_2[i+1:]:
                result_2.remove(result_2[i])
            else:
                i += 1
        result = result_2

    return result


def get_filter_results(Twitterverse_dictionary, get_search_results, filter_specification_dictionary):
    '''(Twitterverse dictionary, list of str, filter specification dictionary) -> list of str
    '''

    chosen_name_includes = filter_specification_dictionary['name-includes']
    chosen_location_includes = filter_specification_dictionary['location-includes']
    chosen_follower = filter_specification_dictionary['follower']
    chosen_following = filter_specification_dictionary['following']

    for i in range(len(get_search_results)):
        if chosen_name_includes.lower() not in get_search_results[i].lower():
            get_search_results.remove(get_search_results[i])

        actual_location = Twitterverse_dictionary[get_search_results[i]]['location']
        if chosen_location_includes.lower() not in actual_location.lower():
            get_search_results.remove(get_search_results[i])

        actual_following = Twitterverse_dictionary[get_search_results[i]]['following']
        if chosen_following != actual_following:
            get_search_results.remove(get_search_results[i])

        actual_follower = all_followers(Twitterverse_dictionary, get_search_results[i])
        if chosen_follower != actual_follower:
            get_search_results.remove(get_search_results[i])

    return get_search_results


def get_present_string(Twitterverse_dictionary, get_filter_results, presentation_specification_dictionary):
    ''' (Twitterverse dictionary, list of str, presentation specification dictionary) -> str

    return a str

    
    >>> twitter_data = {\
    'Gazzale':{'name':'Robert Gazzale', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'Indart':{'name':'Gustavo Indart', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'Pesando':{'name':'James E. Pesando', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> get_filter_results = ['Gazzale', 'Indart', 'Pesando']
    >>> presentation_specification_dictionary = {'sort-by': 'username', 'format': 'short'}
    >>> get_present_string(Twitterverse_dictionary, get_filter_results, presentation_specification_dictionary)

    >>> presentation_specification_dictionary = {'sort-by': 'name', 'format': 'long'}
    >>> get_present_string(Twitterverse_dictionary, get_filter_results, presentation_specification_dictionary)
    
    '''

    sort_method = presentation_specification_dictionary['sort-by']
    specific_format = presentation_specification_dictionary['format']

    if sort_method == 'username':
        tweet_sort(Twitterverse_dictionary, get_filter_results, username_first)
    elif sort_method == 'name':
        tweet_sort(Twitterverse_dictionary, get_filter_results, name_first)
        name_list = []
        for i in range(len(get_filter_results)):
            username = get_filter_results[i]
            name_list.append(Twitterverse_dictionary[username]['name'])
        for i in range(len(name_list)):
            if name_list[i] == name_list[i+1]:
                tweet_sort(Twitterverse_dictionary, get_filter_results[i:i+2], username_first)
    elif sort_method == 'popularity':
        tweet_sort(Twitterverse_dictionary, get_filter_results, more_popular)

    if specific_format == 'short':
        short_present = ''
        for name in get_filter_results:
            short_present = short_present + name + ' '
    return short_present[:-1]

    if specific_format == 'long':
        






    
# --- Sorting Helper Functions ---
def tweet_sort(twitter_data, results, cmp):
    """ (Twitterverse dictionary, list of str, function) -> NoneType

    Sort the results list using the comparison function cmp and the data in 
    twitter_data.

    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> result_list = ['c', 'a', 'b']
    >>> tweet_sort(twitter_data, result_list, username_first)
    >>> result_list
    ['a', 'b', 'c']
    >>> tweet_sort(twitter_data, result_list, name_first)
    >>> result_list
    ['b', 'a', 'c']
    """
    
    # Insertion sort
    for i in range(1, len(results)):
        current = results[i]
        position = i
        while position > 0 and cmp(twitter_data, results[position - 1], current) > 0:
            results[position] = results[position - 1]
            position = position - 1 
        results[position] = current  
            
def more_popular(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
    
    Return -1 if user a has more followers than user b, 1 if fewer followers, 
    and the result of sorting by username if they have the same, based on the 
    data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> more_popular(twitter_data, 'a', 'b')
    1
    >>> more_popular(twitter_data, 'a', 'c')
    -1
    """
    
    a_popularity = len(all_followers(twitter_data, a)) 
    b_popularity = len(all_followers(twitter_data, b))
    if a_popularity > b_popularity:
        return -1
    if a_popularity < b_popularity:
        return 1
    return username_first(twitter_data, a, b)
    
def username_first(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
    
    Return 1 if user a has a username that comes after user b's username 
    alphabetically, -1 if user a's username comes before user b's username, 
    and 0 if a tie, based on the data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> username_first(twitter_data, 'c', 'b')
    1
    >>> username_first(twitter_data, 'a', 'b')
    -1
    """
    
    if a < b:
        return -1
    if a > b:
        return 1
    return 0

def name_first(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
        
    Return 1 if user a's name comes after user b's name alphabetically, 
    -1 if user a's name comes before user b's name, and the ordering of their
    usernames if there is a tie, based on the data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> name_first(twitter_data, 'c', 'b')
    1
    >>> name_first(twitter_data, 'b', 'a')
    -1
    """
    
    a_name = twitter_data[a]["name"]
    b_name = twitter_data[b]["name"]
    if a_name < b_name:
        return -1
    if a_name > b_name:
        return 1
    return username_first(twitter_data, a, b)       


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    data_file = 'data.txt'
    file = open(data_file)
    data = process_data(file)
    print(data)

    query_file = 'query5.txt'
    file = open(query_file)
    query = process_query(file)
    print(query)

    result = get_search_results(data, query['search'])
    print(result)
