#!/bin/bash
# 2026 世界杯预测 — 启动脚本

echo "🏆 启动 2026 世界杯预测系统..."

# 安装依赖
pip install -r requirements.txt -q

# 初始化数据 (首次运行会自动创建数据库和种子数据)
python -c "
from data.store import Store
from data.seed_data import seed_all
store = Store()
if store.is_empty():
    print('📦 首次运行，初始化种子数据...')
    seed_all(store)
    print('✅ 初始化完成')
else:
    print('✅ 数据已存在，跳过初始化')
store.close()
"

# 启动 Streamlit
streamlit run web/app.py --server.port 8501
