# Tarea 1: Dccasillas :school_satchel:

## Consideraciones generales :octocat:

<Fui capaz de hacer casi todo, con mucha ayuda de internet, de los cuales coloqué los links de lo que utilicé por el codigo, lo implemente como comentarios, no saque codigos directamente pero igual dejé la constancia de los links que visité, en esos links busque como se utilizaban funciones que no sabia como funcionaban>

### Cosas implementadas y no implementadas :white_check_mark: :x:

##### Funcionalidades 
* En la primera parte, clase Tablero, logre sacar todos los testscases con cada una de las funciones, para la funcion de encontrar solucion definí otra funcion dentro de ella para crear una funcion recursiva (backtracking) hasta que validar() se cumpliera y en caso de que recursivamente se convirtiera el tablero en el inicial esta retorna None y asi se encuentra la solución. 🟢


* Para la segunda clase no logré hacer la función de recuperar estado, me dió demasiados problemas desde el principio. Pero de resto logré sacar todos los testcases y durante el código deje links con todo lo que saque de internet para lograr sacar la tarea🟨

* Para el menú hice todo lo que pedían. Primero se pide el nombre de usuario, luego la configuración que se quiere utlizar (con o sin .txt) y despues de probar llama bien a las funciones de tablero y dccasillas y puedes jugar el juego a traves del menú.-🟢

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Tienen que tener los archivos ```tablero.py``` y ```dccasillas.py``` y ```visualizador.pyc``` en una carpeta y ejecutar ```main.py``` para que funcione, no es necesario instalar nada más


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: ```os.path.join``` y ```os.path.exists```
2. ```copy```: ```copy.deepcopy```
3. ``visualizador.pyc```: ```visualizador.imprimir_tablero```

### Librerías propias
No creé librerias propias solo una funcion recursiva y los menús.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. https://docs.python.org/es/3.13/tutorial/errors.html. Esto me explico que era try, except y como se usaba
2. https://www.geeksforgeeks.org/dsa/introduction-to-backtracking-2 esto me explico que era el backtracking para usarlo en la funcion de encontrar solucion
3. https://www.pythontutorial.net/python-basics/python-create-text-file esto me explico como se creba un archivo desde python para guardar un estado
4. https://stackoverflow.com/questions/2259382/pythonic-way-to-check-if-a-file-exists este me explico como saber si un archivo existe o no
5. 
