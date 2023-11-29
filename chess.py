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

king = King(king_black, dif*4+50,50)
pawn = Pawn(pawn_black, dif*4+50, dif+50)
queen = Queen(queen_black, dif*3+50, 50)
knight = Knight(knight_black, dif*2+50, 50)
rook = Rook(rook_black, 50, 50)
bishop = Bishop(bishop_black, dif+50, 50)

chess_pieces = [king, pawn, queen, knight, rook, bishop]

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
    
    
    
    
    pygame.display.update()