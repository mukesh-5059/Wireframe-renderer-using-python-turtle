import turtle,math,os,ctypes

#lookup tables
torad=math.pi/180
sintable=[]
for i in range(0,3600):
    sintable.append(math.sin((i+0.001)*0.1*torad))
def sin(angle):
    angle=int((angle%360)*10)
    return sintable[angle]
costable=[]
for i in range(0,3600):
    costable.append(math.cos((i+0.001)*0.1*torad))
def cos(angle):
    angle=int((angle%360)*10)
    return costable[angle]

#camera settings
camera=[0,0,-10]
cameraangle=[0,0,0]
rotsx=sin(cameraangle[0])
rotcx=cos(cameraangle[0])
rotsy=sin(cameraangle[1])
rotcy=cos(cameraangle[1])

#test cube
vertices = [(-1,-1,-1),(1,-1,-1), (1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),( 1,1,1),(-1,1,1)]
triangles = [(0,1,2),(2,3,0),(0,4,5),(5,1,0),(0,4,3),(4,7,3),(5,4,7),(7,6,5),(7,6,3),(6,2,3),(5,1,2),(2,6,5)]
angle=0,180,180
pos=0,0,0

#open the obj file and read all the vertices and edges
current_script_directory = os.path.dirname(os.path.abspath(__file__))# Get the directory of the current script
script_path = os.path.abspath(__file__)
script_name = os.path.basename(script_path)
print("Current script directory:", current_script_directory)
directory_path = current_script_directory  # Replace with the path of your directory
files = os.listdir(directory_path)# List all files in the directory
f=[]
# Display the files
print("Files in the directory: ")
c=1
for file in files:
    if file!=script_name:
        f.append(file)
        print(c,')',file)
        c+=1
x=input("Enter the S.No of the obj file you want to display: ")
while not(x.isdigit()) or int(x) not in range(1,len(f)+1):
    x=input("Please enter a valid number: ")
file=f[int(x)-1]
os.system('cls')
print("Your choice:",file)
print('''
SOME BASIC INFORMATION:
1)This is a program to display the 3d models you have downloaded
2)Points to remember when downloading a 3d model
    i)choose a low poly(less polygons) model [since this project is not optimized since this is made purely for educational purposes]
    ii)choose a model made only of triangles[since triangulation is not implimented in this version]
    iii)place the downloaded 3d model in the same folder as this project code
3)Movements
    i)use 'w,a,s,d' keys to move around the world
    ii)use 'e,q' respectively to moveup and down in the world
    iii)use the mouse to rotate around the world
    iv)use 'x,y,z' keys to rotate the model in its x,y,z axes respectively
4)If you can't see the model, place the cursor at the center of the screen
5)THIS IS NOT THE FINAL PROJECT AND YOU CAN EXPET ERRORS
''')
bfc=input('Would you like to enable backface cuilling to boost performance(EXPERIMENTAL)(1 for yes and 0 for no):')
while not(bfc.isdigit()) or int(bfc) not in [0,1]:
    bfc=input("Please enter a valid option: ")
file=open(file,'r')
vertex=[]
edges=[]
for i in file:
    if i.startswith('v '):
        line=i.split()
        line.pop(0)
        c=0
        for i in line:
            line[c]=float(i)
            c+=1
        vertex.append(line)
    elif i.startswith("f "):
        line=i.split()
        line.pop(0)
        if '//' in line[0]:
            element=[]
            for j in line:
                one=j.split('//')
                element.append(one[0])
            c=0
            for i in element:
                element[c]=int(i)-1
                c+=1
            edges.append(element)
        elif '/' in line[0]:
            element=[]
            for j in line:
                one=j.split('/')
                element.append(one[0])
            c=0
            for i in element:
                element[c]=int(i)-1
                c+=1
            edges.append(element)
        else:
            line=i.split()
            line.pop(0)
            c=0
            for i in line:
                line[c]=int(i)-1
                c+=1
            edges.append(line)
