# 时光胶囊 - 前端项目

## 📖 项目介绍

时光胶囊前端项目基于 Vue 3 + TypeScript + Vite 构建，采用现代化的开发技术栈，提供美观、流畅的用户体验。

## 🛠️ 技术栈

- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全的JavaScript超集
- **Vite** - 现代前端构建工具
- **Pinia** - Vue的状态管理库
- **Vue Router** - 官方路由管理器
- **Element Plus** - Vue 3 UI组件库
- **Tailwind CSS** - 实用优先的CSS框架

## 🚀 快速开始

### 环境要求

- Node.js 16+
- npm 8+ 或 yarn

### 安装依赖

```bash
# 进入前端项目目录
cd frontend

# 安装依赖
npm install
# 或
yarn install
```

### 开发环境

```bash
# 启动开发服务器
npm run dev
# 或
yarn dev
```

访问 http://localhost:3000 查看应用

### 构建生产版本

```bash
# 构建生产版本
npm run build
# 或
yarn build

# 预览构建结果
npm run preview
# 或
yarn preview
```

### 代码检查

```bash
# 运行TypeScript类型检查
npm run type-check
# 或
yarn type-check

# 运行ESLint代码检查
npm run lint
# 或
yarn lint
```

## 📁 项目结构

```
frontend/
├── src/
│   ├── assets/          # 静态资源
│   │   └── styles/      # 样式文件
│   ├── components/      # 公共组件
│   │   ├── AlbumCard.vue       # 相册卡片
│   │   ├── PhotoCard.vue       # 照片卡片
│   │   ├── TravelCard.vue      # 旅行卡片
│   │   └── CreateAlbumModal.vue # 创建相册模态框
│   ├── views/           # 页面组件
│   │   ├── Home.vue     # 首页
│   │   ├── Albums.vue   # 相册页
│   │   └── Travel.vue   # 旅行页
│   ├── stores/          # Pinia状态管理
│   │   ├── user.ts      # 用户状态
│   │   ├── album.ts     # 相册状态
│   │   └── travel.ts    # 旅行状态
│   ├── services/        # 服务层
│   │   ├── api.ts       # API服务
│   │   └── mockData.ts  # 模拟数据
│   ├── types/           # TypeScript类型定义
│   │   └── index.ts     # 全局类型
│   ├── utils/           # 工具函数
│   │   └── format.ts    # 格式化工具
│   ├── router/          # 路由配置
│   │   └── index.ts     # 路由定义
│   ├── App.vue          # 根组件
│   └── main.ts          # 应用入口
├── public/              # 公共静态资源
├── index.html           # HTML模板
├── package.json         # 项目配置
├── vite.config.js       # Vite配置
└── README.md            # 项目文档
```

## 🎨 设计特色

### 苹果风格设计
- **简洁优雅** - 遵循苹果设计原则
- **直观易用** - 用户友好的界面设计
- **响应式布局** - 支持各种屏幕尺寸
- **流畅动画** - 现代化的交互动画

### 核心组件

#### 卡片组件
- **AlbumCard** - 相册展示卡片
- **PhotoCard** - 照片展示卡片
- **TravelCard** - 旅行地点卡片

#### 布局组件
- **响应式导航** - 适配移动端和桌面端
- **模态框组件** - 统一的弹窗交互
- **加载状态** - 优雅的加载动画

## 🔧 开发指南

### 代码规范

#### 组件命名
```typescript
// 组件文件使用大驼峰命名
// AlbumCard.vue, PhotoGallery.vue

// 组件内部使用小驼峰
const albumList = ref([])
const photoCount = computed(() => ...)
```

#### TypeScript 类型
```typescript
// 明确定义接口
interface PhotoCardProps {
  photo: Photo
  size?: 'small' | 'medium' | 'large'
}

// 使用类型断言
const photo = props.photo as Photo
```

### 状态管理

#### Pinia Store 使用
```typescript
// 在组件中使用
import { useUserStore } from '../stores/user'

const userStore = useUserStore()

// 响应式数据
const user = computed(() => userStore.currentUser)
const isAuthenticated = computed(() => userStore.isAuthenticated)

// 方法调用
const login = async () => {
  await userStore.login(credentials)
}
```

### API 调用

#### 使用封装的API服务
```typescript
import { photoApi } from '../services/api'

// 获取照片列表
const fetchPhotos = async (albumId: number) => {
  try {
    const response = await photoApi.getAlbumPhotos(albumId)
    return response.data
  } catch (error) {
    console.error('获取照片失败:', error)
  }
}
```

## 📱 功能特性

### 相册管理
- ✅ 创建、编辑、删除相册
- ✅ 相册分类和标签管理
- ✅ 批量操作支持
- ✅ 隐私设置

### 照片浏览
- ✅ 网格布局展示
- ✅ 照片详细信息查看
- ✅ 缩放和旋转操作
- ✅ 智能分类筛选

### 旅行足迹
- ✅ 地理位置记录
- ✅ 旅行统计分析
- ✅ 地图可视化
- ✅ 旅行回忆生成

### 响应式设计
- ✅ 移动端适配
- ✅ 触摸手势支持
- ✅ 自适应布局
- ✅ 离线功能支持

## 🔍 调试技巧

### 开发工具
- **Vue DevTools** - 调试Vue组件和状态
- **Chrome DevTools** - 网络请求和性能分析
- **Vite Dev Server** - 热重载和错误提示

### 调试命令
```bash
# 启用详细日志
VITE_ENABLE_DEBUG=true npm run dev

# 检查TypeScript类型
npm run type-check

# 代码检查
npm run lint
```

## 🚢 部署说明

### 生产构建
```bash
# 构建生产版本
npm run build

# 构建输出位于 dist/ 目录
# 将 dist/ 目录部署到Web服务器
```

### 环境配置
```bash
# 开发环境
cp env.development .env

# 生产环境
cp env.production .env
```

### Nginx 配置
```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8080;
    }
}
```

## 🤝 贡献指南

1. Fork 项目到你的仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 提交规范
- `feat:` 新功能
- `fix:` 修复bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](../LICENSE) 文件了解详情

## 📞 技术支持

- 📧 邮箱: support@timecapsule.com
- 🐦 Twitter: @time_capsule
- 💬 Discord: 时光胶囊社区

---

**时光胶囊前端** - 让每一张照片都成为永恒的记忆！




