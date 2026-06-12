# 🔗 时光胶囊 - API 接口文档

## 1. API 概述

### 1.1 接口规范
- **协议**：HTTPS
- **数据格式**：JSON
- **字符编码**：UTF-8
- **认证方式**：JWT Bearer Token
- **版本控制**：URL 路径版本控制（/api/v1/）

### 1.2 通用响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": "2023-01-01T00:00:00.000Z"
}
```

### 1.3 错误码说明
| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| 200 | 成功 | - |
| 400 | 请求参数错误 | 检查参数格式 |
| 401 | 未认证/Token过期 | 重新登录 |
| 403 | 权限不足 | 检查用户权限 |
| 404 | 资源不存在 | 检查资源ID |
| 409 | 资源冲突 | 检查重复操作 |
| 429 | 请求过于频繁 | 稍后重试 |
| 500 | 服务器内部错误 | 联系技术支持 |

## 2. 认证接口

### 2.1 用户注册
**POST** `/api/v1/auth/register`

**请求参数：**
```json
{
  "email": "string, required, email格式",
  "password": "string, required, 8-20位",
  "nickname": "string, optional, 2-20字符",
  "verificationCode": "string, required, 邮箱验证码"
}
```

**响应：**
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "nickname": "时光旅人",
    "avatar": null,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 3600
  }
}
```

### 2.2 用户登录
**POST** `/api/v1/auth/login`

**请求参数：**
```json
{
  "email": "string, required",
  "password": "string, required"
}
```

### 2.3 发送验证码
**POST** `/api/v1/auth/send-verification-code`

**请求参数：**
```json
{
  "email": "string, required, email格式",
  "type": "string, required, enum[register,reset_password]"
}
```

### 2.4 刷新Token
**POST** `/api/v1/auth/refresh`

**请求头：**
```
Authorization: Bearer {refresh_token}
```

## 3. 用户管理接口

### 3.1 获取用户信息
**GET** `/api/v1/users/{userId}`

### 3.2 更新用户信息
**PUT** `/api/v1/users/{userId}`

**请求参数：**
```json
{
  "nickname": "string, optional",
  "avatar": "string, optional",
  "birthday": "string, optional, YYYY-MM-DD格式",
  "gender": "string, optional, enum[male,female,other]",
  "bio": "string, optional"
}
```

### 3.3 修改密码
**PUT** `/api/v1/users/{userId}/password`

**请求参数：**
```json
{
  "oldPassword": "string, required",
  "newPassword": "string, required, 8-20位",
  "confirmPassword": "string, required"
}
```

### 3.4 获取用户偏好
**GET** `/api/v1/users/{userId}/preferences`

### 3.5 更新用户偏好
**PUT** `/api/v1/users/{userId}/preferences`

**请求参数：**
```json
{
  "theme": "string, optional, enum[light,dark,auto]",
  "language": "string, optional",
  "timezone": "string, optional",
  "autoBackup": "boolean, optional",
  "syncThumbnails": "boolean, optional",
  "autoSync": "boolean, optional",
  "notificationEmail": "boolean, optional",
  "notificationPush": "boolean, optional",
  "privacyLevel": "string, optional, enum[public,friends,private]"
}
```

## 4. 相册管理接口

### 4.1 获取相册列表
**GET** `/api/v1/albums`

**查询参数：**
- `page`: 页码，默认1
- `pageSize`: 每页数量，默认20
- `albumType`: 相册类型
- `keyword`: 搜索关键词

### 4.2 创建相册
**POST** `/api/v1/albums`

**请求参数：**
```json
{
  "name": "string, required",
  "description": "string, optional",
  "isPrivate": "boolean, optional",
  "albumType": "string, optional, enum[normal,couple,collaborative,smart,template]",
  "templateId": "number, optional"
}
```

### 4.3 更新相册
**PUT** `/api/v1/albums/{albumId}`

### 4.4 删除相册
**DELETE** `/api/v1/albums/{albumId}`