file.close()

#general settings
user32 = ctypes.windll.user32               #getting the resolution of the screen
resolutionx = user32.GetSystemMetrics(0)
resolutiony = user32.GetSystemMetrics(1)
width=resolutionx
height=resolutiony
win = turtle.Screen()
win.setup(width,height)
win.tracer(0)
win.listen()
turtle.Screen().bgcolor("black")
turtle.pencolor("white")
scalingx=width/2
scalingy=height/2
turtle.hideturtle()


#camera transform and movements
canvas = turtle.getcanvas()
def camerarotate():
    global cameraangle
    cx, cy = canvas.winfo_pointerx()-resolutionx//2, -(canvas.winfo_pointery()-resolutiony//2)
    cameraangle[0]=cy*0.5
    cameraangle[1]=cx*0.5
    
def updatecameraangles():
    global rotsx,rotcx,rotsy,rotcy
    rotsx=sin(cameraangle[0])
    rotcx=cos(cameraangle[0])
    rotsy=sin(cameraangle[1])
    rotcy=cos(cameraangle[1])

def moveforward():
    global camera
    camera[0]+=0.1*rotsy
    camera[2]+=0.1*cos(cameraangle[1])
    
def movebackward():
    global camera
    camera[0]-=0.1*rotsy
    camera[2]-=0.1*cos(cameraangle[1])

def moveright():
    global camera
    camera[0]+=0.1*cos(cameraangle[1])
    camera[2]-=0.1*rotsy

def moveleft():
    global camera
    camera[0]-=0.1*cos(cameraangle[1])
    camera[2]+=0.1*rotsy
    
def moveup():
    global camera
    camera[1]-=0.1
    
def movedown():
    global camera
    camera[1]+=0.1

#calculations for backface cuilling
def normalcalc(pt1,pt2,pt3):
    ax=pt2[0]-pt1[0]
    ay=pt2[1]-pt1[1]
    az=pt2[2]-pt1[2]
    bx=pt3[0]-pt1[0]
    by=pt3[1]-pt1[1]
    bz=pt3[2]-pt1[2]
    nx=ay*bz-az*by
    ny=az*bx-ax*bz
    nz=ax*by-ay*bx
    return nx,ny,nz

def dotproduct(pt1,pt2):
    return pt1[0]*pt2[0]+pt1[1]*pt2[1]+pt1[2]*pt2[2]

#functions to project,rotate and display the model
def offsetpt(pt):
    x=pt[0]-camera[0]+pos[0]
    y=pt[1]-camera[1]+pos[1]
    z=pt[2]-camera[2]+pos[2]
    return x,y,z

def pt3d(pt):
    x,y,z=pt
    cx=cos(cameraangle[0])
    cy=cos(cameraangle[1])
    cz=cos(cameraangle[2])
    sx=sin(cameraangle[0])
    sy=rotsy
    sz=sin(cameraangle[2])

    dx=cy*(sz*y+cz*x)-sy*z
    #dy=sx*(cy*z+sy*(sz*y+cz*x))+cx*(cz*y-sz*x)    use this to invert camera
    dy=-sx*(cy*z+sy*(sz*y+cz*x))-cx*(cz*y-sz*x)
    dz=cx*(cy*z+sy*(sz*y+cz*x))-sx*(cz*y-sz*x)

    return dx,dy,dz

def rotation(pt):
    dx, dy, dz = pt
    dyrotated = dy * cos(angle[0]) - dz * sin(angle[0])                       # rotation around the x-axis
    dzrotated = dy * sin(angle[0]) + dz * cos(angle[0])
    dxrotated = dx * cos(angle[1]) + dzrotated * sin(angle[1])             # rotation around the y-axis
    dzrotated = dzrotated * cos(angle[1]) - dx * sin(angle[1])
    finaldx = dxrotated * cos(angle[2]) - dyrotated * sin(angle[2])      # rotation around the z-axis
    finaldy = dxrotated * sin(angle[2]) + dyrotated * cos(angle[2])

    return finaldx, finaldy, dzrotated

