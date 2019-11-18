'''Class for MongoDB functions'''

from pymongo import MongoClient
import base64

class Client():
    def __init__(self):
        try:
            self.client = MongoClient("mongodb+srv://test:passfuckingword123@thotcollection-0mt7k.mongodb.net/test?retryWrites=true&w=majority")
            print("Connection success")
        except:
            print("Connection fail")

        self.db = self.client.ThotDatabase
        self.collection = self.db.ThotCollection

    def insertImage(self, image_id, imagestr):
        '''Store image as encoded str in mongo'''
        # with open(image, "rb") as imageFile:
        #     self.str = base64.b64encode(imageFile.read())
        self.collection.insert_one({"image_id": image_id, "image_str": imagestr})

    def retrieveImage(self, image_id):
        '''Retrieve image_str from mongo'''
        if self.collection.count_documents({"image_id": image_id}, limit = 1) == 0:
            raise Exception('Item not found in database')
        else:
            self.myCursor = self.collection.find_one({"image_id": image_id})
            self.image_encoded = self.myCursor["image_str"]
            return base64.b64decode(self.image_encoded)

    def printDesktop(self, image_id, outputname):
        '''Print image from database to desktop (testing purposes)'''
        try:
            self.imgdata = self.retrieveImage(image_id)
        except:
            print('Image with "id: ' + str(image_id) + '" not found in database!')

        self.filename = 'C:\\Users\\Darren\\Desktop\\mongo images\\' + outputname + '.jpg'
        with open(self.filename, 'wb') as f:
            f.write(self.imgdata)

    def printDesktopAll(self):
        '''Print all images from database to desktop (testing purposes)'''
        self.count = self.collection.count()
        if self.count == 0:
            print('Collection is empty!')
        for i in range(0, self.count):
            try:
                self.imgdata = self.retrieveImage(i)
                self.filename = 'C:\\Users\\Darren\\Desktop\\mongo images\\' + str(i) + '.jpg'
                with open(self.filename, 'wb') as f:
                    f.write(self.imgdata)
            except:
                print('Image with "id: ' + str(i) + '" not found in database!')
    

    def getSize(self):
        '''Get the size of collection'''
        return self.collection.count()

    def getHighestCount(self):
        '''Return the highest image_id in collection'''
        return self.collection.find_one({"image_id": {"$exists": True}}, sort=[("image_id", -1)])["image_id"]

    def deleteAll(self):
        '''Deletes all items in collection'''
        self.collection.delete_many({})
        print('Collection cleared!')

def main():
    '''Interface for testing database'''
    client = Client()

    while(True):
        num = input('Enter an operation:\n(1) Save all photos\n(2) Clear database\n')
        if (num == '1'):
            client.printDesktopAll()
            break
        elif (num == "2"):
            client.deleteAll()
            break
        else:
            print('Invalid operation!')

    # with open("C:\\Users\\Darren\Desktop\\111319.jpg", "rb") as imageFile:
    #     str = base64.b64encode(imageFile.read())
    #     store str in mongo
    # collection.insert_one({"image_name": 1, "image_str": str})

    #client.printDesktop(1, 'test')

    # print(client.getSize())
    # print(client.getHighestCount())

    
    

if __name__ == "__main__":
    main()