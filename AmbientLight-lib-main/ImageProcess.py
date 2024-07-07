from skimage import io
from ConfigLoad import ConfLoad

class ImageProcess:

    def __init__(self, dir): 
        self.img = None

    #
    #   nacitanie noveho obrazku z weboveho servera
    #
    def load(self):     
        conf = ConfLoad()
        url = conf.conf_url()
        self.img = io.imread(url)
        
        return self.img

    def cropp(self,x,y,w,h):
        if(self.img.size != 0):
            cropped_image = self.img[y: y + h, x: x + w]               
        else:
            print("No image")
        return cropped_image
   

 
