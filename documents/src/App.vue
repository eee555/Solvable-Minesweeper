<template>
  <el-container style="height: 100%">
    <el-aside width="200px">
      <el-menu
        default-active="6"
        text-color="#000"
        background-color="#fff"
        active-text-color="#000"
        ><router-link to="/" replace>
          <el-menu-item index="1" style="font-size: 20px">
            <template #title><i class="el-icon-menu"></i>简介</template>
          </el-menu-item></router-link
        ><router-link to="/download" replace>
          <el-menu-item index="2" style="font-size: 20px">
            <template #title><i class="el-icon-menu"></i>下载及安装</template>
          </el-menu-item></router-link
        ><router-link to="/tutorial" replace>
          <el-menu-item index="3" style="font-size: 20px">
            <template #title><i class="el-icon-menu"></i>软件教程</template>
          </el-menu-item></router-link
        ><router-link to="/doc" replace>
          <el-menu-item index="4" style="font-size: 20px">
            <template #title><i class="el-icon-menu"></i>工具箱文档</template>
          </el-menu-item></router-link
        ><router-link to="/development" replace>
          <el-menu-item index="5" style="font-size: 20px">
            <template #title><i class="el-icon-menu"></i>开发和贡献</template>
          </el-menu-item></router-link
        ><router-link to="/links" replace>
          <el-menu-item index="6" style="font-size: 20px">
            <template #title><i class="el-icon-menu"></i>友链</template>
          </el-menu-item></router-link
        >
      </el-menu>
    </el-aside>
    <router-view></router-view>
  </el-container>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

.el-aside {
  display: block;
  position: relative;
  background-color: rgb(255, 255, 255);
}

.router-link-active {
  text-decoration: none;
}

a {
  text-decoration: none;
}
</style>




