#Philip Mascaro




#DATA SOURCE:
#https://www.kaggle.com/datasets/akashdeepkuila/bakery?resource=download


import datetime

#log the start time and display
start_time = datetime.datetime.now()
print("start time:",start_time)

from matrix_creation_functions import save_all_data_matrices


#choose a max cart size and save out the data
max_existing_cart_size = 3
save_all_data_matrices(max_existing_cart_size)


#log the end time and display both the start and end times
end_time = datetime.datetime.now()
print("start time:",start_time)
print("end time:",end_time)


#calculate time elapsed and display in terms of seconds, minutes, and hours
time_elapsed = (end_time - start_time).total_seconds()
print("time elapsed in seconds:",time_elapsed)
print("time elapsed in minutes:",time_elapsed/60)
print("time elapsed in hours:",time_elapsed/(60*60))