"""天气仪表板模块 - 使用 Open-Meteo（无需 API Key）"""

import requests
from typing import Dict
from datetime import datetime


class WeatherDashboard:
    """天气仪表板 - 支持多个天气 API"""
    
    # Open-Meteo API (免费，无需 API Key)
    OPENMETEO_API = "https://api.open-meteo.com/v1/forecast"
    
    # Open-Meteo Geocoding API (地理编码)
    GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
    
    # 天气代码映射
    WEATHER_CODES = {
        0: ("晴天", "☀️"),
        1: ("主要晴朗", "🌤️"),
        2: ("部分多云", "⛅"),
        3: ("阴天", "☁️"),
        45: ("雾霾", "🌫️"),
        48: ("沉积雾", "🌫️"),
        51: ("小雨", "🌧️"),
        53: ("中雨", "🌧️"),
        55: ("大雨", "⛈️"),
        61: ("小雨", "🌧️"),
        63: ("中雨", "🌧️"),
        65: ("大雨", "⛈️"),
        71: ("小雪", "❄️"),
        73: ("中雪", "❄️"),
        75: ("大雪", "❄️"),
        77: ("雪粒", "❄️"),
        80: ("小阵雨", "🌦️"),
        81: ("中阵雨", "🌧️"),
        82: ("大阵雨", "⛈️"),
        85: ("小阵雪", "🌨️"),
        86: ("大阵雪", "🌨️"),
        95: ("雷暴", "⛈️"),
        96: ("冰雹雷暴", "⛈️"),
        99: ("冰雹雷暴", "⛈️"),
    }
    
    @staticmethod
    def get_coordinates(city_name: str) -> Dict:
        """
        通过城市名获取坐标
        
        Args:
            city_name: 城市名称（支持中文）
        
        Returns:
            坐标数据
        """
        try:
            params = {
                "name": city_name,
                "count": 1,
                "language": "zh",
                "format": "json"
            }
            
            response = requests.get(WeatherDashboard.GEOCODING_API, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("results") and len(data["results"]) > 0:
                result = data["results"][0]
                return {
                    "success": True,
                    "latitude": result.get("latitude"),
                    "longitude": result.get("longitude"),
                    "city": result.get("name"),
                    "country": result.get("country"),
                    "admin": result.get("admin1"),
                    "timezone": result.get("timezone")
                }
            
            return {
                "success": False,
                "error": f"未找到城市: {city_name}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"地理编码错误: {str(e)}"
            }
    
    @staticmethod
    def get_current_weather(latitude: float, longitude: float, city_name: str = "Unknown") -> Dict:
        """
        获取当前天气
        
        Args:
            latitude: 纬度
            longitude: 经度
            city_name: 城市名称
        
        Returns:
            天气数据
        """
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": True,
                "hourly": "temperature_2m,weathercode",
                "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max",
                "temperature_unit": "celsius",
                "timezone": "auto",
                "language": "zh"
            }
            
            response = requests.get(WeatherDashboard.OPENMETEO_API, params=params, timeout=6)
            response.raise_for_status()
            
            data = response.json()
            current = data.get("current_weather", {})
            
            weather_code = current.get("weathercode", 0)
            weather_name, weather_icon = WeatherDashboard.WEATHER_CODES.get(weather_code, ("未知", "❓"))
            
            return {
                "success": True,
                "city": city_name,
                "timezone": data.get("timezone"),
                "current": {
                    "temperature": round(current.get("temperature", 0), 1),
                    "wind_speed": round(current.get("windspeed", 0), 1),
                    "wind_direction": current.get("winddirection", 0),
                    "weather_code": weather_code,
                    "weather_name": weather_name,
                    "weather_icon": weather_icon,
                    "time": current.get("time")
                },
                "hourly": data.get("hourly", {}),
                "daily": data.get("daily", {}),
                "latitude": latitude,
                "longitude": longitude
            }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "请求超时（可能是网络问题）",
                "city": city_name
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"天气获取错误: {str(e)}",
                "city": city_name
            }
    
    @staticmethod
    def get_weather_by_city(city_name: str) -> Dict:
        """
        通过城市名获取天气
        
        Args:
            city_name: 城市名称
        
        Returns:
            天气数据
        """
        # 首先获取坐标
        coords = WeatherDashboard.get_coordinates(city_name)
        
        if not coords.get("success"):
            return coords
        
        # 然后获取天气
        weather = WeatherDashboard.get_current_weather(
            coords["latitude"],
            coords["longitude"],
            coords.get("city", city_name)
        )
        
        return weather
    
    @staticmethod
    def format_weather_display(weather: Dict) -> str:
        """
        格式化天气显示
        
        Args:
            weather: 天气数据
        
        Returns:
            格式化的天气文本
        """
        if not weather.get("success"):
            return f"❌ 获取天气失败: {weather.get('error', '未知错误')}"
        
        current = weather.get("current", {})
        city = weather.get("city", "Unknown")
        
        icon = current.get("weather_icon", "❓")
        weather_name = current.get("weather_name", "未知")
        temp = current.get("temperature", "--")
        wind_speed = current.get("wind_speed", "--")
        
        display = f"{icon} {city} 的天气\\n\\n"
        display += f"🌡️ 温度: {temp}°C\\n"
        display += f"💨 风速: {wind_speed} km/h\\n"
        display += f"☁️ 天气: {weather_name}"
        
        return display
    
    @staticmethod
    def get_html_dashboard() -> str:
        """生成天气仪表板的 HTML"""
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>天气仪表板</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }
        .container { background: white; border-radius: 20px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); padding: 40px; max-width: 900px; width: 100%; }
        h1 { text-align: center; color: #333; margin-bottom: 30px; font-size: 2.2em; }
        .search-box { display: flex; gap: 10px; margin-bottom: 30px; }
        .search-box input { flex: 1; padding: 12px 15px; border: 2px solid #ddd; border-radius: 8px; font-size: 1em; }
        .search-box input:focus { outline: none; border-color: #667eea; }
        .search-box button { padding: 12px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; transition: all 0.3s; }
        .search-box button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4); }
        .weather-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 15px; margin-bottom: 20px; text-align: center; display: none; }
        .weather-card.show { display: block; animation: slideIn 0.3s ease; }
        @keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .city-name { font-size: 2em; font-weight: 600; margin-bottom: 20px; }
        .weather-icon { font-size: 5em; margin-bottom: 20px; display: inline-block; animation: bounce 2s infinite; }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        .temperature { font-size: 4em; font-weight: bold; margin-bottom: 10px; }
        .temp-unit { font-size: 0.5em; vertical-align: super; }
        .details-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px; margin-top: 30px; padding-top: 30px; border-top: 2px solid rgba(255, 255, 255, 0.3); }
        .detail-item { text-align: center; background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; }
        .detail-label { font-size: 0.9em; opacity: 0.8; margin-bottom: 8px; }
        .detail-value { font-size: 1.4em; font-weight: 600; }
        .forecast { margin-top: 30px; }
        .forecast-title { font-size: 1.2em; font-weight: 600; color: #333; margin-bottom: 15px; }
        .forecast-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 12px; }
        .forecast-item { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 10px; text-align: center; transition: all 0.3s; }
        .forecast-item:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3); }
        .forecast-day { font-weight: 600; font-size: 0.95em; margin-bottom: 8px; }
        .forecast-icon { font-size: 2em; margin-bottom: 5px; }
        .forecast-temp { font-weight: 600; font-size: 1em; }
        .error-message { background: #ffebee; color: #c62828; padding: 15px; border-radius: 8px; margin-bottom: 20px; display: none; }
        .error-message.show { display: block; }
        .loading { text-align: center; padding: 20px; }
        .spinner { border: 4px solid #f0f0f0; border-top: 4px solid #667eea; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 10px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .city-suggestions { display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; }
        .suggestion-btn { padding: 6px 12px; background: #f0f0f0; border: 1px solid #ddd; border-radius: 20px; cursor: pointer; font-size: 0.9em; transition: all 0.2s; }
        .suggestion-btn:hover { background: #e8e8e8; border-color: #667eea; }
        .info-box { background: #e3f2fd; border-left: 4px solid #667eea; padding: 12px; border-radius: 5px; margin-bottom: 20px; font-size: 0.9em; color: #1565c0; }
        @media (max-width: 600px) { .container { padding: 25px; } h1 { font-size: 1.8em; } .temperature { font-size: 3em; } .weather-icon { font-size: 3em; } }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌤️ 天气仪表板</h1>
        <div class="info-box">💡 提示: 输入城市名称即可查询当前天气和 7 天预报</div>
        <div class="search-box">
            <input type="text" id="cityInput" placeholder="输入城市名称（如：北京、上海、东京）" value="北京">
            <button id="searchBtn">🔍 搜索</button>
        </div>
        <div class="city-suggestions">
            <button class="suggestion-btn" onclick="searchCity('北京')">北京</button>
            <button class="suggestion-btn" onclick="searchCity('上海')">上海</button>
            <button class="suggestion-btn" onclick="searchCity('广州')">广州</button>
            <button class="suggestion-btn" onclick="searchCity('东京')">东京</button>
            <button class="suggestion-btn" onclick="searchCity('纽约')">纽约</button>
            <button class="suggestion-btn" onclick="searchCity('伦敦')">伦敦</button>
            <button class="suggestion-btn" onclick="searchCity('悉尼')">悉尼</button>
        </div>
        <div class="error-message" id="errorMsg"></div>
        <div class="weather-card" id="weatherCard"><div class="loading"><div class="spinner"></div><p>加载中...</p></div></div>
        <div id="forecastSection" class="forecast" style="display: none;">
            <div class="forecast-title">📅 未来 7 天预报</div>
            <div class="forecast-grid" id="forecastGrid"></div>
        </div>
    </div>
    <script>
        const cityInput = document.getElementById('cityInput');
        const searchBtn = document.getElementById('searchBtn');
        const weatherCard = document.getElementById('weatherCard');
        const errorMsg = document.getElementById('errorMsg');
        const forecastSection = document.getElementById('forecastSection');
        
        searchBtn.addEventListener('click', getWeather);
        cityInput.addEventListener('keypress', e => { if (e.key === 'Enter') getWeather(); });
        
        function searchCity(city) {
            cityInput.value = city;
            getWeather();
        }
        
        async function getWeather() {
            const city = cityInput.value.trim();
            if (!city) { showError('请输入城市名称'); return; }
            weatherCard.innerHTML = '<div class="loading"><div class="spinner"></div><p>加载中...</p></div>';
            weatherCard.classList.add('show');
            errorMsg.classList.remove('show');
            try {
                const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
                const data = await response.json();
                if (data.success) { displayWeather(data); } else { showError(data.error || '获取天气失败'); }
            } catch (error) { showError('网络错误，请检查网络连接'); console.error(error); }
        }
        
        function displayWeather(weather) {
            const current = weather.current;
            const city = weather.city;
            const daily = weather.daily || {};
            let html = `<div class="city-name">${city}</div><div class="weather-icon">${current.weather_icon}</div><div class="temperature">${current.temperature}<span class="temp-unit">°C</span></div><div class="weather-main">${current.weather_name}</div><div class="details-grid"><div class="detail-item"><div class="detail-label">💨 风速</div><div class="detail-value">${current.wind_speed} km/h</div></div><div class="detail-item"><div class="detail-label">🧭 风向</div><div class="detail-value">${current.wind_direction}°</div></div></div>`;
            weatherCard.innerHTML = html;
            weatherCard.classList.add('show');
            if (daily.time && daily.temperature_2m_max) { displayForecast(daily); }
        }
        
        function displayForecast(daily) {
            const days = daily.time || [];
            const maxTemps = daily.temperature_2m_max || [];
            const minTemps = daily.temperature_2m_min || [];
            const codes = daily.weathercode || [];
            const weatherIcons = { 0: '☀️', 1: '🌤️', 2: '⛅', 3: '☁️', 45: '🌫️', 48: '🌫️', 51: '🌧️', 53: '🌧️', 55: '⛈️', 61: '🌧️', 63: '🌧️', 65: '⛈️', 71: '❄️', 73: '❄️', 75: '❄️', 77: '❄️', 80: '🌦️', 81: '🌧️', 82: '⛈️', 85: '🌨️', 86: '🌨️', 95: '⛈️', 96: '⛈️', 99: '⛈️' };
            const forecastGrid = document.getElementById('forecastGrid');
            forecastGrid.innerHTML = '';
            for (let i = 0; i < Math.min(7, days.length); i++) {
                const date = new Date(days[i]);
                const dayName = ['日', '一', '二', '三', '四', '五', '六'][date.getDay()];
                const icon = weatherIcons[codes[i]] || '❓';
                const item = document.createElement('div');
                item.className = 'forecast-item';
                item.innerHTML = `<div class="forecast-day">周${dayName}</div><div class="forecast-icon">${icon}</div><div class="forecast-temp">${Math.round(maxTemps[i])}° / ${Math.round(minTemps[i])}°</div>`;
                forecastGrid.appendChild(item);
            }
            forecastSection.style.display = 'block';
        }
        
        function showError(message) {
            errorMsg.textContent = '❌ ' + message;
            errorMsg.classList.add('show');
            weatherCard.classList.remove('show');
            forecastSection.style.display = 'none';
        }
        
        getWeather();
    </script>
</body>
</html>"""
        return html


# 创建全局天气仪表板实例
weather_dashboard = WeatherDashboard()
