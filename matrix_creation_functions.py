#Philip Mascaro



#DATA SOURCE:
#https://www.kaggle.com/datasets/akashdeepkuila/bakery?resource=download

import pandas as pd
from itertools import combinations
import numpy as np

#use student ID as random seed
np.random.seed(10458430)


#need this for later for saving matrices to files
import pickle

def pickle_item(item_to_pickle,location_to_pickle):
    pickle_name = location_to_pickle + ".pickle"
    pickled_file = open(pickle_name,"wb")
    pickle.dump(item_to_pickle, pickled_file)
    pickled_file.close()



#load the data
bakery_data = pd.read_csv("archive/bakery_sales_revised.csv")

#show the loaded data
print("bakery_data")
print(bakery_data)
print()
print()
print()
print()

#show dataframe size
print(bakery_data.shape)

#get all column headers
column_headers = bakery_data.columns.tolist()

#remove duplicate rows
bakery_data = bakery_data.drop_duplicates(subset=column_headers, keep="first")

#confirm the dataframe size decreased
print(bakery_data.shape)
print()
print()
print()
print()


#get the lists of unique items, unique period_day options, and unique weekday_weekend options
item_options = sorted(list(set(bakery_data['Item'].tolist())))
period_day_options = sorted(list(set(bakery_data['period_day'].tolist())))
day_type_options = sorted(list(set(bakery_data['weekday_weekend'].tolist())))

print("len(item_options)")
print(len(item_options))
print("len(period_day_options)")
print(len(period_day_options))
print("len(day_type_options)")
print(len(day_type_options))
print()
print()
print()
print()



#given an item, a period, and a day type, select only the rows of the dataframe that contain all three
#output a dataframe
def subset_dataframe(in_item, in_period, in_day_type):
    #print("subset_dataframe")
    sub_item = bakery_data[bakery_data['Item'] == in_item]
    sub_item_and_period = sub_item[sub_item['period_day'] == in_period]
    sub_item_and_period_and_day_type = sub_item_and_period[sub_item_and_period['weekday_weekend'] == in_day_type]
    
    return sub_item_and_period_and_day_type



"""
given a list of items, a period, and a day type,
for each individual item, select only the rows of the dataframe that contain
that item, the period, and the day type

output a list of dataframes
"""
def subset_dataframe_list(in_item_list, in_period, in_day_type):
    #print("subset_dataframe_list")
    return [subset_dataframe(in_item, in_period, in_day_type) for in_item in in_item_list]
    



#get the transaction numbers for all transactions containing every item in the list, for the provided period and day type
#output a list of transaction numbers
def get_transaction_nums(in_item_list, in_period, in_day_type):
    #print("get_transaction_nums")
    
    
    #get the dataframes for each item
    specific_dataframes = subset_dataframe_list(in_item_list, in_period, in_day_type)

    #for each item, get the transaction numbers for the transactions containing that item
    transaction_nums_list = [i['Transaction'].tolist() for i in specific_dataframes]
    
    #take the intersection of all sets of transaction numbers
    transaction_nums = list(set.intersection(*map(set,transaction_nums_list)))
    
    return transaction_nums



"""
given a list of items, a period, and a day type,
find all transactions involving those items,
output the rows of the dataframe containing the transactions,
INCLUDING rows of items NOT specified by the user

the items not specified are the ones of interest
these are the items commonly paired with the ones of interst
"""
def paired_purchase_dataframe(in_item_list, in_period, in_day_type):
    #print("paired_purchase_dataframe")
    transaction_nums = get_transaction_nums(in_item_list, in_period, in_day_type)
    purchases_with_items = bakery_data[bakery_data['Transaction'].isin(transaction_nums)]
    
    return purchases_with_items
                                                    
                  


"""
given a list of items, a period, and a day type,
find all transactions involving those items,
output the rows of the dataframe containing the transactions,
EXCEPT the rows involving the items specified by the user

these are all the rows of items paired with the ones of interest, but aren't the ones of interest
"""
def paired_purchases_only(in_item_list, in_period_list, in_day_type_list):
    #print("paired_purchases_only")
    purchases_with_items = paired_purchase_dataframe(in_item_list, in_period_list, in_day_type_list)

    exclude_items_dataframe = purchases_with_items[~(purchases_with_items['Item'].isin(in_item_list))]
    
    
    return exclude_items_dataframe




