# 🛠️ 时光胶囊 - 开发指南

## 1. 开发环境设置

### 1.1 系统要求
- **操作系统**: macOS 10.15+, Windows 10+, Ubuntu 18.04+
- **Node.js**: 16.0.0+
- **Java**: 17+
- **MySQL**: 8.0+
- **Redis**: 6.0+
- **Git**: 2.0+

### 1.2 环境变量配置

```bash
# 复制环境变量模板
cp env.example .env

# 编辑配置文件
vim .env
```

关键配置项：
```bash
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_NAME=time_capsule
DB_USERNAME=timecapsule
DB_PASSWORD=timecapsule2024

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT 配置
JWT_SECRET=your_jwt_secret_key
JWT_EXPIRATION=3600000

# 文件存储
UPLOAD_PATH=./uploads
STORAGE_PATH=./storage
```

### 1.3 依赖安装

#### 前端依赖
```bash
cd frontend
npm install
```

#### 后端依赖
```bash
cd backend
# 如果使用 Maven
./mvnw clean install

# 如果使用 Gradle
./gradlew build
```

### 1.4 服务启动

#### 方式一：Docker 启动（推荐）
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 方式二：手动启动

```bash
# 1. 启动 MySQL
sudo systemctl start mysql

# 2. 启动 Redis
sudo systemctl start redis

# 3. 创建数据库
mysql -u root -p < scripts/init.sql

# 4. 启动后端服务
cd backend
./mvnw spring-boot:run

# 5. 启动前端服务
cd frontend
npm run dev
```

### 1.5 开发工具推荐

#### IDE 配置
- **前端**: VS Code + Vue.js Extension Pack
- **后端**: IntelliJ IDEA + Spring Boot Extension
- **数据库**: DataGrip 或 MySQL Workbench

#### VS Code 推荐插件
```json
{
  "recommendations": [
    "vue.volar",
    "vue.vscode-typescript-vue-plugin",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-vscode.vscode-json",
    "bradlc.vscode-tailwindcss",
    "formulahendry.auto-rename-tag",
    "christian-kohler.path-intellisense"
  ]
}
```

## 2. 项目结构说明

### 2.1 前端项目结构

```
frontend/
├── src/
│   ├── components/       # 公共组件
│   │   ├── common/       # 通用组件
│   │   ├── photo/        # 照片相关组件
│   │   ├── album/        # 相册相关组件
│   │   └── user/         # 用户相关组件
│   ├── views/           # 页面视图
│   │   ├── Home.vue      # 首页
│   │   ├── Album/        # 相册页面
│   │   ├── Photo/        # 照片页面
│   │   └── User/         # 用户页面
│   ├── stores/          # Pinia 状态管理
│   │   ├── user.js       # 用户状态
│   │   ├── album.js      # 相册状态
│   │   └── photo.js      # 照片状态
│   ├── utils/           # 工具函数
│   │   ├── api.js       # API 请求封装
│   │   ├── auth.js      # 认证相关
│   │   └── file.js      # 文件处理
│   ├── types/           # TypeScript 类型定义
│   │   ├── index.ts     # 全局类型
│   │   └── api.ts       # API 类型
│   └── assets/          # 静态资源
│       ├── styles/      # 样式文件
│       └── images/      # 图片资源
├── public/              # 公共静态资源
├── tauri/               # Tauri 桌面应用配置
└── package.json         # 项目配置
```

### 2.2 后端项目结构

