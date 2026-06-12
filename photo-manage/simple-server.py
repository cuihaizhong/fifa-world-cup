#!/usr/bin/env python3
"""
简单的测试服务器 - 用于调试MIME类型问题
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 3000
FRONTEND_DIR = Path(__file__).parent / "frontend"

class SimpleServer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def do_GET(self):
        # 特殊处理TypeScript文件
        if self.path.endswith('.ts'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()

            # 返回一个简单的TypeScript内容
            content = b'console.log("TypeScript module loaded successfully");'
            self.wfile.write(content)
            return

        # 对于其他文件，使用默认处理
        return super().do_GET()

def main():
    print("🧪 简单测试服务器")
    print(f"📁 服务目录: {FRONTEND_DIR}")
    print(f"🌐 访问地址: http://localhost:{PORT}")
    print("❌ 停止服务: Ctrl+C\n")

    try:
        with socketserver.TCPServer(("", PORT), SimpleServer) as httpd:
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ 端口 {PORT} 已被占用")
        else:
            print(f"❌ 服务器启动失败: {e}")

if __name__ == "__main__":
    main()