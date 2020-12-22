import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers import Adam, SGD
from networks import SSD300_VGG16_ORIGINAL
from losses import SSD_LOSS
from data_generators import SSD_VOC_DATA_GENERATOR
import xml.etree.ElementTree as ET
from tensorflow.keras.callbacks import ModelCheckpoint

if __name__ == "__main__":
    with open("configs/ssd300_vgg16_original.json") as config_file:
        config = json.load(config_file)

    model = SSD300_VGG16_ORIGINAL(config)
    model.compile(
        optimizer=SGD(
            lr=config["training"]["optimizer"]["lr"],
            momentum=config["training"]["optimizer"]["momentum"],
            decay=config["training"]["optimizer"]["decay"],
            nesterov=config["training"]["optimizer"]["nesterov"]
        ),
        loss=SSD_LOSS(
            alpha=config["training"]["alpha"],
            min_negative_boxes=config["training"]["min_negative_boxes"],
            negative_boxes_ratio=config["training"]["negative_boxes_ratio"]
        ).compute
    )

    training_samples = ["data/test.jpg data/test.xml"]
    validation_samples = ["data/test.jpg data/test.xml"]

    history = model.fit(
        x=SSD_VOC_DATA_GENERATOR(
            samples=training_samples,
            config=config
        ),
        batch_size=config["training"]["batch_size"],
        epochs=config["training"]["epochs"],
        steps_per_epoch=len(training_samples)//config["training"]["batch_size"],
        validation_data=SSD_VOC_DATA_GENERATOR(
            samples=validation_samples,
            config=config
        ),
        validation_steps=len(validation_samples)//config["training"]["batch_size"],
        callbacks=[
            ModelCheckpoint(
                'output/cp_{epoch:02d}_{loss:.4f}_{val_loss:.4f}.h5',
                mode='min',
                monitor='val_loss',
                save_weights_only=True,
                verbose=1,
            ),
        ]
    )

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.savefig('output/training_graph.png')
