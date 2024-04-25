# remove tmp file
import os
import sys
import torch
from PIL import Image, ImageDraw
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
from exception import CustomException

class PredictPipeline:
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
                    outputs = model(**inputs),
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

            return images, results


        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    def __init__(self, tmp_path):
        """
        From a directory path (where images are stored)
        creates a list of image objects
        """
        self.image_paths = list()
        for idx, (tmp_dir, _, images) in enumerate(os.walk(tmp_path)):
            single_image_path = os.path.join(tmp_dir, images[idx])
            self.image_paths.append(single_image_path)

    def get_data(self): 
        try:
            images = [Image.open(img).convert('RGB') for img in self.image_paths]

            return images

        except Exception as e:
            raise CustomException(e, sys)
        
#if __name__ == "__main__":
#    print('hi')