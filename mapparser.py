import configparser

# read map file
def read_map(map):
    config = configparser.ConfigParser()
    config.sections()
    config.read(map)

    map = config.get('MAP', 'minimap')
    entities = [x.strip() for x in config['ENTITIES']['entities'].split('\n')]

    # Important stuff
    title = config.get('SETTINGS', 'title')
    next_map = (config.get('SETTINGS', 'nextmap') + '.txt')
    mini_map = []
    entity_list = []
    door_list = []
    soundtrack = config.get('SETTINGS', 'soundtrack')
    player = [
        [float(x.strip()) for x in config['PLAYER']['position'].split(',')], 
        int(config.get('PLAYER', 'angle')),
        [(x.strip()) for x in config['PLAYER']['weapons'].split('\n')]
    ]

    # line = 0
    # for i, in map:
    #     if i != ',' and i != ' ':
    #         if i == '\n':
    #             line += 1
    #             mini_map.append([])
    #         else:
    #             if i == '_':
    #                 i = False
    #             mini_map[line].append(int(i))   

    for i in entities:
        entity_list.append([x.strip() for x in i.split(',')])

    map = ([[x.strip() for x in i.split(',')] for i in map.split('\n')])

    for i in range(len(map)):
        mini_map.append([])
        for j in range(len(map[i])):
            match map[i][j]:
                case '__':
                    mini_map[i].append(False)
                case '_D':
                    mini_map[i].append(False)
                    door_list.append((j, i))
                case _:
                    mini_map[i].append(int(map[i][j]))

    return title, mini_map, entity_list, player, door_list, next_map, soundtrack

# read save file
def open_save():
    try:
        file = open("save.txt","r")
        return file.readlines()[0]
    except:
        return False

# save game
def write_save(game):
    file = open("save.txt","w")
    file.writelines(game.map_file)
    file.close()