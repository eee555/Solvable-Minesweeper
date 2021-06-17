import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
// import Tutorials from '@/views/Tutorials.vue'
// import Docs from '@/views/Docs.vue'
// import Development from '@/views/Development.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: '简介',
    props: true,
    component: () => import('../views/doc.vue')
  },
  {
    path: '/download',
    name: '下载及安装',
    props: true,
    component: () => import('../views/doc.vue')
  },
  {
    path: '/tutorial',
    name: '软件教程',
    props: true,
    component: () => import('../views/doc.vue')
  },
  {
    path: '/doc',
    name: '工具箱文档',
    props: true,
    component: () => import('../views/doc.vue')
  },
  {
    path: '/development',
    name: '开发和贡献',
    props: true,
    component: () => import('../views/doc.vue')
  },
  {
    path: '/links',
    name: '友链',
    props: true,
    component: () => import('../views/doc.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