```
backend/
├── src/main/java/com/timecapsule/
│   ├── controller/      # REST 控制器
│   │   ├── AuthController.java      # 认证控制器
│   │   ├── UserController.java      # 用户控制器
│   │   ├── AlbumController.java     # 相册控制器
│   │   └── PhotoController.java     # 照片控制器
│   ├── service/         # 业务逻辑层
│   │   ├── impl/        # 实现类
│   │   ├── AuthService.java         # 认证服务
│   │   ├── UserService.java         # 用户服务
│   │   └── AlbumService.java        # 相册服务
│   ├── repository/     # 数据访问层
│   │   ├── UserRepository.java      # 用户仓库
│   │   ├── AlbumRepository.java     # 相册仓库
│   │   └── PhotoRepository.java     # 照片仓库
│   ├── entity/         # JPA 实体类
│   │   ├── User.java                # 用户实体
│   │   ├── Album.java               # 相册实体
│   │   └── Photo.java               # 照片实体
│   ├── dto/           # 数据传输对象
│   │   ├── request/   # 请求 DTO
│   │   └── response/  # 响应 DTO
│   ├── config/        # 配置类
│   │   ├── SecurityConfig.java      # 安全配置
│   │   ├── WebConfig.java           # Web 配置
│   │   └── RedisConfig.java         # Redis 配置
│   ├── security/      # 安全相关
│   │   ├── JwtUtil.java             # JWT 工具类
│   │   └── CustomUserDetails.java   # 用户详情
│   ├── utils/         # 工具类
│   │   ├── FileUtil.java            # 文件工具
│   │   └── StringUtil.java          # 字符串工具
│   └── TimeCapsuleApplication.java   # 主启动类
└── src/main/resources/
    ├── application.yml              # 应用配置
    ├── application-dev.yml          # 开发环境配置
    └── application-prod.yml         # 生产环境配置
```

## 3. 开发规范

### 3.1 代码规范

#### 3.1.1 前端规范

**命名规范：**
```javascript
// 组件命名：大驼峰 + .vue 后缀
// UserProfile.vue, PhotoGallery.vue

// 方法命名：驼峰命名
const getUserInfo = () => { ... }
const handlePhotoUpload = () => { ... }

// 变量命名：驼峰命名
const userData = ref({})
const photoList = ref([])
```

**Vue 组件结构：**
```vue
<template>
  <!-- 模板内容 -->
</template>

<script setup>
import { ref, computed } from 'vue'

// 1. 导入语句
// 2. 类型定义
// 3. 响应式数据
// 4. 计算属性
// 5. 方法定义
// 6. 生命周期钩子
</script>

<style scoped>
/* 样式内容 */
</style>
```

#### 3.1.2 后端规范

**类命名：**
```java
// 实体类：名词 + Entity 后缀（可选）
public class User { ... }
public class AlbumEntity { ... }

// 服务类：名词 + Service 后缀
public interface UserService { ... }
public interface AlbumService { ... }

// 控制器：名词 + Controller 后缀
@RestController
public class UserController { ... }
```

**方法规范：**
```java
// 增删改查方法命名
public User createUser(CreateUserRequest request)
public User getUserById(Long id)
public User updateUser(Long id, UpdateUserRequest request)
public void deleteUser(Long id)

// 业务方法命名
public List<Album> getUserAlbums(Long userId)
public Album createAlbum(CreateAlbumRequest request)
```

### 3.2 Git 提交规范

#### 3.2.1 提交信息格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型说明：**
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建工具或辅助工具的变动

**示例：**
```
feat(auth): add JWT authentication

- Implement JWT token generation and validation
- Add user authentication endpoints
- Update security configuration

Closes #123
```

#### 3.2.2 分支管理
```bash
# 主分支
main                    # 生产环境分支
develop                 # 开发环境分支

# 功能分支
feature/user-auth       # 用户认证功能
feature/photo-upload    # 照片上传功能
feature/album-manage    # 相册管理功能

# 修复分支
bugfix/login-issue      # 登录问题修复
hotfix/security-patch   # 安全补丁

# 发布分支
release/v1.0.0          # v1.0.0 版本发布
```

## 4. API 开发指南

### 4.1 RESTful API 设计

#### 4.1.1 资源命名
```javascript
// 正确
GET    /api/v1/users/{id}           // 获取用户
POST   /api/v1/users                // 创建用户
PUT    /api/v1/users/{id}           // 更新用户
DELETE /api/v1/users/{id}           // 删除用户

GET    /api/v1/albums/{id}/photos   // 获取相册照片
POST   /api/v1/albums/{id}/photos   // 上传照片
```

#### 4.1.2 状态码使用
```javascript
// 成功响应
200: OK                    // 请求成功
201: Created              // 资源创建成功
204: No Content           // 请求成功，无返回内容

// 客户端错误
400: Bad Request          // 请求参数错误
401: Unauthorized         // 未认证
403: Forbidden           // 权限不足
404: Not Found           // 资源不存在
409: Conflict            // 资源冲突

// 服务器错误
500: Internal Server Error // 服务器内部错误
503: Service Unavailable   // 服务不可用
```

