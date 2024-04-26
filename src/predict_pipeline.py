"""
Pipeline for generating images with object detection 
bounding boxes and object detection results from addresses.
"""
import os
import sys
import shutil
import torch
from PIL import Image, ImageDraw
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
from src.exception import CustomException

class PredictPipeline:
    """
    Predict Pipeline
    """
    def __init__(self):
        pass

    def predict(self, images):
        """
        From a list of image objects, returns the images with 
        drawn bounding boxes and object detection results.
        """
        try:
            # Load the model and processor
            check_point = "google/owlv2-base-patch16-ensemble"
            model = AutoModelForZeroShotObjectDetection.from_pretrained(check_point)
            processor = AutoProcessor.from_pretrained(check_point)


            # Define objects to identify
            queries = ['solar panel', 'pool']
            inputs = processor(text=queries, images=images, return_tensors='pt')

            # Pass images to the model
            with torch.no_grad():
                outputs = model(**inputs)
                target_sizes = torch.tensor([img.size[::-1] for img in images])
                results = processor.post_process_object_detection(
                    outputs,
                    threshold = 0.3,
                    target_sizes=target_sizes
                )

            # Draw bounding boxes
            for idx, img in enumerate(images):
                draw = ImageDraw.Draw(img)

                scores = results[idx]['scores'].tolist()
                labels = results[idx]['labels'].tolist()
                boxes = results[idx]['boxes'].tolist()

                for box, score, label in zip(boxes, scores, labels):
                    xmin, ymin, xmax, ymax = box
                    draw.rectangle((xmin, ymin, xmax, ymax), outline="#39ff14", width=2)
                    draw.text((xmin, ymin), f"{queries[label]}: {round(score,2)}", fill="white")

            os.makedirs('static/', exist_ok=True)
            for idx, img in enumerate(images):
                img.save(f'static/img_{idx}.png')

            shutil.rmtree('tmp')

            return images, results

        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    """
    From a tmp directory path, creates a list of image objects
    to be passed to the predict pipeline.
    """
    def __init__(self, tmp_path):
        """
        From a directory path (where images are stored)
        creates a list of image objects
        """
        self.image_paths = list()
        for tmp_dir, _, images in os.walk(tmp_path):
            for img in images:
                single_image_path = os.path.join(tmp_dir, img)
                self.image_paths.append(single_image_path)

    def get_data(self):
        """
        Turns list of image paths to list of image objects
        """
        try:
            images = [Image.open(img).convert('RGB') for img in self.image_paths]

            return images

        except Exception as e:
            raise CustomException(e, sys)

#if __name__ == "__main__":
#    obj = CustomData('../tmp/')
#    img_list = obj.get_data()
#    for i in img_list:
#       print(i)
