<template>
  <el-container>
    <el-header> {{ this.$route.name }} </el-header>
    <el-main>
      <VueMarkdownIt :source="source" />
    </el-main>
  </el-container>
</template>

<script>
import VueMarkdownIt from "vue3-markdown-it";
// import {ref} from 'vue'

// const count = ref('')

export default {
  components: {
    VueMarkdownIt,
  },
  props: {
    title: {
      type: String,
      default: "默认标题",
    },
    url: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      source: "正在载入",
    };
  },
  methods: {
    fetchDate() {
      // 使用 axios获取数据
      this.axios.get(this.$route.name + ".md").then((response) => {
        this.source = response.data;
      });
    },
  },
  created() {
    // console.log(this.$route.name)
    this.fetchDate();
  },
  watch: {
    // 如果路由有变化，会再次执行该方法

    $route: "fetchDate",
  },
};
</script>

<style>
.el-header {
  text-align: left;
  font-size: 30px;
  display: block;
  position: relative;
  background-color: rgb(233, 233, 233);
}

.el-main {
  position: absolute;
  left: 210px;
  right: 10px;
  top: 70px;
  bottom: 5px;
  border: 1px solid #eee;
}
</style>
