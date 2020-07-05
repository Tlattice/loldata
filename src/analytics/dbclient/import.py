from bson import json_util
import os

IMPORT_PATH =  "/home/user/Documents/git/rantme/src/la1/"

for filename in os.listdir(os.path.join(IMPORT_PATH)):
    with open(os.path.join(IMPORT_PATH+filename)) as file:
        data = json_util.loads(file.read())
