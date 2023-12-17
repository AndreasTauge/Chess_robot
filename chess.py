import pygame 
import sys 

pygame.init()

width = 800 
height = 800 
dif = width/8

screen = pygame.display.set_mode((width, height))

squares = []

class Pawn():
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dragging = False
    
    def draw(self):
        image_pos = self.image.get_rect(center = self.rect.center)
        screen.blit(self.image, self.rect)
    
    def update_position(self, pos):
        self.rect.center = pos 
    
    def get_center_rect(self):
        # Create a smaller Rect around the center
        center_rect_size = 10  
        center_rect = pygame.Rect(0, 0, center_rect_size, center_rect_size)
        center_rect.center = self.rect.center
        return center_rect

class King(Pawn):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

class Queen(Pawn):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

class Knight(Pawn):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

class Bishop(Pawn):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

class Rook(Pawn):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

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
                squares.append(myrect)
                screen.fill((118,150,86), myrect)
            else:
                myrect = pygame.draw.rect(screen, (130,130,130), (y*dif, i*dif, dif,dif))
                squares.append(myrect)
                screen.fill((238,238,210), myrect)
            
            y += 1


# gjør det du har gjort med de hvite brikkene, bytt navn på objektene under til fargen deres
# GJØR SÅNN AT BRIKKENE "SNAPPER" PÅ PLASS NÅR DU FLYTTER DE 
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


b_king = King(king_black, dif*4+50,50)
b_queen = Queen(queen_black, dif*3+50, 50)
b_knight = Knight(knight_black, dif*2+50, 50)
b_rook = Rook(rook_black, 50, 50)
b_bishop = Bishop(bishop_black, dif+50, 50)
b_knight2 = Knight(knight_black, dif*5+50, 50)
b_bishop2 = Bishop(bishop_black, dif*6+50, 50)
b_rook2 = Rook(rook_black, dif*7+50, 50)
b_pawn = Pawn(pawn_black, 50, dif+50)
b_pawn2 = Pawn(pawn_black, dif+50, dif+50)
b_pawn3 = Pawn(pawn_black, dif*2+50, dif+50)
b_pawn4 = Pawn(pawn_black, dif*3+50, dif+50)
b_pawn5 = Pawn(pawn_black, dif*4+50, dif+50)
b_pawn6 = Pawn(pawn_black, dif*5+50, dif+50)
b_pawn7 = Pawn(pawn_black, dif*6+50, dif+50)
b_pawn8 = Pawn(pawn_black, dif*7+50, dif+50)
b_pawn9 = Pawn(pawn_black, dif*8+50, dif+50)

w_king = King(king_white, dif*4+50,dif*7+50)
w_queen = Queen(queen_white, dif*3+50, dif*7+50)
w_knight = Knight(knight_white, dif*2+50, dif*7+50)
w_rook = Rook(rook_white, 50, dif*7+50)
w_bishop = Bishop(bishop_white, dif+50, dif*7+50)
w_knight2 = Knight(knight_white, dif*5+50, dif*7+50)
w_bishop2 = Bishop(bishop_white, dif*6+50, dif*7+50)
w_rook2 = Rook(rook_white, dif*7+50, dif*7+50)
w_pawn = Pawn(pawn_white, 50, dif*6+50)
w_pawn2 = Pawn(pawn_white, dif+50, dif*6+50)
w_pawn3 = Pawn(pawn_white, dif*2+50, dif*6+50)
w_pawn4 = Pawn(pawn_white, dif*3+50, dif*6+50)
w_pawn5 = Pawn(pawn_white, dif*4+50, dif*6+50)
w_pawn6 = Pawn(pawn_white, dif*5+50, dif*6+50)
w_pawn7 = Pawn(pawn_white, dif*6+50, dif*6+50)
w_pawn8 = Pawn(pawn_white, dif*7+50, dif*6+50)
w_pawn9 = Pawn(pawn_white, dif*8+50, dif*6+50)


chess_pieces = [b_king, b_queen, b_knight, b_rook, b_bishop, b_knight2, b_bishop2, b_rook2, b_pawn, b_pawn2, 
                b_pawn3, b_pawn4, b_pawn5, b_pawn6,b_pawn7,b_pawn8,w_king, w_bishop,w_bishop2,w_knight,w_knight2, w_queen, w_rook, w_rook2, w_pawn,w_pawn2,w_pawn3,w_pawn4,w_pawn5,w_pawn6,w_pawn7,w_pawn8,w_pawn9]

currently_clicked = None 



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]: 
                for piece in chess_pieces: 
                    if piece.rect.collidepoint(event.pos):
                        currently_clicked = piece

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if currently_clicked:
                    currently_clicked_center_rect = currently_clicked.get_center_rect()
                    for square in squares:
                        if square.colliderect(currently_clicked_center_rect):
                            currently_clicked.update_position((square.x+50, square.y+50))
                            break
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


    