#given a dataframe and an item, count how many times that item appears in the dataframe
def dataframe_entry_count(dataframe, in_item):
    #print("dataframe_entry_count")
    isolated_item_dataframe = dataframe[dataframe['Item'] == in_item]
    return isolated_item_dataframe.shape[0]




"""
given a list of items, a period, and a day type,
find all transactions involving those items,
count how many times every other item is paired with the items of interest

output a dictionary
keys are items paired with the items of interest
values are how many times that item was paired with the items of interest
"""
def pairings_with_counts(in_item_list, in_period_list, in_day_type_list):
    #print("pairings_with_counts")
    exclude_items_dataframe_no_dups = paired_purchases_only(in_item_list, in_period_list, in_day_type_list)
    pairings_list = exclude_items_dataframe_no_dups['Item'].tolist()
    
    pairings_list_unique = list(set(pairings_list))
    
    counts_dictionary = {pair_item:dataframe_entry_count(exclude_items_dataframe_no_dups, pair_item) for pair_item in pairings_list_unique}
    return counts_dictionary





"""
given a period and a day type,
find how often each item is purchased

this is to determine how popular each item is given an "empty cart"
"""
def dict_all_entries(in_period, in_day_type):
    print("dict_all_entries")

    #subset of dataframe for the period and day type
    sub_item_and_period = bakery_data[bakery_data['period_day'] == in_period]
    sub_item_and_period_and_day_type = sub_item_and_period[sub_item_and_period['weekday_weekend'] == in_day_type]
    
    
    #get the list of all items, with and without duplicates
    pairings_list = sub_item_and_period_and_day_type['Item'].tolist()
    
    pairings_list_unique = list(set(pairings_list))
    
    #get the count of every item in the dataframe for the period and day type
    counts_dictionary = {pair_item:dataframe_entry_count(sub_item_and_period_and_day_type, pair_item) for pair_item in pairings_list_unique}
    return counts_dictionary


"""
given a number of items in the cart, find all possible combinations of items up to that specified value

for example, if end_num = 3, find all possible
carts containing 1 item
carts containing 2 items
carts containing 3 items

each cart combination is a tuple
for a given cart size, create a list of tuples
for all cart sizes from 1 to end_num, create a list of lists of tuples

output the list of lists of tuples
"""
def item_combos(end_num):
    #print("item_combos")
    item_set = [[tuple([i]) for i in item_options]]
    for i in range(2,end_num+1):
        item_set = item_set + [list(combinations(item_options, i))]
    
    return item_set



"""
given a list of items, a period, and a day type,
convert to a one-hot encoding
"""
def convert_to_vector(in_tuple, in_period, in_day_type):
    #print("convert_to_vector")
    """
    indices
        0
    to
        len(item_options)-1
    are the one-hot encoding of item_options

    
    indices
        len(item_options)
    to
        len(item_options)+len(period_day_options)-1
    are the one-hot encoding of period_day
    

    indices
        len(item_options)+len(period_day_options)
    to
        len(item_options)+len(period_day_options)+len(day_type_options)-1
    are the one-hot encoding of day_type_options
    """
    data_vec = np.zeros(len(item_options) + len(period_day_options) + len(day_type_options))
    
    in_list = list(in_tuple)
    
    #get one-hot encoding for item_options
    for i in in_list:
        data_vec[item_options.index(i)] = 1
    
    
    #get one-hot encoding for period_day_options
    data_vec[len(item_options) + period_day_options.index(in_period)] = 1


    #get one-hot encoding for day_type_options
    data_vec[len(item_options) + len(period_day_options) + day_type_options.index(in_day_type)] = 1
    
    return data_vec





