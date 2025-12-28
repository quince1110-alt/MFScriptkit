import streamlit as st
import google.generativeai as genai
import os

# --- 1. 页面基础设置 ---
st.set_page_config(
    page_title="女性成长爆款脚本工具",
    page_icon="🧘‍♀️",
    layout="centered"
)

# --- 2. 侧边栏：配置与说明 ---
with st.sidebar:
    st.header("⚙️ 设置")
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ 已自动加载 API Key")
    else:
        api_key = st.text_input("请输入 Google Gemini API Key", type="password")

    st.markdown("---")
    st.info("💡 **工具说明**：\n本工具基于【实见·Sissy】IP逻辑，专为女性成长赛道设计。")

# --- 3. 核心逻辑：定义 Sissy 的大脑 ---
# Gemini Pro 不支持 system_instruction 参数，所以我们把它定义为字符串，后面手动拼接
SYSTEM_PROMPT = """
你是由“实见”品牌打造的【Sissy IP·女性成长爆款策划专家】。
**IP Persona**: 真诚、通透、温柔的一刀、肉身解题。
**核心任务**:
1. 提炼3个“高认知觉醒”选题。
2. 撰写5步结构逐字稿（黄金开头/深度归因/认知翻转/正念解题/结尾引流）。
"""

# --- 4. 界面主区域 ---
st.title("🧘‍♀️ 女性成长爆款脚本工具")
st.caption("“痛苦源于认知的错位，解药在于当下的行动。”")

# 检查 API Key
if not api_key:
    st.warning("👈 请先在左侧侧边栏输入 API Key")
    st.stop()

# 配置 Gemini
try:
    genai.configure(api_key=api_key)
    
    # 🌟 修改点：使用最稳的 gemini-pro
    # 注意：这里去掉了 system_instruction 参数，防止报错
    model = genai.GenerativeModel("gemini-pro") 
    
except Exception as e:
    st.error(f"API Key 配置有误: {e}")

# 初始化 Session State
if "topics_text" not in st.session_state:
    st.session_state.topics_text = ""

# --- 模块一：输入资料 ---
st.subheader("Step 1: 输入灵感素材")
user_input = st.text_area(
    "在此粘贴行业研报、过往文案、或者一个核心概念：",
    height=150,
    placeholder="例如：关于‘35岁焦虑’的思考..."
)

# 生成选题按钮
if st.button("✨ 第一步：生成爆款选题", type="primary"):
    if not user_input:
        st.error("请先输入内容！")
    else:
        with st.spinner("Sissy 正在洞察人性..."):
            try:
                # 🌟 关键修改：手动把 Sissy 的人设拼接到用户输入前面
                full_prompt = f"{SYSTEM_PROMPT}\n\n【用户提供的资料】：\n{user_input}\n\n请基于以上资料生成3个爆款选题。"
                
                response = model.generate_content(full_prompt)
                st.session_state.topics_text = response.text
                st.success("选题已生成！")
            except Exception as e:
                st.error(f"生成失败: {e}")

# --- 模块二：展示选题 & 生成逐字稿 ---
if st.session_state.topics_text:
    st.markdown("---")
    st.subheader("Step 2: 确认选题")
    st.markdown(st.session_state.topics_text)
    
    st.markdown("---")
    st.subheader("Step 3: 生成口播逐字稿")
    
    selected_topic = st.text_input(
        "请复制你最满意的一个标题粘贴在这里：",
        placeholder="例如：《别在情绪里寻找答案》"
    )
    
    if st.button("📝 第二步：生成逐字稿"):
        if not selected_topic:
            st.error("请先填入标题！")
        else:
            with st.spinner("正在撰写逐字稿..."):
                try:
                    # 🌟 关键修改：同样手动拼接人设
                    script_prompt = f"{SYSTEM_PROMPT}\n\n用户选择了标题：【{selected_topic}】。\n请严格按照【实见·5步高转化结构】撰写口播逐字稿。"
                    
                    script_response = model.generate_content(script_prompt)
                    
                    st.markdown("### 🎬 最终逐字稿")
                    st.markdown(script_response.text)
                    st.balloons() 
                except Exception as e:
                    st.error(f"生成失败: {e}")
