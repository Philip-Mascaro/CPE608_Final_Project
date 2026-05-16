#Philip Mascaro



import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

#use student ID as random seed
tf.random.set_seed(10458430)
np.random.seed(10458430)


#need this for loading in the matrices for training
import pickle


def de_pickle_item(location_of_pickle):
    pickle_name = location_of_pickle + ".pickle"
    pickle_read = open(pickle_name,"rb")
    de_pickled_item = pickle.load(pickle_read)
    return de_pickled_item


import datetime



#load in the matrices that were previously created and show their shapes
def load_all_data_matrices(max_combo, is_provided):
    provided_string = ""
    if is_provided:
        provided_string = "_provided"
    x_train = de_pickle_item("x_train_"+str(max_combo)+provided_string)
    y_train = de_pickle_item("y_train_"+str(max_combo)+provided_string)
    x_test = de_pickle_item("x_test_"+str(max_combo)+provided_string)
    y_test = de_pickle_item("y_test_"+str(max_combo)+provided_string)

    
    print("x_train, y_train, x_test, y_test")
    print(x_train.shape)
    print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)
    print()
    print()
    print()

    return x_train, y_train, x_test, y_test




def create_model(in_size, out_size):
    #create a sequential model with dropout layers for better regularization
    #model of this style is useful for problems such as the MNIST dataset for predicting handwritten digits
    model = Sequential([
        Dense(512, activation='relu', input_shape=(in_size,)),
        Dropout(0.2),
        Dense(256, activation='relu'),
        Dropout(0.2),
        Dense(128, activation='relu'),
        Dropout(0.2),
        Dense(out_size, activation='softmax')
    ])

    #compile the model
    model.compile(
        optimizer='adam',
        #TO EDIT BY USER
        #options tested are 'mse' and 'categorical_crossentropy'
        loss='mse',#'categorical_crossentropy',
        metrics=['accuracy']
    )
    return model


def train_model(max_combo, is_provided, my_epochs, my_batch_size):
    #load in the bakery data matrices
    x_train, y_train, x_test, y_test = load_all_data_matrices(max_combo, is_provided)


    #log the start time for training the model and display
    start_time = datetime.datetime.now()
    print("start time:",start_time)

    #create the model and train it on the bakery data
    model = create_model(x_train.shape[1],y_train.shape[1])
    history = model.fit(
        x_train, y_train,
        validation_data=(x_test, y_test),
        epochs=my_epochs,
        batch_size=my_batch_size,
        verbose=1
    )

    #log the end time for training the model and display both the start and end times
    end_time = datetime.datetime.now()
    print("start time:",start_time)
    print("end time:",end_time)
    
    #calculate time elapsed for training the model and display in terms of seconds, minutes, and hours
    time_elapsed = (end_time - start_time).total_seconds()
    print("time elapsed in seconds:",time_elapsed)
    print("time elapsed in minutes:",time_elapsed/60)
    print("time elapsed in hours:",time_elapsed/(60*60))

    #evaluate the model
    scores = model.evaluate(x_test, y_test, verbose=0)
    print(f"Test accuracy: {scores[1]*100:.2f}%")

    #plot the training history of the model, accuracy and loss
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.tight_layout()
    #save the plot
    #TO EDIT BY USER
    #use "mse" or "cce", make sure it matches with the loss function you selected aboce
    model_type = "mse"

    
    provided_string = ""
    if is_provided:
        provided_string = "_provided"

    plt.savefig("Model_plots__max_combo_"+str(max_combo)+"__epochs_"+str(my_epochs)+"__batch_size_"+str(my_batch_size)+"__"+model_type+provided_string)

    #save the model itself
    model.save("my_model_"+str(max_combo)+"_"+model_type+provided_string+".h5")


#set up hyperparameters for model training and train model
#TO EDIT BY USER
#these can be modified
max_existing_cart_size = 3
user_epochs = 20*4
user_batch_size = 128
already_provided = True #make this False if you want to run a model using matrices you created
train_model(max_existing_cart_size, already_provided, user_epochs, user_batch_size)