"""
given an input dictionary listing the counts for item predictions,
convert to a vector of frequencies

IF THE RESULTING COUNTS ARE ALL 0,
return the vector of all 0s
"""
def convert_to_frequency(in_dict):
    #print("convert_to_frequency")

    #create an empty vector for storing counts
    data_vec = np.zeros(len(item_options))
    
    #for each key, save the key value into the corresponding vector index
    for item_id in list(in_dict.keys()):
        data_vec[item_options.index(item_id)] = in_dict[item_id]
    
    #get total count
    data_vec_count = np.sum(data_vec)
    
    #if total count is 0, return the vector as is
    if data_vec_count == 0:
        return data_vec
    
    #otherwise, normalize into proportion
    data_freq = data_vec / data_vec_count
    
    return data_freq



"""
given a list of items, a period, and a day type,
convert to a one-hot encoding vector and a frequency vector
"""
def generate_basic_in_out_pair(in_tuple, in_period, in_day_type):
    #print("generate_basic_in_out_pair")
    input_vector = convert_to_vector(in_tuple, in_period, in_day_type)
    
    out_dict = pairings_with_counts(in_tuple, in_period, in_day_type)
    
    output_vector = convert_to_frequency(out_dict)
    
    return input_vector, output_vector



"""
given a list of item combinations, a period, and a day type,

get the one-hot encoding vector and frequency vector for each item tuple

save the vectors to dictionaries
key is the item combo used to make the vector
value is
    the one-hot encoding vector for one dictionary,
    and the frequency vector for the other dictionary


item combinations are possible carts
for example, item_combos could be [("Jam"), ("Bread", "Jam"), ("Bread", "Coffee"), ("Bread", "Coffee", "Tea"), ...]
"""

#requires item_combos to be a single dimension list of tuples
def get_all_dicts(item_combos, in_period, in_day_type):
    print("get_all_dicts")
    basic_vectors = [generate_basic_in_out_pair(in_tuple, in_period, in_day_type) for in_tuple in item_combos]
    
    in_dict = {item_combos[i]:basic_vectors[i][0] for i in range(len(item_combos))}
    out_dict = {item_combos[i]:basic_vectors[i][1] for i in range(len(item_combos))}
    
    return in_dict, out_dict
    

"""
given a list of items, the dictionary converting from carts to frequency vectors,
and the vector of suggestions for an empty cart,

create a modified frequency vector, taking into account all possible subcarts


for example, the cart ("Bread","Jam") has subcarts
    ("Bread")
    ("Jam")
    ("Bread","Jam")

for each subcart, use the dictionary basic_frequencies_dict to get its basic frequency vector
scale the basic frequency vector by the number of items in the cart
    chose this method so there is a higher weighting when there are multiple items in a subcart

add the scaled basic frequency vectors together
renormalize the sum of scaled vectors if the sum is not all 0s

if the sum is all 0s, meaning this ALL subcarts (including this cart) has never been purchased,
then output the suggestions for an empty cart


this is done so that if the items in in_cart were never purchased together,
the suggested items vector isn't "don't buy anything else" due to all 0s,
and instead looks at the items and subcombinations to inform the suggestion
"""
    
def modified_frequency(in_cart, basic_frequencies_dict, default_suggestion_vector):
    #print("modified_frequency")


    #print("modifying frequency for",in_cart)


    

    #find all subcart combinations, separated by cart size
    all_subcarts = [list(combinations(in_cart, cart_size)) for cart_size in range(1,len(in_cart)+1)]
    
    #set up empty vector
    sum_vec = np.zeros(len(item_options))
    
    #for each cart size
    for cart_size_minus_1 in range(len(all_subcarts)):
        #for each item combo at that cart size
        for combo in all_subcarts[cart_size_minus_1]:
            #add the weighted frequency vector
            sum_vec += (cart_size_minus_1 + 1) * basic_frequencies_dict[combo]
    
    #get the renomalizing denominator
    sum_vec_count = np.sum(sum_vec)
    
    #if, somehow, none of these items have ever been purchased with another item
    if sum_vec_count == 0:
        #output the default vector
        return default_suggestion_vector
    
    #return the normalzied modified frequency
    new_data_freq = sum_vec / sum_vec_count
    
    return new_data_freq


