import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { TravelLocation, TravelStatistics, Photo } from '../types'
import { MockApiService } from '../services/mockData'

// 旅行状态管理
export const useTravelStore = defineStore('travel', () => {
  // 状态
  const locations = ref<TravelLocation[]>([])
  const currentLocation = ref<TravelLocation | null>(null)
  const currentLocationPhotos = ref<Photo[]>([])
  const statistics = ref<TravelStatistics[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // 计算属性
  const locationCount = computed(() => locations.value.length)
  const totalVisits = computed(() =>
    locations.value.reduce((sum, location) => sum + location.visitCount, 0)
  )

  const favoriteLocations = computed(() =>
    locations.value.filter(location => location.isFavorite)
  )

  const recentLocations = computed(() =>
    [...locations.value]
      .sort((a, b) => {
        const dateA = new Date(a.lastVisitAt || a.createdAt).getTime()
        const dateB = new Date(b.lastVisitAt || b.createdAt).getTime()
        return dateB - dateA
      })
      .slice(0, 5)
  )

  const locationsByProvince = computed(() => {
    const grouped: Record<string, TravelLocation[]> = {}
    locations.value.forEach(location => {
      if (!grouped[location.province]) {
        grouped[location.province] = []
      }
      grouped[location.province].push(location)
    })
    return grouped
  })

  const popularLocations = computed(() =>
    [...locations.value]
      .sort((a, b) => b.visitCount - a.visitCount)
      .slice(0, 10)
  )

  // 动作
  const fetchLocations = async () => {
    try {
      isLoading.value = true
      error.value = null

      const data = await MockApiService.getTravelLocations()
      locations.value = data
    } catch (err) {
      error.value = err instanceof Error ? err.message : '获取旅行地点失败'
      console.error('Fetch locations error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const fetchLocationById = async (id: number) => {
    try {
      isLoading.value = true
      error.value = null

      const location = await MockApiService.getTravelLocation(id)
      currentLocation.value = location

      // 获取地点照片
      if (location) {
        const photos = await MockApiService.getTravelLocationPhotos(id)
        currentLocationPhotos.value = photos
      }

      return location
    } catch (err) {
      error.value = err instanceof Error ? err.message : '获取旅行地点详情失败'
      console.error('Fetch location error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const createLocation = async (locationData: Omit<TravelLocation, 'id' | 'createdAt' | 'visitCount'>) => {
    try {
      isLoading.value = true
      error.value = null

      // 模拟创建旅行地点
      const newLocation: TravelLocation = {
        ...locationData,
        id: Date.now(), // 临时ID
        visitCount: 0,
        createdAt: new Date().toISOString()
      }

      locations.value.unshift(newLocation)
      return newLocation
    } catch (err) {
      error.value = err instanceof Error ? err.message : '创建旅行地点失败'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const updateLocation = async (id: number, updates: Partial<TravelLocation>) => {
    try {
      isLoading.value = true
      error.value = null

      const locationIndex = locations.value.findIndex(location => location.id === id)
      if (locationIndex === -1) {
        throw new Error('旅行地点不存在')
      }

      const updatedLocation = {
        ...locations.value[locationIndex],
        ...updates
      }

      locations.value[locationIndex] = updatedLocation

      if (currentLocation.value?.id === id) {
        currentLocation.value = updatedLocation
      }

      return updatedLocation
    } catch (err) {
      error.value = err instanceof Error ? err.message : '更新旅行地点失败'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const deleteLocation = async (id: number) => {
    try {
      isLoading.value = true
      error.value = null

      // 模拟删除操作
      await new Promise(resolve => setTimeout(resolve, 500))

      const locationIndex = locations.value.findIndex(location => location.id === id)
      if (locationIndex === -1) {
        throw new Error('旅行地点不存在')
      }

      locations.value.splice(locationIndex, 1)

      if (currentLocation.value?.id === id) {
        currentLocation.value = null
        currentLocationPhotos.value = []
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : '删除旅行地点失败'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const fetchStatistics = async () => {
    try {
      isLoading.value = true
      error.value = null

      const data = await MockApiService.getTravelStatistics()
      statistics.value = data
    } catch (err) {
      error.value = err instanceof Error ? err.message : '获取旅行统计失败'
      console.error('Fetch statistics error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const setCurrentLocation = (location: TravelLocation | null) => {
    currentLocation.value = location
    if (!location) {
      currentLocationPhotos.value = []
    }
  }

  const toggleFavorite = async (id: number) => {
    try {
      const location = locations.value.find(loc => loc.id === id)
      if (location) {
        location.isFavorite = !location.isFavorite
        // 这里可以调用API更新
        return location.isFavorite
      }
      return false
    } catch (err) {
      console.error('Toggle favorite error:', err)
      return false
    }
  }

  const searchLocations = (query: string) => {
    if (!query.trim()) {
      return locations.value
    }

    const lowerQuery = query.toLowerCase()
    return locations.value.filter(location =>
      location.locationName?.toLowerCase().includes(lowerQuery) ||
      location.province.toLowerCase().includes(lowerQuery) ||
      location.city.toLowerCase().includes(lowerQuery) ||
      location.description?.toLowerCase().includes(lowerQuery)
    )
  }

  const filterLocations = (filter: string) => {
    switch (filter) {
      case 'favorites':
        return favoriteLocations.value
      case 'recent':
        return recentLocations.value
      case 'popular':
        return popularLocations.value
      default:
        return locations.value
    }
  }

  const getLocationsByProvince = (province: string) => {
    return locations.value.filter(location => location.province === province)
  }

  const getLocationStats = (location: TravelLocation) => {
    const photos = currentLocationPhotos.value.filter(photo =>
      photo.province === location.province &&
      photo.city === location.city
    )

    return {
      photoCount: photos.length,
      totalSize: photos.reduce((sum, photo) => sum + photo.fileSize, 0),
      scenes: [...new Set(photos.map(p => p.sceneType).filter(Boolean))],
      dateRange: photos.length > 0 ? {
        start: photos.reduce((earliest, photo) =>
          new Date(photo.takenAt || photo.uploadedAt) < new Date(earliest) ? photo.takenAt || photo.uploadedAt : earliest,
          photos[0]?.takenAt || photos[0]?.uploadedAt || new Date().toISOString()
        ),
        end: photos.reduce((latest, photo) =>
          new Date(photo.takenAt || photo.uploadedAt) > new Date(latest) ? photo.takenAt || photo.uploadedAt : latest,
          photos[0]?.takenAt || photos[0]?.uploadedAt || new Date().toISOString()
        )
      } : null
    }
  }

  return {
    // 状态
    locations,
    currentLocation,
    currentLocationPhotos,
    statistics,
    isLoading,
    error,

    // 计算属性
    locationCount,
    totalVisits,
    favoriteLocations,
    recentLocations,
    locationsByProvince,
    popularLocations,

    // 动作
    fetchLocations,
    fetchLocationById,
    createLocation,
    updateLocation,
    deleteLocation,
    fetchStatistics,
    setCurrentLocation,
    toggleFavorite,
    searchLocations,
    filterLocations,
    getLocationsByProvince,
    getLocationStats
  }
})




