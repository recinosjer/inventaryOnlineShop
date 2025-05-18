<template>
  <div class="container mx-auto p-6">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Productos en Inventario</h2>
      <button
        @click="abrirModalNuevoProducto"
        class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition"
      >
        Agregar Producto
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <ProductoItem
        v-for="producto in productos"
        :key="producto.id"
        :producto="producto"
        :modificarStock="modificarStock"
        :onEditar="abrirModalParaEditarProducto"
        :onEliminar="eliminarProducto"
      />
    </div>

    <ProductoForm
      v-if="mostrarModal"
      :producto="productoSeleccionado"
      @cerrar-modal="cerrarModal"
      @producto-editado="actualizarProducto"
    />

  </div>
</template>

<script setup>
import ProductoItem from './ProductoItem.vue';
import ProductoForm from './ProductoForm.vue';
import { ref, reactive, onMounted, watch } from 'vue';

const productos = reactive([]);
const mostrarModal = ref(false);
const productoSeleccionado = ref(null);


const graphqlFetch = async (query) => {
  const response = await fetch('http://127.0.0.1:5000/graphql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });
  return await response.json();
};

const cargarProductos = async () => {
  const data = await graphqlFetch(`
    {
      productos {
        id nombre precio stock disponible
      }
    }
  `);
  productos.splice(0, productos.length, ...data.data.productos);
};

onMounted(cargarProductos);

const agregarProducto = async (producto) => {
  const query = `
    mutation {
      agregarProducto(nombre: "${producto.nombre}", precio: ${producto.precio}, stock: ${producto.stock}) {
        producto { id nombre precio stock disponible }
      }
    }
  `;
  const data = await graphqlFetch(query);
  productos.splice(productos.length, 0, data.data.agregarProducto.producto);
  cerrarModal();
};

const editarProducto = async (producto) => {
  if (!producto.id) return;

  const query = `
    mutation {
      editarProducto(id: ${producto.id}, nombre: "${producto.nombre}", precio: ${producto.precio}, stock: ${producto.stock}) {
        producto { id nombre precio stock disponible }
      }
    }
  `;
  const data = await graphqlFetch(query);
  const actualizado = data.data.editarProducto.producto;

  const index = productos.findIndex(p => p.id === actualizado.id);
  if (index !== -1) {
    productos[index] = actualizado;
  } else {
    productos.push(actualizado);
  }

  cerrarModal();
};

const eliminarProducto = async (id) => {
  if (!confirm("¿Estás seguro?")) return;
  await graphqlFetch(`
    mutation {
      eliminarProducto(id: ${id}) { ok }
    }
  `);
  const index = productos.findIndex(p => p.id === id);
  if (index !== -1) productos.splice(index, 1);
};

const modificarStock = async (id, cantidad) => {
  const query = `
    mutation {
      modificarStock(id: ${id}, cantidad: ${cantidad}) {
        producto { id stock disponible }
      }
    }
  `;
  const data = await graphqlFetch(query);
  const actualizado = data.data.modificarStock.producto;
  const index = productos.findIndex(p => p.id === id);
  productos[index].stock = actualizado.stock;
  productos[index].disponible = actualizado.disponible;
};

const actualizarProducto = (producto) => {
  const index = productos.findIndex(p => p.id === producto.id);
  if (index !== -1) {
    productos[index] = producto;
  } else {
    productos.push(producto);
  }
};

const abrirModalParaEditarProducto = (producto) => {
  productoSeleccionado.value = { ...producto };
  mostrarModal.value = true;
};

const abrirModalNuevoProducto = () => {
  productoSeleccionado.value = null;
  mostrarModal.value = true;
};

const cerrarModal = () => {
  mostrarModal.value = false;
};
</script>

