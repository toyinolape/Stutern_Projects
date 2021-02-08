#Import necessary libraries
from flask import Flask, render_template, request
 
import numpy as np
import os
 
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
 
#load model
model =load_model("model/dog_or_cat_predictor_bestv1.h5")
 
print('@@ Model loaded')
 
 
def pred_dog_cat(imagefile):
  test_image = load_img(imagefile, target_size = (150, 150)) # load image 
  print("@@ Got Image for prediction")
   
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
   
  result = model.predict(test_image).round(3) # predict class dog or cat
  print('@@ Raw result = ', result)
   
  pred = np.argmax(result) # get the index of max value
 
  if pred == 1:
    return "Dog" # if index 0 
  else:
    return "Cat" # if index 1
 
#------------>>dog cat prediction<<--end
     
 
# Create flask instance
app = Flask(__name__)
 
# render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('index.html')
     
   
@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] # fetch input
        filename = file.filename        
        print("@@ Input posted = ", filename)
         
        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)
 
        print("@@ Predicting class......")
        pred = pred_dog_cat(imagefile=file_path)
               
        return render_template('predict.html', pred_output = pred, user_image = file_path)
     
#Fo local system
if __name__ == "__main__":
    app.run(threaded=False,) 
     
# #Fo AWS cloud
# if __name__ == "__main__":
#     app.run(host='0.0.0.0.0', post='8080',threaded=False,)