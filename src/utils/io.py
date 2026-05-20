import io
import os
import urllib.parse
import json
from sahi.slicing import slice_coco
import cv2 as cv
from handler.file_handler import FileOsHandler

label_folder = r'C:/Users/697/projecten/labeling/Big-bulk-dataset/data/labels'
image_folder = r'C:/Users/697/projecten/labeling/Big-bulk-dataset/data/images'

class IO():
    def __init__(self):
        pass

    def __change_label_number():

        with open('C:/Users/697/projecten/labeling/data/labels/fb437a33-021-1.txt') as topo_file:
            for line in topo_file:
                # print(line.split(" ")[0])
                # print(line[0]),
                match line.split(" ")[0]:
                    case "0":
                        print(f"0 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                    case "1":
                        print(f"1 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                    case "4":
                        print(f"2 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                    case "5":
                        print(f"3 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                    case "16":
                        print(f"4 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                    case "17":
                        print(f"5 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                    case "18":
                        print(f"6 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                    case "19":
                        print(f"7 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                    case "20":
                        print(f"8 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                    case "21":
                        print(f"9 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="") 
                    case "22":
                        print(f"10 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                    case "23":
                        print(f"11 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                    case "24":
                        print(f"12 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                    case "30":
                        print(f"13 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                    case "31":
                        print(f"14 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")

    def __change_label_number2():

        with open("C:/Users/697/projecten/labeling/more data/data/labels/fb437a33-021-1.txt") as topo_file:
            for line in topo_file:
                # print(line.split(" ")[0])
                # print(line[0]),
                match line.split(" ")[0]:
                    case "0":
                        print(f"0 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                    case "1":
                        print(f"1 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                    case "4":
                        print(f"2 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                    case "5":
                        print(f"3 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                    case "16":
                        print(f"4 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                    case "17":
                        print(f"5 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                    case "18":
                        print(f"6 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                    case "19":
                        print(f"7 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                    case "20":
                        print(f"8 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                    case "21":
                        print(f"9 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="") 
                    case "22":
                        print(f"10 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                    case "23":
                        print(f"11 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                    case "24":
                        print(f"12 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                    case "30":
                        print(f"13 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                    case "31":
                        print(f"14 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")

    def __change_label_name():
        for filename in os.listdir(label_folder):
            if filename.endswith(".txt"):
                # 1. Decodeer de gekke tekens zoals %5C naar slashes
                decoded_name = urllib.parse.unquote(filename)
                
                # 2. Pak alleen het gedeelte NA de laatste slash of backslash
                # Dit haalt "C:\Users\...\image-0.txt" terug naar "image-0.txt"
                new_name = decoded_name.split('\\')[-1].split('/')[-1]
                
                # Soms zit er nog een '.tmp' of een vraagteken voor, even opschonen
                if '?' in new_name:
                    new_name = new_name.split('?')[-1]
                if '=' in new_name:
                    new_name = new_name.split('=')[-1]

                old_file = os.path.join(label_folder, filename)
                new_file = os.path.join(label_folder, new_name)
                
                try:
                    os.rename(old_file, new_file)
                    print(f"Hernoemd: {new_name}")
                except Exception as e:
                    print(f"Fout bij {filename}: {e}")

        print("Klaar!")

    def __remove_unnecessary_images():

        label_list = os.listdir(label_folder)

        image_list = os.listdir(image_folder)

        label_name_list = []
        new_list = []

        for label_name in label_list:
            label_name_list.append(os.path.basename(label_name).split('.')[0])

        for file in image_list:
            if os.path.basename(file).split('.')[0] not in label_name_list:
                new_list.append(file)


        for f in new_list:
            try:
                os.remove(f"{image_folder}/{f}")
            except Exception as e:
                print(e)

    def slice_sahi(self, json_to_change: str, cleaned_json_output: str, dir_images_to_slice: str, output_archive_name_of_sliced_images: str, width_in_pix: int = False,
                   slicing_width: int = False, slicing_height: int = False):

        input_json = json_to_change
        cleaned_json = f'C:/Users/697/projecten/labeling/Big-bulk-dataset/attempt/data/{cleaned_json_output}.json'
        image_dir = dir_images_to_slice
        output_dir = f"C:/Users/697/projecten/labeling/Big-bulk-dataset/attempt/{output_archive_name_of_sliced_images}/"
        width = 1500 if not width_in_pix else width_in_pix
        slice_w = 640 if not slicing_width else slicing_width
        slice_h = 640 if not slicing_height else slicing_height

        try:
            with open(input_json, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"The given path: {input_json} : is invalid.")
            return
        
        if not FileOsHandler().create_dir("C:/Users/697/projecten/labeling/Big-bulk-dataset/attempt", output_archive_name_of_sliced_images):
            print("This archiving name already exists, choose another name.")
            return

        new_images = []
        valid_image_ids = set()

        for img in data['images']:
            # 1. Bestandsnaam opschonen
            raw_name = img['file_name'].split('%5C')[-1].split('/')[-1]
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

        # Update de data
        data['images'] = new_images
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

        self.__coco_labeling(output_archive_name_of_sliced_images)

    # slice_sahi()

    def __coco_labeling(self, json_coco: str):
        tiled_json = f'C:/Users/697/projecten/labeling/Big-bulk-dataset/attempt/{json_coco}/tiled_annotations.json_coco.json'
        output_label_dir = f'C:/Users/697/projecten/labeling/Big-bulk-dataset/attempt/{json_coco}/labels/'

        os.makedirs(output_label_dir, exist_ok=True)

        with open(tiled_json, 'r') as f:
            data = json.load(f)

        # Maak een dictionary voor snelle lookup van afbeeldingen
        images = {img['id']: img for img in data['images']}

        for ann in data['annotations']:
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

        print("Done! the labels should be in the 'labels' directory.")

        self.__coco_jpg_removal(json_coco)

    def __coco_jpg_removal(self, dir_name: str):
        image_dir = f'C:/Users/697/projecten/labeling/Big-bulk-dataset/attempt/{dir_name}/'
        label_dir = f'C:/Users/697/projecten/labeling/Big-bulk-dataset/attempt/{dir_name}/labels/'

        valid_names = {os.path.splitext(f)[0] for f in os.listdir(label_dir) if f.endswith('.txt')}

        count = 0
        for img_file in os.listdir(image_dir):
            if img_file.endswith(('.jpg', '.jpeg', '.png')):
                name = os.path.splitext(img_file)[0]
                if name not in valid_names:
                    os.remove(os.path.join(image_dir, img_file))
                    count += 1

        print(f"Done! removed {count} empty images. Now you should have a clean dataset.")
