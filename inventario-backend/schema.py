import graphene

productos = [
    {"id": 1, "nombre": "Laptop", "precio": 1000.0, "stock": 5, "disponible": True},
    {"id": 2, "nombre": "Mouse", "precio": 25.0, "stock": 0, "disponible": False}
]

class ProductoType(graphene.ObjectType):
    id = graphene.Int()
    nombre = graphene.String()
    precio = graphene.Float()
    stock = graphene.Int()
    disponible = graphene.Boolean()

class Query(graphene.ObjectType):
    productos = graphene.List(ProductoType)

    def resolve_productos(self, info):
        return productos

class ModificarStock(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        cantidad = graphene.Int(required=True)

    producto = graphene.Field(ProductoType)

    def mutate(self, info, id, cantidad):
        for p in productos:
            if p["id"] == id:
                p["stock"] += cantidad
                if p["stock"] <= 0:
                    p["stock"] = 0
                    p["disponible"] = False
                else:
                    p["disponible"] = True
                return ModificarStock(producto=p)
        raise Exception("Producto no encontrado")
    
class EditarProducto(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        nombre = graphene.String(required=True)
        precio = graphene.Float(required=True)
        stock = graphene.Int(required=True)

    producto = graphene.Field(ProductoType)

    def mutate(self, info, id, nombre, precio, stock):
        for p in productos:
            if p["id"] == id:
                p["nombre"] = nombre
                p["precio"] = precio
                p["stock"] = stock
                p["disponible"] = stock > 0
                return EditarProducto(producto=p)
        raise Exception("Producto no encontrado")

class AgregarProducto(graphene.Mutation):
    class Arguments:
        nombre = graphene.String(required=True)
        precio = graphene.Float(required=True)
        stock = graphene.Int(required=True)

    producto = graphene.Field(ProductoType)

    def mutate(self, info, nombre, precio, stock):
        nuevo_id = max(p["id"] for p in productos) + 1 if productos else 1
        nuevo = {
            "id": nuevo_id,
            "nombre": nombre,
            "precio": precio,
            "stock": stock,
            "disponible": stock > 0
        }
        productos.append(nuevo)
        return AgregarProducto(producto=nuevo)
    
class EliminarProducto(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        global productos
        productos = [p for p in productos if p["id"] != id]
        return EliminarProducto(ok=True)

class Mutation(graphene.ObjectType):
    modificar_stock = ModificarStock.Field()
    editar_producto = EditarProducto.Field()
    agregar_producto = AgregarProducto.Field()
    eliminar_producto = EliminarProducto.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