### 4.5 批量操作相册
**POST** `/api/v1/albums/batch`

**请求参数：**
```json
{
  "operation": "string, required, enum[delete,move,share,export]",
  "albumIds": "array, required, [1,2,3]",
  "params": "object, optional"
}
```

## 5. 旅行点分类接口

### 5.1 获取旅行点列表
**GET** `/api/v1/travel/locations`

**查询参数：**
- `page`: 页码，默认1
- `pageSize`: 每页数量，默认20
- `province`: 省份筛选
- `city`: 城市筛选
- `isFavorite`: 是否收藏

### 5.2 获取旅行点详情
**GET** `/api/v1/travel/locations/{locationId}`

### 5.3 创建旅行点
**POST** `/api/v1/travel/locations`

**请求参数：**
```json
{
  "province": "string, required, 省份",
  "city": "string, required, 城市",
  "district": "string, optional, 区县",
  "locationName": "string, optional, 具体地点名称",
  "description": "string, optional, 地点描述",
  "latitude": "number, optional, 纬度",
  "longitude": "number, optional, 经度"
}
```

### 5.4 更新旅行点
**PUT** `/api/v1/travel/locations/{locationId}`

### 5.5 删除旅行点
**DELETE** `/api/v1/travel/locations/{locationId}`

### 5.6 获取旅行点照片
**GET** `/api/v1/travel/locations/{locationId}/photos`

### 5.7 按旅行点分类照片
**POST** `/api/v1/travel/classify-photos`

**请求参数：**
```json
{
  "photoIds": "array, required, 照片ID列表",
  "autoDetect": "boolean, optional, 是否自动检测地理位置"
}
```

### 5.8 获取旅行统计
**GET** `/api/v1/travel/statistics`

**查询参数：**
- `year`: 年份
- `month`: 月份
- `province`: 省份
- `city`: 城市

## 6. 照片管理接口

### 6.1 获取照片列表
**GET** `/api/v1/albums/{albumId}/photos`

**查询参数：**
- `page`: 页码，默认1
- `pageSize`: 每页数量，默认20
- `sortBy`: 排序字段，默认uploadedAt
- `order`: 排序方式，默认desc
- `keyword`: 搜索关键词
- `takenAfter`: 拍摄时间开始
- `takenBefore`: 拍摄时间结束
- `sceneType`: 场景类型
- `emotionType`: 情感类型

### 6.2 上传照片
**POST** `/api/v1/albums/{albumId}/photos`

**请求体：** multipart/form-data
- `files`: 照片文件数组
- `description`: 照片描述
- `province`: 省份（可选）
- `city`: 城市（可选）
- `district`: 区县（可选）
- `tags`: 标签数组

### 6.3 分片上传照片
**POST** `/api/v1/upload/chunk`

**请求参数：**
```json
{
  "albumId": "number, required",
  "fileName": "string, required",
  "fileSize": "number, required",
  "chunkIndex": "number, required",
  "totalChunks": "number, required",
  "chunkHash": "string, required",
  "file": "binary, required"
}
```

### 6.4 完成分片上传
**POST** `/api/v1/upload/chunk/complete`

**请求参数：**
```json
{
  "fileName": "string, required",
  "totalChunks": "number, required",
  "albumId": "number, required"
}
```

### 6.5 更新照片信息
**PUT** `/api/v1/photos/{photoId}`

**请求参数：**
```json
{
  "description": "string, optional",
  "takenAt": "string, optional, ISO8601格式",
  "location": "string, optional",
  "latitude": "number, optional",
  "longitude": "number, optional",
  "rating": "number, optional, 1-5"
}
```

### 5.6 批量编辑照片
**PUT** `/api/v1/photos/batch`

**请求参数：**
```json
{
  "photoIds": "array, required",
  "operation": "string, required, enum[delete,move,tag,description,rating]",
  "params": "object, required"
}
```

### 5.7 照片搜索
**GET** `/api/v1/photos/search`