"""
given a list of item combinations, a period, a day type, and the default suggestion vector

get the one-hot encoding vector and the modified frequency vector for each item tuple
"""

#requires item_combos to be a single dimension list of tuples
def new_frequencies_dict(item_combos, in_period, in_day_type, default_suggestion_vector):
    print("new_frequencies_dict")
    in_dict, old_out_dict = get_all_dicts(item_combos, in_period, in_day_type)
    
    out_dict = {combo:modified_frequency(combo, old_out_dict, default_suggestion_vector) for combo in item_combos}
    
    return in_dict, out_dict



"""
given a number of items, and a test-train split value,

split indices into training and testing sets
"""
def generate_index_sequences(num_items, training_cutoff):
    print("generate_index_sequences")

    #create a linspace for the number of items
    rand_list_dataset = np.linspace(0,1,num_items)
    #shuffle the linspace
    np.random.shuffle(rand_list_dataset)
    
    #find the indices where the randomized linspace is below the cutoff for training, and above the cutoff for testing
    training_indices = (np.argwhere(rand_list_dataset < training_cutoff).reshape(-1)).tolist()

    testing_indices = (np.argwhere(rand_list_dataset >= training_cutoff).reshape(-1)).tolist()

    
    return training_indices, testing_indices


"""
given a period, and a day type, and a max cart size,

create a fair 80-20 split, accounting for different cart sizes
"""

def fair_80_20_split(in_period, in_day_type, max_combo):
    print("fair_80_20_split")

    #get every item combination up to the max cart size
    #stored as a list of lists
    combos_multi_list = item_combos(max_combo)

    #get the default prediction vector for this period and day type
    default_suggestion_vector = convert_to_frequency(dict_all_entries(in_period, in_day_type))
    
    #convert the combos list
    #originally a list of lists dependent on cart size
    #turn it into a single list
    combos_single_list = []
    for inner_list in combos_multi_list:
        combos_single_list = combos_single_list + inner_list
    
    #get the one-hot encodings for the combos, and the modified frequencies for the combos
    #these will be used as the inputs and outputs for the model
    combo_to_vec_representation, combo_to_suggested_item_frequencies = new_frequencies_dict(combos_single_list, in_period, in_day_type, default_suggestion_vector)
    
    #get the number of counts for each cart size
    #considering there are 94 unique items, we expect this to be (94 choose (i+1))
    multi_list_counts = [len(i) for i in combos_multi_list]
    
    """
    for each cart size count, generate the test-train splits for those indices
    
    we want to make sure that each cart size is proportionally represented in the training and testing sets,
    especially considering larger cart sizes have many more entries

    test-train split used is 80-20
    """
    training_cutoff = 0.8
    sequences = [generate_index_sequences(num_items, training_cutoff) for num_items in multi_list_counts]
    

    #for each cart size index, get the training indices
    #then, get all combos indicated by the training indices
    combos_training = [combos_multi_list[cart_size_index][training_combo_index]
                       for cart_size_index in range(max_combo) #size of cart - 1
                       for training_combo_index in sequences[cart_size_index][0] #training_indices for this cart size
                       ]
    
    #similarly, for each cart index, get the testing indices
    #then, get all combos indicated by the testing indices
    combos_testing = [combos_multi_list[cart_size_index][testing_combo_index]
                      for cart_size_index in range(max_combo) #size of cart - 1
                      for testing_combo_index in sequences[cart_size_index][1] #testing_indices for this cart size
                      ]
    
    """
    return
    the combos in the training list,
    the combos in the testing list,
    the conversion from combo to one-hot encoding vector,
    and the conversion from combo to modified frequency vector
    """
    return combos_training, combos_testing, combo_to_vec_representation, combo_to_suggested_item_frequencies



"""
given a max cart size,

create a fair 80-20 split for each possible period and day type combination

save as a dictionary
keys are period and day combinations
value is the tuple of 4 items created with fair_80_20_split
"""
def get_all_model_data(max_combo):
    print("get_all_model_data")
    return {(in_period, in_day_type):fair_80_20_split(in_period, in_day_type, max_combo)
            for in_period in period_day_options
            for in_day_type in day_type_options}

    

