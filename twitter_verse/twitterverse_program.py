import twitterverse_functions as tf

if __name__ == '__main__':
    
    data_filename = input('Data file: ')
    data_file = open(data_filename, 'r')
    data = tf.process_data(data_file)
    data_file.close()
    
    query_filename = input('Query file: ')
    query_file = open(query_filename, 'r')
    query = tf.process_query(query_file)
    query_file.close()
        
    search_results = tf.get_search_results(data, query['search'])
    filtered_results = tf.get_filter_results(data, search_results, 
                                             query['filter'])
    presented_results = tf.get_present_string(data, filtered_results, 
                                              query['present'])
    
    print(presented_results, end="")
