# 实验室智能预约系统

基于 AI Agent 的实验室智能预约系统，支持自然语言交互、RAG 知识库问答、实验室/设备预约管理等功能。

## 项目简介

本项目是一个前后端分离的实验室预约管理平台，集成 AI 智能助手，用户可通过自然语言与系统交互，实现智能查询、自动预约等操作。系统采用 RAG（检索增强生成）技术，基于实验室知识库提供有依据的问答服务。

## 技术架构

### 后端 (backend)

| 技术栈 | 说明 |
|--------|------|
| Python 3.12+ | 编程语言 |
| FastAPI | Web 框架 |
| SQLAlchemy 2.x | ORM 框架 |
| MySQL | 关系型数据库 |
| ChromaDB | 向量数据库，用于知识库检索 |
| LangGraph + LangChain | AI Agent 编排框架 |
| OpenAI API | 大语言模型接口 |
| sentence-transformers | 中文文本嵌入模型 (BAAI/bge-small-zh-v1.5) |
| PyJWT + bcrypt | 用户认证与密码加密 |
| Uvicorn | ASGI 服务器 |

### 前端 (frontend)

| 技术栈 | 说明 |
|--------|------|
| Vue 3 | 前端框架 |
| Vite | 构建工具 |
| Element Plus | UI 组件库 |
| Vue Router | 路由管理 |
| Axios | HTTP 客户端 |
| marked | Markdown 渲染 |
| DOMPurify | HTML 安全过滤 |

## 项目结构

```
yy-agent/
├── backend/                    # 后端项目
│   ├── app/
│   │   ├── api/                # API 路由层
│   │   │   ├── ai.py           # AI 聊天接口（普通/流式）
│   │   │   ├── api.py          # 路由聚合
│   │   │   ├── device.py       # 设备管理接口
│   │   │   ├── lab.py          # 实验室管理接口
│   │   │   ├── login.py        # 登录认证接口
│   │   │   ├── reservation.py  # 预约管理接口
│   │   │   ├── upload.py       # 文件上传接口
│   │   │   └── user.py         # 用户管理接口
│   │   ├── common/             # 公共模块
│   │   │   ├── exceptions.py   # 业务异常定义
│   │   │   └── response.py     # 统一响应封装
│   │   ├── config/             # 配置模块
│   │   │   └── config.py       # 环境配置读取
│   │   ├── core/               # 核心模块
│   │   │   └── database.py     # 数据库引擎与模型基类
│   │   ├── deps/               # 依赖注入
│   │   │   └── check_user.py   # 当前用户鉴权
│   │   ├── models/             # 数据模型层
│   │   │   ├── device.py       # 设备模型
│   │   │   ├── lab.py          # 实验室模型
│   │   │   ├── reservation.py  # 预约模型
│   │   │   └── user.py         # 用户模型
│   │   ├── schemas/            # Pydantic 数据校验
│   │   ├── services/           # 业务逻辑层
│   │   │   ├── agent_service.py    # AI Agent 编排（LangGraph）
│   │   │   ├── agent_tools.py      # Agent 可调用的工具集
│   │   │   ├── ai_service.py       # AI 对话服务
│   │   │   ├── auth_service.py     # 认证服务
│   │   │   ├── device_service.py   # 设备服务
│   │   │   ├── kb_service.py       # 知识库服务（ChromaDB）
│   │   │   ├── lab_service.py      # 实验室服务
│   │   │   ├── reservation_service.py  # 预约服务
│   │   │   └── user_service.py     # 用户服务
│   │   ├── utils/              # 工具函数
│   │   │   ├── password.py     # 密码加密
│   │   │   └── token.py        # JWT Token 工具
│   │   └── main.py             # 应用入口
│   ├── data/                   # 数据目录
│   │   ├── kb/                 # 知识库文档（Markdown）
│   │   │   ├── 安全规范.md
│   │   │   ├── 开放时间.md
│   │   │   ├── 设备使用.md
│   │   │   └── 预约规则.md
│   │   └── chroma/             # ChromaDB 向量数据库
│   ├── uploads/                # 上传文件目录
│   ├── .env                    # 环境变量配置
│   ├── pyproject.toml          # Python 依赖配置
│   └── uv.lock                 # uv 锁定文件
│
├── frontend/                   # 前端项目
│   ├── src/
│   │   ├── api/                # API 请求封装
│   │   │   ├── ai.js           # AI 接口（普通/流式）
│   │   │   ├── auth.js         # 认证接口
│   │   │   ├── device.js       # 设备接口
│   │   │   ├── lab.js          # 实验室接口
│   │   │   ├── reservation.js  # 预约接口
│   │   │   ├── upload.js       # 上传接口
│   │   │   └── user.js         # 用户接口
│   │   ├── assets/             # 静态资源
│   │   ├── components/         # 公共组件
│   │   ├── layouts/            # 布局组件
│   │   ├── router/             # 路由配置
│   │   ├── utils/              # 工具函数
│   │   ├── views/              # 页面视图
│   │   │   ├── ai/
│   │   │   │   └── chat.vue        # AI 智能助手
│   │   │   ├── device/
│   │   │   │   └── device.vue      # 设备管理
│   │   │   ├── lab/
│   │   │   │   ├── lab.vue         # 实验室管理
│   │   │   │   ├── lab_device.vue  # 实验室设备
│   │   │   │   └── lab_list.vue    # 实验室列表
│   │   │   ├── reservation/
│   │   │   │   ├── audit_reservation.vue   # 审核预约
│   │   │   │   └── my_reservation.vue      # 我的预约
│   │   │   ├── user/
│   │   │   │   ├── password.vue    # 修改密码
│   │   │   │   ├── profile.vue     # 个人中心
│   │   │   │   └── user.vue        # 用户管理
│   │   │   ├── home.vue          # 系统首页
│   │   │   ├── login.vue         # 登录页
│   │   │   └── register.vue      # 注册页
│   │   ├── App.vue               # 根组件
│   │   └── main.js               # 入口文件
│   ├── .env.development          # 开发环境变量
│   ├── index.html                # HTML 模板
│   ├── package.json              # Node 依赖配置
│   └── vite.config.js            # Vite 配置
│
└── README.md                   # 项目说明文档
```

