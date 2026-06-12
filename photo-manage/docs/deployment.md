# 🚀 时光胶囊 - 部署指南

## 1. 环境要求

### 1.1 系统要求
| 组件 | 最低配置 | 推荐配置 |
|------|----------|----------|
| CPU | 2 核 | 4 核及以上 |
| 内存 | 4GB | 8GB 及以上 |
| 存储 | 50GB | 100GB SSD |
| 网络 | 1Mbps | 10Mbps 及以上 |

### 1.2 软件依赖
| 软件 | 版本 | 说明 |
|------|------|------|
| Java | 1.8+ | 运行 Spring Boot |
| Node.js | 16+ | 构建前端项目 |
| MySQL | 8.0+ | 主数据库 |
| Redis | 6.0+ | 缓存和会话 |
| Nginx | 1.18+ | 反向代理 |

### 1.3 操作系统支持
- **Linux**: Ubuntu 18.04+, CentOS 7+, Debian 10+
- **macOS**: 10.15+ (开发环境)
- **Windows**: 10+ (开发环境)

## 2. 快速开始

### 2.1 传统部署（推荐）

#### 2.1.1 后端部署
```bash
# 1. 克隆项目
git clone https://github.com/your-repo/time-capsule.git
cd time-capsule

# 2. 安装 Java 1.8
sudo apt update
sudo apt install openjdk-8-jdk

# 3. 安装 MySQL 8.0
sudo apt install mysql-server-8.0
sudo systemctl start mysql
sudo mysql_secure_installation

# 4. 创建数据库
mysql -u root -p
CREATE DATABASE time_capsule CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit

# 5. 导入数据库结构
mysql -u root -p time_capsule < scripts/init.sql

# 6. 安装 Redis
sudo apt install redis-server
sudo systemctl start redis

# 7. 构建后端项目
cd backend
./mvnw clean package

# 8. 运行后端服务
java -jar target/time-capsule-backend-1.0.0.jar --spring.profiles.active=prod
```

#### 2.1.2 Docker Compose 配置
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: your_password
      MYSQL_DATABASE: time_capsule
    volumes:
      - mysql_data:/var/lib/mysql
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"

  redis:
    image: redis:6.0-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    environment:
      - SPRING_PROFILES_ACTIVE=prod
    ports:
      - "8080:8080"
    depends_on:
      - mysql
      - redis

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

### 2.2 手动部署

#### 2.1.3 完整部署流程

```bash
# 1. 安装 Java 1.8
sudo apt update
sudo apt install openjdk-8-jdk

# 2. 安装 MySQL 8.0
sudo apt install mysql-server-8.0
sudo systemctl start mysql
sudo mysql_secure_installation

# 3. 创建数据库和用户
mysql -u root -p
CREATE DATABASE time_capsule CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'timecapsule'@'localhost' IDENTIFIED BY 'timecapsule2024';
GRANT ALL PRIVILEGES ON time_capsule.* TO 'timecapsule'@'localhost';
FLUSH PRIVILEGES;
exit

# 4. 导入数据库结构
mysql -u timecapsule -p time_capsule < scripts/init.sql

# 5. 安装 Redis
sudo apt install redis-server
sudo systemctl start redis

# 6. 安装 Node.js 16+
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install nodejs

# 7. 构建后端项目
cd backend
./mvnw clean package -DskipTests

# 8. 构建前端项目
cd ../frontend
npm install
npm run build

# 9. 配置 Nginx
sudo apt install nginx
sudo tee /etc/nginx/sites-available/time-capsule << 'EOF'
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/time-capsule/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws/ {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /upload/ {
        client_max_body_size 100M;
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# 10. 启用配置并重启 Nginx
sudo ln -s /etc/nginx/sites-available/time-capsule /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 11. 启动后端服务
cd backend
java -jar target/time-capsule-backend-1.0.0.jar --spring.profiles.active=prod
```



## 3. 配置文件

