"""Reusable UI components"""
from __future__ import annotations

from typing import Optional

import streamlit as st
from config import THEME
from data.seed_data import FLAG_MAP
from data.models import Match, Prediction, Team


def match_card(match: Match, show_detail: bool = True):
    """Render a match prediction card"""
    home = match.home_team
    away = match.away_team
    pred = match.prediction

    home_flag = FLAG_MAP.get(home.fifa_code, "")
    away_flag = FLAG_MAP.get(away.fifa_code, "")

    lines = []
    lines.append('<div class="match-card">')
    lines.append('<div style="display: flex; justify-content: space-between; align-items: center;">')
    lines.append(f'<div style="flex: 1; text-align: right; font-size: 1.1rem; font-weight: 600;">{home_flag} {home.name_cn}</div>')
    lines.append(f'<div style="margin: 0 20px; color: {THEME["text_secondary"]}; font-size: 0.85rem;">VS</div>')
    lines.append(f'<div style="flex: 1; font-size: 1.1rem; font-weight: 600;">{away_flag} {away.name_cn}</div>')
    lines.append('</div>')

    if pred:
        conf_cls = 'high' if pred.confidence == '高' else 'mid' if pred.confidence == '中' else 'low'
        lines.append(f'<div style="text-align: center; margin-top: 4px; font-size: 0.8rem; color: {THEME["text_secondary"]};">')
        lines.append(f'{match.stage.value} · {match.venue} · Elo差: {pred.elo_diff:+.0f}')
        lines.append(f'<span class="confidence-tag confidence-{conf_cls}" style="margin-left: 8px;">置信度: {pred.confidence}</span>')
        lines.append('</div>')
        lines.append('<div class="progress-container">')
        lines.append(f'<div class="progress-win" style="width: {pred.home_win_pct}%;"></div>')
        lines.append(f'<div class="progress-draw" style="width: {pred.draw_pct}%;"></div>')
        lines.append(f'<div class="progress-lose" style="width: {pred.away_win_pct}%;"></div>')
        lines.append('</div>')
        lines.append('<div class="pct-label">')
        lines.append(f'<span class="win">胜 {pred.home_win_pct}%</span>')
        lines.append(f'<span class="draw">平 {pred.draw_pct}%</span>')
        lines.append(f'<span class="lose">负 {pred.away_win_pct}%</span>')
        lines.append('</div>')
        lines.append(f'<div class="score-prediction">⚽ 预测比分: {pred.expected_home_goals} - {pred.expected_away_goals}</div>')
    else:
        lines.append(f'<div style="text-align: center; margin-top: 12px; color: {THEME["text_secondary"]}; font-size: 0.9rem;">')
        lines.append(f'{match.stage.value} · {match.date.strftime("%m月%d日 %H:%M")} · {match.venue}')
        lines.append('</div>')
        lines.append(f'<div style="text-align: center; margin-top: 4px; color: {THEME["text_secondary"]}; font-size: 0.8rem;">暂无预测数据</div>')

    lines.append('</div>')
    st.markdown('\n'.join(lines), unsafe_allow_html=True)

    if show_detail and pred:
        with st.expander(f"📊 {home.name_cn} vs {away.name_cn} 详细数据"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"{home_flag} {home.name_cn} Elo", f"{home.elo_rating:.0f}")
                st.metric("FIFA 排名", f"#{home.fifa_rank}")
            with col2:
                st.metric(f"{away_flag} {away.name_cn} Elo", f"{away.elo_rating:.0f}")
                st.metric("FIFA 排名", f"#{away.fifa_rank}")
            with col3:
                st.metric("Elo 分差", f"{pred.elo_diff:+.0f}")
                st.metric("置信度", pred.confidence)


def stat_cards(today_count: int, predicted_count: int, total_count: int):
    """Top statistics cards row"""
    cols = st.columns(3)
    with cols[0]:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{today_count}</div><div class="stat-label">🏟️ 今日比赛</div></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{predicted_count}</div><div class="stat-label">🔮 已预测场次</div></div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{total_count}</div><div class="stat-label">📅 总比赛数</div></div>', unsafe_allow_html=True)


def team_selector(teams: list[Team], key: str = "team_select") -> Optional[Team]:
    """Team dropdown selector"""
    options = {f"{FLAG_MAP.get(t.fifa_code, '')} {t.name_cn} ({t.fifa_code})": t for t in teams}
    selected = st.selectbox("选择球队", list(options.keys()), key=key)
    return options.get(selected)


def footer():
    st.markdown('<div class="footer">🏆 2026 FIFA World Cup 预测系统 · 仅供娱乐参考 · 数据基于数学模型</div>', unsafe_allow_html=True)
