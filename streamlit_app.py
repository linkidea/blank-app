import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io
import numpy as np


def create_scene_image(scene_type, size=(800, 500)):
    """Create scene-specific illustration"""
    img = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(img)
    if scene_type == "contract":
        # 계약 체결 장면
        draw.rectangle([300, 200, 500, 300], fill='lightblue')  # 문서
        draw.line([350, 250, 450, 250], fill='black', width=3)  # 서명
        draw.rectangle([200, 150, 250, 200], fill='brown')  # 도장
    elif scene_type == "office":
        # 사무실 장면
        draw.rectangle([100, 200, 700, 400], fill='beige')  # 책상
        draw.rectangle([300, 100, 500, 180], fill='lightgray')  # 모니터
        draw.rectangle([380, 180, 420, 200], fill='gray')  # 모니터 받침대
    elif scene_type == "factory":
        # 공장 장면
        draw.polygon([(300, 100), (500, 100), (600, 200), (200, 200)], fill='gray')  # 지붕
        draw.rectangle([200, 200, 600, 400], fill='lightgray')  # 건물
        draw.rectangle([350, 300, 450, 400], fill='brown')  # 문
    elif scene_type == "court":
        # 법정 장면
        draw.rectangle([300, 100, 500, 200], fill='brown')  # 재판석
        draw.ellipse([380, 50, 420, 90], fill='black')  # 머리
        draw.rectangle([350, 90, 450, 150], fill='black')  # 법복
    elif scene_type == "money":
        # 금전적 손실 장면
        draw.rectangle([200, 200, 300, 250], fill='green')  # 지폐
        draw.text((220, 215), "$", fill='gold', font=ImageFont.load_default())
        draw.line([400, 150, 350, 250], fill='red', width=3)  # 하락 그래프
    elif scene_type == "lesson":
        # 교훈 장면
        draw.ellipse([350, 150, 450, 250], fill='yellow')  # 전구
        draw.rectangle([390, 250, 410, 300], fill='gray')  # 전구 받침
    return img


def main():
    st.set_page_config(page_title="PE 품질 사건 카드뉴스", layout="wide")

    # Custom CSS
    st.markdown("""
<style>
        .stButton button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border-radius: 5px;
        }
        .card {
            padding: 20px;
            border-radius: 15px;
            background-color: white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        .chapter-title {
            color: #1E88E5;
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
        .scene-content {
            font-size: 20px;
            line-height: 1.8;
            margin: 15px 0;
        }
</style>
    """, unsafe_allow_html=True)

    # 카드뉴스 내용
    stories = [
        {
            "chapter": "제1화: 계약의 시작",
            "scenes": [
                {
                    "title": "KTH사 사무실",
                    "content": [
                        "KTH사 대표: '드디어! 미국의 대형 플라스틱 제조업체와 큰 계약을 체결했어!'",
                        "직원들: '와, 정말 대단해요! 축하드립니다!'"
                    ],
                    "image_type": "contract"
                },
                {
                    "title": "미국의 대형 플라스틱 제조업체 사무실",
                    "content": [
                        "미국 제조업체 대표: 'KTH사와의 계약 덕분에 우리도 고품질의 PE를 안정적으로 공급받을 수 있게 되었어.'"
                    ],
                    "image_type": "office"
                }
            ]
        },
        {
            "chapter": "제2화: 비용 절감의 유혹",
            "scenes": [
                {
                    "title": "KTH사 사무실",
                    "content": [
                        "KTH사 대표: '비용을 좀 더 절감할 수 있는 방법이 없을까?'",
                        "직원 A: '저렴한 PE를 구매하면 비용을 절감할 수 있을 것 같습니다.'"
                    ],
                    "image_type": "money"
                }
            ]
        },
        # ... 나머지 챕터들 계속
    ]

    # Session state 초기화
    if 'current_chapter' not in st.session_state:
        st.session_state.current_chapter = 0
    if 'current_scene' not in st.session_state:
        st.session_state.current_scene = 0

    # 현재 챕터와 장면
    current_story = stories[st.session_state.current_chapter]
    current_scene = current_story["scenes"][st.session_state.current_scene]

    # 카드 내용 표시
    col1, col2 = st.columns([2, 3])
    with col1:
        # 이미지 표시
        scene_image = create_scene_image(current_scene["image_type"])
        st.image(scene_image, use_column_width=True)

    with col2:
        st.markdown(f'<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="chapter-title">{current_story["chapter"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<h3>{current_scene["title"]}</h3>', unsafe_allow_html=True)
        for line in current_scene["content"]:
            st.markdown(f'<div class="scene-content">{line}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 네비게이션 버튼
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("◀ 이전") and (st.session_state.current_scene > 0 or st.session_state.current_chapter > 0):
            if st.session_state.current_scene > 0:
                st.session_state.current_scene -= 1
            else:
                st.session_state.current_chapter -= 1
                st.session_state.current_scene = len(stories[st.session_state.current_chapter]["scenes"]) - 1
            st.experimental_rerun()

    with col3:
        if st.button("다음 ▶") and (st.session_state.current_scene < len(current_story["scenes"]) - 1 or
                                  st.session_state.current_chapter < len(stories) - 1):
            if st.session_state.current_scene < len(current_story["scenes"]) - 1:
                st.session_state.current_scene += 1
            else:
                st.session_state.current_chapter += 1
                st.session_state.current_scene = 0
            st.experimental_rerun()

    # 진행 상황 표시
    total_scenes = sum(len(story["scenes"]) for story in stories)
    current_progress = sum(len(stories[i]["scenes"]) for i in range(st.session_state.current_chapter))
    current_progress += st.session_state.current_scene + 1
    st.progress(current_progress / total_scenes)
    st.text(f"진행 상황: {current_progress} / {total_scenes}")


if __name__ == "__main__":
    main()
