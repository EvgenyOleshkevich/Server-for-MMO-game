import math

class Player:
    def __init__(self, id, x, y, hp, angle_view):
        self.id = id
        self.x = x
        self.y = y
        self.hp =hp
        self.angle_view = angle_view
        
    def X(self):
        return self.x
    
    def Y(self):
        return self.y
    
    def AngleView(self):
        return self.angle_view
    
    def SetX(self, x):
        self.x = x
    
    def SetY(self, y):
        self.y = y
    
    def SetAngleView(self, angle_view):
        self.angle_view = angle_view
    
    def ID(self):
        return self.id
    
    def HP(self):
        return self.hp
    
    def Decrease_HP(self, value):
        self.hp = min(self.hp - value, 0)
        
    def Increase_HP(self, value):
        self.hp = max(self.hp + value, 100)

def hit(player, players, angle):
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    print('cos: ', cos_angle, 'sin: ', sin_angle)
    dist_square = 1000000
    hited_enemy = None
    
    for key, enemy in players:
        if (enemy.ID() == player.ID()):
            continue
        x = enemy.X() - player.X()
        y = enemy.Y() - player.Y()
        
        dist_to = x*x+y*y
        scal_prod = cos_angle*x + sin_angle*y
        prod = abs(scal_prod) * scal_prod/ dist_to -1
        
        #print('prod: ', prod)
        if prod > -0.01:
            if dist_square > dist_to:
                dist_square = dist_to
                print('prod: ', prod)
                print('pos ', [ enemy.X(), enemy.Y()], '; dist: ', dist_square)
                hited_enemy = enemy
    return dist_square, enemy

def cross(vec1, vec2):
    return vec1[0]*vec2[1] - vec1[1]*vec2[0]

def is_cross(cut1, cut2):

    vec1 = [cut1[1][0] - cut1[0][0], cut1[1][1] - cut1[0][1]] # AB
    vec2 = [cut2[1][0] - cut2[0][0], cut2[1][1] - cut2[0][1]] # CD
    
    AC = [cut2[0][0] - cut1[0][0], cut2[0][1] - cut1[0][1]]
    AD = [cut2[1][0] - cut1[0][0], cut2[1][1] - cut1[0][1]]
    CA = [-AC[0], - AC[1]]
    CB = [cut1[1][0] - cut2[0][0], cut1[1][1] - cut2[0][1]]

    
    prod1 = cross(vec2, CA)
    prod2 = cross(vec2, CB)

    if (cross(vec1, AC) * cross(vec1, AD) >= 0) or (prod1 * prod2 >= 0):
        return None
    
    px = cut1[0][0] + vec1[0] * abs(prod1/(prod2-prod1))
    py = cut1[0][1] + vec1[1] * abs(prod1/(prod2-prod1))
    return px, py

def wall_shot(shot, box):
    dist_hit = ((shot[1][0]-shot[0][0])**2 + (shot[1][1]-shot[0][1])**2) * 2
    for cut in box:
        print(shot)
        print(cut)
        point = is_cross(shot, cut)
        if point is not None:
            dist = (shot[0][0]-point[0])*2+(shot[0][1]-point[1])*2
            if (dist_hit is None) or (dist_hit > dist):
                dist_hit = dist
                
    return dist_hit
    

def nearest_wall_shot(shot, boxes):
    dist_hit = ((shot[1][0]-shot[0][0])**2 + (shot[1][1]-shot[0][1])**2) * 2
    for box in boxes:
        dist = wall_shot(shot, box)
        if (dist_hit is None) or (dist_hit > dist):
            dist_hit = dist
    return dist_hit


def box_to_cuts(box):
    result = []
    print(box)
    for i in [1, -1]:
        for j in [1, -1]:
            temp1 = []       
            temp1.append( box["x"] + i * box["width"] / 2)
            temp1.append( box["y"] + j * box["length"] / 2)
            temp2 = []
            temp2.append( box["x"] - i * box["width"] / 2)
            temp2.append( box["y"] - j * box["length"] / 2)
            result.append([temp1,temp2])
    return result
