import io
import os
import urllib.parse
import json
from sahi.slicing import slice_coco
import cv2 as cv
from handler.file_handler import FileOsHandler
import pathlib

local_appdata = os.environ.get('LOCALAPPDATA')
app_folder = pathlib.Path(f"{local_appdata}/interpret_extract_system")

class IO():
    """
    The IO class is mainly used to transfer a coco dataset from label studio,
    to a normal yolov8 dataset. The functionalities are very precise in their execution.

    It basically slices all the images that have been labeled, removes the images that have no label, 
    Uses the original json coco file where all the labels and images have been documented and creates
    new .txt files with all the coordinates and labels of the sliced images, before removing the empty images.
    This then creates a new dataset, which still has to be manually transferred over to a yolov8 dataset folder structure.
    Or can be used as is, depending on how you created your map structure. 
    """
    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback

    def slice_sahi(self, json_to_change: str, cleaned_json_output: str, dir_images_to_slice: str, width_in_pix: int = False,
                   slicing_width: int = False, slicing_height: int = False):
        
        """
        This function is responsible for cutting up the images into tiles and inserting
        the new positions of these tiles into a new json file. The same goes for the coordinates
        of the labels, which now correspond to their respective tile.
        """

        if self.progress_callback:
            self.progress_callback(0, "Preparing dataset... %p%")

        FileOsHandler().create_dir(app_folder, 'dataset')
        dataset_folder = app_folder / 'dataset'

        input_json = json_to_change
        cleaned_json = dataset_folder / f'{cleaned_json_output}.json'
        image_dir = dir_images_to_slice
        output_dir = dataset_folder / "images/"
        width = 1500 if not width_in_pix else width_in_pix
        slice_w = 640 if not slicing_width else slicing_width
        slice_h = 640 if not slicing_height else slicing_height

        try:
            with open(input_json, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"The given path: {input_json} : is invalid.")
            return
        
        if not FileOsHandler().create_dir(dataset_folder, "images"):
            print("This archiving name already exists, choose another name.")
            return

        new_images = []
        valid_image_ids = set()

        image_amount = len(data['images'])

        for i, img in enumerate(data['images']):
            # 1. Bestandsnaam opschonen
            raw_name = img['file_name'].split('%5C')[-1].split('/')[-1].split('\\')[-1]
            if '__' in raw_name:
                original_name = raw_name.split('__')[-1]
            else:
                original_name = raw_name
            
            img['file_name'] = original_name
            
            # 2. Breedte/Hoogte checken (met fallback)
            w = img.get('width')
            
            # Als breedte ontbreekt in JSON, probeer het bestand te openen
            if w is None:
                file_path = os.path.join(image_dir, original_name)
                if os.path.exists(file_path):
                    temp_img = cv.imread(file_path)
                    if temp_img is not None:
                        w = temp_img.shape[1]
                        img['width'] = w
                        img['height'] = temp_img.shape[0]
                    else:
                        print(f"Warning: can't read {original_name}.")
                        continue
                else:
                    print(f"Warning: {original_name} could not be found.")
                    continue

            # 3. FILTER: Alleen afbeeldingen groter dan 1500px
            if w > width:
                new_images.append(img)
                valid_image_ids.add(img['id'])

            if self.progress_callback:
                percentage = int((i / image_amount) * 100)
                self.progress_callback(percentage, "Extracted data, ready to slice... %p%")

        # Update de data
        data['images'] = new_images
        categories = [c['name'] for c in data['categories']]
        self.__extract_categories(categories=categories)
        data['annotations'] = [a for a in data['annotations'] if a['image_id'] in valid_image_ids]

        with open(cleaned_json, 'w') as f:
            json.dump(data, f)

        print(f"Done! saved {len(new_images)} big images.")

        slice_coco(
            coco_annotation_file_path=cleaned_json, # De opgeschoonde JSON van de vorige stap
            image_dir=image_dir,
            output_dir=output_dir,
            output_coco_annotation_file_name="tiled_annotations.json", # DIT ONTBRAK
            slice_height=slice_h,
            slice_width=slice_w,
            overlap_height_ratio=0.2,
            overlap_width_ratio=0.2,
            ignore_negative_samples=True,
        )

        self.__coco_labeling("images")

    # slice_sahi()

    def __coco_labeling(self, json_coco: str):
        """
        This function creates label files for each new sliced tile.
        """
        if self.progress_callback:
            self.progress_callback(0, "Readying Labels... %p%")

        dataset_folder = app_folder / 'dataset'
        tiled_json = dataset_folder / f'{json_coco}/tiled_annotations.json_coco.json'
        output_label_dir = dataset_folder / 'labels/'

        os.makedirs(output_label_dir, exist_ok=True)

        with open(tiled_json, 'r') as f:
            data = json.load(f)

        # Maak een dictionary voor snelle lookup van afbeeldingen
        images = {img['id']: img for img in data['images']}

        amount_of_annotations = len(data['annotations'])
        for i, ann in enumerate(data['annotations']):
            img = images[ann['image_id']]
            file_name = os.path.splitext(img['file_name'])[0] + ".txt"
            
            # Verkrijg de 4 hoekpunten (segmentation in COCO is vaak de OBB)
            # COCO segmentation: [x1, y1, x2, y2, x3, y3, x4, y4]
            seg = ann['segmentation'][0]
            
            # Normaliseren voor YOLO (waardes tussen 0 en 1)
            w, h = img['width'], img['height']
            normalized_seg = []
            for i in range(0, len(seg), 2):
                normalized_seg.append(str(seg[i] / w))   # X
                normalized_seg.append(str(seg[i+1] / h)) # Y
            
            line = f"{ann['category_id']} " + " ".join(normalized_seg) + "\n"
            
            with open(os.path.join(output_label_dir, file_name), 'a') as f:
                f.write(line)

            if self.progress_callback:
                percentage = int((i / amount_of_annotations) * 100)
                self.progress_callback(percentage, "Finished Labeling... %p%")

        print("Done! the labels should be in the 'labels' directory.")

        self.__coco_jpg_removal(json_coco)

    def __coco_jpg_removal(self, dir_name: str):
        """
        This function removes all the tiles that are empty.
        """

        if self.progress_callback:
            self.progress_callback(0, "Optional jpg removal... %p%")

        dataset_folder = app_folder / 'dataset'
        image_dir = dataset_folder / f'{dir_name}/'
        label_dir = dataset_folder / 'labels/'

        valid_names = {os.path.splitext(f)[0] for f in os.listdir(label_dir) if f.endswith('.txt')}

        amount_image = len(os.listdir(image_dir))
        count = 0
        for img_file in os.listdir(image_dir):
            if img_file.endswith(('.jpg', '.jpeg', '.png')):
                name = os.path.splitext(img_file)[0]
                if name not in valid_names:
                    os.remove(os.path.join(image_dir, img_file))
                    count += 1
            
            if self.progress_callback:
                percentage = int((count / amount_image) * 100)
                self.progress_callback(percentage, "Images removed... %p%")

        print(f"Done! removed {count} empty images. Now you should have a clean dataset.")

    
    def __extract_categories(self, categories: list):
        """
        This function extracts the categories from the json
        and places them into a new classes.txt. 
        """
        if not categories:
            return 
        
        dataset_folder = app_folder / 'dataset'

        try:
        
            with open(f"{dataset_folder}/classes.txt", 'w') as file:
                for item in categories:
                    file.write(item + "\n")
        
        except Exception as ex:
            print(ex)
