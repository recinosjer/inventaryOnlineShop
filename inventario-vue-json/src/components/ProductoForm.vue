<template>
  <div class="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center">
    <div class="bg-white p-6 rounded-lg w-96">
      <h2 class="text-2xl font-semibold mb-4">{{ producto.id ? 'Editar Producto' : 'Agregar Producto' }}</h2>

      <form @submit.prevent="guardarProducto">
        <div class="mb-4">
          <label class="block text-gray-700">Nombre</label>
          <input v-model="producto.nombre" class="w-full p-2 border rounded-md" required />
        </div>
        <div class="mb-4">
          <label class="block text-gray-700">Precio</label>
          <input v-model="producto.precio" type="decimal" class="w-full p-2 border rounded-md" required />
        </div>
        <div class="mb-4">
          <label class="block text-gray-700">Stock</label>
          <input v-model="producto.stock" type="number" class="w-full p-2 border rounded-md" required />
        </div>

        <div class="flex justify-end space-x-2">
          <button type="button" @click="cerrar" class="bg-gray-400 text-white px-4 py-2 rounded-md hover:bg-gray-500">Cancelar</button>
          <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">Guardar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  producto: Object
});
const emit = defineEmits(['cerrar-modal', 'producto-editado']);

const producto = ref({ ...props.producto });

const guardarProducto = async () => {
  const Nombre = producto.value.nombre.replace(/"/g, '\\"');

  const query = producto.value.id
    ? `
      mutation {
        editarProducto(id: ${producto.value.id}, nombre: "${Nombre}", precio: ${producto.value.precio}, stock: ${producto.value.stock}) {
          producto { id nombre precio stock disponible }
        }
      }`
    : `
      mutation {
        agregarProducto(nombre: "${Nombre}", precio: ${producto.value.precio}, stock: ${producto.value.stock}) {
          producto { id nombre precio stock disponible }
        }
      }`;

  const response = await fetch('http://127.0.0.1:5000/graphql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });

  const data = await response.json();
  const resultado = data.data.editarProducto?.producto || data.data.agregarProducto.producto;

  emit('producto-editado', resultado);
  emit('cerrar-modal');
};

const cerrar = () => {
  emit('cerrar-modal');
};
</script>

<style scoped>
/* Estilo del modal */
</style>
