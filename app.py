"""整合主应用：记账、时钟、笑话、天气仪表板"""

from flask import Flask, request, jsonify, render_template_string
from ai.parser import parse_expense_message, format_response
from clock.digital_clock import global_clock
from jokes.generator import joke_generator
from jokes.web_ui import get_jokes_html
from weather.dashboard import weather_dashboard
import hashlib

app = Flask(__name__)

# 用于演示的内存存储
expenses_log = []


@app.route('/', methods=['GET'])
def index():
    """首页 - 显示所有功能"""
    return jsonify({
        "name": "AI 工具集合",
        "status": "运行中 🚀",
        "version": "0.3.0",
        "features": [
            "🤖 AI 消费记账解析",
            "💬 微信消息处理",
            "📊 消费统计",
            "🕐 全球数字时钟",
            "😂 随机笑话生成器",
            "🌤️ 天气仪表板"
        ],
        "endpoints": {
            "test": "/test",
            "parse": "/parse (POST)",
            "stats": "/stats",
            "clock_ui": "/clock",
            "clocks_api": "/api/clocks",
            "joke_ui": "/jokes",
            "joke_api": "/api/joke/<type>",
            "weather_ui": "/weather",
            "weather_api": "/api/weather?city=..."
        }
    })


# ========== 消费记账相关 API ==========

@app.route('/test', methods=['GET'])
def test():
    """测试接口"""
    return jsonify({
        "status": "ok",
        "message": "AI 工具集合正在运行中 ✨"
    })


@app.route('/parse', methods=['POST'])
def parse():
    """解析消费信息接口"""
    
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({
            "success": False,
            "error": "消息不能为空"
        }), 400
    
    # 调用 AI 解析
    result = parse_expense_message(message)
    
    # 保存到日志
    if result.get("success"):
        expenses_log.append({
            "message": message,
            "result": result,
            "timestamp": str(__import__('datetime').datetime.now())
        })
    
    # 格式化回复
    reply = format_response(result)
    
    return jsonify({
        "success": result.get("success"),
        "message": reply,
        "data": result,
        "total_logged": len(expenses_log)
    })


@app.route('/stats', methods=['GET'])
def stats():
    """获取统计信息"""
    
    if not expenses_log:
        return jsonify({
            "total_count": 0,
            "total_amount": 0,
            "entries": []
        })
    
    # 简单统计
    total_amount = 0
    categories = {}
    
    for log in expenses_log:
        if log["result"].get("success"):
            items = log["result"].get("items", [])
            for item in items:
                amount = item.get("amount", 0)
                total_amount += amount
                
                category = item.get("category", "未分类")
                categories[category] = categories.get(category, 0) + amount
    
    return jsonify({
        "total_count": len(expenses_log),
        "total_amount": round(total_amount, 2),
        "by_category": categories,
        "recent_entries": expenses_log[-10:] if len(expenses_log) > 10 else expenses_log
    })


# ========== 时钟相关 API ==========

@app.route('/clock', methods=['GET'])
def clock_ui():
    """显示全球时钟网页界面"""
    html = global_clock.get_html_display()
    return render_template_string(html)


@app.route('/api/clocks', methods=['GET'])
def api_clocks():
    """获取所有时区的时间 (JSON)"""
    return jsonify({
        "timestamp": str(__import__('datetime').datetime.now()),
        "timezones": global_clock.get_all_times()
    })


# ========== 笑话生成器 ==========

@app.route('/jokes', methods=['GET'])
def jokes_ui():
    """笑话网页界面"""
    html = get_jokes_html()
    return render_template_string(html)


@app.route('/api/joke/<string:api_type>', methods=['GET'])
def api_joke(api_type):
    """笑话 API"""
    result = joke_generator.get_random_joke(api_type)
    return jsonify(result)


# ========== 天气仪表板 ==========

@app.route('/weather', methods=['GET'])
def weather_ui():
    """天气网页界面"""
    html = weather_dashboard.get_html_dashboard()
    return render_template_string(html)


@app.route('/api/weather', methods=['GET'])
def api_weather():
    """天气 API - 通过 ?city= 参数查询"""
    city = request.args.get('city', '北京')
    result = weather_dashboard.get_weather_by_city(city)
    return jsonify(result)


if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║  🤖 AI 工具集合已启动 ✨                                 ║
    ║                                                           ║
    ║  🌐 主页: http://localhost:5000                          ║
    ║  🕐 时钟: http://localhost:5000/clock                    ║
    ║  😂 笑话: http://localhost:5000/jokes                    ║
    ║  🌤️ 天气: http://localhost:5000/weather                 ║
    ║                                                           ║
    ║  API 文档: http://localhost:5000/                        ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, port=5000)
