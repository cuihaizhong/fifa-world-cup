# 🗄️ 时光胶囊 - 数据库设计文档

## 1. 数据库概述

### 1.1 数据库架构
时光胶囊采用 MySQL 8.0 作为主数据库，Redis 6.0 作为缓存数据库，SQLite 作为本地数据缓存。整体采用读写分离和多级缓存策略。

### 1.2 设计原则
- **规范化设计**：采用第三范式，减少数据冗余
- **索引优化**：合理使用索引提升查询性能
- **分区策略**：对大数据表采用分区存储
- **安全设计**：敏感数据加密存储
- **扩展性**：支持水平扩展和业务扩展

### 1.3 ER图

```
用户(User) --(1:N)--> 相册(Album)
相册(Album) --(1:N)--> 照片(Photo)
用户(User) --(1:1)--> 用户偏好(UserPreference)
用户(User) --(N:M)--> 好友关系(FriendRelation)
用户(User) --(1:1)--> 情侣关系(CoupleRelation)
照片(Photo) --(1:N)--> 评论(Comment)
照片(Photo) --(1:N)--> 点赞(Like)
照片(Photo) --(N:M)--> 标签(Tag)
相册(Album) --(1:N)--> 分享记录(ShareRecord)
用户(User) --(1:N)--> 视频生成任务(VideoTask)
用户(User) --(1:N)--> 操作日志(OperationLog)
用户(User) --(1:N)--> 系统通知(Notification)
相册(Album) --(1:N)--> 相册权限(AlbumPermission)
照片(Photo) --(1:N)--> 文件分片(FileChunk)
用户(User) --(1:N)--> 收藏夹(Favorite)
收藏夹(Favorite) --(N:M)--> 照片(Photo)
用户(User) --(1:N)--> 消息(Message)
```

## 2. 数据表结构

### 2.1 用户相关表

