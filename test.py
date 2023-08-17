from constants import *
from sudoku_generator import *
import pygame


class Cell:

    def __init__(self, value, row, col):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.selected = False  # utilized to outline current cell

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self, screen):
        chip_font = pygame.font.Font(None, CHIP_FONT)  # 0 - 9

        # outline cell selected
        if self.selected:
            pygame.draw.rect(screen, BUTTON_BG_COLOR,
                             pygame.Rect(self.col * SQUARE_SIZE, self.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 7)

        # iterate through board and display marks in pygame window
        for chip in range(1, 10):

            # trying this out
            if self.sketched_value == chip:
                chip_surf = chip_font.render(str(chip), 0, USER_SKETCHED_COLOR)
                chip_rect = chip_surf.get_rect(
                    center=(SQUARE_SIZE * self.col + SQUARE_SIZE // 4 - 8, SQUARE_SIZE * self.row + SQUARE_SIZE // 4))
                screen.blit(chip_surf, chip_rect)

            if self.value == chip:
                chip_surf = chip_font.render(str(chip), 0, NUMBERS_SOLVED_COLOR)
                chip_rect = chip_surf.get_rect(
                    center=(SQUARE_SIZE * self.col + SQUARE_SIZE // 2, SQUARE_SIZE * self.row + SQUARE_SIZE // 2))
                screen.blit(chip_surf, chip_rect)


class Board:

    def __init__(self, width, height, screen, difficulty):
        self.width = WIDTH
        self.height = HEIGHT
        self.screen = screen
        self.difficulty = difficulty
        self.board = generate_sudoku(9, difficulty)

        # fill cells with board values
        self.rows = 9
        self.cols = 9
        self.cells = [
            [Cell(self.board[i][j], i, j) for j in range(self.cols)]
            for i in range(self.rows)]

        self.initial_board = self.initial_board_clone()

        self.box_length = math.sqrt(self.rows)

    def draw(self, initial=False):
        screen.fill(BG_COLOR)  # update screen so previous cell selected goes away

        # draw horizontal lines
        for i in range(1, BOARD_ROWS + 1):
            # if line is #3 or #6, draw a thick line
            if i % 3 == 0:
                pygame.draw.line(
                    screen,
                    LINE_COLOR,
                    (0, i * SQUARE_SIZE),
                    (WIDTH, i * SQUARE_SIZE),
                    THICK_LINE_WIDTH
                )
            else:

                pygame.draw.line(
                    screen,
                    LINE_COLOR,
                    (0, i * SQUARE_SIZE),
                    (WIDTH, i * SQUARE_SIZE),
                    CELL_LINE_WIDTH
                )

        # draw vertical lines
        for j in range(1, BOARD_COLS):
            # if line is #3 or #6, draw a thick line
            if j % 3 == 0:
                pygame.draw.line(
                    screen,
                    LINE_COLOR,
                    (j * SQUARE_SIZE, 0),
                    (j * SQUARE_SIZE, HEIGHT - 100),
                    THICK_LINE_WIDTH
                )
            else:

                pygame.draw.line(
                    screen,
                    LINE_COLOR,
                    (j * SQUARE_SIZE, 0),
                    (j * SQUARE_SIZE, HEIGHT - 100),
                    CELL_LINE_WIDTH
                )

        # draw cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(self.screen)

        # draw buttons
        button_font = pygame.font.Font(None, BUTTON_FONT)

        reset_text = button_font.render("RESET", 0, BUTTON_COLOR)
        reset_surf = pygame.Surface((reset_text.get_size()[0] + 20, reset_text.get_size()[1] + 20))
        reset_surf.fill(BUTTON_BG_COLOR)
        reset_outline = pygame.Surface((reset_text.get_size()[0] + 28, reset_text.get_size()[1] + 28))
        reset_outline.fill(LINE_COLOR)
        reset_rect = reset_outline.get_rect(center=(WIDTH / 10, HEIGHT * 0.95))
        reset_surf.blit(reset_text, (10, 10))
        reset_outline.blit(reset_surf, (4, 4))
        screen.blit(reset_outline, reset_rect)

        restart_text = button_font.render("RESTART", 0, BUTTON_COLOR)
        restart_surf = pygame.Surface((restart_text.get_size()[0] + 20, restart_text.get_size()[1] + 20))
        restart_surf.fill(BUTTON_BG_COLOR)
        restart_outline = pygame.Surface((restart_text.get_size()[0] + 28, restart_text.get_size()[1] + 28))
        restart_outline.fill(LINE_COLOR)
        restart_rect = restart_outline.get_rect(center=(WIDTH / 3, HEIGHT * 0.95))
        restart_surf.blit(restart_text, (10, 10))
        restart_outline.blit(restart_surf, (4, 4))
        screen.blit(restart_outline, restart_rect)

        exit_text = button_font.render("EXIT", 0, BUTTON_COLOR)
        exit_surf = pygame.Surface((exit_text.get_size()[0] + 20, exit_text.get_size()[1] + 20))
        exit_surf.fill(BUTTON_BG_COLOR)
        exit_outline = pygame.Surface((exit_text.get_size()[0] + 28, exit_text.get_size()[1] + 28))
        exit_outline.fill(LINE_COLOR)
        exit_rect = exit_outline.get_rect(center=(WIDTH * 0.90, HEIGHT * 0.95))
        exit_rect.topright = (WIDTH - reset_rect.left, reset_rect.top)
        exit_surf.blit(exit_text, (10, 10))
        exit_outline.blit(exit_surf, (4, 4))
        screen.blit(exit_outline, exit_rect)

        # return statement for making buttons available outside of function when called when game starts
        if initial:
            return {"RESET": reset_rect, "RESTART": restart_rect, "EXIT": exit_rect,
                    "RESTART_SURFACE": restart_outline, "EXIT_SURFACE": exit_outline}

    def select(self, row, col):
        self.cells[row][col].selected = True

    def deselect(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].selected = False

    def click(self, x, y):  # check if click is within the board coordinates and return (row, col)
        if x < self.width and y < self.height - 100:
            row = y // SQUARE_SIZE
            col = x // SQUARE_SIZE

            return row, col

        return False

    def clear(self, row, col):
        self.cells[row][col].sketched_value = 0
        self.cells[row][col].value = 0  # TRYING THIS OUT

    def sketch(self, value, row, col):
        self.cells[row][col].sketched_value = value
        self.update_board()

    # places user's number in board and calls update_board to show it on screen
    def place_number(self, value, row, col):
        self.board[row][col] = value
        self.update_board()
        self.update_cells()

    def reset_to_original(self):  # with button
        self.cells = [
            [Cell(self.initial_board[i][j], i, j) for j in range(self.cols)]
            for i in range(self.rows)]

    def is_full(self):
        if not self.find_empty():
            self.check_board()

    # TRYING THIS OUT (NOT FINAL) -> updates the screen to show new board values
    def update_board(self):
        self.draw()
        pygame.display.update()

    def find_empty(self):
        # check if there is an empty cell (cell is not zero)

        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != 0:
                    return True

        return False

    def check_board(self):
        pass

    # clone the initial board
    def initial_board_clone(self):
        initial_board = [[0 for j in range(BOARD_COLS)] for i in range(9)]
        for row in range(self.rows):
            for col in range(self.cols):
                initial_board[row][col] = self.board[row][col]
        return initial_board

    # update cells with current board values
    def update_cells(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].sketched_value == 0:
                    self.cells[i][j] = Cell(self.board[i][j], i, j)

    # checks if the user's selected cell can be modified
    def can_place(self, row, col):

        if self.initial_board[row][col] == 0:
            return True

        return False

    # METHODS TO CHECK WHETHER THE BOARD IS COMPLETED CORRECTLY

    def is_valid(self, row, col, num):
        # makes sure to pass (x,x) to valid in box
        if self.valid_in_box(row - (row % self.box_length), col - (col % self.box_length), num) and self.valid_in_row(row, num) and self.valid_in_col(col, num):
            return True

        return False

    def valid_in_row(self, row, num):
        for j in range(self.rows):
            if self.board[row][j] == num:
                return False

        return True

    def valid_in_col(self, col, num):
        for i in range(self.cols):
            if self.board[i][col] == num:
                return False

        return True

    def valid_in_box(self, row_start, col_start, num):

        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                if num == self.board[i][j]:
                    return False

        return True


def draw_start_screen(screen):
    welcome_font = pygame.font.Font(None, WELCOME_FONT)
    diff_font = pygame.font.Font(None, DIFFICULTY_FONT)
    button_font = pygame.font.Font(None, BUTTON_FONT)

    screen.fill(BG_COLOR)

    # display welcome text
    welcome_surf = welcome_font.render("Welcome to Sudoku", 0, LINE_COLOR)
    welcome_rect = welcome_surf.get_rect(center=(WIDTH / 2, HEIGHT / 4))
    screen.blit(welcome_surf, welcome_rect)

    # display difficulty selection text
    diff_surf = diff_font.render("Select Game Mode:", 0, LINE_COLOR)
    diff_rect = diff_surf.get_rect(center=(WIDTH / 2, HEIGHT * 0.60))
    screen.blit(diff_surf, diff_rect)

    # display buttons
    easy_text = button_font.render("EASY", 0, BUTTON_COLOR)
    easy_surf = pygame.Surface((easy_text.get_size()[0] + 20, easy_text.get_size()[1] + 20))
    easy_surf.fill(BUTTON_BG_COLOR)
    easy_surf.blit(easy_text, (10, 10))
    easy_outline = pygame.Surface((easy_text.get_size()[0] + 28, easy_text.get_size()[1] + 28))
    easy_outline.fill(LINE_COLOR)
    easy_outline.blit(easy_surf, (4, 4))
    easy_rect = easy_outline.get_rect(center=(WIDTH / 4, HEIGHT * 0.75))

    screen.blit(easy_outline, easy_rect)

    mid_text = button_font.render("MEDIUM", 0, BUTTON_COLOR)
    mid_surf = pygame.Surface((mid_text.get_size()[0] + 20, mid_text.get_size()[1] + 20))
    mid_surf.fill(BUTTON_BG_COLOR)
    mid_surf.blit(mid_text, (10, 10))
    mid_outline = pygame.Surface((mid_text.get_size()[0] + 28, mid_text.get_size()[1] + 28))
    mid_outline.fill(LINE_COLOR)
    mid_outline.blit(mid_surf, (4, 4))
    mid_rect = mid_outline.get_rect(center=(WIDTH / 2, HEIGHT * 0.75))

    screen.blit(mid_outline, mid_rect)

    hard_text = button_font.render("HARD", 0, BUTTON_COLOR)
    hard_surf = pygame.Surface((hard_text.get_size()[0] + 20, hard_text.get_size()[1] + 20))
    hard_surf.fill(BUTTON_BG_COLOR)
    hard_surf.blit(hard_text, (10, 10))
    hard_outline = pygame.Surface((hard_text.get_size()[0] + 28, hard_text.get_size()[1] + 28))
    hard_outline.fill(LINE_COLOR)
    hard_outline.blit(hard_surf, (4, 4))
    hard_rect = hard_outline.get_rect(center=(WIDTH * 0.75, HEIGHT * 0.75))

    screen.blit(hard_outline, hard_rect)

    pygame.display.update()

    while True:  # check if user clicked buttons and return selected difficulty
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    return 30
                if mid_rect.collidepoint(event.pos):
                    return 40
                if hard_rect.collidepoint(event.pos):
                    return 50


def draw_game_won_screen(screen, exit_surf):
    screen.fill(BG_COLOR)
    game_won_font = pygame.font.Font(None, WELCOME_FONT)
    game_won_text = game_won_font.render("Game Won!", 0, LINE_COLOR)
    game_won_rect = game_won_text.get_rect(center=(WIDTH / 2, HEIGHT / 3))
    screen.blit(game_won_text, game_won_rect)

    exit_rect = exit_surf.get_rect(center=(WIDTH / 2, HEIGHT * 0.60))
    screen.blit(exit_surf, exit_rect)


def draw_game_over_screen(screen, restart_surf):
    screen.fill(BG_COLOR)
    game_over_font = pygame.font.Font(None, WELCOME_FONT)
    game_over_text = game_over_font.render("Game Over :(", 0, LINE_COLOR)
    game_over_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 3))
    screen.blit(game_over_text, game_over_rect)

    restart_rect = restart_surf.get_rect(center=(WIDTH / 2, HEIGHT * 0.60))
    screen.blit(restart_surf, restart_rect)


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")

    while True:
        cor = False
        selected_cell_value = 0
        game_over = False

        diff = draw_start_screen(screen)
        screen.fill(BG_COLOR)
        board = Board(WIDTH, HEIGHT, screen, diff)

        button_dict = board.draw(True)  # will store game buttons so they can be used

        while True and not game_over:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    board.deselect()
                    x, y = event.pos
                    cor = board.click(x, y)  # stores the coordinate of the user's click

                    if button_dict["RESET"].collidepoint(event.pos):
                        print("si")
                    if button_dict["RESTART"].collidepoint(event.pos):  # show start screen
                        game_over = True
                        continue
                    if button_dict["EXIT"].collidepoint(event.pos):
                        pygame.quit()

                    # sets the selected cell value to the previously sketched one
                    selected_cell_value = board.cells[cor[0]][cor[1]].sketched_value if cor else 0
                    if cor:
                        board.select(cor[0], cor[1])  # select the cell that user clicked cor[0] = row, cor[1] = col
                    board.draw()  # draw board to show rectangle around cell

                if event.type == pygame.KEYDOWN and cor:  # get number clicked by the user

                    if event.key == pygame.K_1 and board.can_place(cor[0], cor[1]):
                        board.sketch(1, cor[0], cor[1])
                        selected_cell_value = board.cells[cor[0]][
                            cor[1]].sketched_value  # sets the user number equal to the selected value
                    if event.key == pygame.K_RETURN and selected_cell_value == 1:
                        board.clear(cor[0], cor[1])
                        board.place_number(1, cor[0], cor[1])
                        board.draw()

                    if event.key == pygame.K_2 and board.can_place(cor[0], cor[1]):
                        board.sketch(2, cor[0], cor[1])
                        selected_cell_value = board.cells[cor[0]][cor[1]].sketched_value
                    if event.key == pygame.K_RETURN and selected_cell_value == 2:
                        board.clear(cor[0], cor[1])
                        board.place_number(2, cor[0], cor[1])
                        board.draw()

                    if event.key == pygame.K_3 and board.can_place(cor[0], cor[1]):
                        board.sketch(3, cor[0], cor[1])
                        selected_cell_value = board.cells[cor[0]][cor[1]].sketched_value
                    if event.key == pygame.K_RETURN and selected_cell_value == 3:
                        board.clear(cor[0], cor[1])
                        board.place_number(3, cor[0], cor[1])
                        board.draw()

                    if event.key == pygame.K_4 and board.can_place(cor[0], cor[1]):
                        board.sketch(4, cor[0], cor[1])
                        selected_cell_value = board.cells[cor[0]][cor[1]].sketched_value
                    if event.key == pygame.K_RETURN and selected_cell_value == 4:
                        board.clear(cor[0], cor[1])
                        board.place_number(4, cor[0], cor[1])
                        board.draw()

                    if event.key == pygame.K_5 and board.can_place(cor[0], cor[1]):
                        board.sketch(5, cor[0], cor[1])
                        selected_cell_value = board.cells[cor[0]][cor[1]].sketched_value
                    if event.key == pygame.K_RETURN and selected_cell_value == 5:
                        board.clear(cor[0], cor[1])
                        board.place_number(5, cor[0], cor[1])
                        board.draw()

                    if event.key == pygame.K_6 and board.can_place(cor[0], cor[1]):
                        board.sketch(6, cor[0], cor[1])
                        selected_cell_value = board.cells[cor[0]][cor[1]].sketched_value
                    if event.key == pygame.K_RETURN and selected_cell_value == 6:
                        board.clear(cor[0], cor[1])
                        board.place_number(6, cor[0], cor[1])
                        board.draw()

                    if event.key == pygame.K_7 and board.can_place(cor[0], cor[1]):
                        board.sketch(7, cor[0], cor[1])
                        selected_cell_value = board.cells[cor[0]][cor[1]].sketched_value
                    if event.key == pygame.K_RETURN and selected_cell_value == 7:
                        board.clear(cor[0], cor[1])
                        board.place_number(7, cor[0], cor[1])
                        board.draw()

                    if event.key == pygame.K_8 and board.can_place(cor[0], cor[1]):
                        board.sketch(8, cor[0], cor[1])
                        selected_cell_value = board.cells[cor[0]][cor[1]].sketched_value
                    if event.key == pygame.K_RETURN and selected_cell_value == 8:
                        board.clear(cor[0], cor[1])
                        board.place_number(8, cor[0], cor[1])
                        board.draw()

                    if event.key == pygame.K_9 and board.can_place(cor[0], cor[1]):
                        board.sketch(9, cor[0], cor[1])
                        selected_cell_value = board.cells[cor[0]][cor[1]].sketched_value
                    if event.key == pygame.K_RETURN and selected_cell_value == 9:
                        board.clear(cor[0], cor[1])
                        board.place_number(9, cor[0], cor[1])
                        board.draw()

                    if event.key == pygame.K_BACKSPACE and board.can_place(cor[0], cor[1]):
                        if board.cells[cor[0]][cor[1]].sketched_value != 0:
                            board.clear(cor[0], cor[1])
                            board.update_cells()

                        if board.board[cor[0]][cor[1]] != 0:
                            board.board[cor[0]][cor[1]] = 0

                            board.update_cells()

                    board.update_board()

                    if event.key == pygame.K_w:
                        draw_game_won_screen(screen, button_dict["EXIT_SURFACE"])
                    if event.key == pygame.K_o:
                        draw_game_over_screen(screen, button_dict["RESTART_SURFACE"])

            pygame.display.update()
