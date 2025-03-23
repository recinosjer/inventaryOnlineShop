<template>
  <div class="bg-white p-4 rounded-lg shadow-md hover:scale-105 transition">
    <h3 class="text-xl font-semibold">{{ producto.nombre }}</h3>
    <p class="text-gray-500">Precio: ${{ producto.precio }}</p>
    
    <!-- Mostrar disponibilidad -->
    <p :class="{'text-red-500': !producto.disponible, 'text-green-500': producto.disponible}">
      {{ producto.disponible ? 'Disponible' : 'No Disponible' }}
    </p>
    
    <p class="text-sm text-gray-500">Stock: {{ producto.stock }}</p>

    <!-- Botones para aumentar y disminuir el stock -->
    <div class="flex space-x-2 mt-4">
      <button 
        @click="disminuirStock" 
        class="bg-yellow-600 text-white px-4 py-2 rounded-md hover:bg-yellow-700 transition"
        :disabled="producto.stock <= 0"
      >
        -
      </button>
      <button 
        @click="aumentarStock" 
        class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition"
      >
        +
      </button>
      <button 
        @click="editarProducto" 
        class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition"
      >
        Editar
      </button>
      <button 
        @click="eliminarProducto" 
        class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition"
      >
        Eliminar
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, watch, reactive } from 'vue';

// Recibimos el producto desde el componente padre
const props = defineProps({
  producto: Object
});
const emit = defineEmits(['producto-eliminado', 'producto-editado']);

// Hacemos que el producto sea reactivo para observar sus cambios
const producto = reactive({ ...props.producto });

// Funciones para aumentar y disminuir el stock
const disminuirStock = async () => {
  if (producto.stock > 0) {
    // Actualizar el stock en el frontend inmediatamente
    producto.stock--;
    producto.disponible = producto.stock > 0; // Actualizar disponibilidad
    
    // Actualizar el stock en el servidor sin esperar
    actualizarStockEnServidor(producto);
  }
};

const aumentarStock = async () => {
  // Actualizar el stock en el frontend inmediatamente
  producto.stock++;
  producto.disponible = producto.stock > 0; // Actualizar disponibilidad
  
  // Actualizar el stock en el servidor sin esperar
  actualizarStockEnServidor(producto);
};

// Función para actualizar el stock en el servidor
const actualizarStockEnServidor = (producto) => {
  fetch(`http://localhost:3008/productos/${producto.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(producto)
  }).catch((error) => {
    console.error("Error al actualizar stock en servidor:", error);
    // Si hay error, puedes revertir el cambio visual si lo deseas
  });
};

// Emitir para editar el producto
const editarProducto = () => {
  emit('producto-editado', producto);
};

// Emitir para eliminar el producto
const eliminarProducto = () => {
  if (confirm("¿Estás seguro de eliminar este producto?")) {
    emit('producto-eliminado', producto.id);
  }
};

// Usamos watch para observar los cambios en el stock del producto
watch(() => producto.stock, (nuevoStock) => {
  producto.disponible = nuevoStock > 0;
  actualizarStockEnServidor(producto); // Actualizar servidor cada vez que cambie el stock
});
</script>

<style scoped>
/* Estilos adicionales si son necesarios */
</style>
