import pygame, requests, sys, os
 
# Создайте оконное приложение, отображающее карту по координатам и в масштабе, который задаётся программно.
api_server = "http://static-maps.yandex.ru/1.x/"


def load_map():
    lon = 37.481338 # Координаты центра карты на старте. Задал координаты университета
    lat = 55.669913
    delta = "0.002"
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
         
def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    running = True
    while running:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
           running = False
        map = load_map()
        screen.blit(pygame.image.load(map), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map) 
   
if __name__ == "__main__":
    main()