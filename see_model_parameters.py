#Philip Mascaro


from tensorflow.keras.models import load_model
import numpy as np



#load model
#TO EDIT BY USER
#these can be modified to load the desired model
max_combo = 3
model_type = "cce"
is_provided = True #make this False if you want to run a model you created



provided_string = ""
if is_provided:
    provided_string = "_provided"

model = load_model("my_model_"+str(max_combo)+"_"+model_type+provided_string+".h5")

#show model summary
model.summary()

#show min and max weights in the model
min_weights = []
max_weights = []
for layer in model.layers:
    for i in layer.get_weights():
        print(np.min(i), np.max(i))
        min_weights = min_weights + [np.min(i)]
        max_weights = max_weights + [np.max(i)]

print()
print("min val",min(min_weights))
print("max val",max(max_weights))