#### 2.1.1 用户表 (user)
```sql
CREATE TABLE `user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `email` varchar(255) NOT NULL COMMENT '邮箱地址',
  `password` varchar(255) NOT NULL COMMENT '密码（加密）',
  `nickname` varchar(100) DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(500) DEFAULT NULL COMMENT '头像URL',
  `birthday` date DEFAULT NULL COMMENT '生日',
  `gender` enum('male','female','other') DEFAULT NULL COMMENT '性别',
  `bio` text COMMENT '个人简介',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `last_login_at` timestamp NULL DEFAULT NULL COMMENT '最后登录时间',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态：0-禁用,1-正常,2-待验证',
  `is_vip` tinyint(1) DEFAULT '0' COMMENT 'VIP状态',
  `vip_expire_at` timestamp NULL DEFAULT NULL COMMENT 'VIP到期时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_email` (`email`),
  UNIQUE KEY `uk_phone` (`phone`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```

#### 2.1.2 用户偏好表 (user_preference)
```sql
CREATE TABLE `user_preference` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `theme` enum('light','dark','auto') DEFAULT 'light' COMMENT '主题偏好',
  `language` varchar(10) DEFAULT 'zh-CN' COMMENT '语言设置',
  `timezone` varchar(50) DEFAULT 'Asia/Shanghai' COMMENT '时区',
  `auto_backup` tinyint(1) DEFAULT '0' COMMENT '自动备份',
  `sync_thumbnails` tinyint(1) DEFAULT '1' COMMENT '同步缩略图',
  `auto_sync` tinyint(1) DEFAULT '1' COMMENT '自动同步',
  `storage_limit` bigint(20) DEFAULT '10737418240' COMMENT '存储限制（字节）',
  `notification_email` tinyint(1) DEFAULT '1' COMMENT '邮件通知',
  `notification_push` tinyint(1) DEFAULT '1' COMMENT '推送通知',
  `privacy_level` enum('public','friends','private') DEFAULT 'private' COMMENT '隐私等级',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_id` (`user_id`),
  CONSTRAINT `fk_preference_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户偏好表';
```

### 2.2 相册和照片表

#### 2.2.1 相册表 (album)
```sql
CREATE TABLE `album` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '创建者ID',
  `name` varchar(255) NOT NULL COMMENT '相册名称',
  `description` text COMMENT '相册描述',
  `cover_image` varchar(500) DEFAULT NULL COMMENT '封面图片URL',
  `is_private` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否私密',
  `album_type` enum('normal','couple','collaborative','smart','template') NOT NULL DEFAULT 'normal' COMMENT '相册类型',
  `template_id` bigint(20) DEFAULT NULL COMMENT '模板ID',
  `sort_order` int(11) DEFAULT '0' COMMENT '排序',
  `photo_count` int(11) DEFAULT '0' COMMENT '照片数量',
  `total_size` bigint(20) DEFAULT '0' COMMENT '总大小（字节）',
  `location` varchar(255) DEFAULT NULL COMMENT '地理位置',
  `tags` json DEFAULT NULL COMMENT '标签集合',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_album_type` (`album_type`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_album_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='相册表';
```

#### 2.2.2 照片表 (photo)
```sql
CREATE TABLE `photo` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `album_id` bigint(20) NOT NULL COMMENT '相册ID',
  `original_name` varchar(255) NOT NULL COMMENT '原始文件名',
  `storage_path` varchar(500) NOT NULL COMMENT '存储路径',
  `thumbnail_path` varchar(500) DEFAULT NULL COMMENT '缩略图路径',
  `preview_path` varchar(500) DEFAULT NULL COMMENT '预览图路径',
  `file_size` bigint(20) DEFAULT NULL COMMENT '文件大小',
  `width` int(11) DEFAULT NULL COMMENT '图片宽度',
  `height` int(11) DEFAULT NULL COMMENT '图片高度',
  `format` varchar(20) DEFAULT NULL COMMENT '图片格式',
  `mime_type` varchar(100) DEFAULT NULL COMMENT 'MIME类型',
  `metadata` json DEFAULT NULL COMMENT '元数据（EXIF等）',
  `hash` varchar(64) DEFAULT NULL COMMENT '文件哈希（去重）',
  `uploaded_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
  `taken_at` timestamp NULL DEFAULT NULL COMMENT '拍摄时间',
  `location` varchar(255) DEFAULT NULL COMMENT '拍摄地点',
  `latitude` decimal(10,8) DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(11,8) DEFAULT NULL COMMENT '经度',
  `province` varchar(100) DEFAULT NULL COMMENT '省份（如云南、北京）',
  `city` varchar(100) DEFAULT NULL COMMENT '城市（如昆明、杭州）',
  `district` varchar(100) DEFAULT NULL COMMENT '区县（如西山区、萧山区）',
  `description` text COMMENT '照片描述',
  `is_favorite` tinyint(1) DEFAULT '0' COMMENT '是否收藏',
  `rating` tinyint(1) DEFAULT '0' COMMENT '评分（1-5）',
  `ai_tags` json DEFAULT NULL COMMENT 'AI识别标签',
  `face_data` json DEFAULT NULL COMMENT '人脸识别数据',
  `scene_type` varchar(50) DEFAULT NULL COMMENT '场景类型',
  `emotion_type` varchar(50) DEFAULT NULL COMMENT '情感类型',
  `quality_score` decimal(3,2) DEFAULT NULL COMMENT '质量评分',
  PRIMARY KEY (`id`),
  KEY `idx_album_id` (`album_id`),
  KEY `idx_taken_at` (`taken_at`),
  KEY `idx_uploaded_at` (`uploaded_at`),
  KEY `idx_hash` (`hash`),
  KEY `idx_scene_type` (`scene_type`),
  KEY `idx_location` (`province`, `city`),
  KEY `idx_is_favorite` (`is_favorite`),
  CONSTRAINT `fk_photo_album` FOREIGN KEY (`album_id`) REFERENCES `album` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='照片表';
```

### 2.3 社交功能表

#### 2.3.1 好友关系表 (friend_relation)
```sql
CREATE TABLE `friend_relation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `friend_id` bigint(20) NOT NULL COMMENT '好友ID',
  `status` enum('pending','accepted','rejected','blocked') NOT NULL DEFAULT 'pending' COMMENT '关系状态',
  `group_id` bigint(20) DEFAULT NULL COMMENT '分组ID',
  `remark` varchar(100) DEFAULT NULL COMMENT '备注',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_friend` (`user_id`,`friend_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_friend_id` (`friend_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `fk_friend_relation_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_friend_relation_friend` FOREIGN KEY (`friend_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='好友关系表';
```

#### 2.3.2 情侣关系表 (couple_relation)
```sql
CREATE TABLE `couple_relation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user1_id` bigint(20) NOT NULL COMMENT '用户1ID',
  `user2_id` bigint(20) NOT NULL COMMENT '用户2ID',
  `status` enum('pending','accepted','dissolved') NOT NULL DEFAULT 'pending' COMMENT '关系状态',
  `anniversary_date` date DEFAULT NULL COMMENT '纪念日',
  `relationship_start` date DEFAULT NULL COMMENT '关系开始日期',
  `verification_question` varchar(500) DEFAULT NULL COMMENT '验证问题',
  `verification_answer` varchar(500) DEFAULT NULL COMMENT '验证答案',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_pair` (`user1_id`,`user2_id`),
  KEY `idx_user1_id` (`user1_id`),
  KEY `idx_user2_id` (`user2_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `fk_couple_relation_user1` FOREIGN KEY (`user1_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_couple_relation_user2` FOREIGN KEY (`user2_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='情侣关系表';
```

### 2.4 标签和分类表

#### 2.4.1 标签表 (tag)
```sql
CREATE TABLE `tag` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '创建者ID',
  `name` varchar(100) NOT NULL COMMENT '标签名称',
  `color` varchar(20) DEFAULT '#1890ff' COMMENT '标签颜色',
  `description` varchar(255) DEFAULT NULL COMMENT '标签描述',
  `tag_type` enum('manual','ai_face','ai_scene','ai_emotion','location','event') NOT NULL DEFAULT 'manual' COMMENT '标签类型',
  `usage_count` int(11) DEFAULT '0' COMMENT '使用次数',
  `is_system` tinyint(1) DEFAULT '0' COMMENT '是否系统标签',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_tag_type` (`tag_type`),
  KEY `idx_name` (`name`),
  CONSTRAINT `fk_tag_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='标签表';
```

#### 2.4.1.1 旅行点分类表 (travel_location)
```sql
CREATE TABLE `travel_location` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `province` varchar(100) NOT NULL COMMENT '省份',
  `city` varchar(100) NOT NULL COMMENT '城市',
  `district` varchar(100) DEFAULT NULL COMMENT '区县',
  `location_name` varchar(255) DEFAULT NULL COMMENT '具体地点名称',
  `description` text COMMENT '地点描述',
  `latitude` decimal(10,8) DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(11,8) DEFAULT NULL COMMENT '经度',
  `visit_count` int(11) DEFAULT '0' COMMENT '访问次数',
  `first_visit_at` timestamp NULL DEFAULT NULL COMMENT '首次访问时间',
  `last_visit_at` timestamp NULL DEFAULT NULL COMMENT '最后访问时间',
  `cover_image` varchar(500) DEFAULT NULL COMMENT '封面图片',
  `is_favorite` tinyint(1) DEFAULT '0' COMMENT '是否收藏',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_location` (`user_id`, `province`, `city`, `district`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_location` (`province`, `city`),
  KEY `idx_is_favorite` (`is_favorite`),
  CONSTRAINT `fk_travel_location_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='旅行点分类表';
```

#### 2.4.1.2 旅行统计表 (travel_statistics)
```sql
CREATE TABLE `travel_statistics` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `province` varchar(100) NOT NULL COMMENT '省份',
  `city` varchar(100) DEFAULT NULL COMMENT '城市',
  `year` int(11) NOT NULL COMMENT '年份',
  `month` int(11) DEFAULT NULL COMMENT '月份',
  `visit_count` int(11) DEFAULT '0' COMMENT '访问次数',
  `photo_count` int(11) DEFAULT '0' COMMENT '照片数量',
  `total_size` bigint(20) DEFAULT '0' COMMENT '总大小',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_location_time` (`user_id`, `province`, `city`, `year`, `month`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_location` (`province`, `city`),
  KEY `idx_time` (`year`, `month`),
  CONSTRAINT `fk_travel_stats_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='旅行统计表';
```

#### 2.4.2 照片标签关联表 (photo_tag)
```sql
CREATE TABLE `photo_tag` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `photo_id` bigint(20) NOT NULL COMMENT '照片ID',
  `tag_id` bigint(20) NOT NULL COMMENT '标签ID',
  `confidence` decimal(3,2) DEFAULT '1.00' COMMENT '置信度（AI标签）',
  `tagged_by` bigint(20) DEFAULT NULL COMMENT '标签添加者',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_photo_tag` (`photo_id`,`tag_id`),
  KEY `idx_photo_id` (`photo_id`),
  KEY `idx_tag_id` (`tag_id`),
  CONSTRAINT `fk_photo_tag_photo` FOREIGN KEY (`photo_id`) REFERENCES `photo` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_photo_tag_tag` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='照片标签关联表';
```

### 2.5 互动功能表

#### 2.5.1 评论表 (comment)
```sql
CREATE TABLE `comment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '评论者ID',
  `photo_id` bigint(20) NOT NULL COMMENT '照片ID',
  `content` text NOT NULL COMMENT '评论内容',
  `parent_id` bigint(20) DEFAULT NULL COMMENT '父评论ID',
  `like_count` int(11) DEFAULT '0' COMMENT '点赞数',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_photo_id` (`photo_id`),
  KEY `idx_parent_id` (`parent_id`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_comment_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_comment_photo` FOREIGN KEY (`photo_id`) REFERENCES `photo` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_comment_parent` FOREIGN KEY (`parent_id`) REFERENCES `comment` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评论表';
```

#### 2.5.2 点赞表 (like)
```sql
CREATE TABLE `like` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '点赞者ID',
  `photo_id` bigint(20) DEFAULT NULL COMMENT '照片ID',
  `comment_id` bigint(20) DEFAULT NULL COMMENT '评论ID',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_photo` (`user_id`,`photo_id`),
  UNIQUE KEY `uk_user_comment` (`user_id`,`comment_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_photo_id` (`photo_id`),
  KEY `idx_comment_id` (`comment_id`),
  CONSTRAINT `fk_like_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_like_photo` FOREIGN KEY (`photo_id`) REFERENCES `photo` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_like_comment` FOREIGN KEY (`comment_id`) REFERENCES `comment` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='点赞表';
```

### 2.6 分享和权限表

#### 2.6.1 分享记录表 (share_record)
```sql
CREATE TABLE `share_record` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `album_id` bigint(20) DEFAULT NULL COMMENT '相册ID',
  `photo_id` bigint(20) DEFAULT NULL COMMENT '照片ID',
  `share_type` enum('link','friend','collaborative','public') NOT NULL DEFAULT 'link' COMMENT '分享类型',
  `share_code` varchar(100) DEFAULT NULL COMMENT '分享码',
  `password` varchar(100) DEFAULT NULL COMMENT '访问密码',
  `expires_at` timestamp NULL DEFAULT NULL COMMENT '过期时间',
  `view_count` int(11) DEFAULT '0' COMMENT '查看次数',
  `download_count` int(11) DEFAULT '0' COMMENT '下载次数',
  `created_by` bigint(20) NOT NULL COMMENT '创建者ID',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_album_id` (`album_id`),
  KEY `idx_photo_id` (`photo_id`),
  KEY `idx_share_code` (`share_code`),
  KEY `idx_created_by` (`created_by`),
  KEY `idx_expires_at` (`expires_at`),
  CONSTRAINT `fk_share_album` FOREIGN KEY (`album_id`) REFERENCES `album` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_share_photo` FOREIGN KEY (`photo_id`) REFERENCES `photo` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_share_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='分享记录表';
```

#### 2.6.2 相册权限表 (album_permission)
```sql
CREATE TABLE `album_permission` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `album_id` bigint(20) NOT NULL COMMENT '相册ID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `permission_type` enum('view','edit','delete','share','admin') NOT NULL DEFAULT 'view' COMMENT '权限类型',
  `granted_by` bigint(20) NOT NULL COMMENT '授权者ID',
  `expires_at` timestamp NULL DEFAULT NULL COMMENT '过期时间',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_album_user` (`album_id`,`user_id`),
  KEY `idx_album_id` (`album_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_permission_type` (`permission_type`),
  CONSTRAINT `fk_album_permission_album` FOREIGN KEY (`album_id`) REFERENCES `album` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_album_permission_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_album_permission_granted_by` FOREIGN KEY (`granted_by`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='相册权限表';
```

### 2.7 视频和任务表

#### 2.7.1 视频生成任务表 (video_task)
```sql
CREATE TABLE `video_task` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `task_name` varchar(255) NOT NULL COMMENT '任务名称',
  `photo_ids` json NOT NULL COMMENT '照片ID列表',
  `template` varchar(50) NOT NULL COMMENT '模板',
  `music` varchar(100) DEFAULT NULL COMMENT '背景音乐',
  `resolution` enum('720p','1080p','4k') DEFAULT '1080p' COMMENT '分辨率',
  `duration` int(11) DEFAULT NULL COMMENT '目标时长（秒）',
  `status` enum('pending','processing','completed','failed','cancelled') NOT NULL DEFAULT 'pending' COMMENT '状态',
  `progress` int(11) NOT NULL DEFAULT '0' COMMENT '进度（0-100）',
  `result_path` varchar(500) DEFAULT NULL COMMENT '结果文件路径',
  `result_size` bigint(20) DEFAULT NULL COMMENT '结果文件大小',
  `error_message` text COMMENT '错误信息',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `completed_at` timestamp NULL DEFAULT NULL COMMENT '完成时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_video_task_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='视频生成任务表';
```

#### 2.7.2 文件分片表 (file_chunk)
```sql
CREATE TABLE `file_chunk` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `photo_id` bigint(20) NOT NULL COMMENT '照片ID',
  `chunk_index` int(11) NOT NULL COMMENT '分片索引',
  `total_chunks` int(11) NOT NULL COMMENT '总分片数',
  `chunk_size` bigint(20) NOT NULL COMMENT '分片大小',
  `chunk_hash` varchar(64) NOT NULL COMMENT '分片哈希',
  `storage_path` varchar(500) NOT NULL COMMENT '存储路径',
  `status` enum('uploading','completed','failed') DEFAULT 'uploading' COMMENT '状态',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `completed_at` timestamp NULL DEFAULT NULL COMMENT '完成时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_photo_chunk` (`photo_id`,`chunk_index`),
  KEY `idx_photo_id` (`photo_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `fk_file_chunk_photo` FOREIGN KEY (`photo_id`) REFERENCES `photo` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文件分片表';
```

### 2.8 系统功能表

#### 2.8.1 操作日志表 (operation_log)
```sql
CREATE TABLE `operation_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '操作用户ID',
  `operation_type` varchar(50) NOT NULL COMMENT '操作类型',
  `resource_type` varchar(50) DEFAULT NULL COMMENT '资源类型',
  `resource_id` bigint(20) DEFAULT NULL COMMENT '资源ID',
  `description` text COMMENT '操作描述',
  `ip_address` varchar(45) DEFAULT NULL COMMENT 'IP地址',
  `user_agent` text COMMENT '用户代理',
  `status` enum('success','failed','blocked') DEFAULT 'success' COMMENT '操作状态',
  `error_message` text COMMENT '错误信息',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_operation_type` (`operation_type`),
  KEY `idx_resource_type` (`resource_type`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志表';
```

#### 2.8.2 系统通知表 (notification)
```sql
CREATE TABLE `notification` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '接收用户ID',
  `type` enum('system','friend','album','photo','comment','like','share') NOT NULL COMMENT '通知类型',
  `title` varchar(255) NOT NULL COMMENT '通知标题',
  `content` text COMMENT '通知内容',
  `resource_type` varchar(50) DEFAULT NULL COMMENT '关联资源类型',
  `resource_id` bigint(20) DEFAULT NULL COMMENT '关联资源ID',
  `sender_id` bigint(20) DEFAULT NULL COMMENT '发送者ID',
  `is_read` tinyint(1) DEFAULT '0' COMMENT '是否已读',
  `priority` enum('low','normal','high','urgent') DEFAULT 'normal' COMMENT '优先级',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_type` (`type`),
  KEY `idx_is_read` (`is_read`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_notification_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统通知表';
```

#### 2.8.3 消息表 (message)
```sql
CREATE TABLE `message` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sender_id` bigint(20) NOT NULL COMMENT '发送者ID',
  `receiver_id` bigint(20) NOT NULL COMMENT '接收者ID',
  `message_type` enum('text','image','photo','file','system') DEFAULT 'text' COMMENT '消息类型',
  `content` text NOT NULL COMMENT '消息内容',
  `photo_id` bigint(20) DEFAULT NULL COMMENT '关联照片ID',
  `file_path` varchar(500) DEFAULT NULL COMMENT '文件路径',
  `is_read` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已读',
  `read_at` timestamp NULL DEFAULT NULL COMMENT '读取时间',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_sender_id` (`sender_id`),
  KEY `idx_receiver_id` (`receiver_id`),
  KEY `idx_message_type` (`message_type`),
  KEY `idx_is_read` (`is_read`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_message_sender` FOREIGN KEY (`sender_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_message_receiver` FOREIGN KEY (`receiver_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_message_photo` FOREIGN KEY (`photo_id`) REFERENCES `photo` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='消息表';
```

#### 2.8.4 收藏夹表 (favorite)
```sql
CREATE TABLE `favorite` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `name` varchar(255) NOT NULL COMMENT '收藏夹名称',
  `description` text COMMENT '收藏夹描述',
  `cover_image` varchar(500) DEFAULT NULL COMMENT '封面图片',
  `is_private` tinyint(1) DEFAULT '0' COMMENT '是否私密',
  `sort_order` int(11) DEFAULT '0' COMMENT '排序',
  `photo_count` int(11) DEFAULT '0' COMMENT '照片数量',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_is_private` (`is_private`),
  CONSTRAINT `fk_favorite_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='收藏夹表';
```

#### 2.8.5 收藏夹照片关联表 (favorite_photo)
```sql
CREATE TABLE `favorite_photo` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `favorite_id` bigint(20) NOT NULL COMMENT '收藏夹ID',
  `photo_id` bigint(20) NOT NULL COMMENT '照片ID',
  `added_by` bigint(20) NOT NULL COMMENT '添加者ID',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_favorite_photo` (`favorite_id`,`photo_id`),
  KEY `idx_favorite_id` (`favorite_id`),
  KEY `idx_photo_id` (`photo_id`),
  CONSTRAINT `fk_favorite_photo_favorite` FOREIGN KEY (`favorite_id`) REFERENCES `favorite` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_favorite_photo_photo` FOREIGN KEY (`photo_id`) REFERENCES `photo` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_favorite_photo_added_by` FOREIGN KEY (`added_by`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='收藏夹照片关联表';
```

## 3. 索引策略

### 3.1 复合索引
```sql
-- 照片搜索优化
CREATE INDEX idx_photo_search ON photo (user_id, taken_at, scene_type, is_favorite);

-- 相册查询优化
CREATE INDEX idx_album_query ON album (user_id, album_type, created_at);

-- 好友关系优化
CREATE INDEX idx_friend_query ON friend_relation (user_id, status, created_at);

-- 评论查询优化
CREATE INDEX idx_comment_query ON comment (photo_id, created_at, like_count);
```

### 3.2 分区策略
```sql
-- 照片表按时间分区
ALTER TABLE photo PARTITION BY RANGE (YEAR(taken_at)) (
  PARTITION p2020 VALUES LESS THAN (2021),
  PARTITION p2021 VALUES LESS THAN (2022),
  PARTITION p2022 VALUES LESS THAN (2023),
  PARTITION p2023 VALUES LESS THAN (2024),
  PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- 操作日志按月分区
ALTER TABLE operation_log PARTITION BY RANGE (MONTH(created_at)) (
  PARTITION p202312 VALUES LESS THAN (13),
  PARTITION p202401 VALUES LESS THAN (2),
  PARTITION p202402 VALUES LESS THAN (3),
  PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

## 4. 数据安全

### 4.1 加密策略
- **密码加密**：BCrypt 哈希算法
- **敏感数据**：AES-256 加密存储
- **传输加密**：TLS 1.3 协议
- **文件加密**：本地文件 AES 加密

### 4.2 备份策略
- **自动备份**：每日增量备份，每周全量备份
- **异地备份**：多地域备份存储
- **备份加密**：所有备份文件加密存储
- **备份验证**：定期验证备份完整性

### 4.3 审计策略
- **操作审计**：记录所有敏感操作
- **访问审计**：记录数据访问行为
- **安全审计**：定期安全漏洞扫描
- **合规审计**：满足 GDPR 等法规要求

---

*数据库设计遵循高性能、高可用、高安全的设计原则，支持海量数据存储和快速查询。*
