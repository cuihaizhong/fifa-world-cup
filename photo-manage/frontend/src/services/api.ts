// API 服务层
import axios from 'axios'
import type {
  Album,
  Photo,
  TravelLocation,
  TravelStatistics,
  User,
  Comment,
  ApiResponse
} from '../types'

// 创建 axios 实例
const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    if (error.response?.status === 401) {
      // token 过期，清除本地存储并跳转到登录页
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// 用户相关 API
export const userApi = {
  // 用户注册
  register: (data: { email: string; password: string; nickname: string }): Promise<ApiResponse<User>> => {
    return api.post('/auth/register', data)
  },

  // 用户登录
  login: (data: { email: string; password: string }): Promise<ApiResponse<{ user: User; token: string }>> => {
    return api.post('/auth/login', data)
  },

  // 刷新token
  refreshToken: (): Promise<ApiResponse<{ token: string }>> => {
    return api.post('/auth/refresh')
  },

  // 获取用户信息
  getUser: (userId: number): Promise<ApiResponse<User>> => {
    return api.get(`/users/${userId}`)
  },

  // 更新用户信息
  updateUser: (userId: number, data: Partial<User>): Promise<ApiResponse<User>> => {
    return api.put(`/users/${userId}`, data)
  },

  // 获取用户偏好
  getUserPreferences: (userId: number): Promise<ApiResponse<any>> => {
    return api.get(`/users/${userId}/preferences`)
  },

  // 更新用户偏好
  updateUserPreferences: (userId: number, data: any): Promise<ApiResponse<any>> => {
    return api.put(`/users/${userId}/preferences`, data)
  }
}

// 相册相关 API
export const albumApi = {
  // 获取相册列表
  getAlbums: (params?: { page?: number; pageSize?: number; albumType?: string }): Promise<ApiResponse<Album[]>> => {
    return api.get('/albums', { params })
  },

  // 获取单个相册
  getAlbum: (albumId: number): Promise<ApiResponse<Album>> => {
    return api.get(`/albums/${albumId}`)
  },

  // 创建相册
  createAlbum: (data: Omit<Album, 'id' | 'createdAt' | 'updatedAt' | 'photoCount' | 'totalSize'>): Promise<ApiResponse<Album>> => {
    return api.post('/albums', data)
  },

  // 更新相册
  updateAlbum: (albumId: number, data: Partial<Album>): Promise<ApiResponse<Album>> => {
    return api.put(`/albums/${albumId}`, data)
  },

  // 删除相册
  deleteAlbum: (albumId: number): Promise<ApiResponse<void>> => {
    return api.delete(`/albums/${albumId}`)
  },

  // 批量操作相册
  batchOperation: (data: { operation: string; albumIds: number[]; params?: any }): Promise<ApiResponse<void>> => {
    return api.post('/albums/batch', data)
  }
}

// 照片相关 API
export const photoApi = {
  // 获取相册照片
  getAlbumPhotos: (albumId: number, params?: { page?: number; pageSize?: number; sortBy?: string; order?: string }): Promise<ApiResponse<Photo[]>> => {
    return api.get(`/albums/${albumId}/photos`, { params })
  },

  // 获取照片详情
  getPhoto: (photoId: number): Promise<ApiResponse<Photo>> => {
    return api.get(`/photos/${photoId}`)
  },

  // 上传照片
  uploadPhotos: (albumId: number, formData: FormData): Promise<ApiResponse<Photo[]>> => {
    return api.post(`/albums/${albumId}/photos`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 更新照片信息
  updatePhoto: (photoId: number, data: Partial<Photo>): Promise<ApiResponse<Photo>> => {
    return api.put(`/photos/${photoId}`, data)
  },

  // 删除照片
  deletePhoto: (photoId: number): Promise<ApiResponse<void>> => {
    return api.delete(`/photos/${photoId}`)
  },

  // 批量操作照片
  batchOperation: (data: { operation: string; photoIds: number[]; params?: any }): Promise<ApiResponse<void>> => {
    return api.post('/photos/batch', data)
  },

  // 搜索照片
  searchPhotos: (params: { keyword: string; tags?: string[]; sceneType?: string; emotionType?: string; takenAfter?: string; takenBefore?: string }): Promise<ApiResponse<Photo[]>> => {
    return api.get('/photos/search', { params })
  },

  // 获取照片评论
  getPhotoComments: (photoId: number, params?: { page?: number; pageSize?: number }): Promise<ApiResponse<Comment[]>> => {
    return api.get(`/photos/${photoId}/comments`, { params })
  },

  // 添加评论
  addComment: (photoId: number, content: string): Promise<ApiResponse<Comment>> => {
    return api.post(`/photos/${photoId}/comments`, { content })
  },

  // 点赞照片
  likePhoto: (photoId: number): Promise<ApiResponse<void>> => {
    return api.post(`/photos/${photoId}/like`)
  },

  // 取消点赞
  unlikePhoto: (photoId: number): Promise<ApiResponse<void>> => {
    return api.delete(`/photos/${photoId}/like`)
  }
}

// 旅行地点相关 API
export const travelApi = {
  // 获取旅行地点列表
  getLocations: (params?: { page?: number; pageSize?: number; province?: string; city?: string; isFavorite?: boolean }): Promise<ApiResponse<TravelLocation[]>> => {
    return api.get('/travel/locations', { params })
  },

  // 获取旅行地点详情
  getLocation: (locationId: number): Promise<ApiResponse<TravelLocation>> => {
    return api.get(`/travel/locations/${locationId}`)
  },

  // 创建旅行地点
  createLocation: (data: Omit<TravelLocation, 'id' | 'createdAt'>): Promise<ApiResponse<TravelLocation>> => {
    return api.post('/travel/locations', data)
  },

  // 更新旅行地点
  updateLocation: (locationId: number, data: Partial<TravelLocation>): Promise<ApiResponse<TravelLocation>> => {
    return api.put(`/travel/locations/${locationId}`, data)
  },

  // 删除旅行地点
  deleteLocation: (locationId: number): Promise<ApiResponse<void>> => {
    return api.delete(`/travel/locations/${locationId}`)
  },

  // 获取旅行地点照片
  getLocationPhotos: (locationId: number): Promise<ApiResponse<Photo[]>> => {
    return api.get(`/travel/locations/${locationId}/photos`)
  },

  // 按旅行点分类照片
  classifyPhotosByLocation: (data: { photoIds: number[]; autoDetect?: boolean }): Promise<ApiResponse<void>> => {
    return api.post('/travel/classify-photos', data)
  },

  // 获取旅行统计
  getTravelStatistics: (params?: { year?: number; month?: number; province?: string; city?: string }): Promise<ApiResponse<TravelStatistics[]>> => {
    return api.get('/travel/statistics', { params })
  }
}

// 分享相关 API
export const shareApi = {
  // 创建分享
  createShare: (data: { resourceType: string; resourceId: number; shareType: string; expiresAt?: string; password?: string; permissions?: string[] }): Promise<ApiResponse<any>> => {
    return api.post('/share', data)
  },

  // 通过分享码访问
  accessShare: (shareCode: string, params?: { password?: string }): Promise<ApiResponse<any>> => {
    return api.get(`/share/${shareCode}`, { params })
  },

  // 获取分享统计
  getShareStatistics: (shareCode: string): Promise<ApiResponse<any>> => {
    return api.get(`/share/${shareCode}/statistics`)
  }
}

// 系统相关 API
export const systemApi = {
  // 获取数据统计
  getStatistics: (type: string): Promise<ApiResponse<any>> => {
    return api.get(`/statistics/${type}`)
  },

  // 获取通知列表
  getNotifications: (params?: { page?: number; pageSize?: number }): Promise<ApiResponse<any[]>> => {
    return api.get('/notifications', { params })
  },

  // 标记通知已读
  markNotificationAsRead: (notificationId: number): Promise<ApiResponse<void>> => {
    return api.put(`/notifications/${notificationId}/read`)
  },

  // 批量标记已读
  batchMarkAsRead: (notificationIds: number[]): Promise<ApiResponse<void>> => {
    return api.put('/notifications/batch-read', { notificationIds })
  },

  // 删除通知
  deleteNotification: (notificationId: number): Promise<ApiResponse<void>> => {
    return api.delete(`/notifications/${notificationId}`)
  },

  // 获取操作日志
  getOperationLogs: (params?: { page?: number; pageSize?: number; operationType?: string; startDate?: string; endDate?: string }): Promise<ApiResponse<any[]>> => {
    return api.get('/logs/operations', { params })
  }
}

// 数据导入导出 API
export const importExportApi = {
  // 导出数据
  exportData: (data: { exportType: string; format: string; albumIds?: number[]; includeThumbnails?: boolean }): Promise<ApiResponse<{ taskId: string }>> => {
    return api.post('/export', data)
  },

  // 获取导出进度
  getExportProgress: (taskId: string): Promise<ApiResponse<any>> => {
    return api.get(`/export/${taskId}/progress`)
  },

  // 下载导出文件
  downloadExportFile: (taskId: string): Promise<Blob> => {
    return api.get(`/export/${taskId}/download`, { responseType: 'blob' })
  },

  // 导入数据
  importData: (formData: FormData): Promise<ApiResponse<{ taskId: string }>> => {
    return api.post('/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 获取导入进度
  getImportProgress: (taskId: string): Promise<ApiResponse<any>> => {
    return api.get(`/import/${taskId}/progress`)
  }
}

export default api




