import pygame, requests, sys, os
 
# Создайте оконное приложение, отображающее карту по координатам и в масштабе, который задаётся программно.
api_server = "http://static-maps.yandex.ru/1.x/"


def load_map(scale):
    lon = 37.481338 # Координаты центра карты на старте. Задал координаты университета
    lat = 55.669913
    delta = str(scale)
    params = {
        "ll": ",".join([str(lon), str(lat)]),
        "spn": ",".join([delta, delta]),
        "l": "map"
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


def page_up(scale):
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
    map = load_map(scale)
    return map, scale


def page_down(scale):
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
    map = load_map(scale)
    return map, scale 

      
def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    running = True
    scale = 0.002
    map = load_map(scale)
    screen.blit(pygame.image.load(map), (0, 0))
    while running:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
           running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                new_map, scale = page_up(scale)
                screen.blit(pygame.image.load(new_map), (0, 0))
            if event.key == pygame.K_DOWN:
                new_map, scale = page_down(scale)
                screen.blit(pygame.image.load(new_map), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map) 

if __name__ == "__main__":
    main()