## 核心功能

### 1. 用户认证
- 用户注册 / 登录
- JWT Token 鉴权
- 个人中心（信息修改、密码修改、头像上传）

### 2. 实验室管理
- 实验室的增删改查
- 实验室图片上传
- 开放状态管理

### 3. 设备管理
- 设备的增删改查
- 设备与实验室关联
- 设备规格、数量管理

### 4. 预约管理
- 实验室 / 设备预约提交
- 预约状态流转：待审核 -> 已通过 / 已拒绝 / 已取消
- 我的预约查询
- 管理员审核预约
- 预约过期自动处理

### 5. AI 智能助手
- **自然语言交互**：用户可用自然语言描述需求，如"帮我预约明天下午的计算机实验室"
- **RAG 知识库问答**：基于实验室规则、开放时间、安全规范等文档进行检索回答
- **智能 Agent**：基于 LangGraph 构建工作流，自动调用工具完成查询和预约
- **流式输出**：支持 SSE 流式对话，实时展示 AI 思考过程
- **工具调用**：
  - `search_lab_docs` — 检索知识库
  - `list_open_labs` — 查询开放实验室
  - `list_lab_devices` — 查询实验室设备
  - `create_reservation` — 创建预约（需用户确认）
  - `get_today` — 获取当前日期

## 环境要求

- Python >= 3.12
- Node.js >= 22.18.0
- MySQL >= 5.7

## 快速开始

### 后端启动

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐 uv）
uv venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 安装依赖
uv pip install -r pyproject.toml

