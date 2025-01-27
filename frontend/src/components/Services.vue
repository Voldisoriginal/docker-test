<template>
  <div class="services-container">
    <h2 class="services-heading">Список сервисов</h2>
    <ul class="services-list">
      <li v-for="service in services" :key="service.id">
        <a 
          class="service-link" 
          href="#" 
          @click.prevent="fetchContainerDetails(service.id)">
          {{ service.name }}
        </a>
      </li>
    </ul>
    
    <div v-if="containerDetails" class="container-details">
      <h3 class="container-title">Форма для контейнера: {{ containerDetails.name }}</h3>
      <form @submit.prevent="submitContainerData" class="form-container">
        <div class="form-fields">
          <div v-for="(value, key) in containerFields" :key="key" class="form-field">
            <label :for="key">{{ key }}</label>
            <input 
              :id="key" 
              v-model="formData[key]" 
              required 
              class="input-field" 
            />
          </div>
        </div>
        <button type="submit" class="submit-button">Отправить данные</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      services: [],
      containerDetails: null,
      containerId: null,
      formData: {},
      containerFields: {},
    };
  },
  created() {
    this.fetchServices();
  },
  methods: {
    async fetchServices() {
      const response = await axios.get('http://127.0.0.1:8000/services');
      this.services = response.data.map(service => ({
        id: service.id,
        name: service.name,
      }));
    },
    async fetchContainerDetails(containerId) {
      const response = await axios.get(`http://127.0.0.1:8000/getapi/${containerId}`);
      this.containerFields = response.data; 
      this.containerId=containerId
      this.containerDetails = response.data; 
      this.formData = {};

      // Инициализируем поля для формы
      for (const key in this.containerFields) {
        this.formData[key] = ''; 
      }
    },
    async submitContainerData() {
      // Добавляем имя контейнера в formData перед отправкой
      this.formData.containerName = this.containerId;

      const response = await axios.post('http://127.0.0.1:8000/submit_task', this.formData);
      alert(response.data.message); 
    },
  }
};
</script>

<style>
.services-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.services-heading {
  font-size: 24px;
  font-weight: bold;
  color: #42b983;
  text-align: center;
  margin-bottom: 20px;
}

.services-list {
  list-style: none;
  padding: 0;
}

.service-link {
  display: block;
  padding: 10px 15px;
  background-color: #35495e; /* Цвет фона */
  color: white;
  text-decoration: none;
  border-radius: 5px; /* Уголки */
  margin: 5px 0; /* Отступы между элементами */
  transition: background-color 0.3s;
}

.service-link:hover {
  background-color: #42b983; /* Цвет на наведение */
}

.container-details {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9; /* Цвет фона формы */
}

.container-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
}

.form-container {
  display: flex;
  flex-direction: column;
}

.form-fields {
  margin-bottom: 15px;
}

.form-field {
  margin-bottom: 10px; /* Отступ между полями */
}

.input-field {
  width: 100%; /* Полная ширина */
  padding: 8px;
  border: 1px solid #ccc; /* Граница полей */
  border-radius: 4px; /* Углы */
  font-size: 14px;
}

.submit-button {

  padding: 10px;
  background-color: #42b983; /* Цвет кнопки */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #35495e; /* Цвет кнопки на наведение */
}
</style>
