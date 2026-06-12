// 类型定义

export interface User {
  id: number
  email: string
  nickname: string
  avatar?: string
  bio?: string
  createdAt: string
}

export interface Album {
  id: number
  userId: number
  name: string
  description?: string
  coverImage?: string
  isPrivate: boolean
  albumType: 'normal' | 'couple' | 'collaborative' | 'smart' | 'template'
  templateId?: number
  photoCount: number
  totalSize: number
  location?: string
  tags?: string[]
  createdAt: string
  updatedAt: string
}

export interface Photo {
  id: number
  albumId: number
  originalName: string
  storagePath: string
  thumbnailPath?: string
  previewPath?: string
  fileSize: number
  width: number
  height: number
  format: string
  mimeType: string
  metadata?: PhotoMetadata
  uploadedAt: string
  takenAt?: string
  location?: string
  latitude?: number
  longitude?: number
  province?: string
  city?: string
  district?: string
  description?: string
  isFavorite: boolean
  rating?: number
  aiTags?: string[]
  faceData?: any
  sceneType?: 'nature' | 'urban' | 'portrait' | 'food' | 'architecture' | 'event' | 'other'
  emotionType?: 'happy' | 'sad' | 'peaceful' | 'excited' | 'serene' | 'awe' | 'proud' | 'delicious' | 'other'
  qualityScore?: number
}

export interface PhotoMetadata {
  camera?: string
  lens?: string
  iso?: number
  aperture?: number
  exposureTime?: string
  focalLength?: number
  [key: string]: any
}

export interface TravelLocation {
  id: number
  userId: number
  province: string
  city: string
  district?: string
  locationName?: string
  description?: string
  latitude?: number
  longitude?: number
  visitCount: number
  firstVisitAt?: string
  lastVisitAt?: string
  coverImage?: string
  isFavorite: boolean
  createdAt: string
  updatedAt?: string
}

export interface Comment {
  id: number
  userId: number
  photoId: number
  content: string
  likeCount: number
  createdAt: string
  updatedAt: string
  user: User
}

export interface TravelStatistics {
  province: string
  city: string
  year: number
  month?: number
  visitCount: number
  photoCount: number
  totalSize: number
}

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
  timestamp: string
}

export interface PaginationParams {
  page?: number
  pageSize?: number
  sortBy?: string
  order?: 'asc' | 'desc'
}

export interface AlbumListResponse {
  list: Album[]
  pagination: {
    page: number
    pageSize: number
    total: number
  }
}

export interface PhotoListResponse {
  list: Photo[]
  pagination: {
    page: number
    pageSize: number
    total: number
  }
}

export interface CommentListResponse {
  list: Comment[]
  pagination: {
    page: number
    pageSize: number
    total: number
  }
}

// 组件 Props 类型
export interface PhotoCardProps {
  photo: Photo
  size?: 'small' | 'medium' | 'large'
  showOverlay?: boolean
  lazy?: boolean
}

export interface AlbumCardProps {
  album: Album
  size?: 'small' | 'medium' | 'large'
  showStats?: boolean
}

export interface TravelCardProps {
  location: TravelLocation
  size?: 'small' | 'medium' | 'large'
  showStats?: boolean
}

// 表单类型
export interface CreateAlbumForm {
  name: string
  description?: string
  isPrivate: boolean
  albumType: Album['albumType']
  tags?: string[]
}

export interface UpdatePhotoForm {
  description?: string
  takenAt?: string
  location?: string
  province?: string
  city?: string
  district?: string
  rating?: number
}

export interface CommentForm {
  content: string
  parentId?: number
}

// 状态管理类型
export interface UserState {
  currentUser: User | null
  isAuthenticated: boolean
  preferences: UserPreferences
}

export interface AlbumState {
  albums: Album[]
  currentAlbum: Album | null
  loading: boolean
  error: string | null
}

export interface PhotoState {
  photos: Photo[]
  currentPhoto: Photo | null
  loading: boolean
  error: string | null
}

export interface TravelState {
  locations: TravelLocation[]
  currentLocation: TravelLocation | null
  statistics: TravelStatistics[]
  loading: boolean
  error: string | null
}

export interface UserPreferences {
  theme: 'light' | 'dark' | 'auto'
  language: string
  autoBackup: boolean
  syncThumbnails: boolean
  autoSync: boolean
  notificationEmail: boolean
  notificationPush: boolean
  privacyLevel: 'public' | 'friends' | 'private'
}

// 工具类型
export type LoadingState = 'idle' | 'loading' | 'success' | 'error'

export interface AsyncState<T> {
  data: T | null
  loading: boolean
  error: string | null
}

// 事件类型
export interface PhotoEvents {
  click: [photo: Photo]
  delete: [photoId: number]
  edit: [photo: Photo]
  like: [photoId: number]
}

export interface AlbumEvents {
  click: [album: Album]
  delete: [albumId: number]
  edit: [album: Album]
  share: [album: Album]
}

