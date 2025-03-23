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
          @producto-eliminado="eliminarProducto"
          @producto-editado="abrirModalParaEditarProducto" 
        />
      </div>
  
      <!-- Modal para Agregar/Editar Producto -->
      <ProductoForm
        v-if="mostrarModal"
        :producto="productoSeleccionado"
        @cerrar-modal="cerrarModal"
        @producto-agregado="agregarProducto"
        @producto-editado="editarProducto"
      />
    </div>
  </template>
  
  <script setup>
  import ProductoItem from './ProductoItem.vue';
  import ProductoForm from './ProductoForm.vue';
  import { ref, reactive, onMounted } from 'vue';
  
  const productos = reactive([]); // Productos desde JSON Server
  const mostrarModal = ref(false); // Para mostrar/ocultar modal
  const productoSeleccionado = ref(null); // Producto a editar
  
  // Cargar productos desde JSON Server
  const cargarProductos = async () => {
    try {
      const response = await fetch('http://localhost:3008/productos');
      const data = await response.json();
      // Establecer disponibilidad basada en el stock al cargar los productos
      data.forEach(producto => {
        producto.disponible = producto.stock > 0;
      });
      productos.splice(0, productos.length, ...data);
    } catch (error) {
      console.error("Error al cargar productos:", error);
    }
  };
  
  // Llamamos a cargar productos cuando el componente se monte
  onMounted(cargarProductos);
  
  // Función para abrir el modal de edición
  const abrirModalParaEditarProducto = (producto) => {
    productoSeleccionado.value = { ...producto }; // Hacer una copia del producto para evitar mutaciones directas
    mostrarModal.value = true;
  };
  
  // Agregar producto
  const agregarProducto = async (producto) => {
    try {
      producto.disponible = producto.stock > 0;
      const response = await fetch('http://localhost:3008/productos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(producto)
      });
      const nuevoProducto = await response.json();
      productos.push(nuevoProducto); // Agregar producto a la lista
    } catch (error) {
      console.error("Error al agregar producto:", error);
    }
  };
  
  // Editar producto
  const editarProducto = async (producto) => {
    try {
      producto.disponible = producto.stock > 0;
      await fetch(`http://localhost:3008/productos/${producto.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(producto)
      });
      const index = productos.findIndex((p) => p.id === producto.id);
      productos[index] = producto;
    } catch (error) {
      console.error("Error al editar producto:", error);
    }
  };
  
  // Eliminar producto
  const eliminarProducto = async (id) => {
    try {
      await fetch(`http://localhost:3008/productos/${id}`, { method: 'DELETE' });
      productos.splice(productos.findIndex(p => p.id === id), 1); // Eliminar del array reactivo
    } catch (error) {
      console.error("Error al eliminar producto:", error);
    }
  };
  
  // Abrir modal para agregar producto
  const abrirModalNuevoProducto = () => {
    productoSeleccionado.value = null; // No editar, solo agregar
    mostrarModal.value = true;
  };
  
  // Cerrar modal
  const cerrarModal = () => {
    mostrarModal.value = false;
  };
  </script>
  
  <style scoped>
  /* Estilo para los productos */
  </style>
  