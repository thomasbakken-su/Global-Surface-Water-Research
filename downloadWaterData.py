import urllib.request, sys, getopt, os

OCCURENCE = 'occurence'
CHANGE = 'change'
SEASONALITY = 'seasonality'
RECURRANCE = 'recurrence' 
TRANSITIONS = 'transitions'


class downloadWaterData:
    def __init__(self, destination_folder):
        self.DESTINATION_FOLDER = destination_folder
        self.processDest()

    def processDest(self):
        if (self.DESTINATION_FOLDER[-1:]!="/"):
            self.DESTINATION_FOLDER = self.DESTINATION_FOLDER + "/"
        if not os.path.exists(self.DESTINATION_FOLDER):
            print("Creating folder " + self.DESTINATION_FOLDER)
            os.makedirs(self.DESTINATION_FOLDER)

    def prepareLatsNLongs(self):
        longs = [str(w) + "W" for w in range(180,0,-10)]
        longs.extend([str(e) + "E" for e in range(0,180,10)])
        lats = [str(s) + "S" for s in range(50,0,-10)]
        lats.extend([str(n) + "N" for n in range(0,90,10)])
        return lats, longs

    def downloadData(self, dataset, lats = None, longs = None):
        if not lats or not longs:
            lats, longs = self.prepareLatsNLongs()
        fileCount = len(longs)*len(lats)
        counter = 1
        for lng in longs:
            for lat in lats:
                print(lat, lng)
                filename = dataset + "_" + str(lng) + "_" + str(lat) + "v1_3_2020.tif"
                if os.path.exists(self.DESTINATION_FOLDER + filename):
                    print(self.DESTINATION_FOLDER + filename + " already exists - skipping")
                else:
                    url = "http://storage.googleapis.com/global-surface-water/downloads2020/" + dataset + "/" + filename
                    code = urllib.request.urlopen(url).getcode()
                    if (code != 404):
                        print("Downloading " + url + " (" + str(counter) + "/" + str(fileCount) + ")")
                        urllib.request.urlretrieve(url, self.DESTINATION_FOLDER + filename)
                    else:
                        print(url + " not found")
                counter += 1
            