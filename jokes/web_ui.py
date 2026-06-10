"""笑话生成器前端 - HTML 网页界面"""


def get_jokes_html():
    """生成笑话生成器的 HTML"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>随机笑话生成器</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                padding: 40px;
                max-width: 600px;
                width: 100%;
            }
            
            h1 {
                text-align: center;
                color: #333;
                margin-bottom: 10px;
                font-size: 2.2em;
            }
            
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
                font-size: 0.95em;
            }
            
            .api-selector {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
                flex-wrap: wrap;
            }
            
            .api-button {
                flex: 1;
                min-width: 120px;
                padding: 10px 15px;
                border: 2px solid #667eea;
                background: white;
                color: #667eea;
                border-radius: 8px;
                cursor: pointer;
                font-size: 0.9em;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .api-button:hover {
                background: #667eea;
                color: white;
                transform: translateY(-2px);
            }
            
            .api-button.active {
                background: #667eea;
                color: white;
            }
            
            .button-group {
                display: flex;
                gap: 10px;
                margin-bottom: 30px;
            }
            
            .btn {
                flex: 1;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            }
            
            .btn-primary:active {
                transform: translateY(0);
            }
            
            .btn-secondary {
                background: #f0f0f0;
                color: #333;
                border: 2px solid #ddd;
            }
            
            .btn-secondary:hover {
                background: #e0e0e0;
            }
            
            .joke-container {
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 25px;
                border-radius: 8px;
                margin-bottom: 20px;
                min-height: 150px;
                display: none;
            }
            
            .joke-container.show {
                display: block;
                animation: slideIn 0.3s ease;
            }
            
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .joke-emoji {
                font-size: 2.5em;
                margin-bottom: 15px;
            }
            
            .joke-type {
                font-size: 0.85em;
                color: #667eea;
                font-weight: 600;
                text-transform: uppercase;
                margin-bottom: 10px;
            }
            
            .joke-setup {
                font-size: 1.1em;
                color: #333;
                margin-bottom: 15px;
                font-weight: 500;
            }
            
            .joke-punchline {
                font-size: 1.2em;
                color: #764ba2;
                font-weight: 600;
                padding: 15px;
                background: white;
                border-radius: 5px;
            }
            
            .joke-text {
                font-size: 1.1em;
                color: #333;
                line-height: 1.6;
            }
            
            .joke-source {
                font-size: 0.8em;
                color: #999;
                margin-top: 15px;
                text-align: right;
            }
            
            .loading {
                text-align: center;
                padding: 20px;
            }
            
            .spinner {
                border: 4px solid #f0f0f0;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .error-message {
                background: #ffebee;
                color: #c62828;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                display: none;
            }
            
            .error-message.show {
                display: block;
            }
            
            .history {
                margin-top: 30px;
                padding-top: 30px;
                border-top: 2px solid #eee;
            }
            
            .history-title {
                font-size: 1.1em;
                font-weight: 600;
                color: #333;
                margin-bottom: 15px;
            }
            
            .joke-item {
                background: #f8f9fa;
                padding: 12px;
                margin-bottom: 10px;
                border-radius: 5px;
                font-size: 0.9em;
                color: #666;
                border-left: 3px solid #667eea;
            }
            
            .joke-item:hover {
                background: #f0f1f3;
            }
            
            @media (max-width: 600px) {
                .container {
                    padding: 25px;
                }
                
                h1 {
                    font-size: 1.8em;
                }
                
                .api-selector {
                    flex-direction: column;
                }
                
                .api-button {
                    min-width: unset;
                }
                
                .button-group {
                    flex-direction: column;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>😂 笑话生��器</h1>
            <p class="subtitle">一键获取随机笑话，开心一整天！</p>
            
            <div class="api-selector">
                <button class="api-button active" data-api="official">官方笑话</button>
                <button class="api-button" data-api="dad_jokes">爸爸笑话</button>
                <button class="api-button" data-api="programming">编程笑话</button>
            </div>
            
            <div class="button-group">
                <button class="btn btn-primary" id="jokeBtn">获取笑话</button>
                <button class="btn btn-secondary" id="clearBtn">清空历史</button>
            </div>
            
            <div class="error-message" id="errorMsg"></div>
            
            <div class="joke-container" id="jokeContainer">
                <div class="loading">
                    <div class="spinner"></div>
                    <p>加载中...</p>
                </div>
            </div>
            
            <div class="history" id="history" style="display: none;">
                <div class="history-title">📝 最近的笑话</div>
                <div id="historyList"></div>
            </div>
        </div>
        
        <script>
            let currentApi = 'official';
            let jokeHistory = [];
            
            // API 选择
            document.querySelectorAll('.api-button').forEach(btn => {
                btn.addEventListener('click', function() {
                    document.querySelectorAll('.api-button').forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    currentApi = this.dataset.api;
                });
            });
            
            // 获取笑话
            document.getElementById('jokeBtn').addEventListener('click', getJoke);
            
            // 清空历史
            document.getElementById('clearBtn').addEventListener('click', function() {
                jokeHistory = [];
                document.getElementById('history').style.display = 'none';
                document.getElementById('historyList').innerHTML = '';
            });
            
            async function getJoke() {
                const jokeContainer = document.getElementById('jokeContainer');
                const errorMsg = document.getElementById('errorMsg');
                
                // 显示加载状态
                jokeContainer.classList.add('show');
                jokeContainer.innerHTML = '<div class="loading"><div class="spinner"></div><p>加载中...</p></div>';
                errorMsg.classList.remove('show');
                
                try {
                    const response = await fetch(`/api/joke/${currentApi}`);
                    const data = await response.json();
                    
                    if (data.success) {
                        displayJoke(data);
                        addToHistory(data);
                    } else {
                        showError(data.error || '获取笑话失败');
                    }
                } catch (error) {
                    showError('网络错误，请重试');
                    console.error(error);
                }
            }
            
            function displayJoke(joke) {
                const jokeContainer = document.getElementById('jokeContainer');
                let html = '<div class="joke-emoji">😂</div>';
                
                if (joke.type) {
                    html += `<div class="joke-type">${joke.type}</div>`;
                }
                
                if (joke.setup) {
                    html += `<div class="joke-setup">问: ${joke.setup}</div>`;
                    html += `<div class="joke-punchline">答: ${joke.punchline}</div>`;
                } else if (joke.joke) {
                    html += `<div class="joke-text">${joke.joke}</div>`;
                } else {
                    html += `<div class="joke-text">${JSON.stringify(joke.data)}</div>`;
                }
                
                html += `<div class="joke-source">来源: ${joke.api}</div>`;
                
                jokeContainer.innerHTML = html;
                jokeContainer.classList.add('show');
            }
            
            function showError(message) {
                const errorMsg = document.getElementById('errorMsg');
                errorMsg.textContent = '❌ ' + message;
                errorMsg.classList.add('show');
            }
            
            function addToHistory(joke) {
                let text = '';
                if (joke.setup) {
                    text = `Q: ${joke.setup} A: ${joke.punchline}`;
                } else if (joke.joke) {
                    text = joke.joke;
                }
                
                if (text) {
                    jokeHistory.unshift(text);
                    if (jokeHistory.length > 5) {
                        jokeHistory.pop();
                    }
                    updateHistoryDisplay();
                }
            }
            
            function updateHistoryDisplay() {
                const history = document.getElementById('history');
                const historyList = document.getElementById('historyList');
                
                if (jokeHistory.length > 0) {
                    history.style.display = 'block';
                    historyList.innerHTML = jokeHistory
                        .map(joke => `<div class="joke-item">${joke}</div>`)
                        .join('');
                }
            }
            
            // 页面加载时获取一个笑话
            getJoke();
        </script>
    </body>
    </html>
    """
    return html
