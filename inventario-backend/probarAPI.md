# Cómo ejecutar y probar la API Flask + GraphQL

El proyecto tiene dos partes: un frontend en Vue y un backend en Flask-GraphQL. El proyecto permite manejar productos de una tienda online de forma reactiva.

## Requisitos

- Python 3 instalado
- Node.js y npm instalados


## Instrucciones paso a paso

1. Clona el repositorio

git clone https://github.com/recinosjer/inventaryOnlineShop.git

cd inventario-backend

2. Ejecuta el backend

cd inventario-backend

python app.py

La API GraphQL estará corriendo en:
http://127.0.0.1:5000/graphql

**Importante**: Esta API solo acepta peticiones POST.  
Si visitas esa URL desde el navegador, verás esto:

La API GraphQL está activa. Usa POST con el front en VUE, solo clonando y corriendo con npm run dev para consultas.
Eso es completamente normal. La API no acepta GET por seguridad y diseño.

3. Ejecuta el frontend

En otra terminal:

cd inventario-vue-json:
npm install,
npm run dev

El frontend estará disponible en:
http://localhost:5173

Ahí puede:

- Ver los productos
- Agregar, editar o eliminar productos
- Aumentar y disminuir stock
- Ver si están disponibles o no

4. Opcional: Puede probar con Postman

Use la URL: http://127.0.0.1:5000/graphql  
Con POST  
En el Header: Content-Type: application/json  
Y en el Body (raw JSON):
```
{"query": "{ productos { id nombre precio stock disponible } }"}
```
## ¿Por qué aparece "La API GraphQL está activa. Usa POST con el front en VUE, solo clonando y corriendo con npm run dev para consultas."?

Porque abrio la URL en el navegador, y eso hace una petición GET, pero nuestra API GraphQL está configurada solo para POST.  
No significa que haya un error, simplemente no es la forma correcta de acceder.

## ¿Cómo comprobar que funciona?


``` 
- Abre `http://localhost:5173`
- Prueba agregar, editar y eliminar productos
- Prueba modificar el stock
- Verifica que la disponibilidad cambie automáticamente
- Reinicia la app para comprobar que los datos son momentaneos se podria decir  (guardados en memoria)
```
---

Esto resume todo lo necesario para ejecutar y probar correctamente el backend y frontend del proyecto.