### 4.2 错误处理

#### 4.2.1 全局异常处理
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ApiResponse> handleBusinessException(BusinessException e) {
        return ResponseEntity.badRequest()
            .body(ApiResponse.error(e.getCode(), e.getMessage()));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ApiResponse> handleException(Exception e) {
        return ResponseEntity.status(500)
            .body(ApiResponse.error(500, "服务器内部错误"));
    }
}
```

#### 4.2.2 自定义异常
```java
// 业务异常
public class BusinessException extends RuntimeException {
    private int code;
    private String message;

    public BusinessException(int code, String message) {
        super(message);
        this.code = code;
        this.message = message;
    }
}

// 使用示例
throw new BusinessException(4001, "用户不存在");
throw new BusinessException(4002, "密码错误");
```

## 5. 数据库开发指南

### 5.1 实体类设计

#### 5.1.1 JPA 实体示例
```java
@Entity
@Table(name = "user")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    private String email;

    @Column(nullable = false)
    private String password;

    @Column(nullable = false)
    private String nickname;

    @Column
    private String avatar;

    @Column
    private LocalDate birthday;

    @Enumerated(EnumType.STRING)
    private Gender gender;

    @Column(length = 500)
    private String bio;

    @CreationTimestamp
    private LocalDateTime createdAt;

    @UpdateTimestamp
    private LocalDateTime updatedAt;

    // 关联关系
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL)
    private List<Album> albums;
}
```

### 5.2 Repository 设计

#### 5.2.1 基础 Repository
```java
public interface UserRepository extends JpaRepository<User, Long> {

    // 按邮箱查找用户
    Optional<User> findByEmail(String email);

    // 检查邮箱是否存在
    boolean existsByEmail(String email);

    // 按状态查找用户
    List<User> findByStatus(UserStatus status);

    // 自定义查询
    @Query("SELECT u FROM User u WHERE u.createdAt >= :startDate")
    List<User> findUsersCreatedAfter(@Param("startDate") LocalDateTime startDate);
}
```

#### 5.2.2 复杂查询 Repository
```java
public interface PhotoRepository extends JpaRepository<Photo, Long> {

    // 按相册查找照片
    Page<Photo> findByAlbumIdOrderByUploadedAtDesc(Long albumId, Pageable pageable);

    // 按时间范围查找
    @Query("SELECT p FROM Photo p WHERE p.takenAt BETWEEN :startDate AND :endDate")
    List<Photo> findPhotosByDateRange(@Param("startDate") LocalDateTime startDate,
                                     @Param("endDate") LocalDateTime endDate);

    // 搜索照片
    @Query("SELECT p FROM Photo p WHERE p.description LIKE %:keyword% OR p.originalName LIKE %:keyword%")
    Page<Photo> searchPhotos(@Param("keyword") String keyword, Pageable pageable);
}
```

## 6. 前端开发指南

### 6.1 组件开发

#### 6.1.1 组件结构
```vue
<template>
  <div class="photo-card">
    <!-- 模板内容 -->
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Photo } from '@/types'

// 类型定义
interface Props {
  photo: Photo
  size?: 'small' | 'medium' | 'large'
}

interface Emits {
  (e: 'click', photo: Photo): void
  (e: 'delete', photoId: number): void
}

// Props 和 Emits
const props = withDefaults(defineProps<Props>(), {
  size: 'medium'
})

const emit = defineEmits<Emits>()

// 响应式数据
const isLoading = ref(false)
const isSelected = ref(false)

// 计算属性
const imageUrl = computed(() => {
  return `${API_BASE_URL}/photos/${props.photo.id}/thumbnail`
})

// 方法
const handleClick = () => {
  emit('click', props.photo)
}

const handleDelete = () => {
  emit('delete', props.photo.id)
}
</script>

