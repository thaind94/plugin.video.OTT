import xml.etree.ElementTree as ET
import os.path
print os.path.realpath('test.py')
tree = ET.parse('list_channel.xml')
root = tree.getroot()