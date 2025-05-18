# Inventario Vue 3 + Tailwind + JSON Server

Este proyecto es un CRUD de productos de inventario construido con Vue 3, Tailwind CSS y un backend simulado con JSON Server.  
Permite agregar, editar, eliminar y actualizar el stock de productos en tiempo real, reflejando los cambios tanto en la interfaz como en el servidor simulado.

## Preguntas respondidas

### 1. Vue no detecta cambios dentro de objetos reactivos de la forma que esperarías. ¿Cómo podrías observar un cambio en una propiedad anidada?

Vue 3, cuando trabajamos con `reactive()`, no siempre detecta cambios en propiedades anidadas si modificamos objetos de manera no reactiva.  
Para observar un cambio en una propiedad anidada, puedo hacerlo de dos maneras:  

- Usando `watch` con una función que retorne la propiedad anidada:  

```js
watch(() => objeto.anidado.propiedad, (nuevoValor) => {
  console.log('La propiedad cambió a', nuevoValor);
});
```

- O utilizando un `deep watch` (`deep: true`) si quiero observar todo el objeto de forma profunda (aunque esto es menos eficiente):

```js
watch(objeto, (nuevoValor) => {
  console.log('Cualquier cambio en el objeto reactivo:', nuevoValor);
}, { deep: true });
```

---

### 2. `watch()` permite escuchar cambios en propiedades específicas dentro de `reactive()`, explica cómo funciona.

`watch()` es una función de Vue que me permite reaccionar cuando cambia una o varias propiedades reactivas.  
Funciona observando un valor o una función que retorna un valor reactivo. Cada vez que ese valor cambia, ejecuta un callback.  

Por ejemplo, si tengo un objeto reactivo llamado `producto`, y quiero escuchar solo los cambios de su stock, puedo hacerlo así:  

```js
watch(() => producto.stock, (nuevoStock) => {
  console.log('El stock cambió a', nuevoStock);
});
```

La función que le paso a `watch` (`() => producto.stock`) es la que le dice a Vue qué propiedad quiero escuchar. Cuando detecta un cambio en esa propiedad, ejecuta la función que le paso como segundo parámetro.

---

### 3. ¿Cómo harías que un `watch()` detecte cambios en stock dentro de un array de productos?

Si tengo un array de productos (reactivo) y quiero detectar los cambios en el `stock` de cualquier producto dentro del array, puedo hacerlo utilizando un `deep watch` sobre el array completo:  

```js
watch(productos, (nuevosProductos) => {
  console.log('Se ha cambiado el stock o cualquier propiedad dentro de un producto');
}, { deep: true });
```

También, si quiero hacerlo de forma más específica y eficiente, puedo iterar sobre cada producto y crear un `watch` individual para cada uno:  

```js
productos.forEach(producto => {
  watch(() => producto.stock, (nuevoStock) => {
    console.log(`El stock del producto ${producto.nombre} cambió a ${nuevoStock}`);
  });
});
```

---

### Tecnologías usadas:
- Vue 3 (Composition API)
- Tailwind CSS
- JSON Server

---
