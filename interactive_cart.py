#Philip Mascaro



import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model



#DATA SOURCE:
#https://www.kaggle.com/datasets/akashdeepkuila/bakery?resource=download

#load data
bakery_data = pd.read_csv("archive/bakery_sales_revised.csv")

#get all column headers
column_headers = bakery_data.columns.tolist()

#remove duplicate rows
bakery_data = bakery_data.drop_duplicates(subset=column_headers, keep="first")

#get the lists of unique items, unique period_day options, and unique weekday_weekend options
item_options = sorted(list(set(bakery_data['Item'].tolist())))
period_day_options = sorted(list(set(bakery_data['period_day'].tolist())))
day_type_options = sorted(list(set(bakery_data['weekday_weekend'].tolist())))


#load model
#TO EDIT BY USER
#these can be modified to load the desired model
max_combo = 2
model_type = "cce"
is_provided = True #make this False if you want to run a model you created



provided_string = ""
if is_provided:
    provided_string = "_provided"

model = load_model("my_model_"+str(max_combo)+"_"+model_type+provided_string+".h5")



#set up empty cart
data_vec = np.zeros(len(item_options) + len(period_day_options) + len(day_type_options)).reshape(1,-1)


#set up a repeating prompt to be used for the day and period types
def user_prompt(list_text, options_list):
    valid_choice_entered = False

    while not valid_choice_entered:
        #ask the user to enter the number corresponding to one of the options from the input list
        print("Available "+list_text+"s:")
        for i in range(len(options_list)):
            print(str(i+1)+"\t"+str(options_list[i]))
        print()
        user_reply = int(input("Enter the number for your "+list_text+": "))-1

        #check for valid user reply
        if 0 <= user_reply and user_reply < len(options_list):
            print()
            print("Selected "+list_text+":",options_list[user_reply])
            valid_choice_entered = True
            print()
            print()
            print()
        else:
            print("That is not a valid choice, please try again")
            print()
    return user_reply


print()
print()
print()
print()
#prompt day type
day_choice = user_prompt("day type", day_type_options)

#update one-hot encoding
data_vec[0][len(item_options) + len(period_day_options) + day_choice] = 1





#prompt period type
period_choice = user_prompt("part of day", period_day_options)

#update one-hot encoding
data_vec[0][len(item_options) + period_choice] = 1


#function for showing the current contents of the user's cart
def display_current_cart():
    cart_string = ""
    cart_count = 0
    #append each item string to the list
    for i in range(len(item_options)):
        if data_vec[0][i] == 1:
            if cart_count > 0:
                cart_string = cart_string + ", "
            cart_string = cart_string + item_options[i]
            cart_count += 1
    #if no items in the cart, display that the cart is empty
    if cart_count == 0:
          cart_string = cart_string + "empty"
    #show the cart items
    print("Current cart: ")
    print(cart_string)
    print()
            


#BEGIN LOOP
cart_size = 0
stop_shopping = False

#while the user is shopping
while cart_size < len(item_options) and not stop_shopping:
    print()
    print()
    print()
    #show the user's cart
    display_current_cart()

    #suggest up to 5 of the most popular items given the user's current cart

    #given the user's current cart, get the frequency predictions from the model
    prediction = model(data_vec)
    usable_prediction_vals = np.array(prediction).reshape(-1)

    #sort the item indices based on the prediction values
    sorted_pred_index = np.argsort(usable_prediction_vals).tolist()
    sorted_pred_index.reverse()


    #as the cart size increases, higher likelyhood to suggest items already in the cart due to the reweighting
    #choose the top 5 cart items that AREN'T already in the cart
    #if the cart is nearly every item, suggest as many items as are available that aren't in the cart

    top_item_count = 5

    suggestion_counter = 0
    skipped_item_count = 0

    top_indices = []

    #while less than the requested suggestion amount OR nearly running out of items to suggest
    while suggestion_counter < top_item_count and suggestion_counter+skipped_item_count < len(item_options):

        #determine the suggestion index
        suggestion_index = suggestion_counter+skipped_item_count
        #get the best suggestion
        best_suggestion = sorted_pred_index[suggestion_index]

        #if the item is already in the cart, move to the next index
        if (data_vec[0][best_suggestion] == 1):
            skipped_item_count += 1
        #otherwise, add the item to the list of suggestions
        else:
            suggestion_counter += 1
            top_indices = top_indices + [best_suggestion]

    #get the strings for the items to suggest
    top_suggestions = [item_options[i] for i in top_indices]

    #show the top suggestions
    num_suggestions = len(top_indices)

    s_string = ""
    if num_suggestions > 1:
        s_string = "s"

    print("Top "+str(num_suggestions)+" suggestion"+s_string+" to add to your cart:")
    print("ID\tItem")
    print()
    for i in range(num_suggestions):
        print(str(top_indices[i]+1)+"\t"+top_suggestions[i])
    print()

    #ask user to enter another item to the cart, or enter 0 to finish shopping
    print("If you would like to add another item to your cart, please enter its item ID")
    print("Otherwise, please enter 0 to proceed to checkout")


    #until the user enters a valid number
    item_valid = False

    while not item_valid:
        #get user input
        user_item_selection = int(input("Item selection: "))

        #if user wants to proceed to checkout, show their final cart and exit loop
        if user_item_selection == 0:
            print("Heading to checkout!")
            display_current_cart()
            stop_shopping = True
            item_valid = True

        else:
            item_index = user_item_selection - 1

            #check if user has selected a valid item
            if not(0 <= item_index and item_index < len(item_options)):
                print("Not a valid item ID, try again")
            else:
                #only allow the user to add items to the cart that they don't already have in the cart
                if data_vec[0][item_index] == 1:
                    print("Your cart already contains '"+item_options[item_index]+"', please add a different item or proceed to checkout")
                else:
                    #add the new item to the cart by setting the indicator and updating the vector
                    item_valid = True
                    data_vec[0][item_index] = 1
                    #increase the cart size by 1
                    cart_size = cart_size + 1

                    #if the cart contains every possible item in the list, proceed to checkout
                    if cart_size == len(item_options):
                        print("You have selected all possible purchasable items")
                        print("Proceeding to checkout")
                        print()
                        display_current_cart()

#LOOP EXITED

#thank the user for shopping
print()
print("Thank you for shopping!")