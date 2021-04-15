import pygame, requests, sys, os
 
# Создайте оконное приложение, отображающее карту по координатам и в масштабе, который задаётся программно.
api_server = "http://static-maps.yandex.ru/1.x/"


def load_map(scale, lon, lat, view):
    lon, lat, view = lon, lat, view
    delta = str(scale)
    params = {
        "ll": ",".join([str(lon), str(lat)]),
        "spn": ",".join([delta, delta]),
        "l": view
    }
    response = requests.get(api_server, params=params)
    if not response:
        print("Ошибка выполнения запроса:")

 
    # Запись полученного изображения в файл.
    map = "map.png"
    try:
        with open(map, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map


def page_up(scale, view):
    if scale <= 0.31:
        if scale == 0.001:
            scale += 0.001
        elif scale == 0.002:
            scale += 0.001
        elif scale == 0.003:
            scale += 0.003
        elif scale == 0.006:
            scale += 0.005
        elif scale == 0.011:
            scale += 0.02
    map = load_map(scale, 0, 0, view)
    return map, scale


def page_down(scale, view):
    if scale >= 0.001:
        if scale == 0.002:
            scale -= 0.001
        elif scale == 0.003:
            scale -= 0.001
        elif scale == 0.006:
            scale -= 0.003
        elif scale == 0.011:
            scale = round(scale - 0.005, 3)
        elif scale == 0.031:
            scale -= 0.02
    map = load_map(scale, 0, 0, view)
    return map, scale 


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    running = True
    lon = 37.481338 
    lat = 55.669913
    scale = 0.002
    view = "map"
    map = load_map(scale, lon, lat, view)
    screen.blit(pygame.image.load(map), (0, 0))
    while running:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
           running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS: #page_up
                new_map, scale = page_up(scale, view)
                screen.blit(pygame.image.load(new_map), (0, 0))
            if event.key == pygame.K_MINUS: #page_down
                new_map, scale = page_down(scale, view)
                screen.blit(pygame.image.load(new_map), (0, 0))
            if event.key == pygame.K_RIGHT:
                lon += 0.001
                screen.blit(pygame.image.load(load_map(scale, lon, lat, view)), (0, 0))
            if event.key == pygame.K_LEFT:
                lon -= 0.001
                screen.blit(pygame.image.load(load_map(scale, lon, lat, view)), (0, 0))
            if event.key == pygame.K_UP:
                lat += 0.001
                screen.blit(pygame.image.load(load_map(scale, lon, lat, view)), (0, 0))
            if event.key == pygame.K_DOWN:
                lat -= 0.001
                screen.blit(pygame.image.load(load_map(scale, lon, lat, view)), (0, 0))
            if event.key == pygame.K_m: #кнопка с латинской буквой m
                view = "map"
                screen.blit(pygame.image.load(load_map(scale, lon, lat, view)), (0, 0))
            if event.key == pygame.K_s:
                view = "sat" # Кнопка с латинской буквой s
                screen.blit(pygame.image.load(load_map(scale, lon, lat, view)), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map) 


if __name__ == "__main__":
    main()