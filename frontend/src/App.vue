<template>
  <div id="app">
    <nav class="navbar">
      <img src="./assets/logo.svg" alt="Logo" class="logo" />
      <div class="nav-links">
        <router-link to="/">Сервисы</router-link>
        <router-link to="/tasks">Задачи</router-link>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
}

.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between; 
  background-color: #35495e; /* темный цвет для навбара */
  padding: 10px 20px;
}

.logo {
  height: 50px; /* Настройте размер логотипа */
}

.nav-links {
  display: flex;
  gap: 20px; /* Промежуток между ссылками */
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.nav-links a:hover {
  text-decoration: underline; /* Эффект наведения */
}
</style>