def pt2d(pt):  
    dx,dy,dz=pt
    if dz==0:
        bx=dx
        by=dy
    else:
        bx=((scalingx)*dx)/dz
        by=((scalingy)*dy)/dz

    return bx,by

def drawtriangles(triangle):
    for i in triangle:
        turtle.penup()
        turtle.goto(i[0])
        turtle.pendown()
        turtle.goto(i[1])
        turtle.goto(i[2])
        turtle.goto(i[0])
        
speed=3
def x():
    global angle
    angle=angle[0]+speed,angle[1],angle[2]

def y():
    global angle
    angle=angle[0],angle[1]+speed,angle[2]

def z():
    global angle
    angle=angle[0],angle[1],angle[2]+speed

#keyboard controls
turtle.onkeypress(moveforward,'w')
turtle.onkeypress(movebackward,'s')
turtle.onkeypress(moveleft,'a')
turtle.onkeypress(moveright,'d')
turtle.onkeypress(moveup,'e')
turtle.onkeypress(movedown,'q')
turtle.onkeypress(x,'x')
turtle.onkeypress(y,'y')
turtle.onkeypress(z,'z')

#mainloop
if int(bfc)==1:
    while True:
        triangle=[]
        for i in edges:
            orginalpt1=vertex[i[0]]
            orginalpt2=vertex[i[1]]
            orginalpt3=vertex[i[2]]
            #Rotated points
            rotatedpt1=rotation(orginalpt1)
            rotatedpt2=rotation(orginalpt2)
            rotatedpt3=rotation(orginalpt3)
            camerarotate()
            updatecameraangles()
            #Offset pts
            offsetpt1=offsetpt(rotatedpt1)
            offsetpt2=offsetpt(rotatedpt2)
            offsetpt3=offsetpt(rotatedpt3)
            #backface cuilling
            normal=normalcalc(offsetpt1,offsetpt2,offsetpt3)
            if dotproduct(normal,offsetpt1)<=0:
                #project points
                projectedpt1=pt3d(offsetpt1)
                projectedpt2=pt3d(offsetpt2)
                projectedpt3=pt3d(offsetpt3)
                #z clipping
                if projectedpt1[2]>0.1 and projectedpt2[2]>0.1 and projectedpt3[2]>0.1:
                    pt1=pt2d(projectedpt1)
                    pt2=pt2d(projectedpt2)
                    pt3=pt2d(projectedpt3)
                    triangle.append((pt1,pt2,pt3))
        #final draw           
        turtle.clear()
        drawtriangles(triangle)
        win.update()
else:
        while True:
            triangle=[]
            for i in edges:
                orginalpt1=vertex[i[0]]
                orginalpt2=vertex[i[1]]
                orginalpt3=vertex[i[2]]
                #Rotated points
                rotatedpt1=rotation(orginalpt1)
                rotatedpt2=rotation(orginalpt2)
                rotatedpt3=rotation(orginalpt3)
                camerarotate()
                updatecameraangles()
                #Offset pts
                offsetpt1=offsetpt(rotatedpt1)
                offsetpt2=offsetpt(rotatedpt2)
                offsetpt3=offsetpt(rotatedpt3)
                projectedpt1=pt3d(offsetpt1)
                projectedpt2=pt3d(offsetpt2)
                projectedpt3=pt3d(offsetpt3)
                #z clipping
                if projectedpt1[2]>0.1 and projectedpt2[2]>0.1 and projectedpt3[2]>0.1 and projectedpt1[2]<100 and projectedpt2[2]<100 and projectedpt3[2]<100:
                    pt1=pt2d(projectedpt1)
                    pt2=pt2d(projectedpt2)
                    pt3=pt2d(projectedpt3)
                    triangle.append((pt1,pt2,pt3))
                #final draw           
            turtle.clear()
            drawtriangles(triangle)
            win.update()