"""
data needs to be a matrix, with
    samples as rows
    features as columns

"""

"""
given a list of cart combinations,
the conversion from combos to one-hot encodings,
and the conversion from combos to modified frequencies,

create an input and output matrix
"""
def convert_to_matrix(combos_list, combos_to_one_hot, combos_to_frequencies):
    print("convert_to_matrix")
    #for each combo, get the list of vectors and convert to a matrix
    input_matrix = np.array([combos_to_one_hot[combo].tolist() for combo in combos_list])

    output_matrix = np.array([combos_to_frequencies[combo].tolist() for combo in combos_list])

    return input_matrix, output_matrix


"""
given a tuple split_data produced by fair_80_20_split,

create the training and testing matrices

training_matrices is a tuple of 2 matrices
testing_matrices is a tuple of 2 matrices

testing is produced before training because it has less entries
"""
def split_data_to_matrices(split_data):
    print("split_data_to_matrices")
    combos_training, combos_testing, combo_to_vec_representation, combo_to_suggested_item_frequencies = split_data
    
    print("creating testing matrices")
    testing_matrices = convert_to_matrix(combos_testing, combo_to_vec_representation, combo_to_suggested_item_frequencies)
    
    print("creating training matrices")
    training_matrices = convert_to_matrix(combos_training, combo_to_vec_representation, combo_to_suggested_item_frequencies)
    
    return training_matrices, testing_matrices


    

"""
given a max cart size,

create a training and testing matrices for both the input and the output of the model,
under an 80-20 split
"""
def all_model_data_to_matrices(max_combo):
    print("all_model_data_to_matrices")

    #get the dictionary converting from period and day type combinations to 80-20 split vectors and dictionaries
    all_data = get_all_model_data(max_combo)

    #all_data is a dictionary of fair_80_20_split outputs
    


    #get all period and day type combinations
    data_keys = list(all_data.keys())
    
    #for each tuple in the all_data dictionary, convert that tuple into the 4 matrices
    all_matrices = {key:split_data_to_matrices(all_data[key]) for key in data_keys}
    
    #separate the training and testing matrices
    all_training_matrices = {key:all_matrices[key][0] for key in data_keys}
    all_testing_matrices = {key:all_matrices[key][1] for key in data_keys}
    
    
    #separate the input and output matrices
    all_training_input_matrices = {key:all_training_matrices[key][0] for key in data_keys}
    all_training_output_matrices = {key:all_training_matrices[key][1] for key in data_keys}
    
    all_testing_input_matrices = {key:all_testing_matrices[key][0] for key in data_keys}
    all_testing_output_matrices = {key:all_testing_matrices[key][1] for key in data_keys}

    #values of these 4 dictionaries are matrices
    
    """
    for each matrix type and each period and day type combination,
    combine the individual matrices into a single matrix
    """
    training_input_matrix = np.concatenate(tuple(all_training_input_matrices.values()), axis=0)
    training_output_matrix = np.concatenate(tuple(all_training_output_matrices.values()), axis=0)
    
    testing_input_matrix = np.concatenate(tuple(all_testing_input_matrices.values()), axis=0)
    testing_output_matrix = np.concatenate(tuple(all_testing_output_matrices.values()), axis=0)
    
    #output the 4 matrices to be used in model training
    return training_input_matrix, training_output_matrix, testing_input_matrix, testing_output_matrix



"""
given a max cart size,

create the 4 matrices for model training, and save them out as pickle files
"""
def save_all_data_matrices(max_combo):
    print("save_all_data_matrices")
    x_train, y_train, x_test, y_test = all_model_data_to_matrices(max_combo)

    print("x_train, y_train, x_test, y_test")
    print(x_train.shape)
    print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)
    print()
    print()
    print()


    pickle_item(x_train,"x_train_"+str(max_combo))
    pickle_item(y_train,"y_train_"+str(max_combo))
    pickle_item(x_test,"x_test_"+str(max_combo))
    pickle_item(y_test,"y_test_"+str(max_combo))