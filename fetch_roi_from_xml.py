# -*- coding: utf-8 -*-
from lxml import etree
import cv2


def fetch_region(object):
    name_begin = object.find("<name>")
    if name_begin == -1:
        return 0
    name_end = object.find("</name>",name_begin + 1)
    name = object[name_begin+6:name_end]

    xmin_begin = object.find("<xmin>")
    xmin_end = object.find("</xmin>", xmin_begin + 1)
    xmin = int(object[xmin_begin + 6:xmin_end])

    ymin_begin = object.find("<ymin>")
    ymin_end = object.find("</ymin>", ymin_begin + 1)
    ymin = int(object[ymin_begin + 6:ymin_end])

    xmax_begin = object.find("<xmax>")
    xmax_end = object.find("</xmax>", xmax_begin + 1)
    xmax = int(object[xmax_begin + 6:xmax_end])

    ymax_begin = object.find("<ymax>")
    ymax_end = object.find("</ymax>", ymax_begin + 1)
    ymax = int(object[ymax_begin + 6:ymax_end])
    return [[xmin,xmax,ymin,ymax],name]

html = etree.parse('pexels-photo-110812.xml')
result = str(etree.tostring(html, pretty_print=True))
result_list = result.split("\\n")
# for ele in result_list:
#     print(ele)
path_begin = result.find("<path>")
path_end = result.find("</path>",path_begin + 1)
path = result[path_begin+6:path_end]
# print(path)
object_begin = 0
last_result = []
while 1:
    if result.find("object",object_begin+1) == -1:
        break
    object_begin = result.find("object",object_begin+1)
    object_end = result.find("object", object_begin + 1)
    object = result[object_begin:object_end]
    region_label = fetch_region(object)
    if region_label == 0:
        continue
    region_label.append(path)
    last_result.append(region_label)
# print(last_result)
for ele in last_result:
    img = cv2.imread(ele[2])
    region = ele[0]
    label = ele[1]
    img_result = img[region[2]:region[3],region[0]:region[1]]
    cv2.imshow("img",img_result)
    cv2.waitKey()


