import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Lingkaran Solid")

# Warna
black = (0, 0, 0)
white = (255, 255, 255)

# Koordinat pusat dan radius lingkaran
center = (width // 1.25, height // 1.25)
radius = 50

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Bersihkan layar
    screen.fill(black)

    # Gambar lingkaran solid
    pygame.draw.circle(screen, white, center, radius)

    # Perbarui tampilan
    pygame.display.flip()
