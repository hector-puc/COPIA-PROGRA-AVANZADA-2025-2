
# Tarea 2: DCCartas contra la DCCatástrofe

## Consideraciones generales :octocat:

El juego solo se puede jugar si en la consola ejecutas main.py en conjunto con la carpeta de archivos que está en el git **importante:** No puede faltar el archivo __init __.py en la carpeta funciones pq crashea ya que no se pueden importar los archivos 

**Detalles**
> 
 -   El flujo de combate que usa el programa está centralizado en `funciones/contexto.py` (función `ejecutar_ronda_ccontexto`)
>     
 -   La selección inicial agrega las cartas directamente al mazo (no a la colección)pero luego las puedes mover en el inventario, quedan correctamente en `coleccion`
>     
 -   La IA DeepSheep muestra una vida “falsa” en los listados `vida_fake` pero no cambia la vida real
>     
-   Se eliminan los buffs al final de la ronda (ej: buffs del Caballero y del Cañón) para que los multiplicadores se reinicien     

### Cosas implementadas y no implementadas :white_check_mark: :x:

-   **POO (ABC, herencia, polimorfismo, properties)**: Hecha completa
    
    -   `Carta` abstracta + `Tropa`, `Estructura`, `Mixta`; property `vida` con setter acotado.
        
-   Entidades Carta (atributos/métodos): Hecha completa
    
    -   `recibir_dano`, `usar_habilidad_especial`, `__str__`, habilidades por ronda.
        
-   Tropa (atributos/atacar/habilidades): Hecha completa
    
    -   Duendes, P.E.P.P.A., Montapatos, Antimuros IngUC, Caballero, Maldecidor duende, Escuadrón de esqueletos, Bárbaros, Espíritu Ígneo, Globo.
        
-   Estructura (atributos/habilidades): Hecha completa
    
    -   Cañón (debuff IA + self-nerf defensa), Torre DIE (stun condicional), Recolector de Agua / Horno / Cuartel de Bárbaros / Cuartel de Duendes / Lápida.
        
-   Mixta (modelado y reglas de combinación): Hecha completa
    
    -   Vida = vida_estructura + (vida_tropa/2), mejor defensa (min de multiplicadores), ataque/mult. ataque de la tropa, prob. especial = promedio + 10% del daño actual y con oop avanzado hereda habilidades de estructura.
        
-   Jugador (atributos/atacar/recibir daño/presentarse): Hecha completa
    
    -   Daño IA se reparte entre Estructuras y Mixtas vivas a partes iguales; luego Tropas si no hay defensivas.
        
-   IA (atributos/atacar/recibir daño/habilidad especial): Hecha completa
    
    -   CatGPT, CowPilot, Crok, DeepSheep, Gemibee con efectos especificados.
        
-   Menú principal: Hecho completo
    
    -   Combatir, Inventario, Tienda, “Espiar IA”, ver info de cartas y salir.
        
-   Tienda: Hecha completa
    
    -   Catálogo persistente hasta reroll, comprar/curar/revivir/reroll, acceso a Taller.
        
-   Taller (combinar cartas): Hecho completo
    
    -   Consume las dos bases, crea Mixta y la agrega a la colección.
    
-   Archivos CSV y `parametros.py`: Hecho completo
    
-   Inicio por argumentos (`sys.argv`): Hecho completo
    
    -   `py main.py <facil|normal|dificil> <nombre>`
        
   -   Esta la opción Espiar a la IA en el menú para la información de esta
        
-   Bonus Guardar/Recuperar partida + Cheat "veotodo": ❌ No implementado.
    

## Ejecución :computer:

El módulo principal de la tarea a ejecutar es  
`main.py`

Además, se deben contar con los siguientes archivos en la carpeta funciones: 
init__.py, carta, contexto, estructura, ia, jugador, leer_archivos, mixta, tropa.

En la carpeta que este al mismo nivel de main (en mi caso T2) tienen que tener: menus, main y parametros 
    

 Notas de uso:
> 
 -   En la selección inicial tienes que elegir 4 cartas (siempre puedes rerollear sugerencias).
>     
 -   En Inventario puedes mover cartas entre Colección/Mazo (**no se puede** tener la misma carta dos veces) y reordenar el mazo.
