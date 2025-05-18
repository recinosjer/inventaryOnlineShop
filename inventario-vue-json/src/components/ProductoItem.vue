<template>
  <div class="bg-white p-4 rounded-lg shadow-md hover:scale-105 transition">
    <h3 class="text-xl font-semibold">{{ producto.nombre }}</h3>
    <p class="text-gray-500">Precio: ${{ producto.precio }}</p>

    <p :class="{'text-red-500': !producto.disponible, 'text-green-500': producto.disponible}">
      {{ producto.disponible ? 'Disponible' : 'No Disponible' }}
    </p>

    <p class="text-sm text-gray-500">Stock: {{ producto.stock }}</p>

    <div class="flex space-x-2 mt-4">
      <button @click="disminuirStock" class="bg-yellow-600 text-white px-3 py-1 rounded hover:bg-yellow-700">-</button>
      <button @click="aumentarStock" class="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700">+</button>
      <button @click="editarProducto" class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition">Editar</button>
      <button @click="eliminarProducto" class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition">Eliminar</button>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  producto: Object,
  modificarStock: Function,
  onEditar: Function,
  onEliminar: Function
});

const aumentarStock = () => {
  props.modificarStock(props.producto.id, 1);
};

const disminuirStock = () => {
  if (props.producto.stock > 0) {
    props.modificarStock(props.producto.id, -1);
  }
};

const editarProducto = () => {
  props.onEditar(props.producto);
};

const eliminarProducto = () => {
  if (confirm("¿Seguro que quieres eliminar este producto?")) {
    props.onEliminar(props.producto.id);
  }
};
</script>
