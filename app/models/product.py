class Product():



    def __init__(self,id,name,price,img_url=None):
        self.name = name
        self.id = id
        self.price = price
        self.imgurl = img_url
    
    def getId(self):
        return self.id
    def getName(self):
        return self.name
    def getPrice(self):
        return self.price
    def getImgUrl(self):
        return self.imgurl
    def setImgUrl(self,imgurl):
        self.imgurl = imgurl