import pygame 
import sys 


pygame.init()
pygame.mixer.init()
move = pygame.mixer.Sound("move-self.mp3")
capture = pygame.mixer.Sound("capture.mp3")


width = 800 
height = 800 
dif = width/8

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Insane Crazy Hjemmelagd Sjakk')
Icon = pygame.image.load("chess_icon.png")
pygame.display.set_icon(Icon)

squares_rects = []

board = []

def remove_pieces(location):
    for x in chess_pieces:
        if x.start_pos == location:
            chess_pieces.remove(x)
            pygame.mixer.Sound.play(capture)

def handle_click_event(currently_clicked, turn):
    if currently_clicked:
        if ((currently_clicked.color == "white" and turn == 0) or (currently_clicked.color == "black" and turn == 1)):
            currently_clicked_center_rect = currently_clicked.get_center_rect()
            piece_moved = False
            for square in squares_rects:
                if square.colliderect(currently_clicked_center_rect) and [x.square for x in chess_pieces].count(currently_clicked.square) == 1 and currently_clicked.valid_move((square.x // 100, square.y // 100), board) and currently_clicked.check_saved((square.x // 100, square.y // 100)):
                    pygame.mixer.Sound.play(move)
                    board[currently_clicked.start_pos[1]][currently_clicked.start_pos[0]] = "p"
                    board[square.y // 100][square.x // 100] = currently_clicked
                    remove_pieces((square.x // 100, square.y // 100))
                    currently_clicked.start_pos = (square.x // 100, square.y // 100)
                    currently_clicked.update_position((square.x + 50, square.y + 50))
                    turn = 1 - turn  # Toggle turn between 0 and 1
                    for piece in chess_pieces:
                        piece.valid_move(piece.start_pos, board)

                    if (b_king.check_danger(board) and not b_king.check_mate()) or (w_king.check_danger(board) and not w_king.check_mate()):
                        print("check")
                    if (b_king.check_mate()) or (w_king.check_mate()):
                        print("checkmate")
                    piece_moved = True
                    break
                else:
                    currently_clicked.update_position(currently_clicked_start_pos)
            if not piece_moved:
                currently_clicked.update_position(currently_clicked_start_pos)
            currently_clicked = None
            currently_clicked_center_rect = None
        else:
            currently_clicked.update_position(currently_clicked_start_pos)
            currently_clicked = None
            currently_clicked_center_rect = None
            
    return currently_clicked, turn


class Pawn():
    def __init__(self, image, x, y, color):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.square = (x//100, y//100)
        self.dragging = False
        self.color = color
        self.start_pos = (int(x//100), int(y//100))
        self.valid_moves = []
        
    
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
    
    def is_capture(self, square, board):
        if board[square[1]][square[0]] != "p" and board[square[1]][square[0]].color != self.color:
            return True
        else:
            return False
        
    def is_empty(self, square, board):
        if board[square[1]][square[0]] == "p":
            return True
        else:
            return False


    def valid_move(self, square, board):
        self.valid_moves = []
        col = self.start_pos[0]
        row = self.start_pos[1]

        if self.color == "white":
            direction = -1
        else:
            direction = 1

        # Check if the square in front of the pawn is empty
        if board[row + direction][col] == "p":
            self.valid_moves.append((col, row + direction))

        # Check if the pawn can move two squares forward from its starting position
        if self.first_move() and board[row + direction][col] == "p" and board[row + 2 * direction][col] == "p":
            self.valid_moves.append((col, row + 2 * direction))

        # Check for capturing moves
        if col > 0 and board[row + direction][col - 1] != "p" and board[row + direction][col - 1].color != self.color:
            self.valid_moves.append((col - 1, row + direction))

        if col < 7 and board[row + direction][col + 1] != "p" and board[row + direction][col + 1].color != self.color:
            self.valid_moves.append((col + 1, row + direction))

        if square in self.valid_moves:
            return True
        
        return False
    
    def check_saved(self, square):
        w_king.check_danger(board)
        b_king.check_danger(board)

        if self.color == "white" and w_king.threatening_piece:
            if w_king.threatening_piece.start_pos == square and square in self.valid_moves:
                return True 
        if self.color == "black" and b_king.threatening_piece:
            if b_king.threatening_piece.start_pos == square and square in self.valid_moves:
                return True 
            
        original = self.start_pos
        clone = [row[:] for row in board]
        clone[self.start_pos[1]][self.start_pos[0]] = "p"
        self.start_pos = square
        clone[square[1]][square[0]] = self

        for piece in chess_pieces:
            piece.valid_move(piece.start_pos, clone)

        if self.color == "white":
            if w_king.check_danger(clone):
                self.start_pos = original
                for piece in chess_pieces:
                    piece.valid_move(piece.start_pos, board)
                return False

        elif self.color == "black":
            if b_king.check_danger(clone):
                self.start_pos = original
                for piece in chess_pieces:
                    piece.valid_move(piece.start_pos, board)
                return False

        self.start_pos = original
        for piece in chess_pieces:
            piece.valid_move(piece.start_pos, board)
        return True

    def check_danger(self, board):
        self.threatening_piece = None
        col = self.start_pos[1]
        row = self.start_pos[0]

        for piece in chess_pieces:
            if piece != self and piece.color != self.color and not isinstance(piece, King):
                if piece.valid_move((row, col), board):
                    self.threatening_piece = piece
                    return True

        return False
  
    def diagonal_moves(self, square, board):
        valid_moves = []
        row = self.start_pos[1]
        col = self.start_pos[0]
        #left up diagonal
        for y, x in enumerate(range(col-1, -1, -1), start = 1):
            if board[row-y][x] == "p":
                valid_moves.append((x, row-y))
            elif board[row-y][x] != "p" and board[row-y][x].color != self.color:
                valid_moves.append((x, row-y))
                break
            elif board[row-y][x] != "p" and board[row-y][x].color == self.color:
                break

        #right up diagonal 
        for y, x in enumerate(range(col+1, 8, 1), start = 1):
            if board[row-y][x] == "p":
                valid_moves.append((x, row-y))
            elif board[row-y][x] != "p" and board[row-y][x].color != self.color:
                valid_moves.append((x, row-y))
                break
            elif board[row-y][x] != "p" and board[row-y][x].color == self.color:
                break
        
        #left down diagonal 
        for y, x in enumerate(range(col-1, -1, -1), start = 1):
            if row+y == 8:
                break
            if board[row+y][x] == "p":
                valid_moves.append((x, row+y))
            elif board[row+y][x] != "p" and board[row+y][x].color != self.color:
                valid_moves.append((x, row+y))
                break
            elif board[row+y][x] != "p" and board[row+y][x].color == self.color:
                break
        
        #right down diagonal
        for y, x in enumerate(range(col+1, 8, 1), start = 1):
            if row+y == 8:
                break
            if board[row+y][x] == "p":
                valid_moves.append((x, row+y))
            elif board[row+y][x] != "p" and board[row+y][x].color != self.color:
                valid_moves.append((x, row+y))
                break
            elif board[row+y][x] != "p" and board[row+y][x].color == self.color:
                break
        
        return valid_moves
    
    def horizontal_moves(self, square, board):
        valid_moves = []
        col = self.start_pos[0]
        row = self.start_pos[1]

        #left horizontal
        for x in range(col-1, -1, -1):
            if board[row][x] == "p":
                valid_moves.append((x, row))
            elif board[row][x] != "p" and board[row][x].color != self.color:
                valid_moves.append((x, row))
                break
            elif board[row][x] != "p" and board[row][x].color == self.color:
                break

        #right horizontal 
        for x in range(col+1, 8, 1):
            if board[row][x] == "p":
                valid_moves.append((x, row))
            elif board[row][x] != "p" and board[row][x].color != self.color:
                valid_moves.append((x, row))
                break
            elif board[row][x] != "p" and board[row][x].color == self.color:
                break
        
        #check vertical up 
        for x in range(row-1, -1, -1):
            if board[x][col] == "p":
                valid_moves.append((col, x))
            elif board[x][col] != "p" and board[x][col].color != self.color:
                valid_moves.append((col, x))
                break
            elif board[x][col] != "p" and board[x][col].color == self.color:
                break
        
        #vertical down
        for x in range(row+1, 8, 1):
            if board[x][col] == "p":
                valid_moves.append((col, x))
            elif board[x][col] != "p" and board[x][col].color != self.color:
                valid_moves.append((col, x))
                break
            elif board[x][col] != "p" and board[x][col].color == self.color:
                break
        
        return valid_moves


    

class King(Pawn):
    def __init__(self, image, x, y, color):
        super().__init__(image, x, y, color)
        self.valid_moves = []
    
    def valid_move(self, square, board):
        self.valid_moves = []
        col = self.start_pos[1]
        row = self.start_pos[0]
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1), (1, 0),  (1, 1)
        ]

    # Check each direction and add valid moves within the board limits
        original = self.start_pos
        for dx, dy in directions:
            new_x, new_y = row + dx, col + dy
            
            # Ensure the new position is within the bounds of the board (assuming an 8x8 board)
            if 0 <= new_x <= 7 and 0 <= new_y <= 7:
                temp_board = [row[:] for row in board]
                temp_board[self.start_pos[1]][self.start_pos[0]] = "p"
                temp_board[new_x][new_y] = self
                self.start_pos = (new_x, new_y)

                # Check if the King is safe after the move
                self.check_danger(temp_board)
                if not self.check_danger(temp_board):
                    if self.is_empty((new_x, new_y), board) or self.is_capture((new_x, new_y), board):
                        self.valid_moves.append((new_x, new_y))
               
        if square in self.valid_moves:
            self.start_pos = original 
            return True 
        else:
            self.start_pos = original 
            return False 
    
    
    def check_mate(self):
        for move in self.valid_moves:
            temp_board = [row[:] for row in board]
            temp_board[self.start_pos[1]][self.start_pos[0]] = "p"
            temp_board[move[1]][move[0]] = self


            # Check if any piece of the same color can save the king
        for piece in chess_pieces:
            if piece.color == self.color: 
                for move in piece.valid_moves:
                        # Simulate the move and check if it saves the king
                    if piece.check_saved(move):
                        return False  # It's not checkmate if a move saves the king

            # Check if the threatening piece can be captured
        for piece in chess_pieces:
            if self.threatening_piece:
                if piece.valid_move(self.threatening_piece.start_pos, board):
                    return False  # It's not checkmate if the threatening piece can be captured

                # If the threatening piece cannot be captured and no moves save the king, it's checkmate
                return True
        return True



class Queen(Pawn):
    def __init__(self, image, x, y, color):
        super().__init__(image, x, y, color)
        self.valid_moves = []
    
    def valid_move(self, square, board):
        valid_moves = []
        col = self.start_pos[0]
        row = self.start_pos[1]

        valid_moves.extend(self.diagonal_moves(square, board))
        valid_moves.extend(self.horizontal_moves(square, board))
        
        self.valid_moves = valid_moves
        if square in valid_moves:
            return True 
        else:
            return False 

class Knight(Pawn):
    def __init__(self, image, x, y, color):
        super().__init__(image, x, y, color)
        self.valid_moves = []
    
    def valid_move(self, square, board):
        col = self.start_pos[1]
        row = self.start_pos[0]
        valid_moves = []
        knight_moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)]

        for move in knight_moves:
            new_row = row + move[0]
            new_col = col + move[1]

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                valid_moves.append((new_row, new_col))
        
        self.valid_moves = valid_moves
        if square in valid_moves:
            return True 

        else:
            return False 

class Bishop(Pawn):
    def __init__(self, image, x, y, color):
        super().__init__(image, x, y, color)
        self.valid_moves = []
    
    def valid_move(self, square, board):
        valid_moves = []

        valid_moves.extend(self.diagonal_moves(square, board))
        
        self.valid_moves = valid_moves
        if square in valid_moves:
            return True 
        else:
            return False 


class Rook(Pawn):
    def __init__(self, image, x, y, color):
        super().__init__(image, x, y, color)
        self.valid_moves = []

    def valid_move(self, square, board):
        valid_moves = []

        valid_moves.extend(self.horizontal_moves(square, board))

        self.valid_moves = valid_moves
        if square in valid_moves:
            return True 
        else:
            return False 

        

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
b_knight = Knight(knight_black, dif+50, 50, "black")
b_rook = Rook(rook_black, 50, 50, "black")
b_bishop = Bishop(bishop_black, dif*2+50, 50, "black")
b_knight2 = Knight(knight_black, dif*6+50, 50, "black")
b_bishop2 = Bishop(bishop_black, dif*5+50, 50, "black")
b_rook2 = Rook(rook_black, dif*7+50, 50, "black")
b_pawn = Pawn(pawn_black, 50, dif+50, "black")
b_pawn2 = Pawn(pawn_black, dif+50, dif+50, "black")
b_pawn3 = Pawn(pawn_black, dif*2+50, dif+50, "black")
b_pawn4 = Pawn(pawn_black, dif*3+50, dif+50, "black")
b_pawn5 = Pawn(pawn_black, dif*4+50, dif+50, "black")
b_pawn6 = Pawn(pawn_black, dif*5+50, dif+50, "black")
b_pawn7 = Pawn(pawn_black, dif*6+50, dif+50, "black")
b_pawn8 = Pawn(pawn_black, dif*7+50, dif+50, "black")


w_king = King(king_white, dif*4+50,dif*7+50, "white")
w_queen = Queen(queen_white, dif*3+50, dif*7+50, "white")
w_knight = Knight(knight_white, dif+50, dif*7+50, "white")
w_rook = Rook(rook_white, 50, dif*7+50, "white")
w_bishop = Bishop(bishop_white, dif*2+50, dif*7+50, "white")
w_knight2 = Knight(knight_white, dif*6+50, dif*7+50, "white")
w_bishop2 = Bishop(bishop_white, dif*5+50, dif*7+50, "white")
w_rook2 = Rook(rook_white, dif*7+50, dif*7+50, "white")
w_pawn = Pawn(pawn_white, 50, dif*6+50, "white")
w_pawn2 = Pawn(pawn_white, dif+50, dif*6+50, "white")
w_pawn3 = Pawn(pawn_white, dif*2+50, dif*6+50, "white")
w_pawn4 = Pawn(pawn_white, dif*3+50, dif*6+50, "white")
w_pawn5 = Pawn(pawn_white, dif*4+50, dif*6+50, "white")
w_pawn6 = Pawn(pawn_white, dif*5+50, dif*6+50, "white")
w_pawn7 = Pawn(pawn_white, dif*6+50, dif*6+50, "white")
w_pawn8 = Pawn(pawn_white, dif*7+50, dif*6+50, "white")



chess_pieces = [b_king, b_queen, b_knight, b_rook, b_bishop, b_knight2, b_bishop2, b_rook2, b_pawn, b_pawn2, 
                b_pawn3, b_pawn4, b_pawn5, b_pawn6,b_pawn7,b_pawn8,w_king, w_bishop,w_bishop2,w_knight,w_knight2, w_queen, w_rook, w_rook2, w_pawn,w_pawn2,w_pawn3,w_pawn4,w_pawn5,w_pawn6,w_pawn7,w_pawn8]


board = [['p' for _ in range(8)] for _ in range(8)]
for x in chess_pieces:
    board[x.start_pos[1]][x.start_pos[0]] = x


 
currently_clicked = None 
turn = 0


for piece in chess_pieces:
    piece.valid_move(piece.start_pos, board)



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
                currently_clicked, turn = handle_click_event(currently_clicked, turn)
                
        
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


    