**查询参数：**
- `keyword`: 搜索关键词
- `tags`: 标签过滤
- `sceneType`: 场景类型
- `emotionType`: 情感类型
- `takenAfter`: 时间范围开始
- `takenBefore`: 时间范围结束
- `location`: 地理位置
- `rating`: 评分

## 6. 标签管理接口

### 6.1 获取标签列表
**GET** `/api/v1/tags`

### 6.2 创建标签
**POST** `/api/v1/tags`

**请求参数：**
```json
{
  "name": "string, required",
  "color": "string, optional",
  "description": "string, optional",
  "tagType": "string, optional"
}
```

### 6.3 为照片添加标签
**POST** `/api/v1/photos/{photoId}/tags`

**请求参数：**
```json
{
  "tagIds": "array, required"
}
```

### 6.4 批量标签操作
**POST** `/api/v1/photos/tags/batch`

**请求参数：**
```json
{
  "photoIds": "array, required",
  "tagIds": "array, required",
  "operation": "string, required, enum[add,remove,replace]"
}
```

## 7. 收藏夹管理接口

### 7.1 获取收藏夹列表
**GET** `/api/v1/favorites`

### 7.2 创建收藏夹
**POST** `/api/v1/favorites`

**请求参数：**
```json
{
  "name": "string, required",
  "description": "string, optional",
  "isPrivate": "boolean, optional"
}
```

### 7.3 添加照片到收藏夹
**POST** `/api/v1/favorites/{favoriteId}/photos`

**请求参数：**
```json
{
  "photoIds": "array, required"
}
```

## 8. 情侣空间接口

### 8.1 发送情侣邀请
**POST** `/api/v1/couple/invite`

**请求参数：**
```json
{
  "targetUserId": "number, required",
  "verificationQuestion": "string, optional",
  "verificationAnswer": "string, optional"
}
```

### 8.2 响应情侣邀请
**POST** `/api/v1/couple/respond`

**请求参数：**
```json
{
  "relationId": "number, required",
  "accept": "boolean, required",
  "verificationAnswer": "string, optional"
}
```

### 8.3 获取情侣关系信息
**GET** `/api/v1/couple/relation`

### 8.4 获取情侣相册
**GET** `/api/v1/couple/albums`

### 8.5 获取情侣统计
**GET** `/api/v1/couple/statistics`

## 9. 社交功能接口

### 9.1 搜索用户
**GET** `/api/v1/friends/search`

**查询参数：**
- `keyword`: 搜索关键词
- `page`: 页码
- `pageSize`: 每页数量

### 9.2 发送好友请求
**POST** `/api/v1/friends/add`

**请求参数：**
```json
{
  "targetUserId": "number, required",
  "message": "string, optional"
}
```

### 9.3 处理好友请求
**POST** `/api/v1/friends/respond`

**请求参数：**
```json
{
  "requestId": "number, required",
  "accept": "boolean, required"
}
```

### 9.4 获取好友列表
**GET** `/api/v1/friends`

### 9.5 获取好友动态
**GET** `/api/v1/friends/activities`

## 10. 分享功能接口

### 10.1 创建分享
**POST** `/api/v1/share`

**请求参数：**
```json
{
  "resourceType": "string, required, enum[album,photo,favorite]",
  "resourceId": "number, required",
  "shareType": "string, required, enum[link,friend,collaborative,public]",
  "expiresAt": "string, optional, ISO8601格式",
  "password": "string, optional",
  "permissions": "array, optional, [view,download,comment]"
}
```

### 10.2 通过分享码访问
**GET** `/api/v1/share/{shareCode}`

**查询参数：**
- `password`: 访问密码（如果需要）

### 10.3 获取分享统计
**GET** `/api/v1/share/{shareCode}/statistics`

## 11. 评论和点赞接口

### 11.1 评论照片
**POST** `/api/v1/photos/{photoId}/comments`

**请求参数：**
```json
{
  "content": "string, required",
  "parentId": "number, optional"
}
```

