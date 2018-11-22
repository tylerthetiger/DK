class Player:
    def __init__(self,name,NBAplayerID,position,avgPoints,salary):
        self.name = name
        self.NBAplayerID = NBAplayerID
        self.position = position
        self.avgPoints = avgPoints
        self.salary = salary
        self.projection = 0
    def __repr__(self):
        return 'Player({},{},{},{},{})'.format(self.name,self.NBAplayerID,self.position,self.avgPoints,self.salary,self.projection)
       # return (self.name + ', ' + self.position + ', ' + self.avgPoints + ', ' + self.salary)
    def __str__(self):
        return '{},{},{},{},{}'.format(self.name,self.NBAplayerID,self.position,self.avgPoints,self.salary,self.projection)

        #return (self.name + ', ' + self.position + ', ' + self.avgPoints + ', ' + self.salary)
    