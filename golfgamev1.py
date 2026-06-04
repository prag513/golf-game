import tkinter as tk
import math
import random

ticktime = 10 #milliseconds
canvas_dimension = [900, 670]
canvasX = canvas_dimension[0]
canvasY = canvas_dimension[1]
movement = None
aimer = None
walls = {}
radius = 10
speedfactor = 0.01
maxspeed = 5
friction = 0.007
strokes = 0

def mouseDown(event):
    global startPos, aimer
    if movement == None:
        startPos = canvas.coords(ball1)
        aimer = canvas.create_line(startPos[0], startPos[1], startPos[0], startPos[1], fill = "white", width = 1)
        #print(startPos[0], startPos[1])

def followMouse(event):
    global startPos
    if aimer:
        canvas.coords(aimer, startPos[0]+radius, startPos[1]+radius, event.x, event.y)

def mouseUp(event):
    global startPos, speed, deltax, deltay, aimer, strokes
    if aimer == None:
        return
    #print("release: ", event.x, event.y)
    canvas.delete(aimer)
    aimer = None
    dx = event.x - startPos[0]
    dy = event.y - startPos[1]
    distance = math.sqrt(dx**2 + dy**2)
    maxdistance = 200
    if distance > maxdistance:
        distance = maxdistance
    if distance < 10:
        distance = 10
    speed = (distance/maxdistance) * maxspeed
    #print("speed = ", speed)
    deltax = speed * dx * speedfactor * -1
    deltay = speed * dy * speedfactor * -1
    strokes += 1
    textbox.config(state=tk.NORMAL)
    textbox.insert(tk.END, f"Strokes: {strokes}\n")
    textbox.config(state=tk.DISABLED)
    moveBall(ball1)

def createBall(x, y):
    x0 = x - radius
    y0 = y - radius
    x1 = x + radius
    y1 = y + radius
    return(canvas.create_oval(x0, y0, x1, y1, fill = "blue", tags = "circle"))

def moveBall(circID):
    global deltax, deltay, movement
    
    pos = canvas.coords(circID)
    next_left = pos[0] + deltax
    next_top = pos[1] + deltay
    next_right = pos[2] + deltax
    next_bottom = pos[3] + deltay
    currentx = pos[0] + radius
    currenty = pos[1] + radius
    next_centrex = currentx + deltax
    next_centrey = currenty + deltay
    
    #checks for edge collision
    if next_left <= 0 or next_right >= canvasX:
        deltax = deltax * -1
    if next_top <= 0 or next_bottom >= canvasY:
        deltay = deltay * -1
    
    #check for wall collision
    for wall in walls.values():
        wallpos = canvas.coords(wall)

        if deltax < 0: #if going left
            if next_left <= wallpos[2] and wallpos[1] <= next_centrey <= wallpos[3] and abs(wallpos[2] - next_centrex) <= radius:
                    deltax = deltax * -1
            if deltay < 0:
                if next_top <= wallpos[3] and wallpos[0] <= next_centrex <= wallpos[2] and abs(wallpos[3] - next_centrey) <= radius:
                    deltay = deltay * -1
            if deltay > 0:
                if next_bottom >= wallpos[1] and wallpos[0] <= next_centrex <= wallpos[2] and abs(wallpos[1] - next_centrey) <= radius:
                    deltay = deltay * -1
        else: #if going right
            if next_right >= wallpos[0] and wallpos[1] <= next_centrey <= wallpos[3] and abs(wallpos[0] - next_centrex) <= radius:
                deltax = deltax * -1
            if deltay < 0:
                if next_top <= wallpos[3] and wallpos[0] <= next_centrex <= wallpos[2] and abs(wallpos[3] - next_centrey) <= radius:
                    deltay = deltay * -1 
            if deltay > 0:
                if next_bottom >= wallpos[1] and wallpos[0] <= next_centrex <= wallpos[2] and abs(wallpos[1] - next_centrey) <= radius:
                    deltay = deltay * -1
    
    goaldistance = math.sqrt((targx-currentx)**2 + (targy-currenty)**2)
    if goaldistance < targetRadius:
        textbox.config(state=tk.NORMAL)
        textbox.insert(tk.END, "Scored!\n")
        textbox.config(state=tk.DISABLED)
        return

    canvas.move(circID, deltax, deltay)
    
    #friction mechanics
    currentspeed = math.sqrt(deltax**2 + deltay**2)
    if currentspeed > 0:
        friction_force = friction * currentspeed
        deltax -= (deltax / currentspeed) * friction_force
        deltay -= (deltay / currentspeed) * friction_force
        if currentspeed < 0.4:
            deltax = 0
            deltay = 0
            movement = None
            return

    movement = root.after(ticktime, moveBall, circID)

def restart():
    global ball1, strokes, movement, deltax, deltay, aimer
    
    if movement is not None:
        root.after_cancel(movement)
        movement = None
    
    deltax = 0
    deltay = 0
    aimer = None
    strokes = 0
    
    canvas.delete(ball1)
    ball1 = createBall(320, 320)
    canvas.tag_bind("circle", "<ButtonPress-1>", mouseDown)
    
    textbox.config(state=tk.NORMAL)
    textbox.delete("1.0", tk.END)
    textbox.config(state=tk.DISABLED)
   
#-------------------------------------------------------
#setup for the root window
root = tk.Tk()
root.geometry("1300x720")
root.config(bg = "white")
canvas = tk.Canvas(root, width=canvasX, height=canvasY, bg="black")
canvas.place(x=40, y=25)
#-------------------------------------------------------
#buttons and textbox
textbox = tk.Text(root, height = 15, width = 40, state = tk.DISABLED, bg = "black", fg = "white")
textbox.place(x=980, y=300)
tk.Button(root, text = "Restart", command = restart).place(x=1000, y=600)
#-------------------------------------------------------
#target hole
targetRadius = 25
targx = 400
targy = 400
x0 = targx - targetRadius
y0 = targy - targetRadius
x1 = targx + targetRadius
y1 = targy + targetRadius
target = canvas.create_oval(x0, y0, x1, y1, fill = "dark green")
#-------------------------------------------------------
#walls
walls["wall1"] = canvas.create_rectangle(500,200,600,300, fill = "grey")
walls["wall2"] = canvas.create_rectangle(200,200,300,300, fill = "grey")
walls["wall3"] = canvas.create_rectangle(200,400,300,500, fill = "grey")
walls["wall4"] = canvas.create_rectangle(500,400,600,500, fill = "grey")
#-------------------------------------------------------
ball1 = createBall(320, 320)

canvas.tag_bind("circle", "<ButtonPress-1>", mouseDown)
canvas.bind("<ButtonRelease-1>", mouseUp)
canvas.bind("<Motion>", followMouse)

root.mainloop()