### 11.2 获取照片评论
**GET** `/api/v1/photos/{photoId}/comments`

### 11.3 点赞照片
**POST** `/api/v1/photos/{photoId}/like`

### 11.4 取消点赞
**DELETE** `/api/v1/photos/{photoId}/like`

## 12. 消息接口

### 12.1 发送消息
**POST** `/api/v1/messages`

**请求参数：**
```json
{
  "receiverId": "number, required",
  "messageType": "string, required, enum[text,image,photo,file,system]",
  "content": "string, required",
  "photoId": "number, optional",
  "file": "binary, optional"
}
```

### 12.2 获取消息列表
**GET** `/api/v1/messages`

**查询参数：**
- `withUserId`: 指定用户ID
- `page`: 页码
- `pageSize`: 每页数量

### 12.3 标记消息已读
**PUT** `/api/v1/messages/{messageId}/read`

### 12.4 获取未读消息数量
**GET** `/api/v1/messages/unread-count`

## 13. 视频生成功能接口

### 13.1 生成视频
**POST** `/api/v1/videos/generate`

**请求参数：**
```json
{
  "taskName": "string, required",
  "photoIds": "array, required",
  "template": "string, required",
  "music": "string, optional",
  "resolution": "string, optional, enum[720p,1080p,4k]",
  "duration": "number, optional"
}
```

### 13.2 获取视频生成进度
**GET** `/api/v1/videos/{taskId}/progress`

### 13.3 下载视频
**GET** `/api/v1/videos/{taskId}/download`

### 13.4 获取模板列表
**GET** `/api/v1/videos/templates`

### 13.5 获取背景音乐列表
**GET** `/api/v1/videos/music`

## 14. 数据统计接口

### 14.1 获取用户统计
**GET** `/api/v1/statistics/user`

### 14.2 获取相册统计
**GET** `/api/v1/statistics/albums`

### 14.3 获取照片统计
**GET** `/api/v1/statistics/photos`

### 14.4 获取使用情况统计
**GET** `/api/v1/statistics/usage`

## 15. 系统通知接口

### 15.1 获取通知列表
**GET** `/api/v1/notifications`

### 15.2 标记通知已读
**PUT** `/api/v1/notifications/{notificationId}/read`

### 15.3 批量标记已读
**PUT** `/api/v1/notifications/batch-read`

### 15.4 删除通知
**DELETE** `/api/v1/notifications/{notificationId}`

## 16. 操作日志接口

### 16.1 获取操作日志
**GET** `/api/v1/logs/operations`

**查询参数：**
- `page`: 页码
- `pageSize`: 每页数量
- `operationType`: 操作类型
- `startDate`: 开始日期
- `endDate`: 结束日期

## 17. 数据导入导出接口

### 17.1 导出数据
**POST** `/api/v1/export`

**请求参数：**
```json
{
  "exportType": "string, required, enum[albums,photos,metadata,all]",
  "format": "string, required, enum[json,csv,zip]",
  "albumIds": "array, optional",
  "includeThumbnails": "boolean, optional"
}
```

### 17.2 获取导出进度
**GET** `/api/v1/export/{taskId}/progress`

### 17.3 下载导出文件
**GET** `/api/v1/export/{taskId}/download`

### 17.4 导入数据
**POST** `/api/v1/import`

**请求体：** multipart/form-data
- `file`: 导入文件
- `importType`: 导入类型

## 18. WebSocket 接口

### 18.1 连接建立
**WebSocket** `/ws/connect?token={jwt_token}`

### 18.2 消息格式
```json
{
  "type": "string, required",
  "data": "object, required",
  "timestamp": "string"
}
```

### 18.3 支持的消息类型
- `chat_message`: 聊天消息
- `notification`: 系统通知
- `video_progress`: 视频生成进度
- `sync_status`: 数据同步状态
- `online_status`: 用户在线状态

---

*API 设计遵循 RESTful 规范，支持版本控制和向后兼容。所有接口都经过安全验证和权限控制。*
