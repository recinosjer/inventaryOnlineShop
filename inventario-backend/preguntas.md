# Respuestas.md

## 1. Ventajas de GraphQL vs REST para gestión de inventarios

Cuando trabajamos con un sistema de inventario de productos, GraphQL nos ofrece varias ventajas prácticas frente al tradicional REST:

- **Solo pides lo que necesitas**: Imagina que solo quieres el nombre y stock de un producto. Con GraphQL puedes pedir exactamente esos campos, sin recibir datos innecesarios que ralentizan la comunicación.
  
- **Simplifica las conexiones**: Olvídate de crear múltiples endpoints. Todo funciona a través de una única ruta (`/graphql`), haciendo el backend más ordenado y fácil de mantener.

- **Modificaciones a medida**: Si necesitas, por ejemplo, aumentar el stock de un producto, puedes hacerlo con operaciones específicas (mutaciones) diseñadas exactamente para ese propósito.

- **Más eficiencia**: Al reducir la cantidad de datos que viajan entre cliente y servidor, todo funciona más rápido, especialmente importante en apps con muchos usuarios.

## 2. Cómo estructuramos los tipos y resolvers en GraphQL

Cuando construimos una API con Flask y Graphene, organizamos el código así:

**Definiendo los tipos (el modelo de datos):**
Cada tipo (como Producto) se define como una clase que hereda de `ObjectType`, donde especificamos qué campos tendrá y de qué tipo son:

```python
class ProductoType(graphene.ObjectType):
    id = graphene.Int()
    nombre = graphene.String()
    precio = graphene.Float()
    stock = graphene.Int()
    disponible = graphene.Boolean()
```


## Resolvers (Resolutores)

Los resolvers son métodos que se encargan de procesar las consultas (queries) o modificaciones (mutaciones). Se definen en las clases `Query` y `Mutation`.

Ejemplo en código:
```python
class Query(graphene.ObjectType):
    productos = graphene.List(ProductoType)

    def resolve_productos(self, info):
        return productos
```

Las mutaciones como `modificarStock`, `editarProducto` o `agregarProducto` también se definen como clases con métodos `mutate()` que incluyen toda la lógica necesaria.

---

## 3. ¿Por qué es clave que el backend gestione `disponible` y no depender solo del frontend?

Hay varias razones importantes:

* **Seguridad y coherencia**: Si solo el frontend actualizara este campo, un usuario con malas intenciones podría manipular el valor a su favor.
* **Flexibilidad**: Otros sistemas (como apps móviles o integraciones externas) podrían usar la API y necesitan que los datos sean consistentes por sí mismos.
* **Fuente confiable**: El backend debe ser siempre la única fuente verdadera del estado de los datos. Esto previene errores y situaciones incoherentes.

En nuestro caso, el campo `disponible` se actualiza automáticamente en el backend cada vez que cambia el `stock`, siguiendo este principio fundamental.

---

## 4. ¿Cómo aseguras que la actualización de stock y disponibilidad sea siempre correcta?

Lo garantizamos mediante este enfoque:

* Toda la lógica de negocio está **concentrada en el backend**, usando mutaciones de GraphQL.
* Operaciones como `modificarStock`, `editarProducto` y `agregarProducto` recalculan automáticamente `disponible` (verificando si `stock > 0`).
* El frontend **nunca toma decisiones** sobre el valor de `disponible`; solo muestra lo que el backend envía.
* Esto nos asegura que la disponibilidad siempre refleje la realidad, sin importar desde dónde se hagan los cambios en la aplicación.