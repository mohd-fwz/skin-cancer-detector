import tensorflow as tf
import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

MODEL_PATH = "model/final_model.keras"
CONF_THRESH = 0.60
OUTPUT_DIR = "static/images/gradcam"

labels = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']
label_full = {
    'akiec': 'Actinic Keratoses / Intraepithelial Carcinoma',
    'bcc': 'Basal Cell Carcinoma',
    'bkl': 'Benign Keratosis',
    'df': 'Dermatofibroma',
    'mel': 'Melanoma',
    'nv': 'Melanocytic Nevus',
    'vasc': 'Vascular Lesion'
}

os.makedirs(OUTPUT_DIR, exist_ok=True)
model = load_model(MODEL_PATH)
backbone = model.get_layer("MobileNetV3Large")

def find_last_conv(backbone):
    last = None
    for layer in backbone.layers:
        if isinstance(layer, tf.keras.layers.Conv2D):
            last = layer
    if last is None:
        raise ValueError("No Conv2D found.")
    return last

LAST_CONV_LAYER = find_last_conv(backbone)
print("Using conv layer:", LAST_CONV_LAYER.name)

def generate_gradcam(model, img_tensor, target_layer):
    img_tensor = tf.convert_to_tensor(img_tensor, dtype=tf.float32)


    outputs = {}

    def grab_output(layer, args, ret):
        outputs["conv"] = ret


    target_layer._output_hook = target_layer.call
    def patched_call(*args, **kwargs):
        ret = target_layer._output_hook(*args, **kwargs)
        outputs["conv"] = ret
        return ret
    target_layer.call = patched_call


    with tf.GradientTape() as tape:
        tape.watch(img_tensor)
        preds = model(img_tensor)
        class_idx = tf.argmax(preds[0])
        score = preds[:, class_idx]


    target_layer.call = target_layer._output_hook

    conv_out = outputs["conv"]
    grads = tape.gradient(score, conv_out)
    pooled = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv = conv_out[0].numpy()
    pooled = pooled.numpy()

    for i in range(conv.shape[-1]):
        conv[:, :, i] *= pooled[i]

    heat = np.mean(conv, axis=-1)
    heat = np.maximum(heat, 0)
    heat /= (heat.max() + 1e-7)
    return heat

def overlay_heatmap(orig, heat):
    heat = cv2.resize(heat, (orig.shape[1], orig.shape[0]))
    heat = np.uint8(255 * heat)
    heat_color = cv2.applyColorMap(heat, cv2.COLORMAP_JET)
    return cv2.addWeighted(orig, 0.6, heat_color, 0.4, 0)

def predict_with_gradcam(path):
    img = load_img(path, target_size=(256, 256))
    arr = (img_to_array(img) / 127.5) - 1.0
    batch = np.expand_dims(arr, 0)

    preds = model.predict(batch)[0]
    idx = np.argmax(preds)
    conf = float(preds[idx])

    heat = generate_gradcam(model, batch, LAST_CONV_LAYER)
    orig = cv2.cvtColor(img_to_array(img).astype("uint8"), cv2.COLOR_RGB2BGR)
    result = overlay_heatmap(orig, heat)

    fname = os.path.basename(path).split(".")[0] + "_gradcam.jpg"
    save_path = os.path.join(OUTPUT_DIR, fname)
    cv2.imwrite(save_path, result)

    return {
        "prediction": label_full[labels[idx]],
        "confidence": round(conf, 4),
        "above_threshold": conf >= CONF_THRESH,
        "gradcam_path": save_path
    }