>     
 -   En Tienda el catálogo permanece hasta que hagas reroll (costo en `parametros.py`).
>     
 -   Entrar en combate corre una ronda completa y vuelve al Menú, ganas oro por ronda y oro por victoria.
 >
-    Siempre que mueran todas tus cartas puedes revivirlas en la tienda, es decir, pierdes pero puedes volver a intentarlo despues de tener mas cartas vivas

## Librerías :books:

### Librerías externas utilizadas

-   `random`(sample) (choice) (randint) (random): generación de aleatoriedad (turnos, probabilidades, selección aleatoria).
    
-   `os` (rutas relativas) 
-  `sys.argv` 
    

### Librerías propias (módulos)

-   `parametros.py`: constantes del juego (costos, probabilidades, oro por ronda/victoria, etc.).
    
-   `funciones/carta.py`: clase abstracta `Carta` (base de Tropa/Estructura/Mixta).
    
-   `funciones/tropa.py`: `Tropa` + habilidades de todas las tropas requeridas.
    
-   `funciones/estructura.py`: `Estructura` + habilidades, reemplazos al morir y reversión de efectos.
    
-   `funciones/mixta.py`: `Mixta` (combinación Tropa+Estructura con reglas de stats y hooks heredados).
    
-   `funciones/jugador.py`: `Jugador` (colección/mazo, ataque, recibir daño, utilidades).
    
-   `funciones/ia.py`: `IA` (stats, multiplicadores, habilidades CatGPT/CowPilot/Crok/DeepSheep/Gemibee).
    
-   `funciones/leer_archivos.py`: lectura CSV robusta (incluye parser para descripciones con comas).
    
-   `funciones/contexto.py`: El cerebro del combate y lo que hace que todo funcione xd  (orden de turnos, habilidades inicio/fin, ataque IA/Jugador, etc)
    
-   `menus.py`:  Incluye algunos menus, compra/curar/revivir/reroll, taller, formateos, inventario
    
    

## Supuestos y consideraciones adicionales :thinking:

1.  Selección inicial = 4 cartas
    Decidi que el mazo siempre tuviera 4 cartas y en un principio tienes opcion para elegir tus primeras 4 cartas del mazo
    
2.  Sin duplicados por nombre en el mazo y compras/inventario evitan duplicados en la colección.  
    
3.  Velocidad de turno: si hay Montapatos vivo, siempre parte el jugador; en otro caso se compara `random()` con `velocidad` de la IA.  

    
4.  Daño de la IA: se divide equitativamente entre Estructuras y Mixtas vivas; sólo si no hay, las Tropas reciben daño.  
    Se aplica multiplicador por tipo y luego el multiplicador_defensa de cada carta
    
5.  Restauración por ronda: efectos temporales como el buff del Caballero y el cañón  se revierte al final de la ronda
    
6.  **Mixtas**:
    
    -   Ataque y multiplicador de ataque provienen de la **Tropa**;
        
    -   Defensa usa el mejor caso (menor multiplicador: menos daño recibido)
        
    -   Vida combinada = vida_estructura + mitad de vida_tropa;
        
    -   Prob. especial = promedio de ambas +10% de la probabilidad inicial
        
        
7.  DeepSheep: únicamente modifica la visualización  para confundir al jugador. No altera el estado real.
    
8.  Puntos no implementados:
    
    -   Bonus Guardar/Recuperar partida
        
    -   Cheatcode `veotodo`
        
        


----------


## Referencias de código externo :book:

Todo lo que utilice lo coloque a lo largo del codigo pero aqui estan los links:

1.  Importar módulos desde otra ubicación:  
    [https://stackoverflow.com/questions/50559539/import-a-file-from-another-location-python](https://stackoverflow.com/questions/50559539/import-a-file-from-another-location-python)  

    
2.  Documentación de `random` (elecciones aleatorias y probabilidades):  
    [https://docs.python.org/3/library/random.html](https://docs.python.org/3/library/random.html)
    
3.  `if __name__ == "__main__"` (ejecución de módulo principal):  
    [https://www.freecodecamp.org/espanol/news/python-if-name-main](https://www.freecodecamp.org/espanol/news/python-if-name-main)
