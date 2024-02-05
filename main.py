from random import randint as random

game_height = 10
game_width = 10

UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

directions = {
    'w': UP,
    's': DOWN,
    'a': LEFT,
    'd': RIGHT
}

def get_wrapped_board_coordinates(x, y):
    ''' Returns opposite edge coordinate of board if input is out of bounds '''
    position = (x, y)

    if x >= game_width:
        position = (0, y)
    elif x <= -1:
        position = (game_width-1, y)

    if y >= game_height:
        position = (x, 0)
    elif y <= -1:
        position = (x, game_height-1)

    return position

class snake:
    def __init__(self, init_body, init_direction):
        self.body = init_body
        self.direction = init_direction
        self.alive = True

    def head(self):
        return self.body[-1]

    def take_step(self):
        x, y = self.head()[0] + self.direction[0], self.head()[1] + self.direction[1]
        position = get_wrapped_board_coordinates(x, y)

        # Collision
        if position in self.body:
            self.alive = False
            return

        # Movement
        self.body = self.body[1:]
        self.body.append(position)

    def set_direction(self, direction):
        self.direction = direction

    def grow(self):
        position = self.body[0]
        self.take_step()
        self.body.insert(0, position)

class apple:
    def __init__(self, init_position):
        self.inc = 1
        self.points = 1
        self.position = init_position

    def spawn(self):
        self.position = (random(0, game_width-1), random(0, game_height-1))       

class game:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.snake = snake([(0, 0), (0, 1), (0, 2)], UP)
        self.apple = apple((int(self.width/2), int(self.height/2)))
        self.score = 0

    def board_matrix(self):
        b = [[None for _ in range(self.width)] for _ in range(self.height)]
        
        # Spawn snake
        for i in self.snake.body:
            x = i[0]
            y = i[1]

            b[y][x] = i
        
        b[self.snake.head()[1]][self.snake.head()[0]] = 'head'
        b[self.apple.position[1]][self.apple.position[0]] = 'apple'

        return b
    
    def render(self):
        top_border = ' - '
        side_border = ' | '
        corner_border = ' + '
        empty_space = '   '
        snake_head = ' X '
        snake_body = ' 0 '
        apple = ' a '

        matrix = self.board_matrix()

        def topbottom_row():
            return '\n' + corner_border + top_border*len(matrix[0]) + corner_border + '\n'
         
        grid = ''
        grid += topbottom_row()

        for i in range(len(matrix), 0, -1):
            row = matrix[i-1]
            grid += side_border

            for space in row:
                if space == 'apple':
                    grid += apple
                elif space == 'head':
                    grid += snake_head
                elif space is not None:
                    grid += snake_body
                else:
                    grid += empty_space
            
            grid += side_border

            if i != 1:
                grid += '\n'

        grid += topbottom_row()
        print(grid)

    def start(self):
        while self.snake.alive == True:
            self.render()

            input_direction = input('Choose direction: W - Up, S - Down, A - Left, D - Right\nInput: ').lower()

            if input_direction in directions:
                self.snake.set_direction(directions[input_direction])

            self.snake.take_step()
            
            if self.apple.position in self.snake.body:
                self.score += self.apple.points

                for i in range(self.apple.inc):
                    self.snake.grow()

                while self.apple.position in self.snake.body:
                    self.apple.spawn()
                
        print(f'Game Over!\nScore: {self.score}')

main_game = game(game_height, game_width)
main_game.start()