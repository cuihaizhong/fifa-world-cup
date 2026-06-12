<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero-section bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div class="text-center">
          <h1 class="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            记录每一段
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600">
              美好时光
            </span>
          </h1>
          <p class="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            时光胶囊 - 智能相册管理工具，让每一张照片都成为永恒的记忆
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <button class="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-3 rounded-full text-lg font-semibold hover:shadow-lg transform hover:scale-105 transition-all duration-200">
              开始使用
            </button>
            <button class="border-2 border-gray-300 text-gray-700 px-8 py-3 rounded-full text-lg font-semibold hover:border-gray-400 transition-colors duration-200">
              了解更多
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div class="text-center">
            <div class="text-3xl font-bold text-gray-900">{{ stats.totalPhotos }}</div>
            <div class="text-gray-600 mt-2">张照片</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-gray-900">{{ stats.totalAlbums }}</div>
            <div class="text-gray-600 mt-2">个相册</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-gray-900">{{ stats.totalLocations }}</div>
            <div class="text-gray-600 mt-2">个旅行点</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-gray-900">{{ stats.daysActive }}</div>
            <div class="text-gray-600 mt-2">天活跃</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Recent Albums Section -->
    <section class="recent-albums-section py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center mb-8">
          <h2 class="text-3xl font-bold text-gray-900">最近相册</h2>
          <router-link to="/albums" class="text-blue-600 hover:text-blue-700 font-semibold">
            查看全部 →
          </router-link>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <AlbumCard
            v-for="album in recentAlbums"
            :key="album.id"
            :album="album"
            size="medium"
            class="slide-up-enter-active"
          />
        </div>
      </div>
    </section>

    <!-- Travel Map Section -->
    <section class="travel-map-section py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center mb-8">
          <h2 class="text-3xl font-bold text-gray-900">旅行足迹</h2>
          <router-link to="/travel" class="text-blue-600 hover:text-blue-700 font-semibold">
            查看足迹 →
          </router-link>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <TravelCard
            v-for="location in recentTravelLocations"
            :key="location.id"
            :location="location"
            size="medium"
            class="slide-up-enter-active"
          />
        </div>
      </div>
    </section>

    <!-- Recent Photos Section -->
    <section class="recent-photos-section py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center mb-8">
          <h2 class="text-3xl font-bold text-gray-900">最新照片</h2>
          <button class="text-blue-600 hover:text-blue-700 font-semibold">
            查看全部 →
          </button>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
          <PhotoCard
            v-for="photo in recentPhotos"
            :key="photo.id"
            :photo="photo"
            size="small"
            class="slide-up-enter-active"
          />
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">为什么选择时光胶囊？</h2>
          <p class="text-gray-600 max-w-2xl mx-auto">
            我们提供最先进的照片管理体验，让每一次回忆都触手可及
          </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center p-6 rounded-2xl hover:shadow-lg transition-shadow duration-200">
            <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">智能分类</h3>
            <p class="text-gray-600">AI 驱动的照片自动分类，按时间、地点、人脸智能整理</p>
          </div>
          <div class="text-center p-6 rounded-2xl hover:shadow-lg transition-shadow duration-200">
            <div class="w-16 h-16 bg-gradient-to-br from-green-500 to-teal-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">旅行足迹</h3>
            <p class="text-gray-600">记录每一次旅行，按地理位置自动分类和统计</p>
          </div>
          <div class="text-center p-6 rounded-2xl hover:shadow-lg transition-shadow duration-200">
            <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">情侣空间</h3>
            <p class="text-gray-600">专属的情侣互动空间，分享甜蜜时光和回忆</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section py-16 bg-gradient-to-r from-blue-500 to-purple-600">
      <div class="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-white mb-4">开始记录你的美好时光</h2>
        <p class="text-xl text-blue-100 mb-8">加入数百万用户，选择时光胶囊管理你的珍贵回忆</p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button class="bg-white text-blue-600 px-8 py-3 rounded-full text-lg font-semibold hover:bg-gray-100 transition-colors duration-200">
            立即开始
          </button>
          <button class="border-2 border-white text-white px-8 py-3 rounded-full text-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors duration-200">
            了解更多
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { MockApiService } from '../services/mockData'
import type { Album, Photo, TravelLocation } from '../types'
import AlbumCard from '../components/AlbumCard.vue'
import PhotoCard from '../components/PhotoCard.vue'
import TravelCard from '../components/TravelCard.vue'

// 响应式数据
const stats = ref({
  totalPhotos: 0,
  totalAlbums: 0,
  totalLocations: 0,
  daysActive: 0
})

const recentAlbums = ref<Album[]>([])
const recentPhotos = ref<Photo[]>([])
const recentTravelLocations = ref<TravelLocation[]>([])

// 加载数据
const loadData = async () => {
  try {
    // 加载相册数据
    const [albums, photos, locations] = await Promise.all([
      MockApiService.getAlbums(),
      MockApiService.getAlbumPhotos(1), // 获取第一个相册的照片
      MockApiService.getTravelLocations()
    ])

    recentAlbums.value = albums.slice(0, 3)
    recentPhotos.value = photos.slice(0, 12)
    recentTravelLocations.value = locations.slice(0, 3)

    // 计算统计数据
    stats.value = {
      totalPhotos: photos.length,
      totalAlbums: albums.length,
      totalLocations: locations.length,
      daysActive: Math.floor(Math.random() * 365) + 30 // 模拟数据
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

// 生命周期
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.hero-section {
  min-height: 80vh;
  display: flex;
  align-items: center;
}

.stats-section {
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
}

.recent-albums-section,
.travel-map-section,
.recent-photos-section {
  scroll-margin-top: 80px;
}

.features-section .slide-up-enter-active {
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

