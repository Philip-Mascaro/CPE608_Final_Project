#Philip Mascaro


import pandas as pd
from itertools import combinations
import numpy as np
np.random.seed(10458430)

from matrix_creation_functions import (subset_dataframe_list,
                                       get_transaction_nums,
                                       paired_purchase_dataframe,
                                       paired_purchases_only,
                                       pairings_with_counts,
                                       dict_all_entries,
                                       item_combos,
                                       convert_to_vector,
                                       convert_to_frequency,
                                       generate_basic_in_out_pair,
                                       get_all_dicts,
                                       new_frequencies_dict,
                                       fair_80_20_split,
                                       get_all_model_data,
                                       split_data_to_matrices,
                                       all_model_data_to_matrices
                                       )


jam_bread_morning_weekend = subset_dataframe_list(tuple(["Jam", "Bread"]), "morning", "weekend")

print("jam_bread_morning_weekend")
print(jam_bread_morning_weekend)
print()
print()
print()
print()


jam_bread_morning_weekend_nums = get_transaction_nums(tuple(["Jam", "Bread"]), "morning", "weekend")

print("jam_bread_morning_weekend_nums")
print(jam_bread_morning_weekend_nums)
print()
print()
print()
print()

               
                  
jam_bread_morning_weekend_transactions = paired_purchase_dataframe(tuple(["Jam", "Bread"]), "morning", "weekend")

print("jam_bread_morning_weekend_transactions")
print(jam_bread_morning_weekend_transactions)
print()
print()
print()
print()



jam_bread_morning_weekend_pairings = paired_purchases_only(tuple(["Jam", "Bread"]), "morning", "weekend")

print("jam_bread_morning_weekend_pairings")
print(jam_bread_morning_weekend_pairings)
print()
print()
print()
print()



jam_bread_morning_weekend_pair_counts = pairings_with_counts(tuple(["Jam", "Bread"]), "morning", "weekend")

print("jam_bread_morning_weekend_pair_counts")
print(jam_bread_morning_weekend_pair_counts)
print()
print()
print()
print()


jam_morning_weekend_pair_counts = pairings_with_counts(tuple(["Jam"]), "morning", "weekend")

print("jam_morning_weekend_pair_counts")
print(jam_morning_weekend_pair_counts)
print()
print()
print()
print()



bread_morning_weekend_pair_counts = pairings_with_counts(tuple(["Bread"]), "morning", "weekend")

print("bread_morning_weekend_pair_counts")
print(bread_morning_weekend_pair_counts)
print()
print()
print()
print()



coffee_morning_weekend_pair_counts = pairings_with_counts(tuple(["Coffee"]), "morning", "weekend")

print("coffee_morning_weekend_pair_counts")
print(coffee_morning_weekend_pair_counts)
print()
print()
print()
print()



jam_bread_coffee_morning_weekend_pair_counts = pairings_with_counts(tuple(["Jam", "Bread", "Coffee"]), "morning", "weekend")

print("jam_bread_coffee_morning_weekend_pair_counts")
print(jam_bread_coffee_morning_weekend_pair_counts)
print()
print()
print()
print()



none_morning_weekend_pair_counts = dict_all_entries("morning", "weekend")

print("none_morning_weekend_pair_counts")
print(none_morning_weekend_pair_counts)
print()
print()
print()
print()


combos_3 = item_combos(3)

print("len(combos_3)")
print(len(combos_3))
print()
for i in combos_3:
    print(len(i))
print()


none_morning_weekend_vector = convert_to_vector(tuple([]), "morning", "weekend")

none_night_weekend_vector = convert_to_vector(tuple([]), "night", "weekend")

none_afternoon_weekday_vector = convert_to_vector(tuple([]), "afternoon", "weekday")

print("none_morning_weekend_vector")
print(none_morning_weekend_vector)
print()
print("none_night_weekend_vector")
print(none_night_weekend_vector)
print()
print("none_afternoon_weekday_vector")
print(none_afternoon_weekday_vector)
print()

jam_bread_coffee_morning_weekend_vector = convert_to_vector(tuple(["Jam", "Bread", "Coffee"]), "morning", "weekend")

print("jam_bread_coffee_morning_weekend_vector")
print(jam_bread_coffee_morning_weekend_vector)
print()



jam_bread_coffee_morning_weekend_freq = convert_to_frequency(jam_bread_coffee_morning_weekend_pair_counts)

print("jam_bread_coffee_morning_weekend_freq")
print(jam_bread_coffee_morning_weekend_freq)
print()
print()
print()
print()



jam_bread_coffee_morning_weekend_in_out = generate_basic_in_out_pair(tuple(["Jam", "Bread", "Coffee"]), "morning", "weekend")

print("jam_bread_coffee_morning_weekend_in_out")
for i in jam_bread_coffee_morning_weekend_in_out:
    print(i)
    print()
    print()



jbc = tuple(["Jam", "Bread", "Coffee"])

subcarts_multi = [list(combinations(jbc, i)) for i in range(1,len(jbc)+1)]
subcarts = []
for i in subcarts_multi:
    subcarts = subcarts + i

jam_bread_coffee_morning_weekend_all_dicts = get_all_dicts(subcarts, "morning", "weekend")

print("jam_bread_coffee_morning_weekend_all_dicts")
for i in jam_bread_coffee_morning_weekend_all_dicts:
    print(i)
    print()
    print()


default_suggestion_vector = convert_to_frequency(dict_all_entries("morning", "weekend"))
jam_bread_coffee_morning_weekend_new_freq = new_frequencies_dict(subcarts, "morning", "weekend", default_suggestion_vector)

print("jam_bread_coffee_morning_weekend_new_freq")
for i in jam_bread_coffee_morning_weekend_new_freq:
    print(i)
    print()
    print()



print("jam_bread_coffee_morning_weekend_all_dicts[1][jbc]")
print(jam_bread_coffee_morning_weekend_all_dicts[1][jbc])
print()
print("jam_bread_coffee_morning_weekend_new_freq[1][jbc]")
print(jam_bread_coffee_morning_weekend_new_freq[1][jbc])
print()
print()
print()
print()



morning_weekend_80_20 = fair_80_20_split("morning", "weekend", 1)
print("morning_weekend_80_20")
print(len(morning_weekend_80_20[0]))
print(len(morning_weekend_80_20[1]))
print()
print()
print()



all_data_test = get_all_model_data(1)
all_data_test_vals = all_data_test.values()
print("all_data_test")
for i in all_data_test_vals:
    print(len(i[0]))
    print(len(i[1]))
print()
print()
print()
    


morning_weekend_80_20_matrices = split_data_to_matrices(morning_weekend_80_20)

print("morning_weekend_80_20_matrices")
for i in morning_weekend_80_20_matrices:
    for j in i:
        print(j.shape)
print()
print()
print()


x_train, y_train, x_test, y_test = all_model_data_to_matrices(1)

print("x_train, y_train, x_test, y_test")
print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)
print()
print()
print()