# 配置环境变量（编辑 .env 文件）
# DATABASE_URL=mysql+pymysql://root:root@127.0.0.1:3306/lab_agent
# JWT_KEY=your-secret-key
# BASE_URL=https://apihub.agnes-ai.com/v1
# API_KEY=your-api-key
# LLM_MODEL=agnes-2.5-flash

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端默认运行在 `http://localhost:5173`，通过代理访问后端 `http://127.0.0.1:8000`。

## 数据库模型

### 用户表 (users)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| account | varchar(32) | 账号 |
| password | varchar(255) | 加密密码 |
| username | varchar(32) | 用户名称 |
| email | varchar(64) | 邮箱 |
| phone | varchar(16) | 手机号 |
| avatar | varchar(255) | 头像地址 |
| status | int | 状态：1启用，-1禁用 |
| is_super | int | 是否超级管理员 |

### 实验室表 (labs)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | varchar(32) | 实验室名称 |
| description | varchar(500) | 描述 |
| image | varchar(256) | 图片 |
| location | varchar(32) | 位置 |
| capacity | int | 容量 |
| open_time | varchar(32) | 开放时间 |
| close_time | varchar(32) | 关闭时间 |
| status | int | 状态：1正常，-1禁用 |

### 设备表 (devices)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| lab_id | int | 所属实验室ID |
| name | varchar(32) | 设备名称 |
| description | varchar(500) | 描述 |
| image | varchar(256) | 图片 |
| spec | varchar(500) | 规格 |
| quantity | int | 数量 |
| status | int | 状态：1正常，-1禁用 |

### 预约表 (reservations)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| user_id | int | 用户ID |
| lab_id | int | 实验室ID |
| device_id | int | 设备ID（可选） |
| date | varchar(32) | 预约日期 |
| start_time | varchar(32) | 开始时间 |
| end_time | varchar(32) | 结束时间 |
| remark | varchar(255) | 备注 |
| status | int | 状态：0待审核，1已通过，-1已拒绝，-2已取消 |

## API 接口概览

| 接口前缀 | 功能 |
|----------|------|
| POST /api/login | 用户登录 |
| POST /api/register | 用户注册 |
| GET /api/user/list | 用户列表 |
| GET /api/lab/list | 实验室列表 |
| POST /api/lab | 创建实验室 |
| GET /api/device/list | 设备列表 |
| POST /api/device | 创建设备 |
| GET /api/reservation/list | 预约列表 |
| POST /api/reservation | 创建预约 |
| PUT /api/reservation/{id}/audit | 审核预约 |
| POST /api/ai/chat | AI 对话 |
| POST /api/ai/chat/stream | AI 流式对话 |
| POST /api/upload | 文件上传 |

## 配置说明

### 后端 .env

```env
# 数据库连接
DATABASE_URL=mysql+pymysql://username:password@host:port/database

# JWT 配置
JWT_KEY=your-secret-key
JWT_EXPIRE_HOURS=24
JWT_ALGORITHM=HS256

# 调试模式
DEBUG=True

# AI 模型配置
BASE_URL=https://apihub.agnes-ai.com/v1
API_KEY=your-api-key
LLM_MODEL=agnes-2.5-flash
```

### 前端 .env.development

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## 知识库维护

将 Markdown 文档放入 `backend/data/kb/` 目录，系统启动时会自动加载到 ChromaDB 向量数据库中。支持以下主题：

- 预约规则
- 开放时间
- 安全规范
- 设备使用

## 开发计划

- [x] 用户认证与权限管理
- [x] 实验室 / 设备 CRUD
- [x] 预约管理与审核流程
- [x] AI 智能助手（普通对话）
- [x] AI Agent 工作流（工具调用 + 流式输出）
- [x] RAG 知识库检索
- [ ] 预约冲突检测
- [ ] 日历视图展示
- [ ] 消息通知系统

## 许可证

MIT License
