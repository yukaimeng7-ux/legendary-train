# AI 记账微信工具

一个基于 AI 的智能微信记账工具，自动识别消费信息并记录。
同时提供全球数字时钟功能，显示多个时区的实时时间。

## 功能特性

### 🤖 AI 记账模块
- AI 智能解析消费信息
- 微信即时交互
- 消费统计和分析
- 自动分类

### 🕐 全球数字时钟
- 实时显示多个时区的时间
- 精美的网页界面
- 支持自定义时区
- JSON API 接口

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
├── ai/
│   └── parser.py         # AI 解析引擎
├── clock/
│   └── digital_clock.py  # 数字时钟
├── database/
│   ├── models.py         # 数据模型
│   └── operations.py     # 数据操作
└── .env                  # 环境变量（不提交）
```

## 🌐 时钟使用示例

### 网页界面
访问 http://localhost:5000/clock

### API 调用

**获取所有时区的时间：**
```bash
curl http://localhost:5000/api/clocks
```

**获取特定时区的时间：**
```bash
curl "http://localhost:5000/api/clock/Asia%2FShanghai"
```

**获取文本格式的时钟：**
```bash
curl http://localhost:5000/api/clock/text
```

## 📝 消费记账使用示例

### 微信中输入
```
早上买咖啡花了50块
下午奶茶25块
晚餐在餐厅消费168元
```

### API 调用
```bash
curl -X POST http://localhost:5000/parse \
  -H "Content-Type: application/json" \
  -d '{"message": "早上买咖啡花了50块，下午奶茶25块"}'
```

### 查看统计
```bash
curl http://localhost:5000/stats
```

## 🔧 支持的时区

- Asia/Shanghai (北京时间)
- Asia/Hong_Kong (香港)
- Asia/Tokyo (东京)
- Europe/London (伦敦)
- America/New_York (纽约)
- America/Los_Angeles (洛杉矶)
- Australia/Sydney (悉尼)

可在 `clock/digital_clock.py` 中修改 `DEFAULT_TIMEZONES` 列表来自定义时区。

## 待开发功能

- [ ] 微信消息接收和处理
- [ ] 数据库持久化
- [ ] 消费报告生成
- [ ] 更多时钟显示样式
- [ ] 时区搜索功能
