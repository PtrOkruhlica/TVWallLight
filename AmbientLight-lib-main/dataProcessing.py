from imgNN import Nnimg
from ImageProcess import ImageProcess
from sectors import ImageSector
from ConfigLoad import ConfLoad
import board
import neopixel

class LedColoring:
    #
    # prvotna inicializacia TV v priestore
    # ak sa TV nachadza v priestore tak vrati jej rozmerove atributy x,y,w,h
    # ak nie tak, tak sa nastavia rozmery zo suboru settings.ini
    #
    def __init__(self):
        self.fileImg = ImageProcess()

    def coloring(self,x,y,w,h,x2,y2,w2,h2,loa):
        pixels = neopixel.NeoPixel(board.D18, 56)

        if(((x2 >= 280) and (x2 <= 350)) and
        ((y2 >= 195) and (y2 <= 235)) and 
        ((w2 >= 400) and (w2 <= 450)) and
        ((h2 >= 240) and (h2 <= 275))):
            x = x2
            y = y2
            w = w2
            h = h2 
        else:
            conf = ConfLoad() 
            x,y,w,h,sectCount,ledCount = conf.conf_image()
            x = x
            y = y
            w = w
            h = h       
               
        print("x,y,w,h = ", x,y,w,h)
        cropped = self.fileImg.cropp(x,y,w,h)
        print(cropped.shape)

        
        sect = ImageSector(cropped, sectCount, ledCount)  #56
        tempColor = sect.get_Sector()    #pole farieb
        for led in range(0,8):
            pixels[led*7] = tempColor[led]
            pixels[led*7+1] = tempColor[led]
            pixels[led*7+2] = tempColor[led]
            pixels[led*7+3] = tempColor[led]
            pixels[led*7+4] = tempColor[led]
            pixels[led*7+5] = tempColor[led]
            pixels[led*7+6] = tempColor[led]
    
    #
    # po spusteni neuronky na detekovanie TV, sa atributy TV pouzivaju na orezanie obrazka
    # pouzije sa nekonecny cyklus, aby kazdy nasleujuci obrazok takto isto orezalo
    # po orezani CROPP sa vysledny obrazok pouzije ako parameter pre vytvorenie objektu Sector
    # kde sa zistuje farba sektorov TV 
    #
    def algo_Run(self):
        
        x = 0
        y = 0
        w = 0
        h = 0
        x2 = 0
        y2 = 0
        w2 = 0
        h2 = 0
        i = 0
        while True:      
            loa = self.fileImg.load() #    nacitanie dalsieho obrazku
            if(loa.any() != None):
                if(i % 5000 == 0):
                    neur = Nnimg()
                    x2,y2,w2,h2 = neur.tv_detection(loa)
                    try:
                        x2,y2,w2,h2 = neur.tv_detection(loa)
                    except Exception as ex1:
                        print("Treba spustit alg znovu")     

                    self.all_together(x,y,w,h,x2,y2,w2,h2,loa)
                    i+=1
                # Ak nájde obrazovku detekcia
                self.all_together(x,y,w,h,x2,y2,w2,h2,loa
                i+=1
            time.sleep(0.2)
        cv2.waitKey(0)


   
    
