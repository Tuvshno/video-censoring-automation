class Captions():

    file = None
    keys = {}
    profanity = set()

    def __init__(self, filePath):
        self.file = open(filePath)
        self.__intializeProfanity()
        self.__initializeKeys()

    def __intializeProfanity(self):
        profanityFile = open("profanity.txt")

        while True:
            word = profanityFile.readline()
            word = word.replace("\n", "")

            if not word:
                break

            self.profanity.add(word)
        
        profanityFile.close()

    def __initializeKeys(self):
        while True:
            time = self.file.readline()
            caption = self.file.readline()
            extra = self.file.readline()

            if not time or not caption or not extra:
                break

            time = time.strip()
            caption = caption.strip()
            times = time.split()

            caption = caption.split()
            
            for word in caption:
                if word in self.profanity:
                    print(word + " " + times[0] + " " + times[2])
                    self.keys.update({times[0] : times[2]})
                    break
            
        self.file.close()

    def getKeys(self):
        return self.keys

    def showProfanity(self):
        print(self.keys)


