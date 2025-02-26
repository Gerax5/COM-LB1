# 🚀 Laboratorio - Construcción Directa de AFD y ecosistema de reconocimiento de expresiones regulares
---
## [📌 Link al video](https://youtu.be/W8fhNUQJccE)
---
## 🎯 Objetivos

✔ Implementación del **algoritmo de construcción directa de AFD**.  
✔ Minimización de AFD, simulación de **AFN y AFD**.  
✔ Generación visual de los autómatas construidos.  
✔ Generación visual de los arboles sintacticos.  
✔ Conversión de expresiones regulares de **infix a postfix** mediante **Shunting Yard**.  
✔ Conversión de expresiones regulares de **infix a postfix** mediante **Shunting Yard**.
---
## 🛠️ Funcionamiento del Programa

### ✅ **1. Entrada**
- Un archivo de texto con lo siguiente:
  - Una **expresiones regulares** para definir un **AFD**.
  - Una o varias **Palabras** para verificar si son aceptadas por el autómata.
- Utilizando el siguiente formato, en el archivo de texto ``1.txt``
```txt
/*Primero la expresion regular*/
0?(1?)?0*
/*Segundo la palabra a evaluar*/
010
```

### 🎯 **2. Procesamiento**
- Convertir la expresión regular en un **AFD** mediante **construcción directa**.
- Convertir la expresion regular sin usar el metodo directo mediante **NFA, DFA, Minimizacion DFA**
- Mostrar el Arbol sintactico del metodo directo y normal.
- Mostrar el AF generado **visualmente**.
- Permitir la simulación de cadenas para verificar si son aceptadas por cada automata creado.

### 🔍 **3. Salida**
- Guardar en carpetas respectivamente los **AF generados** visualmente.
- Indicar si las **cadenas ingresadas** son **aceptadas o rechazadas**.

---
## 👨‍💻 Autor
**Gabriel Gerardo Pineda Riveiro**  
Estudiante de DISEÑO DE LENGUAJES DE PROGRAMACIÓN  
Correo: pin22880@uvg.edu.gt  
ID: 22880  

---
## 📜 Referencias y Uso de Código Externo

- Algoritmo de Shunting Yard, Creacion de Automata NDFA, Creacion de automata DFA y ceracion de Automata Minimizado DFA basado en mi implementacióne para el [Proyecto 1](https://github.com/Gerax5/TCLAB04/tree/Proyecto) de teoria de la computación.
- Generación visual de autómatas utilizando Graphviz (https://graphviz.gitlab.io/).
- Algoritmo de Construción directa AFD basado en la explicacion de [Luis Urbina](https://www.youtube.com/watch?v=1elii9xzYlc)
