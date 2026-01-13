import utils.pretty_print
#import entities.item as item
#import entities.usuario as usuario

lista = []

def cargar_items():
    data = open('items.dcc', 'r')
    for i in data:
        lista.append(i)
    data.close()

print(lista)