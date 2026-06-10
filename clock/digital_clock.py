"""时钟和时区模块"""

from datetime import datetime
import pytz


class DigitalClock:
    """数字时钟类 - 显示不同时区的时间"""
    
    # 默认时区列表
    DEFAULT_TIMEZONES = [
        'Asia/Shanghai',      # 北京时间
        'Asia/Hong_Kong',     # 香港
        'Asia/Tokyo',         # 东京
        'Europe/London',      # 伦敦
        'America/New_York',   # 纽约
        'America/Los_Angeles',# 洛杉矶
        'Australia/Sydney',   # 悉尼
    ]
    
    def __init__(self, timezones=None):
        """
        初始化时钟
        
        Args:
            timezones: 时区列表，默认为 DEFAULT_TIMEZONES
        """
        self.timezones = timezones or self.DEFAULT_TIMEZONES
    
    def get_current_time_in_zone(self, timezone: str) -> dict:
        """获取指定时区的当前时间"""
        try:
            tz = pytz.timezone(timezone)
            now = datetime.now(tz)
            
            return {
                "timezone": timezone,
                "success": True,
                "time": now.strftime("%H:%M:%S"),
                "date": now.strftime("%Y-%m-%d"),
                "day": now.strftime("%A"),
                "formatted": now.strftime("%Y-%m-%d %H:%M:%S %Z"),
                "offset": now.strftime("%z")
            }
        except pytz.exceptions.UnknownTimeZoneError:
            return {
                "timezone": timezone,
                "success": False,
                "error": f"未知时区: {timezone}"
            }
    
    def get_all_times(self) -> dict:
        """获取所有配置时区的当前时间"""
        times = {}
        for tz in self.timezones:
            times[tz] = self.get_current_time_in_zone(tz)
        return times
    
    def get_formatted_display(self) -> str:
        """获取格式化的时钟显示"""
        lines = []
        lines.append("=" * 60)
        lines.append("🕐 全球数字时钟")
        lines.append("=" * 60)
        
        for result in self.get_all_times().values():
            if result.get("success"):
                tz_name = result["timezone"]
                time_str = result["time"]
                date_str = result["date"]
                offset = result["offset"]
                
                # 获取时区的城市名称
                city = tz_name.split('/')[-1]
                
                lines.append(f"\n🌍 {city:<15} ({tz_name})")
                lines.append(f"   时间: {time_str}")
                lines.append(f"   日期: {date_str}")
                lines.append(f"   偏移: {offset}")
        
        lines.append("\n" + "=" * 60)
        return "\n".join(lines)
    
    def get_html_display(self) -> str:
        """生成 HTML 格式的时钟显示"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>全球数字时钟</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: 'Courier New', monospace;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }
                
                .container {
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    padding: 40px;
                    max-width: 1000px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }
                
                h1 {
                    text-align: center;
                    color: #fff;
                    margin-bottom: 40px;
                    font-size: 2.5em;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                }
                
                .clock-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                }
                
                .clock-card {
                    background: rgba(255, 255, 255, 0.15);
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 15px;
                    padding: 20px;
                    text-align: center;
                    transition: all 0.3s ease;
                    cursor: pointer;
                }
                
                .clock-card:hover {
                    background: rgba(255, 255, 255, 0.25);
                    border-color: rgba(255, 255, 255, 0.5);
                    transform: translateY(-5px);
                    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
                }
                
                .city {
                    font-size: 1.3em;
                    font-weight: bold;
                    color: #ffd700;
                    margin-bottom: 10px;
                }
                
                .timezone {
                    font-size: 0.9em;
                    color: #b0e0e6;
                    margin-bottom: 15px;
                }
                
                .time {
                    font-size: 2.2em;
                    font-weight: bold;
                    color: #fff;
                    font-family: 'Digital-7', 'Courier New', monospace;
                    letter-spacing: 2px;
                    margin-bottom: 10px;
                    text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
                }
                
                .date {
                    font-size: 0.95em;
                    color: #e0e0e0;
                    margin-bottom: 8px;
                }
                
                .offset {
                    font-size: 0.85em;
                    color: #90ee90;
                }
                
                .last-update {
                    text-align: center;
                    margin-top: 30px;
                    color: #b0e0e6;
                    font-size: 0.9em;
                }
                
                @media (max-width: 600px) {
                    .container {
                        padding: 20px;
                    }
                    
                    h1 {
                        font-size: 1.8em;
                    }
                    
                    .time {
                        font-size: 1.8em;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🕐 全球数字时钟</h1>
                <div class="clock-grid" id="clockGrid"></div>
                <div class="last-update" id="lastUpdate"></div>
            </div>
            
            <script>
                function updateClocks() {
                    fetch('/api/clocks')
                        .then(response => response.json())
                        .then(data => {
                            const grid = document.getElementById('clockGrid');
                            grid.innerHTML = '';
                            
                            for (const [timezone, timeData] of Object.entries(data.timezones)) {
                                if (timeData.success) {
                                    const city = timezone.split('/').pop();
                                    const card = document.createElement('div');
                                    card.className = 'clock-card';
                                    card.innerHTML = `
                                        <div class="city">${city}</div>
                                        <div class="timezone">${timezone}</div>
                                        <div class="time">${timeData.time}</div>
                                        <div class="date">${timeData.date}</div>
                                        <div class="offset">${timeData.offset}</div>
                                    `;
                                    grid.appendChild(card);
                                }
                            }
                            
                            const lastUpdate = document.getElementById('lastUpdate');
                            lastUpdate.textContent = `最后更新: ${new Date().toLocaleTimeString()}`;
                        })
                        .catch(error => console.error('Error:', error));
                }
                
                // 初始加载
                updateClocks();
                
                // 每秒更新一次
                setInterval(updateClocks, 1000);
            </script>
        </body>
        </html>
        """
        return html


# 创建全局时钟实例
global_clock = DigitalClock()
