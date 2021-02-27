class BeachLine:
    def __init__(self):
        self.contents = []

    def RemoveSite(self, _site):
        for i in range(len(self.contents)):
            if self.contents[i] == _site:
                self.contents.pop(i)
                break

    def Insert(self, _index, _site):
        self.contents.insert(_index, _site)
                

