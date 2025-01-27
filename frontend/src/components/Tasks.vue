<template>
  <div class="tasks-container">
    <h2 class="tasks-heading">Список задач</h2>
    <div class="task-container">
      <div 
        v-for="task in tasks" 
        :key="task.Id" 
        class="task-card" 
        :style="{ backgroundColor: task.Color }"
      >
        <div class="task-number">{{ tasks.indexOf(task) + 1 }}</div>
        <div class="task-title">{{ task.Name }}</div>
        <div class="task-description">{{ task.Description }}</div>
        <div class="task-info">(Сервис: {{ task.ServiceName }}, ID: {{ task.Id }})</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tasks: [],
    };
  },
  created() {
    this.fetchTasks();
  },
  methods: {
    async fetchTasks() {
      const response = await axios.get('http://127.0.0.1:8000/tasks');
      this.tasks = response.data;
    },
  },
};
</script>

<style>
.tasks-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.tasks-heading {
  font-size: 24px;
  font-weight: bold;
  color: #42b983; /* Цвет заголовка */
  text-align: center;
  margin-bottom: 20px;
}

.task-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); /* Гибкая сетка для карточек */
  gap: 15px; /* Отступ между карточками */
}

.task-card {
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Тень для карточек */
  color: #fff; /* Цвет текста в карточке */
  transition: transform 0.2s; /* Эффект при наведении */
}

.task-card:hover {
  transform: scale(1.03); /* Увеличение карточки при наведении */
}

.task-number {
  font-size: 18px;
  font-weight: bold;
}

.task-title {
  font-size: 20px;
  margin: 10px 0;
}

.task-description {
  font-size: 16px;
  margin: 10px 0;
}

.task-info {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8); /* Более светлый цвет для информации */
}
</style>
