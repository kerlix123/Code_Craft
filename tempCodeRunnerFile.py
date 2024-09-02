    next_button = pygame.transform.scale(next_button, (29, 29))

            if 566 <= mouse[0] <= 582 and 598 <= mouse[1] <= 618:
                description("Next level")
                
                transparent_surface = pygame.Surface((22, 20), pygame.SRCALPHA)
                transparent_surface.fill((170, 170, 170, 120))
                window.blit(transparent_surface, (566, 598))
            window.blit(next_button, (562, 592))