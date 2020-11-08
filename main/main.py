import pygame, sys, random

# Functions
def draw_floor():
	screen.blit(floor_surface, (floor_x_pos, 900))
	screen.blit(floor_surface, (floor_x_pos + width, 900))

def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos-300))
	return bottom_pipe, top_pipe

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 1024:
			screen.blit(pipe_surface, pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
			screen.blit(flip_pipe, pipe)

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 5
	return pipes

def check_collision(pipes):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			return False

	if bird_rect.top <= -100 or bird_rect.bottom >= 900:
		return False

	return True

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
	return new_bird, new_bird_rect

pygame.init()

width = 576
height = 1024
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# Background
bg_surface = pygame.image.load('assets/sprites/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

# Floor
floor_surface = pygame.image.load('assets/sprites/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# Bird
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-downflap.png')).convert_alpha()
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-midflap.png')).convert_alpha()
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-upflap.png')).convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 350))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# bird_surface = pygame.image.load('S:/repo/Flappy-Bird/main/assets/sprites/bluebird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center=(100, 350))

# Pipes
pipe_surface = pygame.image.load('assets/sprites/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

# Game Loop
while True:
	# Event Loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active == True:
				bird_movement = 0
				bird_movement -= 12
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = (100, 350)
				bird_movement = 0

		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())

		if event.type == BIRDFLAP:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0
			bird_surface,bird_rect = bird_animation()

	screen.blit(bg_surface, (0, 0))

	if game_active:
		bird_movement += gravity
		rotated_bird = rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird, bird_rect)

		game_active = check_collision(pipe_list)

		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)

	floor_x_pos -= 1
	draw_floor()

	if floor_x_pos <= -576:
		floor_x_pos = 0

	pygame.display.update()
	clock.tick(120)