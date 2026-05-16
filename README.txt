run the command "python interactive_cart.py" in the command line to engage with a simulated online purchasing interface
	does not allow for removal of items in the cart
	
	if you would like to change the items in the cart, you will need to force exit the program (or tell it you are done shopping) and run it again
	
	see "items_list.txt" for full list of items and their IDs
	
	ONLY TYPE IN NUMBERS

---

csv of the dataset is stored in the "archive" folder
	"bakery_sales_revised.csv" is the one used in the python files

dataset source:
	https://www.kaggle.com/datasets/akashdeepkuila/bakery?resource=download


python files
	get_items_list.py
		prints out a list of all the purchase items in the dataset
	
	dataframe_to_matrices.py
		turns the dataset into matrices to use for training the model
	
	matrix_creation_functions.py
		used by dataframe_to_matrices.py
	
	matrix_functions_examples.py
		shows an example of what the functions in matrix_creation_functions.py do
	
	matrices_to_model.py
		turns the matrices into a trained model
	
	interactive_cart.py
		user interface to let the user fill their cart and see the top suggestions
	
	see_model_parameters.py
		loads a trained model
			see the number of parameters in that model
			see the maximum and minimum parameter values in that model for each layer and the model as a whole

for any python file, the comment "#TO EDIT BY USER" indicates a spot where the user can edit hyperparameters


h5 files
	already trained models

png files
	plots of the training process for the provided h5 models

pickle files
	the training and testing input and out matrices used to create the provided h5 models

zip files
	due to Github file upload size restrictions, some of the pickle files needed to be zipped
		if you want to use these, unzip them and move them to the folder containing the python files
	
	one pickle file was still too large to upload even after zipping. the zip of that pickle file is located at this Google Drive link:
		https://drive.google.com/file/d/1EzJjvNbnQlL0TQ6OcCGy1QzYbmHZ660V/view?usp=sharing