<style scoped>
.photo-card {
  /* 样式内容 */
}
</style>
```

### 6.2 状态管理

#### 6.2.1 Pinia Store 示例
```javascript
// stores/user.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userApi } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  // 状态
  const currentUser = ref(null)
  const isAuthenticated = ref(false)
  const preferences = ref({})

  // 计算属性
  const displayName = computed(() => {
    return currentUser.value?.nickname || currentUser.value?.email
  })

  // 动作
  const login = async (credentials) => {
    try {
      const response = await userApi.login(credentials)
      currentUser.value = response.data.user
      isAuthenticated.value = true
      // 保存 token
      localStorage.setItem('token', response.data.token)
      return response
    } catch (error) {
      throw error
    }
  }

  const logout = () => {
    currentUser.value = null
    isAuthenticated.value = false
    preferences.value = {}
    localStorage.removeItem('token')
  }

  const updateProfile = async (profileData) => {
    const response = await userApi.updateProfile(profileData)
    currentUser.value = { ...currentUser.value, ...response.data }
    return response
  }

  return {
    // 状态
    currentUser,
    isAuthenticated,
    preferences,
    // 计算属性
    displayName,
    // 动作
    login,
    logout,
    updateProfile
  }
})
```

### 6.3 API 调用封装

#### 6.3.1 Axios 封装
```javascript
// utils/api.js
import axios from 'axios'

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
      // token 过期，跳转到登录页
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

## 7. 测试指南

### 7.1 单元测试

#### 7.1.1 前端测试
```bash
# 安装测试依赖
npm install --save-dev vitest @vue/test-utils jsdom

# 运行测试
npm run test

# 测试示例
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import PhotoCard from '../components/PhotoCard.vue'

describe('PhotoCard', () => {
  it('renders photo correctly', () => {
    const photo = { id: 1, name: 'test.jpg' }
    const wrapper = mount(PhotoCard, {
      props: { photo }
    })
    expect(wrapper.text()).toContain('test.jpg')
  })
})
```

#### 7.1.2 后端测试
```java
// Spring Boot 测试
@SpringBootTest
public class UserServiceTest {

    @Autowired
    private UserService userService;

    @Test
    public void testCreateUser() {
        CreateUserRequest request = CreateUserRequest.builder()
            .email("test@example.com")
            .password("password123")
            .nickname("测试用户")
            .build();

        User user = userService.createUser(request);

        assertNotNull(user.getId());
        assertEquals("test@example.com", user.getEmail());
    }
}
```

### 7.2 集成测试
```bash
# API 集成测试
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# 前端 E2E 测试
npm install --save-dev cypress
npx cypress open
```

## 8. 部署指南

### 8.1 开发环境部署
```bash
# 1. 环境检查
docker --version
docker-compose --version

# 2. 构建镜像
docker-compose build

# 3. 启动服务
docker-compose up -d

# 4. 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 8.2 生产环境部署
```bash
# 1. 拉取最新代码
git pull origin main

# 2. 构建生产镜像
docker-compose -f docker-compose.prod.yml build

# 3. 部署服务
docker-compose -f docker-compose.prod.yml up -d

# 4. 健康检查
curl http://localhost:8080/actuator/health
```

### 8.3 CI/CD 配置
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build and push Docker image
        run: |
          docker build -t time-capsule .
          docker tag time-capsule:latest registry.example.com/time-capsule:latest
          docker push registry.example.com/time-capsule:latest

      - name: Deploy to server
        run: |
          ssh user@server "docker pull registry.example.com/time-capsule:latest"
          ssh user@server "docker-compose up -d"
```

## 9. 性能优化

### 9.1 前端优化
```javascript
// 图片懒加载
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target
      img.src = img.dataset.src
      observer.unobserve(img)
    }
  })
})

// 虚拟滚动
import VirtualScroller from 'vue-virtual-scroller'

// 代码分割
const PhotoView = () => import('./views/PhotoView.vue')
```

### 9.2 后端优化
```java
// 缓存优化
@Cacheable(value = "user", key = "#id")
public User getUserById(Long id) {
    return userRepository.findById(id).orElse(null);
}

// 异步处理
@Async
public CompletableFuture<List<Photo>> processPhotos(List<Photo> photos) {
    return CompletableFuture.completedFuture(
        photos.stream()
            .map(this::processPhoto)
            .collect(Collectors.toList())
    );
}

// 数据库连接池优化
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.connection-timeout=30000
```

---

*本开发指南涵盖了从环境搭建到部署上线的完整流程，请根据项目实际情况进行调整。*

