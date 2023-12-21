import pygame 
import sys 

pygame.init()

width = 800 
height = 800 
dif = width/8

screen = pygame.display.set_mode((width, height))

squares_rects = []

board = []

def remove_pieces(board, location):
    for x in board:
        if x.start_pos == location:
            board.remove(x)



class Pawn():
    def __init__(self, image, x, y, color):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.square = (x//100, y//100)
        self.dragging = False
        self.color = color
        self.start_pos = (int(x//100), int(y//100))
    
    def __repr__(self):
        return f"{self.__class__.__name__}"
       
    
    def draw(self):
        image_pos = self.image.get_rect(center = self.rect.center)
        screen.blit(self.image, self.rect)
    
    def update_position(self, pos):
        self.rect.center = pos 
        x, y = pos
        self.square = (x//100, y//100)
        
    
    def get_center_rect(self):
        # Create a smaller Rect around the center
        center_rect_size = 10  
        center_rect = pygame.Rect(0, 0, center_rect_size, center_rect_size)
        center_rect.center = self.rect.center
        return center_rect
    
    def first_move(self):
        if self.color == "white":
            if self.start_pos[1] == 6:
                return True 

            else:
                return False
        
        else:
            if self.start_pos[1] == 1:
                return True
            else:
                return False
    
    def is_capture(self, square):
        if board[square[1]][square[0]] != "p" and board[square[1]][square[0]].color != self.color:
            return True
        else:
            return False


    def valid_move(self, square):
        if self.color == "white":
            direction = -1
        else:
            direction = 1

        if self.first_move() and not (self.is_capture(square)) and square == (self.start_pos[0], self.start_pos[1] + 2 * direction):
                board[square[1]][square[0]] = self
                board[self.start_pos[1]][self.start_pos[0]] = "p"
                self.start_pos = square
                return True 

        elif square == (self.start_pos[0], self.start_pos[1] + direction) and not self.is_capture(square):
                board[square[1]][square[0]] = self
                board[self.start_pos[1]][self.start_pos[0]] = "p"
                self.start_pos = square
                return True 
        
        elif self.is_capture(square) and (square == (self.start_pos[0]+1, self.start_pos[1] + direction) or square == (self.start_pos[0]-1, self.start_pos[1] + direction)):
            board[square[1]][square[0]] = self
            remove_pieces(chess_pieces, square)
            self.start_pos  = square
            return True 
            
           




class King(Pawn):
    def __init__(self, image, x, y, color):
        super().__init__(image, x, y, color)

class Queen(Pawn):
    def __init__(self, image, x, y, color):
        super().__init__(image, x, y, color)

class Knight(Pawn):
    def __init__(self, image, x, y, color):
        super().__init__(image, x, y, color)

class Bishop(Pawn):
    def __init__(self, image, x, y, color):
        super().__init__(image, x, y, color)

class Rook(Pawn):
    def __init__(self, image, x, y, color):
        super().__init__(image, x, y, color)

def draw_board():
    j = 0
    i = 0 
    for i in range(8):
        if i % 2 == 0:
            j = 0
        y = 0
        for j in range(j, j+8):
            
            if j % 2 == 0:
                myrect = pygame.draw.rect(screen, (255,255,255), (y*dif, i*dif, dif,dif))
                squares_rects.append(myrect)
                screen.fill((118,150,86), myrect)
            else:
                myrect = pygame.draw.rect(screen, (130,130,130), (y*dif, i*dif, dif,dif))
                squares_rects.append(myrect)
                screen.fill((238,238,210), myrect)
            
            y += 1



king_black = pygame.image.load("black_king.png")
king_black = pygame.transform.scale(king_black, (80, 100))
pawn_black = pygame.image.load("black_pawn.png")
pawn_black = pygame.transform.scale(pawn_black, (60,90))
queen_black = pygame.image.load("black_queen.png")
queen_black = pygame.transform.scale(queen_black, (80, 100))
knight_black = pygame.image.load("black_knight.png")
knight_black = pygame.transform.scale(knight_black, (80, 100))
bishop_black = pygame.image.load("black_bishop.png")
bishop_black = pygame.transform.scale(bishop_black, (80, 100))
rook_black = pygame.image.load("black_tower.png")
rook_black = pygame.transform.scale(rook_black, (80, 100))

king_white = pygame.image.load("white_king.png")
king_white = pygame.transform.scale(king_white, (80, 100))
pawn_white = pygame.image.load("white_pawn.png")
pawn_white = pygame.transform.scale(pawn_white, (60,90))
queen_white = pygame.image.load("white_queen.png")
queen_white = pygame.transform.scale(queen_white, (80, 100))
knight_white = pygame.image.load("white_knight.png")
knight_white = pygame.transform.scale(knight_white, (80, 100))
bishop_white = pygame.image.load("white_bishop.png")
bishop_white = pygame.transform.scale(bishop_white, (80, 100))
rook_white = pygame.image.load("white_rook.png")
rook_white = pygame.transform.scale(rook_white, (80, 100))


b_king = King(king_black, dif*4+50,50, "black")
b_queen = Queen(queen_black, dif*3+50, 50, "black")
b_knight = Knight(knight_black, dif*2+50, 50, "black")
b_rook = Rook(rook_black, 50, 50, "black")
b_bishop = Bishop(bishop_black, dif+50, 50, "black")
b_knight2 = Knight(knight_black, dif*5+50, 50, "black")
b_bishop2 = Bishop(bishop_black, dif*6+50, 50, "black")
b_rook2 = Rook(rook_black, dif*7+50, 50, "black")
b_pawn = Pawn(pawn_black, 50, dif+50, "black")
b_pawn2 = Pawn(pawn_black, dif+50, dif+50, "black")
b_pawn3 = Pawn(pawn_black, dif*2+50, dif+50, "black")
b_pawn4 = Pawn(pawn_black, dif*3+50, dif+50, "black")
b_pawn5 = Pawn(pawn_black, dif*4+50, dif+50, "black")
b_pawn6 = Pawn(pawn_black, dif*5+50, dif+50, "black")
b_pawn7 = Pawn(pawn_black, dif*6+50, dif+50, "black")
b_pawn8 = Pawn(pawn_black, dif*7+50, dif+50, "black")
b_pawn9 = Pawn(pawn_black, dif*8+50, dif+50, "black")

w_king = King(king_white, dif*4+50,dif*7+50, "white")
w_queen = Queen(queen_white, dif*3+50, dif*7+50, "white")
w_knight = Knight(knight_white, dif*2+50, dif*7+50, "white")
w_rook = Rook(rook_white, 50, dif*7+50, "white")
w_bishop = Bishop(bishop_white, dif+50, dif*7+50, "white")
w_knight2 = Knight(knight_white, dif*5+50, dif*7+50, "white")
w_bishop2 = Bishop(bishop_white, dif*6+50, dif*7+50, "white")
w_rook2 = Rook(rook_white, dif*7+50, dif*7+50, "white")
w_pawn = Pawn(pawn_white, 50, dif*6+50, "white")
w_pawn2 = Pawn(pawn_white, dif+50, dif*6+50, "white")
w_pawn3 = Pawn(pawn_white, dif*2+50, dif*6+50, "white")
w_pawn4 = Pawn(pawn_white, dif*3+50, dif*6+50, "white")
w_pawn5 = Pawn(pawn_white, dif*4+50, dif*6+50, "white")
w_pawn6 = Pawn(pawn_white, dif*5+50, dif*6+50, "white")
w_pawn7 = Pawn(pawn_white, dif*6+50, dif*6+50, "white")
w_pawn8 = Pawn(pawn_white, dif*7+50, dif*6+50, "white")
w_pawn9 = Pawn(pawn_white, dif*8+50, dif*6+50, "white")


chess_pieces = [b_king, b_queen, b_knight, b_rook, b_bishop, b_knight2, b_bishop2, b_rook2, b_pawn, b_pawn2, 
                b_pawn3, b_pawn4, b_pawn5, b_pawn6,b_pawn7,b_pawn8,w_king, w_bishop,w_bishop2,w_knight,w_knight2, w_queen, w_rook, w_rook2, w_pawn,w_pawn2,w_pawn3,w_pawn4,w_pawn5,w_pawn6,w_pawn7,w_pawn8]


board = [['p' for _ in range(8)] for _ in range(8)]
for x in chess_pieces:
    board[x.start_pos[1]][x.start_pos[0]] = x
 
currently_clicked = None 




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]: 
                for piece in chess_pieces: 
                    if piece.rect.collidepoint(event.pos):
                        currently_clicked = piece
                        currently_clicked_start_pos = piece.rect.center

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if currently_clicked:
                    currently_clicked_center_rect = currently_clicked.get_center_rect()
                    for square in squares_rects:
                        if square.colliderect(currently_clicked_center_rect) and [x.square for x in chess_pieces].count(currently_clicked.square) == 1 and currently_clicked.valid_move((square.x//100, square.y//100)):
                            currently_clicked.update_position((square.x+50, square.y+50))
                            break
                        else:
                            currently_clicked.update_position(currently_clicked_start_pos)
                    currently_clicked = None
                    currently_clicked_center_rect = None
        
        elif event.type == pygame.MOUSEMOTION:
            if currently_clicked:
                x, y = event.pos
                currently_clicked_center_rect = currently_clicked.get_center_rect()
                currently_clicked.update_position((x, y))
            
    

    draw_board()
    for piece in chess_pieces:
        piece.draw()
    if currently_clicked:
        currently_clicked.draw()
    
    
    
    
    pygame.display.update()


    