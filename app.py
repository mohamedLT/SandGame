from pyray import *
from Colors import *




class Pixel :
    def __init__(self,Position:Vector2,color=YELLOW,func=lambda x:x,dirs=[Vector2(0,1)]) -> None:
        self.color=color
        self.position=Position
        self.func=func
        self.dirs = dirs
        add_dirty(self)

    def update(self):
        if Dirty_Pixels.count(self)==1:
            Dirty_Pixels.remove(self)
        self.func(self)
    
    def alert_close(self):
        for dir in [Vector2(0,1),Vector2(1,1),Vector2(1,0),Vector2(1,-1),Vector2(0,-1),Vector2(-1,-1),Vector2(-1,0),Vector2(-1,1)]:
            targ = to_str(add(self.position,dir))
            if MapedList.get(targ,False):
                add_dirty(MapedList[targ])


class Sand (Pixel):
    def __init__(self, Position: Vector2,color=YELLOW ,dirs = [Vector2(0,1),Vector2(1,1),Vector2(-1,1)] ) -> None:
        super().__init__(Position, color, self.func,dirs)
    
    def func(self,x):
        if self.move():
            self.alert_close()
        
    def move(self):
        res = False
        for dir in self.dirs :
            targ = add(self.position,dir)
            if targ.y<get_screen_height()-5 and targ.y>5 and targ.x<get_screen_width()-5 and targ.x>5:
                if not MapedList.get(to_str(targ),False):
                    MapedList[to_str(targ)]=self
                    if MapedList.get(to_str(self.position),False):   
                        del MapedList[to_str(self.position)]
                    add_dirty(self)
                    self.position= targ
                    res =True 
                    return res
        return res


class Gas (Sand):
    def __init__(self, Position: Vector2, dirs=[Vector2(0, -1), Vector2(1, -1), Vector2(-1, -1)]) -> None:
        super().__init__(Position,GRAY, dirs)


class Water(Sand):
    def __init__(self, Position: Vector2, color=BLUE, dirs=[Vector2(0, 1), Vector2(1, 1), Vector2(-1, 1),Vector2(1,0),Vector2(-1,0)]) -> None:
        super().__init__(Position, color, dirs)


class PixelButton :
    def __init__(self,rect,color,id) -> None:
        self.rec = rect
        self.color = color
        self.id=id
    
    def draw(self):
        if SelectedPixel==self.id:
            rect = Rectangle(self.rec.x-2,self.rec.y-2,self.rec.width+4,self.rec.height+4)
            draw_rectangle_lines_ex(rect,2,WHITE)
        draw_rectangle(int(self.rec.x),int(self.rec.y),int(self.rec.width),int(self.rec.height),self.color)


def add(a,b):
    return Vector2(a.x+b.x,a.y+b.y)

def to_str(vec):
    return f"{vec.x} {vec.y}"

def eq(a,b):
    return a.x==b.x and a.y==b.y

def add_dirty(pixel):
    if Dirty_Pixels.count(pixel)==0:
        Dirty_Pixels.append(pixel)

def create_pixel(index,pos):
    if index == 0:
        return Sand(pos)
    if index == 1:
        return Gas(pos)
    if index==2 :
        return Water(pos)




MapedList = {}
Dirty_Pixels = []
N=100
SelectedPixel = 0
MapedColors = [ create_pixel(i,Vector2(-100,-100) ).color for i in range(3)]
color_rects = [PixelButton(Rectangle(150+30*(i+1),10,25,25),MapedColors[i],i) for i in range(3)]



class App:

    def start(self):
        self.iter = self.iter_pixels()
        init_window(1024,512,"sand sand")
        set_target_fps(60)
        for x in range(100,110):
            for y in range(10,50):
                pos = Vector2(x,y)
                MapedList[to_str(pos)]=Sand(pos)
        while not window_should_close():
            self.update()
        close_window()

    def update(self):
        self.process_input()
        self.draw()    

    def process_input(self):
        global SelectedPixel
        if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT):
            mouse_pos =get_mouse_position() 
            for button in color_rects:
                if check_collision_point_rec(mouse_pos,button.rec):
                    SelectedPixel=button.id
                    return
            MapedList[to_str(mouse_pos)]=create_pixel(SelectedPixel,mouse_pos)

    def draw(self):
        begin_drawing()
        clear_background(BLACK)
        draw_fps(10,10)
        for but in color_rects:
            but.draw()
        draw_text(str(len(MapedList)),10,30,16,WHITE)
        if next(self.iter,-1) == -1:
            self.iter = self.iter_pixels()
        self.draw_pixels()
        end_drawing()
    
    def draw_pixels(self):
        for pixel in MapedList.values():
            draw_pixel_v(pixel.position,pixel.color)

    def iter_pixels(self):
        i=0
        for pixel in Dirty_Pixels :
            pixel.update()
            i+=1
            if i==200:
                i=0
                yield

if __name__=="__main__":
    app = App()
    app.start()