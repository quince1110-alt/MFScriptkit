import streamlit as st
import google.generativeai as genai
import os

# --- 1. 页面基础设置 (SaaS 风格配置) ---
st.set_page_config(
    page_title="MF 灵感工作台",
    page_icon="💠", 
    layout="centered"
)

# --- 2. 侧边栏：核心验证逻辑 ---
with st.sidebar:
    st.header("💠 MF Workbench")
    st.caption("Content OS for Female Growth")
    st.markdown("---")
    
    # ==========================================
    # 🔐 身份验证模块 (Secrets版)
    # ==========================================
    
    # 初始化 session_state
    if "auth_status" not in st.session_state:
        st.session_state.auth_status = False

    # A. 如果未登录 -> 显示输入框
    if not st.session_state.auth_status:
        st.info("🔒 System Locked / 系统已锁定")
        user_kami = st.text_input("Access Code / 卡密验证", type="password", placeholder="请输入您的 VIP 卡密")
        
        if st.button("🚀 Verify & Login / 验证"):
            # 【关键修改】从 secrets 读取卡密列表
            # 兼容性处理：防止 secrets 里没配报错
            try:
                # 获取配置中的卡密字符串，并按逗号分割成列表
                valid_codes = st.secrets["access_codes"]["valid_list"]
                # 简单的去空格处理
                valid_codes = [code.strip() for code in valid_codes.split(",")]
                
                if user_kami.strip() in valid_codes:
                    st.session_state.auth_status = True
                    st.toast("✅ 验证成功！欢迎回来。", icon="🎉")
                    st.rerun()
                else:
                    st.error("❌ 无效的卡密 (Invalid Access Code)")
            except Exception as e:
                st.error("⚠️ 系统配置缺失，请联系管理员检查 secrets.toml")
        
        # ⛔️ 强制阻断：未登录时不加载后续代码
        st.markdown("---")
        st.caption("Protected by MF Cognitive System")
        st.stop() 

    # B. 如果已登录 -> 显示用户信息和登出按钮
    else:
        st.success("✅ System Online / 已连接")
        if st.button("Log out / 退出登录"):
            st.session_state.auth_status = False
            st.rerun()
        
        # 读取 API Key (登录后才加载，省钱又安全)
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        else:
            st.error("⚠️ API Key Not Found in Secrets")
            st.stop()

    st.markdown("---")
    st.info("ℹ️ **System Specs**：\n\n搭载 `Cognitive-Model` (认知模型)，辅助输出高维女性成长内容。")
    st.markdown("---")
    st.caption("© 2025 Scriptoolkit for MF · v1.0.3")

# --- 3. 核心逻辑：提示词库 ---
CORE_PERSONA = """
**Role**: 你是专为女性成长赛道打造的【高维认知内容专家】。
**Tone**: 真诚、通透、温柔的一刀、肉身解题。
**Mission**: 辅助创作者输出“打破思维惯性、具备心理学深度”的短视频内容。
"""

TOPIC_PROMPT_TEMPLATE = f"""
{CORE_PERSONA}
**任务**：基于用户资料，提炼 3 个具有“高认知觉醒”的选题。
**格式要求**：直接输出 3 个选题，用 '|||' 分隔。
"""

SCRIPT_PROMPT_TEMPLATE = f"""
{CORE_PERSONA}
**任务**：遵循【MF·5步高转化结构】撰写口播逐字稿。
1. Hook (撕开假象)
2. Analysis (深度归因)
3. Insight (认知翻转)
4. Action (行为交付)
5. Close (结尾引流)
"""

# --- 4. 界面主区域 ---
st.title("💠 MF 灵感工作台")
st.markdown("**MF Workbench** · 专为女性成长赛道打造的内容操作系统")

# 配置 Gemini
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-flash-latest") 
except Exception as e:
    st.error(f"System Error: {e}")

# 初始化状态
if "topics_list" not in st.session_state: st.session_state.topics_list = []
if "current_script" not in st.session_state: st.session_state.current_script = ""

# --- Module 1: Input ---
st.markdown("### 1️⃣ Input Stream / 灵感输入")
user_input = st.text_area("输入原始素材、研报摘要或核心概念：", height=100)

if st.button("🚀 Run Analysis / 生成认知选题", type="primary"):
    if not user_input:
        st.warning("Input is empty.")
    else:
        with st.spinner("Analyzing deep psychology patterns..."):
            try:
                full_prompt = f"{TOPIC_PROMPT_TEMPLATE}\n\n【Input】\n{user_input}"
                response = model.generate_content(full_prompt)
                topics = [t.strip() for t in response.text.split("|||") if t.strip()]
                if topics:
                    st.session_state.topics_list = topics
                    st.success(f"Analysis Complete. {len(topics)} topics generated.")
            except Exception as e:
                st.error(f"Error: {e}")

# --- Module 2: Selection ---
if st.session_state.topics_list:
    st.markdown("---")
    st.markdown("### 2️⃣ Select Logic / 选题决策")
    for i, topic in enumerate(st.session_state.topics_list):
        with st.container():
            st.info(f"**Topic 0{i+1}**\n\n{topic}")
            if st.button(f"⚡ Generate Script (Topic 0{i+1})", key=f"btn_{i}"):
                with st.spinner("Synthesizing script..."):
                    try:
                        s_prompt = f"{SCRIPT_PROMPT_TEMPLATE}\n\nSelected:\n{topic}"
                        res = model.generate_content(s_prompt)
                        st.session_state.current_script = res.text
                        st.rerun()
                    except Exception as e: st.error(e)

# --- Module 3: Output ---
if st.session_state.current_script:
    st.markdown("---")
    st.markdown("### 3️⃣ Output / 交付与提词")
    tab1, tab2 = st.tabs(["📄 Script", "📺 Teleprompter"])
    with tab1: st.markdown(st.session_state.current_script)
    with tab2:
        html = f"""<div style="background:#0e1117;color:#fff;font-size:38px;padding:40px;height:600px;overflow-y:scroll;">{st.session_state.current_script.replace(chr(10), '<br>')}</div>"""
        st.components.v1.html(html, height=600)
