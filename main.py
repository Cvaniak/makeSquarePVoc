import os
from xml.dom import minidom

from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

import xml.etree.ElementTree as ET
import copy
from scipy import misc
from PIL import Image

def read_content(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    list_with_all_boxes = []
    m_name = xml_file.split(".")[0]


    m1_tree = ElementTree.ElementTree()
    m2_tree = ElementTree.ElementTree()
    m1_root = ElementTree.Element('annotation')
    m2_root = ElementTree.Element('annotation')

    m_folder = root.find('folder')
    m_source = root.find("source")
    m_path = root.find("path")
    m_size = root.find('size')
    m_segmented = root.find('segmented')

    t_width = int(m_size.find('width').text)
    t_height = int(m_size.find('height').text)
    t_smaller = min(t_height,t_width)
    t_difference = abs(t_width-t_height)

    m_size.find('width').text = str(t_smaller)
    m_size.find('height').text = str(t_smaller)

    m1_path = ElementTree.Element('path')
    m1_path.text = (root.find("path").text).split(".")[0] + "_1." + IMAGE_EXT
    m2_path = ElementTree.Element('path')
    m2_path.text = (root.find("path").text).split(".")[0] + "_2." + IMAGE_EXT

    m1_root.append(m_folder)
    m1_root.append(m_source)
    m1_root.append(m_size)
    m1_root.append(m_segmented)

    m2_root.append(m_folder)
    m2_root.append(m_source)
    m2_root.append(m_size)
    m2_root.append(m_segmented)

    m1_root.append(m1_path)
    m2_root.append(m2_path)

    for boxes in root.iter('object'):
        ymin, xmin, ymax, xmax = None, None, None, None

        for box in boxes.findall("bndbox"):
            ymin = int(box.find("ymin").text)
            xmin = int(box.find("xmin").text)
            ymax = int(box.find("ymax").text)
            xmax = int(box.find("xmax").text)

            ymin2 = int(box.find("ymin").text)-int(t_difference)
            ymax2 = int(box.find("ymax").text)-int(t_difference)

        boxes2 = copy.deepcopy(boxes)
        boxes2.find("bndbox").find('ymin').text = str(ymin2)
        boxes2.find("bndbox").find('ymax').text = str(ymax2)

        if ymax > t_smaller:
            m2_root.append(boxes2)
        elif ymin < t_difference:
            m1_root.append(boxes)
        else:
            m1_root.append(boxes)
            m2_root.append(boxes2)


        # list_with_single_boxes = [xmin, ymin, xmax, ymax]
        # list_with_all_boxes.append(list_with_single_boxes)


    m1_tree._setroot(m1_root)
    m2_tree._setroot(m2_root)

    m1_tree.write(m_name+"_1.xml")
    m2_tree.write(m_name+"_2.xml")

    # Cuting image ----------------------
    im = Image.open(m_name + ".png")

    # Setting the points for cropped image
    left = 0
    right = t_width
    bottom1 = 0
    top1 = t_height-t_difference
    bottom2 = t_difference
    top2 = t_height

    im1 = im.crop((left, bottom1, right, top1))
    im2 = im.crop((left, bottom2, right, top2))
    # im1.show()
    im1.save(m_name + "_1." + IMAGE_EXT)
    im2.save(m_name + "_2." + IMAGE_EXT)



FOLDER_NAME = "59_70"
IMAGE_EXT = "png"

m_path = os.path.dirname(__file__)
m_path = os.path.join(m_path, "59_70")

print(m_path)
m_file = None

for file in os.listdir(m_path):
    if file.endswith(".xml"):
        m_file = os.path.join(m_path, file)
        print(m_file)
        read_content(m_file)