### 3.1 后端配置 (application-prod.yml)
```yaml
spring:
  profiles: prod
  datasource:
    url: jdbc:mysql://localhost:3306/time_capsule?useSSL=true&serverTimezone=Asia/Shanghai&useUnicode=true&characterEncoding=utf-8
    username: timecapsule
    password: timecapsule2024
    driver-class-name: com.mysql.jdbc.Driver  # Java 1.8 兼容
  redis:
    host: localhost
    port: 6379
    password:
  security:
    jwt:
      secret: timecapsule_jwt_secret_key_2024
      expiration: 3600000  # 1小时

logging:
  level:
    com.timecapsule: INFO
  file:
    name: logs/time-capsule.log
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"

file:
  upload:
    path: ./uploads/
    max-size: 100MB
    allowed-types: "jpg,jpeg,png,gif,webp,mp4,avi,mov,raw"
  storage:
    local:
      root: ./storage/

travel:
  location:
    auto-detect: true
    api:
      amap:
        key: your_amap_key
        enable: false
      baidu:
        key: your_baidu_key
        enable: false

ai:
  face:
    model: ./models/face_recognition.onnx
    enable: true
  scene:
    model: ./models/scene_classification.onnx
    enable: true
  travel:
    location:
      enable: true
      api-key: your_location_api_key
```

