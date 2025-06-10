import turtle
import time
import random

SCREEN_SIZE = 600 # 螢幕寬高
SNAKE_SIZE = 20 # 蛇和食物的大小
MOVE_SPEED = 20 # 蛇每次移動的距離
GAME_START_DELAY = 0.1 # 遊戲初始速度


class Snake:
    def __init__(self):
        self.head = self._create_segment("yellow") # 蛇頭
        self.head.goto(0, 0)
        self.head.direction = "stop" # 初始
        self.body_segments = [] # 儲存蛇身

    def _create_segment(self, color): 
        segment = turtle.Turtle()
        segment.speed(0) 
        segment.shape("square")
        segment.color(color)
        segment.penup() # 不留軌跡
        return segment

    def change_direction(self, direction): 
        if (direction == "up" and self.head.direction != "down") or \
           (direction == "down" and self.head.direction != "up") or \
           (direction == "left" and self.head.direction != "right") or \
           (direction == "right" and self.head.direction != "left"):
            self.head.direction = direction

    def move(self):
        # 移動身體：從尾巴開始，每個身體往前移動一格
        for i in range(len(self.body_segments) - 1, 0, -1):
            self.body_segments[i].goto(self.body_segments[i-1].pos())
        # 如果有身體，身體往前移到頭的位置
        if self.body_segments:
            self.body_segments[0].goto(self.head.pos())

        # 移動蛇頭
        if self.head.direction == "up":
            self.head.sety(self.head.ycor() + MOVE_SPEED)
        elif self.head.direction == "down":
            self.head.sety(self.head.ycor() - MOVE_SPEED)
        elif self.head.direction == "left":
            self.head.setx(self.head.xcor() - MOVE_SPEED)
        elif self.head.direction == "right":
            self.head.setx(self.head.xcor() + MOVE_SPEED)

    def grow(self): # 增加身體長度
        new_segment = self._create_segment("grey")
        self.body_segments.append(new_segment)

    def reset(self): 
        time.sleep(1) 
        self.head.goto(0, 0)
        self.head.direction = "stop"
        # 清空身體
        for segment in self.body_segments:
            segment.goto(1000, 1000) 
        self.body_segments.clear()

    def check_collision(self): 
        for segment in self.body_segments:
            if self.head.distance(segment) < SNAKE_SIZE / 2: 
                return True
        return False


class Food:
    def __init__(self):
        self.item = turtle.Turtle()
        self.item.speed(0)
        self.item.shape("circle")
        self.item.color("red")
        self.item.penup()
        self.spawn() 

    def spawn(self): 
        x = random.randint(-(SCREEN_SIZE // 2 - SNAKE_SIZE), SCREEN_SIZE // 2 - SNAKE_SIZE)
        y = random.randint(-(SCREEN_SIZE // 2 - SNAKE_SIZE), SCREEN_SIZE // 2 - SNAKE_SIZE)
        self.item.goto(x, y)


class Scoreboard:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.display_pen = turtle.Turtle()
        self.display_pen.speed(0)
        self.display_pen.color("white")
        self.display_pen.penup()
        self.display_pen.hideturtle() 
        self.display_pen.goto(0, SCREEN_SIZE // 2 - 40)
        self._update_display() 

    def _update_display(self): 
        self.display_pen.clear()
        self.display_pen.write(f"score: {self.score}  best score: {self.high_score}",
                               align="center", font=("Courier", 24, "normal"))

    def add_score(self): 
        self.score += 10
        if self.score > self.high_score:
            self.high_score = self.score
        self._update_display()

    def reset_score(self): 
        self.score = 0
        self._update_display()


def run_game():
    window = turtle.Screen()
    window.setup(width=SCREEN_SIZE, height=SCREEN_SIZE)
    window.bgcolor("black")
    window.title("貪吃蛇遊戲")
    window.tracer(0) 

   
    snake = Snake()
    food = Food()
    scoreboard = Scoreboard()

    # 鍵盤事件監聽
    window.listen()
    window.onkeypress(lambda: snake.change_direction("up"), "Up")
    window.onkeypress(lambda: snake.change_direction("down"), "Down")
    window.onkeypress(lambda: snake.change_direction("left"), "Left")
    window.onkeypress(lambda: snake.change_direction("right"), "Right")

    game_delay = GAME_START_DELAY

    
    while True:
        window.update() 

        # 撞牆
        if (snake.head.xcor() > SCREEN_SIZE / 2 - SNAKE_SIZE or
            snake.head.xcor() < -SCREEN_SIZE / 2 + SNAKE_SIZE or
            snake.head.ycor() > SCREEN_SIZE / 2 - SNAKE_SIZE or
            snake.head.ycor() < -SCREEN_SIZE / 2 + SNAKE_SIZE):
            snake.reset()
            scoreboard.reset_score()
            game_delay = GAME_START_DELAY 

        # 吃到食物
        if snake.head.distance(food.item) < SNAKE_SIZE:
            food.spawn() 
            snake.grow() 
            scoreboard.add_score() 
            game_delay = max(0.05, game_delay * 0.9) 

        snake.move() 

        # 檢查撞到自己
        if snake.check_collision():
            snake.reset()
            scoreboard.reset_score()
            game_delay = GAME_START_DELAY 

        time.sleep(game_delay) 

    window.mainloop() 

# 啟動遊戲
if __name__ == "__main__":
    run_game()