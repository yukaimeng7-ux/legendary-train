# AI 记账微信工具

一个基于 AI 的智能微信记账工具，自动识别消费信息并记录。

## 功能特性

- 🤖 AI 智能解析消费信息
- 💬 微信即时交互
- 📊 消费统计和分析
- 🏷️ 自动分类

## 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置环境变量
创建 `.env` 文件：
```
OPENAI_API_KEY=your_api_key_here
WECHAT_TOKEN=your_wechat_token
WECHAT_APPID=your_app_id
WECHAT_APPSECRET=your_app_secret
```

### 运行应用
```bash
python app.py
```

## 项目结构

```
.
├── app.py                 # 主应用
├── config.py             # 配置管理
├── requirements.txt      # 依赖
├── wechat/              # 微信模块
│   ├── handler.py       # 消息处理
│   └── crypto.py        # 加密解密
├── ai/                  # AI 模块
│   └── parser.py        # 信息解析
├── database/            # 数据库
│   ├── models.py        # 数据模型
│   └── operations.py    # 数据操作
└── .env                 # 环境变量（不提交）
```

## 使用示例

### 微信中输入
```
早上买咖啡花了50块
下午奶茶25块
晚餐在餐厅消费168元
```

### AI 自动解析
```json
{
  "items": [
    {"amount": 50, "category": "饮食", "description": "咖啡"},
    {"amount": 25, "category": "饮食", "description": "奶茶"},
    {"amount": 168, "category": "饮食", "description": "晚餐"}
  ],
  "total": 243,
  "date": "2026-06-10"
}
```

## 待开发功能

- [ ] 微信消息接收和处理
- [ ] AI 智能解析
- [ ] 数据库存储
- [ ] 统计和报告
- [ ] 查询功能
