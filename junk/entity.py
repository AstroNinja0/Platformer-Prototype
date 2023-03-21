import pygame, math
from object import Physics_Obj
from animation import animation_database, animation_higher_database

# entity stuff

def simple_entity(x,y,e_type):
    return Entity(x,y,1,1,e_type)

def flip(img,boolean=True):
    return pygame.transform.flip(img,boolean,False)

def blit_center(surf,surf2,pos):
    x = int(surf2.get_width()/2)
    y = int(surf2.get_height()/2)
    surf.blit(surf2,(pos[0]-x,pos[1]-y))

class Entity(object):
    global animation_database, animation_higher_database

    def __init__(self, e_type, x = 0, y = 0, x_size = 20, y_size = 20): # x, y, x_size, y_size, type
        self.x = x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size
        self.obj = Physics_Obj(x,y,x_size,y_size)
        self.animation = None
        self.image = None
        self.animation_frame = 0
        self.animation_tags = []
        self.flip = False
        self.offset = [0,0]
        self.rotation = 0
        self.type = e_type # used to determine animation set among other things
        self.action_timer = 0
        self.action = ''
        self.set_action('idle') # overall action for the entity
        self.entity_data = {}
        self.alpha = None

    def set_pos(self,x,y):
        self.x = x
        self.y = y
        self.obj.x = x
        self.obj.y = y
        self.obj.rect.x = x
        self.obj.rect.y = y

    def move(self,momentum,platforms,ramps=[]):
        collisions = self.obj.move(momentum,platforms,ramps)
        self.x = self.obj.x
        self.y = self.obj.y

        return collisions

    def rect(self):
        return pygame.Rect(self.x, self.y, self.x_size, self.y_size)

    def set_flip(self,boolean):
        self.flip = boolean

    def set_animation_tags(self,tags):
        self.animation_tags = tags

    def set_animation(self, sequence: list[int]):
        self.animation = sequence
        self.animation_frame = 0

    def set_action(self, action_id: str, force=False):
        if (self.action == action_id) and (force == False):
            pass
        else:
            self.action = action_id
            anim = animation_higher_database[self.type][action_id]
            self.animation = anim[0]
            self.set_animation_tags(anim[1])
            self.animation_frame = 0

    def get_entity_angle(entity_2):
        x1 = self.x+int(self.x_size/2)
        y1 = self.y+int(self.y_size/2)
        x2 = entity_2.x+int(entity_2.x_size/2)
        y2 = entity_2.y+int(entity_2.y_size/2)
        angle = math.atan((y2-y1)/(x2-x1))
        if x2 < x1:
            angle += math.pi
        return angle

    def get_center(self):
        x = self.x+int(self.x_size/2)
        y = self.y+int(self.y_size/2)
        return [x,y]

    def clear_animation(self):
        self.animation = None

    def set_image(self,image):
        self.image = image

    def set_offset(self,offset):
        self.offset = offset

    def set_frame(self,amount):
        self.animation_frame = amount

    def handle(self):
        self.action_timer += 1
        self.change_frame(1)

    def change_frame(self,amount):
        self.animation_frame += amount
        if self.animation != None:
            while self.animation_frame < 0:
                if 'loop' in self.animation_tags:
                    self.animation_frame += len(self.animation)
                else:
                    self.animation = 0
            while self.animation_frame >= len(self.animation):
                if 'loop' in self.animation_tags:
                    self.animation_frame -= len(self.animation)
                else:
                    self.animation_frame = len(self.animation)-1

    def get_current_img(self):
        if self.animation == None:
            if self.image != None:
                return flip(self.image,self.flip)
            else:
                return None
        else:
            return flip(animation_database[self.animation[self.animation_frame]],self.flip)

    def get_drawn_img(self):
        image_to_render = None
        if self.animation == None:
            if self.image != None:
                image_to_render = flip(self.image,self.flip).copy()
        else:
            image_to_render = flip(animation_database[self.animation[self.animation_frame]],self.flip).copy()
        if image_to_render != None:
            center_x = image_to_render.get_width()/2
            center_y = image_to_render.get_height()/2
            image_to_render = pygame.transform.rotate(image_to_render,self.rotation)
            if self.alpha != None:
                image_to_render.set_alpha(self.alpha)
            return image_to_render, center_x, center_y

    def display(self,surface,scroll):
        image_to_render = None
        if self.animation == None:
            if self.image != None:
                image_to_render = flip(self.image,self.flip).copy()
        else:
            image_to_render = flip(animation_database[self.animation[self.animation_frame]],self.flip).copy()
        if image_to_render != None:
            center_x = image_to_render.get_width()/2
            center_y = image_to_render.get_height()/2
            image_to_render = pygame.transform.rotate(image_to_render,self.rotation)
            if self.alpha != None:
                image_to_render.set_alpha(self.alpha)
            blit_center(surface,image_to_render,(int(self.x)-scroll[0]+self.offset[0]+center_x,int(self.y)-scroll[1]+self.offset[1]+center_y))
