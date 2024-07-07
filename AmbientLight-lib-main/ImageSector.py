import numpy as np
from ConfigLoad import ConfLoad

class ImageSector: 
    def __init__(self, img, sectors_count, led_count):
        self.img = img
        self.sectors_count = sectors_count
        self.all_Colors = [led_count]
        self.xw = img.shape[1]
        self.yh = img.shape[0]

    #
    #   Vypocet priemernej farby pre jeden sektor 
    #
    def get_Sector_Color(self, img):
        
        
        # vypocet priemernej farby pre kazdy riadok
        row_average_color = np.average(img, axis=0)

        # vypocet priemernej farby z riadokv
        average_colors = np.average(row_average_color, axis=0)

        # priemerna farba je reprezentovana ako skupina priemerych farieb hodnot BGR typu INT
        int_averages = np.array(average_colors, dtype=np.uint8)

        rgb = tuple(reversed(int_averages))

        return rgb
        
    def get_Sector(self):

        conf = ConfLoad() 
        percent = conf.conf_sect()
        zone_Width_Top = int(self.yh * percent)         # sirka 10% okraju
        zone_Width_Sides = int(self.xw * percent)       # sirka 10% okraju
        zoneLR = int(self.sectors_count / 4)
        zoneT = int(self.sectors_count / 2)

        stepY = int(self.yh / zoneLR)
        stepX = int(self.xw / zoneT)
        #pravy okraj
        sideR = self.xw - zone_Width_Sides     # vypocet bodu pre pravy okraj, odkial ma zacat rozdelovanie oblasti 
        
        color_Left = []
        color_Right = []
        color_Top = []
        final_Colors = []

        for sides in range(zoneLR):   # cyklus prechadza vsetky okraje a pocas ktoreho sa zakazdu iteraciu zisti farba sektora
            print(sides)
            leftImg = self.img[sides*stepY:sides*stepY + stepY, 0:zone_Width_Sides ]    # vytycenie rozdelenej oblasti 
            col_Left = self.get_Sector_Color(leftImg)                                      # urci hodnotu 
            print("LEFT")
            print(col_Left)
            color_Left.append(col_Left)

            right_Img = self.img[sides*stepY:sides*stepY + stepY, sideR:sideR + zone_Width_Sides ]
            col_Right = self.get_Sector_Color(right_Img)
            print("RIGHT")
            print(col_Right)
            color_Right.append(col_Right)

        print("TOP")
        for top in range(zoneT):
            top_Img = self.img[0: zone_Width_Top, top*stepX:top*stepX + stepX]
            col_Top = self.get_Sector_Color(top_Img)
            print(col_Top)
            color_Top.append(col_Top)
        
        color_Left.reverse()
        self.all_Colors.append(color_Left)
        self.all_Colors.append(color_Top)
        self.all_Colors.append(color_Right)

        for c in self.all_Colors[1]:
            final_Colors.append(c)

        for c in self.all_Colors[2]:
            final_Colors.append(c)

        for c in self.all_Colors[3]:
            final_Colors.append(c)
        print("final_COlors")
        print(final_Colors)    
        print(len(final_Colors))
        return final_Colors


