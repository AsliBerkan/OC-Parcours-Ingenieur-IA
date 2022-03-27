from flask import Flask, render_template, request, send_file, url_for
#import tensorflow as tf
import segmentation_models as sm
import glob
#import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core import Workspace
#from azureml.core.model import Model
from dotenv import load_dotenv
#from io import BytesIO
import io
import json
from azureml.core.webservice import Webservice

app = Flask(__name__)

# Use local model
sm.set_framework('tf.keras')
sm.framework()
mean_iou = sm.metrics.IOUScore()
mean_dice = sm.metrics.FScore(beta=1)
mean_dice_loss = sm.losses.DiceLoss()
#unet_VGG16 = tf.keras.models.load_model('Models/0_final/unetVgg16final.h5',
#                                 	      custom_objects={'f1-score':mean_dice,
#                                                	      'iou_score':mean_iou,
#							      'dice_loss':mean_dice_loss})

print('récup clé           ...........................')
print(load_dotenv())

# Use Azure ML Service Principal Authentication (not working)
AZUREML_PASSWORD = os.getenv("AZUREML_PASSWORD")
my_tenant_id = os.getenv("my_tenant_id")
my_app_id  = os.getenv("my_app_id")
SUSCRIPTION_ID = os.getenv("SUSCRIPTION_ID")
RESOURCE_GROUP = os.getenv("RESOURCE_GROUP")
WORKSPACE_NAME = os.getenv("WORKSPACE_NAME")

svc_pr = ServicePrincipalAuthentication(
    tenant_id=my_tenant_id,
    service_principal_id=my_app_id,
    service_principal_password=AZUREML_PASSWORD)

ws = Workspace(
    subscription_id=SUSCRIPTION_ID ,
    resource_group=RESOURCE_GROUP,
    workspace_name=WORKSPACE_NAME ,
    auth=svc_pr
    )

print("Found workspace {} at location {}".format(ws.name, ws.location))

# Get service from ws
service = Webservice(workspace=ws, name='myservice')

print("Found service on ws")

# Use Azure ML Interactive Authentication
#ws = Workspace.from_config()
#print("Found workspace {} at location {}".format(ws.name, ws.location))

#model_path = Model.get_model_path(model_name='unet_vgg16')
#unet_VGG16 = tf.keras.models.load_model(model_path,
#                                        custom_objects={'f1-score':mean_dice,
#                                                        'iou_score':mean_iou,
#                                                        'dice_loss':mean_dice_loss})

#def serve_pil_image(pil_img):
#    img_io = BytesIO()
#    pil_img.save(img_io, 'JPEG', quality=70)
#    img_io.seek(0)
#    return send_file(img_io, mimetype='image/jpeg')




#@app.route('/')
#def index():
#    return "Hello world !"

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/predict_mask', methods = ['POST'])
def predict_mask():
    # Obtenir le path de l'image
    image_dict = request.form.to_dict()
    path = "dlapp/static/imTest/"
    fin_path = '_leftImg8bit.png'
    id_image = image_dict['ID Image']
    im_path = glob.glob(path + id_image + fin_path, recursive = True)
    print(im_path)
    
    # Importer l'image
    im = Image.open(im_path[0])
    im = im.resize(size=(256, 256), resample=Image.NEAREST)
    im = np.array(im)/255.
    
    # Sérialiser pour envoie au service
    memfile = io.BytesIO()
    np.save(memfile, im)
    memfile.seek(0)
    serialized = json.dumps(memfile.read().decode('ISO-8859-1'))
    
    # Envoie à l'endpoint
    #service = Webservice(workspace=ws, name='myservice')
    y_hat = service.run(input_data=serialized)
    
    # test deserialised
    memfile = io.BytesIO()
    memfile.write(json.loads(y_hat).encode('ISO-8859-1'))
    memfile.seek(0)
    predicted_mask = np.load(memfile)
    
    # Save image to static folder
    fin_path_mask = '_predicted_mask.png'
    plt.imsave(path + id_image + fin_path_mask, predicted_mask)
    
    return render_template('predict.html',
                           original_image = url_for('static', filename='imTest/' + id_image + fin_path),
                           mask_pred = url_for('static', filename='imTest/' + id_image + fin_path_mask))

#if __name__ == "__main__":
#    app.run()