### 3.2 Nginx 配置
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API 代理
    location /api/ {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket 代理
    location /ws/ {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 文件上传
    location /upload/ {
        client_max_body_size 100M;
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # SSL 配置 (可选)
    listen 443 ssl http2;
    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/key.pem;
}
```

### 3.3 环境变量 (.env)
```bash
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_NAME=time_capsule
DB_USERNAME=your_username
DB_PASSWORD=your_password

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# JWT 配置
JWT_SECRET=your_jwt_secret_key
JWT_EXPIRATION=3600000

# 文件存储
UPLOAD_PATH=/data/time-capsule/uploads
STORAGE_PATH=/data/time-capsule/storage

# AI 模型路径
FACE_MODEL_PATH=/models/face_recognition.onnx
SCENE_MODEL_PATH=/models/scene_classification.onnx

# 邮件服务
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_email@example.com
SMTP_PASSWORD=your_email_password

# 监控配置
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true
```

## 4. 监控和日志

### 4.1 应用监控

#### 4.1.1 Prometheus 配置
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'time-capsule-backend'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: '/actuator/prometheus'

  - job_name: 'time-capsule-frontend'
    static_configs:
      - targets: ['localhost:3000']
```

#### 4.1.2 Grafana 仪表板
- JVM 内存使用情况
- API 响应时间
- 数据库连接池状态
- Redis 缓存命中率
- 文件上传下载统计
- 用户活跃度统计

### 4.2 日志配置

#### 4.2.1 日志级别
```yaml
logging:
  level:
    com.timecapsule: INFO
    org.springframework.security: DEBUG
    org.hibernate.SQL: DEBUG
  file:
    name: logs/time-capsule.log
  logback:
    rollingpolicy:
      max-file-size: 10MB
      max-history: 30
```

#### 4.2.2 ELK Stack 配置
```yaml
# Filebeat 配置
filebeat.inputs:
- type: log
  paths:
    - /data/time-capsule/logs/*.log
  fields:
    service: time-capsule

output.elasticsearch:
  hosts: ["localhost:9200"]
```

### 4.3 健康检查
```bash
# 应用健康检查
curl http://localhost:8080/actuator/health

# 数据库连接检查
curl http://localhost:8080/actuator/health/db

# Redis 连接检查
curl http://localhost:8080/actuator/health/redis
```

## 5. 备份和恢复

### 5.1 数据库备份
```bash
# 全量备份
mysqldump -u root -p time_capsule > backup_$(date +%Y%m%d_%H%M%S).sql

# 增量备份
mysqlbinlog --start-datetime="2023-01-01 00:00:00" mysql-bin.000001 > incremental_backup.sql

# 自动备份脚本
#!/bin/bash
BACKUP_DIR="/data/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u root -p time_capsule > $BACKUP_DIR/time_capsule_$DATE.sql

# 保留最近30天的备份
find $BACKUP_DIR -name "time_capsule_*.sql" -mtime +30 -delete
```

### 5.2 文件备份
```bash
# 增量文件备份
rsync -avz --delete /data/time-capsule/storage/ /backup/storage/

# 压缩备份
tar -czf storage_backup_$(date +%Y%m%d).tar.gz /data/time-capsule/storage/

# 备份到远程服务器
scp storage_backup_$(date +%Y%m%d).tar.gz user@backup-server:/backup/
```

### 5.3 恢复流程
```bash
# 1. 停止服务
docker-compose down

# 2. 恢复数据库
mysql -u root -p time_capsule < backup_20231201_120000.sql

# 3. 恢复文件
tar -xzf storage_backup_20231201.tar.gz -C /data/time-capsule/

# 4. 启动服务
docker-compose up -d

# 5. 验证恢复
curl http://localhost:8080/actuator/health
```

## 6. 性能优化

### 6.1 数据库优化
```sql
-- 创建索引
CREATE INDEX idx_photo_search ON photo (user_id, taken_at, scene_type, is_favorite);
CREATE INDEX idx_album_query ON album (user_id, album_type, created_at);

-- 优化查询
EXPLAIN SELECT * FROM photo WHERE user_id = 1 AND taken_at > '2023-01-01';

-- 分区表
ALTER TABLE photo PARTITION BY RANGE (YEAR(taken_at)) (
  PARTITION p2023 VALUES LESS THAN (2024),
  PARTITION p2024 VALUES LESS THAN (2025),
  PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

### 6.2 Redis 优化
```bash
# Redis 配置优化
maxmemory 2gb
maxmemory-policy allkeys-lru
appendonly yes
appendfsync everysec

# 缓存预热
# 在应用启动时预加载热点数据
```

### 6.3 前端优化
```bash
# 构建优化
npm run build -- --mode production

# CDN 配置
# 静态资源走 CDN
# 图片资源懒加载
# 代码分割和按需加载
```

## 7. 安全加固

### 7.1 系统安全
```bash
# 防火墙配置
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22
sudo ufw --force enable

# 禁用 root 远程登录
sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# 安装安全更新
sudo apt update && sudo apt upgrade
```

### 7.2 应用安全
- 启用 HTTPS (Let's Encrypt)
- 配置安全头 (CSP, HSTS)
- 定期更新依赖包
- 代码安全扫描 (SonarQube)

### 7.3 数据安全
- 数据库敏感数据加密
- 文件存储加密
- 备份文件加密
- 定期安全审计

## 8. 故障排除

### 8.1 常见问题

#### 问题1: 数据库连接失败
```bash
# 检查 MySQL 服务状态
sudo systemctl status mysql

# 检查连接配置
mysql -u root -p -h localhost -P 3306

# 查看错误日志
tail -f /var/log/mysql/error.log
```

#### 问题2: Redis 连接超时
```bash
# 检查 Redis 服务
sudo systemctl status redis

# 测试连接
redis-cli ping

# 检查内存使用
redis-cli info memory
```

#### 问题3: 文件上传失败
```bash
# 检查上传目录权限
ls -la /data/time-capsule/uploads/

# 检查磁盘空间
df -h

# 检查 Nginx 配置
sudo nginx -t
```

#### 问题4: 内存溢出
```bash
# 查看 Java 进程
jps -l

# 监控内存使用
jstat -gcutil <pid> 1000

# 调整 JVM 参数
-Xmx4g -Xms2g -XX:+UseG1GC
```

### 8.2 监控告警
```yaml
# Prometheus 告警规则
groups:
  - name: time-capsule-alerts
    rules:
      - alert: HighResponseTime
        expr: http_request_duration_seconds{quantile="0.9"} > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "API 响应时间过高"

      - alert: HighErrorRate
        expr: rate(http_requests_total{status="500"}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "错误率过高"
```

## 9. 更新升级

### 9.1 滚动更新
```bash
# 1. 备份当前版本
docker tag time-capsule-backend:latest time-capsule-backend:v1.0.0

# 2. 拉取新版本
docker pull time-capsule-backend:v1.1.0

# 3. 滚动更新
docker-compose up -d backend

# 4. 健康检查
curl http://localhost:8080/actuator/health

# 5. 如果失败，回滚
docker-compose up -d time-capsule-backend:v1.0.0
```

### 9.2 数据库迁移
```bash
# 使用 Flyway 进行数据库迁移
./mvnw flyway:migrate

# 验证迁移
./mvnw flyway:validate

# 回滚迁移（如果需要）
./mvnw flyway:repair
```

---

*部署文档包含了从环境准备到监控运维的完整流程，请根据实际环境调整配置参数。*
