#!/usr/bin/env python3
"""
快速启动脚本 - 一键运行 AI 工具集合
"""

import sys
import os
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """检查依赖是否已安装"""
    print("\n📦 检查依赖...")
    try:
        import flask
        import requests
        import pytz
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("\n💡 请运行: pip install -r requirements.txt")
        return False

def create_init_files():
    """创建必要的 __init__.py 文件"""
    print("\n📁 创建包结构...")
    dirs = ["ai", "clock", "jokes", "weather", "database"]
    for dir_name in dirs:
        init_file = Path(dir_name) / "__init__.py"
        if not init_file.exists():
            init_file.parent.mkdir(parents=True, exist_ok=True)
            init_file.touch()
            print(f"  ✅ 创建 {dir_name}/__init__.py")

def start_flask_server():
    """启动 Flask 服务器"""
    print("\n🚀 启动 Flask 应用...")
    print("=" * 60)
    
    # 启动 Flask
    try:
        subprocess.Popen([sys.executable, "app.py"])
        time.sleep(3)  # 等待服务器启动
        print("✅ Flask 服务器已启动 (http://localhost:5000)")
        return True
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False

def open_browser():
    """打开浏览器"""
    print("\n🌐 打开浏览器...")
    
    menu = {
        "1": ("主页 (API 文档)", "http://localhost:5000"),
        "2": ("🕐 全球数字时钟", "http://localhost:5000/clock"),
        "3": ("😂 随机笑话生成器", "http://localhost:5000/jokes"),
        "4": ("🌤️ 天气仪表板", "http://localhost:5000/weather"),
    }
    
    print("\n请选择要打开的功能:")
    print("-" * 60)
    for key, (name, _) in menu.items():
        print(f"  [{key}] {name}")
    print(f"  [0] 打开所有功能")
    print(f"  [q] 退出")
    print("-" * 60)
    
    choice = input("\n请输入选择 (0-4, q): ").strip()
    
    if choice == "0":
        print("\n📱 打开所有功能...")
        for name, url in menu.values():
            print(f"  → 打开 {name}")
            webbrowser.open(url)
            time.sleep(0.5)
    elif choice in menu:
        name, url = menu[choice]
        print(f"\n📱 打开 {name}...")
        webbrowser.open(url)
    elif choice == "q":
        print("\n👋 再见！")
        return False
    else:
        print("\n❌ 无效选择")
        return False
    
    return True

def show_commands():
    """显示常用命令"""
    print("\n" + "=" * 60)
    print("📚 常用命令参考")
    print("=" * 60)
    
    commands = [
        ("获取北京天气", 'curl "http://localhost:5000/api/weather?city=北京"'),
        ("获取随机笑话", 'curl "http://localhost:5000/api/joke/official"'),
        ("查询所有时区", 'curl "http://localhost:5000/api/clocks"'),
        ("解析消费信息", 'curl -X POST http://localhost:5000/parse -H "Content-Type: application/json" -d \'{"message": "买咖啡50块"}\''),
    ]
    
    for desc, cmd in commands:
        print(f"\n📝 {desc}:")
        print(f"   {cmd}")
    
    print("\n" + "=" * 60)

def show_features():
    """显示功能概览"""
    print("\n" + "=" * 60)
    print("✨ 功能概览")
    print("=" * 60)
    
    features = [
        ("🤖 AI 消费记账", "智能识别消费信息，自动分类统计", "POST /parse"),
        ("🕐 全球数字时钟", "实时显示 7 个时区的时间", "GET /clock"),
        ("😂 笑话生成器", "支持 3 种笑话类型随机获取", "GET /jokes"),
        ("🌤️ 天气仪表板", "查询任意城市天气 + 7 天预报", "GET /weather"),
    ]
    
    for icon, desc, endpoint in features:
        print(f"\n{icon}")
        print(f"  描述: {desc}")
        print(f"  端点: {endpoint}")

def main():
    """主函数"""
    print("""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║         🤖 AI 工具集合 - 一键启动器 ✨                     ║
║                                                            ║
║  这个脚本将帮助你快速启动并打开所有功能                    ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 创建包结构
    create_init_files()
    
    # 显示功能概览
    show_features()
    
    # 启动服务器
    if not start_flask_server():
        sys.exit(1)
    
    print("\n✅ 服务器已启动！")
    print("   访问 http://localhost:5000 查看 API 文档")
    
    # 打开浏览器
    while True:
        if not open_browser():
            break
        again = input("\n继续使用? (y/n): ").strip().lower()
        if again != 'y':
            break
    
    # 显示命令参考
    show_commands()
    
    print("\n✨ 感谢使用 AI 工具集合！")
    print("   项目地址: https://github.com/yukaimeng7-ux/legendary-train")
    print("   按 Ctrl+C 停止服务器\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
        sys.exit(0)
