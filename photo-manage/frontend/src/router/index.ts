import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

// 页面组件
const Home = () => import('../views/Home.vue')
const Albums = () => import('../views/Albums.vue')
const AlbumDetail = () => import('../views/AlbumDetail.vue')
const Travel = () => import('../views/Travel.vue')
const Explore = () => import('../views/Explore.vue')
const PhotoDetail = () => import('../views/PhotoDetail.vue')

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: '首页 - 时光胶囊'
    }
  },
  {
    path: '/albums',
    name: 'Albums',
    component: Albums,
    meta: {
      title: '相册 - 时光胶囊'
    }
  },
  {
    path: '/albums/:id',
    name: 'AlbumDetail',
    component: AlbumDetail,
    meta: {
      title: '相册详情 - 时光胶囊'
    }
  },
  {
    path: '/travel',
    name: 'Travel',
    component: Travel,
    meta: {
      title: '旅行足迹 - 时光胶囊'
    }
  },
  {
    path: '/explore',
    name: 'Explore',
    component: Explore,
    meta: {
      title: '发现 - 时光胶囊'
    }
  },
  {
    path: '/photos/:id',
    name: 'PhotoDetail',
    component: PhotoDetail,
    meta: {
      title: '照片详情 - 时光胶囊'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 路由守卫 - 设置页面标题
router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title as string
  }
  next()
})

export default router

