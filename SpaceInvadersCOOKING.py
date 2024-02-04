import sys  # Add this line at the beginning of your script
import random
import hashlib
import sqlite3
import hashlib
import pygame


# Game Constants
ALIEN_ROWS = 4
ALIEN_LIVES = 3
POINT_VALUES = [5, 10, 15, 20]
screen_width = 800
screen_height = 800

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    # Define shooting probabilities and bullet speed
    alien_shooting_chance = 5  # Example: 5% chance of shooting
    alien_bullet_speed = 5  # Example speed for alien bullets
    bullet_speed = 7  # Speed for the spaceship's bullets

    # Initialize game entities
    aliens, spaceship, life, high_score_table = initialize_game()
    bullets = []  # Initialize an empty list for bullets

    running = True
    try:
        while running:
            current_time = pygame.time.get_ticks()  # Update current time each frame

            # Game handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Handling keyboard input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                spaceship.move("left", screen_width)
            elif keys[pygame.K_RIGHT]:
                spaceship.move("right", screen_width)

            # Debug print to check bullet count before processing
            print("Bullet count before processing:", len(bullets))

            # Shooting bullets
            if keys[pygame.K_SPACE]:
                spaceship.shoot_bullet(current_time, bullets, bullet_speed)
            
            bullets_to_remove = []

            # Handling shooting
        if keys[pygame.K_SPACE]:
            spaceship.shoot_bullet(current_time, bullets, bullet_speed)

        # Process each bullet
        for bullet in list(bullets):  # Use list(bullets) to avoid modifying the list during iteration
            bullet.move()
            if bullet.is_off_screen(screen_height):
                bullets.remove(bullet)
            elif bullet.collides_with(spaceship):
                spaceship.lose_life()
                bullets.remove(bullet)
            else:
                for row in aliens:
                    for alien in list(row):  # Again, use list(row) for safe iteration
                        if bullet.collides_with(alien):
                            alien.lose_life()
                            if not alien.is_alive():
                                row.remove(alien)
                                high_score_table.update_current_score(POINT_VALUES[alien.row])
                            bullets.remove(bullet)
                            break
                    if bullet not in bullets:
                        break

                # Check collision with spaceship
                if bullet.collides_with(spaceship):
                    spaceship.lose_life()
                    bullets_to_remove.append(bullet)
                    continue  # Skip further checks if collision with spaceship

                # Check collision with aliens
                for row in aliens:
                    for alien in row:
                        if bullet.collides_with(alien):
                            alien.lose_life()
                            if not alien.is_alive():
                                row.remove(alien)
                                high_score_table.update_current_score(POINT_VALUES[alien.row])
                            bullets_to_remove.append(bullet)
                            break  # Break out of the inner loop once a bullet hits an alien
                    if bullet in bullets_to_remove:
                        break  # Break out of the outer loop if a bullet has hit an alien

            # Safely remove bullets
            for bullet in bullets_to_remove:
                if bullet in bullets:
                    bullets.remove(bullet)

            # Move remaining bullets
            for bullet in bullets:
                bullet.move()

            
        # Game logic updates
        # Update the position of each alien
            for row in aliens:
                for alien in row:
                    alien.move(screen_width)
                    # Check if alien should shoot a bullet
                    if random.randint(0, 100) < alien_shooting_chance:  # 'alien_shooting_chance' is a probability value
                        alien.shoot_bullet(current_time, bullets, alien_bullet_speed)
                        
            # Debug print to check bullet count after processing
            print("Bullet count after processing:", len(bullets))

            # Update alien positions and shooting
            print("Updating alien positions and shooting...")
            for row in aliens:
                for alien in row:
                    alien.move(screen_width)
                    if random.randint(0, 100) < alien_shooting_chance:
                        alien.shoot_bullet(current_time, bullets, alien_bullet_speed)

            # Update the position of each bullet and check for off-screen bullets
            for bullet in bullets[:]:  # Iterate over a copy of the list
                bullet.move()
                if bullet.is_off_screen(screen_height):
                    bullets.remove(bullet)


        # Initialize font for rendering text
        pygame.font.init()  # Ensure the font module is initialized
        font = pygame.font.SysFont(None, 36)  # Choose an appropriate font and size

        handle_game_logic(aliens, spaceship, bullets, current_time, alien_shooting_chance, alien_bullet_speed)

        # Update game state
        handle_game_logic(aliens, spaceship, bullets, current_time, alien_shooting_chance, alien_bullet_speed)

        # Clear the screen at the start of each frame
        screen.fill((0, 0, 0))

        # Render objects
        for row in aliens:
            for alien in row:
                alien.render(screen)
        spaceship.render(screen)
        for bullet in bullets:
            bullet.render(screen)

        # Render the score
        score_text = font.render(f"Score: {high_score_table.current_score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Update the display at the end of each frame
        pygame.display.flip()

        # Tick the clock to cap frame rate
        clock.tick(60)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Game loop exited")
        pygame.quit()

    

    print("Game loop exited")
    
def handle_game_logic(aliens, spaceship, bullets, current_time, alien_shooting_chance, alien_bullet_speed):
    # Add the code to update aliens, handle bullets, check collisions, etc.
    # For example:
    for row in aliens:
        for alien in row:
            alien.move(screen_width)
            if random.randint(0, 100) < alien_shooting_chance:
                alien.shoot_bullet(current_time, bullets, alien_bullet_speed)

def initialize_game():
    # List of alien classes for each row
    alien_classes = [Row1Alien, Row2Alien, Row3Alien, Row4Alien]

    # Create a grid of aliens using the specific subclass for each row
    aliens = []
    for row_index in range(ALIEN_ROWS):
        row_aliens = []
        AlienClass = alien_classes[row_index]  # Get the class for this row
        for alien_index in range(12):  # Assuming 12 aliens per row
            x_pos = initial_x_position(alien_index)
            y_pos = initial_y_position(row_index)
            row_aliens.append(AlienClass(x_pos, y_pos))
        aliens.append(row_aliens)

    spaceship = SpaceShip("SpaceShip.png", screen_width // 2, screen_height - 50)  # Example starting position
    life = Life(ALIEN_LIVES)
    high_score_table = HighScoreTable()
    return aliens, spaceship, life, high_score_table

def start_game():
    auth = PlayerAuthentication("details.db")
    message = ""  # Initialize message variable

    while True:
        action = input("Do you want to sign up or sign in? (signup/signin): ")
        username = input("Enter username: ")
        password = input("Enter password: ")

        if action == "signup":
            success, message = auth.sign_up(username, password)
        elif action == "signin":
            success, message = auth.sign_in(username, password)
        else:
            success = False
            message = "Invalid action. Please choose 'signup' or 'signin'."

        print(message)

        if success:
            break

def main_game_loop(aliens, spaceship, life, high_score_table):
    while not life.is_game_over():
        update_alien_positions(aliens)
        handle_spaceship_movement(spaceship)
        handle_bullets(aliens, spaceship)
        check_collisions(aliens, spaceship, high_score_table)
        update_score(high_score_table)
        display_game_status(life, high_score_table)
        check_for_end_of_round(aliens)

def update_alien_positions(aliens, screen_width):
    for row in aliens:
        for alien in row:
            alien.x_position += alien.movement_direction
            if alien.x_position >= screen_width - alien.width or alien.x_position <= 0:
                alien.movement_direction *= -1
                alien.y_position += 10  # move down by 10 pixels

def handle_spaceship_movement(spaceship, direction, screen_width):
    if direction == "left" and spaceship.x_position > 0:
        spaceship.x_position -= 5  # move left by 5 pixels
    elif direction == "right" and spaceship.x_position < screen_width:
        spaceship.x_position += 5  # move right by 5 pixels

def handle_bullets(alien_bullets, spaceship_bullet, screen_height):
    for bullet in alien_bullets:
        bullet.y_position += bullet.speed
        if bullet.y_position > screen_height:
            alien_bullets.remove(bullet)

    if spaceship_bullet:
        spaceship_bullet.y_position -= spaceship_bullet.speed
        if spaceship_bullet.y_position < 0:
            spaceship_bullet = None


def check_collisions(aliens, spaceship, alien_bullets, spaceship_bullet, high_score_table):
    for bullet in alien_bullets:
        if bullet.collides_with(spaceship):
            spaceship.lose_life()

    if spaceship_bullet:
        for row in aliens:
            for alien in row:
                if spaceship_bullet.collides_with(alien):
                    alien.lose_life()
                    if alien.lives == 0:
                        row.remove(alien)
                        high_score_table.add_score(POINT_VALUES[alien.row])

def update_score(high_score_table, additional_score):
    high_score_table.current_score += additional_score

def display_game_status(life, high_score_table):
    print(f"Lives Left: {life.count}")
    print(f"Current Score: {high_score_table.current_score}")

def check_for_end_of_round(aliens, screen_width):
    if all(not row for row in aliens):
        # Reset alien positions
        for row_index, row in enumerate(aliens):
            for alien in row:
                alien.x_position = initial_x_position(row_index, alien)
                alien.y_position = initial_y_position(row_index)
                alien.lives = ALIEN_LIVES

        print("All aliens eliminated. Starting next round...")

def initial_x_position(alien_index):
    # Example calculation for x position, assuming each alien is 50 pixels wide
    return alien_index * 50

def initial_y_position(row_index):
    # Example calculation for y position, assuming each row is 40 pixels apart
    return row_index * 40
# Game Initialization or Setup Function
def create_aliens():
    aliens = []
    for row_index in range(ALIEN_ROWS):
        row_aliens = []
        for alien_index in range(10):  # Assuming 10 aliens per row
            x_pos = initial_x_position(row_index, alien_index)
            y_pos = initial_y_position(row_index)
            row_aliens.append(Alien("alien_sprite.png", row_index, x_pos, y_pos))
        aliens.append(row_aliens)
    return aliens


class Alien:
    def __init__(self, sprite, row, x_position, y_position):
        self.sprite = sprite
        self.row = row
        self.x_position = x_position
        self.y_position = y_position
        self.movement_direction = 1  # 1 for right, -1 for left
        self.lives = ALIEN_LIVES
        self.bullet_cooldown = 1000  # time in milliseconds
        self.last_shot_time = 0  # Initialize last shot time
        self.image = pygame.image.load(sprite)  # Load the image
        self.width = self.image.get_width()     # Get the width of the image
        self.height = self.image.get_height()  
        self.image = pygame.image.load(sprite)
        try:
            self.image = pygame.image.load(sprite)
        except FileNotFoundError:
            print(f"Error: Image file '{sprite}' not found.")
            sys.exit(1)  # Exit the game if the image file is not found

    def render(self, screen):
        screen.blit(self.image, (self.x_position, self.y_position))

    def move(self, screen_width):
        self.x_position += self.movement_direction
        if self.x_position >= screen_width or self.x_position <= 0:
            self.movement_direction *= -1
            self.y_position += 10  # Example of moving down

    def shoot_bullet(self, current_time, bullets, bullet_speed):
        if current_time - self.last_shot_time >= self.bullet_cooldown:
            bullet = Bullet(self.sprite, bullet_speed, 'down', self.x_position, self.y_position)
            bullets.append(bullet)
            self.last_shot_time = current_time

    def lose_life(self):
        self.lives -= 1

    def is_alive(self):
        return self.lives > 0
    
class Row1Alien(Alien):
    def __init__(self, x_position, y_position):
        super().__init__("Row1invader.png", 1, x_position, y_position)

class Row2Alien(Alien):
    def __init__(self, x_position, y_position):
        super().__init__("Row2invader.png", 2, x_position, y_position)

class Row3Alien(Alien):
    def __init__(self, x_position, y_position):
        super().__init__("Row3invader.png", 3, x_position, y_position)

class Row4Alien(Alien):
    def __init__(self, x_position, y_position):
        super().__init__("Row4invader.png", 4, x_position, y_position)

class SpaceShip:
    def __init__(self, sprite, x_position, y_position):
        self.x_position = x_position
        self.y_position = y_position
        self.lives = ALIEN_LIVES  # Assuming ALIEN_LIVES is a constant defining initial lives

        # Load the sprite image and store it as a surface
        self.image = pygame.image.load(sprite)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # Initialize the last shot time and cooldown period for shooting
        self.last_shot_time = 0
        self.bullet_cooldown = 500  # Cooldown time in milliseconds, adjust as needed

    def move(self, direction, screen_width):
        if direction == "left" and self.x_position > 0:
            self.x_position -= 5  # Move left by 5 pixels
        elif direction == "right" and self.x_position < screen_width - self.width:
            self.x_position += 5  # Move right by 5 pixels

    def shoot_bullet(self, current_time, bullets, bullet_speed):
        if current_time - self.last_shot_time >= self.bullet_cooldown:
            self.last_shot_time = current_time
            bullet_x = self.x_position + self.width // 2
            bullet_y = self.y_position
            bullet = Bullet("bulletinvader.png", bullet_speed, 'up', bullet_x, bullet_y)
            bullets.append(bullet)

    def lose_life(self):
        # Decrease the life count by 1
        self.lives -= 1

        # You can add additional logic here, like checking if lives are zero
        if self.lives <= 0:
            # Handle what happens when lives reach zero, if needed
            pass

    def render(self, screen):
        screen.blit(self.image, (self.x_position, self.y_position))

class Bullet:
    def __init__(self, sprite, speed, direction, x_position, y_position):
        self.speed = speed
        self.direction = direction
        self.x_position = x_position
        self.y_position = y_position

        # Attempt to load the sprite image
        try:
            self.image = pygame.image.load(sprite)
        except FileNotFoundError:
            print(f"Error: Image file '{sprite}' not found.")
            sys.exit(1)  # Exit the game if the image file is not found

        self.width = self.image.get_width()
        self.height = self.image.get_height()


    def render(self, screen):
        screen.blit(self.image, (self.x_position, self.y_position))

    def move(self):
        if self.direction == 'up':
            self.y_position -= self.speed
        elif self.direction == 'down':
            self.y_position += self.speed

    def is_off_screen(self, screen_height):
        if self.direction == 'up' and self.y_position < 0:
            return True
        elif self.direction == 'down' and self.y_position > screen_height:
            return True
        return False
    
    def collides_with(self, other_sprite):
    # Check for overlap between bullet and other sprite
    # This uses the axis-aligned bounding box (AABB) collision detection approach

    # Check horizontal overlap
        overlap_x = (self.x_position + self.width > other_sprite.x_position and
                    self.x_position < other_sprite.x_position + other_sprite.width)

        # Check vertical overlap
        overlap_y = (self.y_position + self.height > other_sprite.y_position and
                    self.y_position < other_sprite.y_position + other_sprite.height)

    # Collision occurs if there is overlap in both dimensions
        return overlap_x and overlap_y

class Life:
    def __init__(self, initial_lives):
        self.lives = initial_lives

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1

    def is_game_over(self):
        return self.lives <= 0

class HighScoreTable:
    def __init__(self):
        self.scores = []  # List to hold score records, each record could be a tuple (player_name, score)
        self.current_score = 0

    def add_score(self, player_name, score):
        self.scores.append((player_name, score))
        self.scores.sort(key=lambda x: x[1], reverse=True)  # Sort scores in descending order

    def display_high_scores(self):
        print("High Scores:")
        for rank, (player_name, score) in enumerate(self.scores, start=1):
            print(f"{rank}. {player_name} - {score}")

    def reset_current_score(self):
        self.current_score = 0

    def update_current_score(self, additional_score):
        self.current_score += additional_score


class PlayerAuthentication:
    def __init__(self, db_file):
        self.db_file = db_file
        self._create_user_table()

    def _create_user_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def sign_up(self, username, password):
        if self._user_exists(username):
            return False, "Username already exists"

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            return True, "Signup successful"
        except sqlite3.IntegrityError:
            return False, "Username already exists"
        finally:
            conn.close()

    def sign_in(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()

        if result and result[0] == hashed_password:
            return True, "Signin successful"
        else:
            return False, "Username or password is incorrect"

    def _user_exists(self, username):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        return result is not None


if __name__ == "__main__":
    start_game() 
    run_game()
