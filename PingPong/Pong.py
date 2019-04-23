# Pong game 
import turtle

# Window
window = turtle.Screen()
window.bgcolor("black")
window.title("Pong game")
window.setup(width = 900, height = 700)
window.tracer()

# Border
border = turtle.Turtle()
border.speed(0)
border.color("white")
border.penup()
border.setposition(-400, -300)
border.pendown()
border.pensize(3)
for side in range(2):
    border.fd(800)
    border.lt(90)
    border.fd(600)
    border.lt(90)
border.hideturtle()

#Score counter
counter_a = 0
counter_b = 0 

# Scores
score = turtle.Turtle()
score.speed(0)
score.color("white")
score.penup()
score.hideturtle()
score.goto(0, 260)
score.write("Player A: {}  Player B: {}".format(counter_a,counter_b), align = "center", font = ("Courier", 20, "normal"))


# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("red")
ball.goto(0, 0)
# Move Ball
ball.dx = 3
ball.dy = -3


# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.penup()
paddle_a.goto(-380, 0)
paddle_a.shapesize(stretch_wid = 7, stretch_len = 1) 

# Move Paddle A
def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)
    
window.listen()
window.onkeypress(paddle_a_up, "w")
window.onkeypress(paddle_a_down, "s")

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.penup()
paddle_b.goto(380, 0)
paddle_b.shapesize(stretch_wid = 7, stretch_len = 1) 

# Move Paddle B
def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)
    
window.listen()
window.onkeypress(paddle_b_up, "Up")
window.onkeypress(paddle_b_down, "Down")

# Main loop
while True:
    window.update()
    
    # Move the Ball
    ball.penup()
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)
    
    # Check the border
    if ball.ycor() > 287:
        ball.sety(287)
        ball.dy *= -1 
        
    if ball.ycor() < -287:
        ball.sety(-287)
        ball.dy *= -1
        
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1 
        counter_a +=1
        score.clear()
        score.write("Player A: {}  Player B: {}".format(counter_a,counter_b), align = "center", font = ("Courier", 20, "normal"))
        
    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        counter_b +=1  
        score.clear()
        score.write("Player A: {}  Player B: {}".format(counter_a,counter_b), align = "center", font = ("Courier", 20, "normal"))
    
    # Check for Ball-Paddle sollision
    if ball.xcor() > 360 and (ball.ycor() < paddle_b.ycor() + 55 and ball.ycor() > paddle_b.ycor() - 55):
        ball.setx(360)
        ball.dx *= -1
        
    if ball.xcor() < -360 and (ball.ycor() < paddle_a.ycor() + 55 and ball.ycor() > paddle_a.ycor() - 55):
        ball.setx(-360)
        ball.dx *= -1
        
    # Check Paddle-Border
    if paddle_a.ycor() > 220:
        paddle_a.sety(220)
        
    if paddle_a.ycor() < -220:
        paddle_a.sety(-220)
    
    if paddle_b.ycor() > 220:
        paddle_b.sety(220)
    
    if paddle_b.ycor() < -220:
        paddle_b.sety(-220)