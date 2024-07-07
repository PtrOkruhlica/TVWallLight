from configparser import ConfigParser

class ConfLoad:  

    def __init__(self):
        pass

    def conf_image(self): 
        file = 'settings.ini'
        config = ConfigParser()
        config.read(file)
        config.sections()
        tempX = config['Settings_ColDet']['x']
        tempY = config['Settings_ColDet']['y']
        tempW = config['Settings_ColDet']['w']
        tempH = config['Settings_ColDet']['h']
        sect_Count = config['Settings_ColDet']['sectorsCount']
        led_Count  = config['Settings_ColDet']['ledCount'] 

        return (int(tempX),int(tempY),int(tempW),int(tempH),int(sect_Count),int(led_Count))

    def conf_sect(self):
        file = 'settings.ini'
        config = ConfigParser()
        config.read(file)
        config.sections()
        percent = config['Settings_Sectors']['percent']

        return (float(percent))

    def conf_url(self):
        file = 'settings.ini'
        config = ConfigParser()
        config.read(file)
        config.sections(),
        url = config['Settings_server']['url']
        
        return url

