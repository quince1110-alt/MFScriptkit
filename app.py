import streamlit as st
import google.generativeai as genai
import os

# --- 1. 页面基础设置 (SaaS 风格配置) ---
st.set_page_config(
    page_title="MF 灵感工作台",
    page_icon="💠", # 换成更有科技感的图标
    layout="centered"
)

# --- 2. 侧边栏：配置与系统信息 ---
with st.sidebar:
    st.header("💠 MF Workbench")
    st.caption("Content OS for Female Growth")
    
    st.markdown("---")
    
    # API Key 输入区
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ System Online / 系统已连接")
    else:
        api_key = st.text_input("🔑 API Key Access", type="password")

    st.markdown("---")
    
    # 🌟 修改点：去 IP 化，改用 SaaS 术语
    st.info("ℹ️ **System Specs / 系统说明**：\n\n本系统搭载专为**女性成长/疗愈赛道**训练的 `Cognitive-Model` (认知模型)。\n\n旨在通过高维视角，将平庸素材转化为具有穿透力的爆款脚本。")
    
    # 🌟 修改点：SaaS 风格页脚
    st.markdown("---")
    st.caption("© 2025 Scriptoolkit for MF · v1.0.2")
    st.caption("Powered by Gemini Flash & MF Logic")

# --- 3. 核心逻辑：提示词库 (隐形的大脑) ---

# 注意：虽然界面上去掉了 Sissy，但提示词里保留“人设逻辑”是为了保证输出质量。
# 我们把提示词里的称呼也稍微抽象化一点，改成“专家”。
CORE_PERSONA = """
**Role**: 你是专为女性成长赛道打造的【高维认知内容专家】。
**Tone**: 真诚、通透、温柔的一刀、肉身解题。
**Mission**: 辅助创作者输出“打破思维惯性、具备心理学深度”的短视频内容。
"""

# 阶段一：选题生成
TOPIC_PROMPT_TEMPLATE = f"""
{CORE_PERSONA}
**任务**：基于用户资料，提炼 3 个具有“高认知觉醒”的选题。
**格式要求（系统级指令）**：
请直接输出 3 个选题，不要加任何废话。
**必须使用 '|||' 作为分隔符**。
"""

# 阶段二：脚本生成
SCRIPT_PROMPT_TEMPLATE = f"""
{CORE_PERSONA}
**任务**：严格遵循【MF·5步高转化结构】撰写口播逐字稿。
**结构定义**：
1. 🟢 黄金开头 (Hook)：撕开假象，建立共情。
2. 🟢 深度归因 (Analysis)：心理学深度剖析。
3. 🟢 认知翻转 (Insight)：提出高维视角，打破常规。
4. 🟢 行为交付 (Action)：落地行动，物理性动作。
5. 🟢 结尾引流 (Close)：金句升华 + 钩子。
"""

# --- 4. 界面主区域 (SaaS 工作台风格) ---
st.title("💠 MF 灵感工作台")
st.markdown("**MF Workbench** · 专为女性成长赛道打造的内容操作系统")

if not api_key:
    st.warning("⚠️ Access Denied. Please input API Key in the sidebar.")
    st.stop()

# 配置 Gemini
try:
    genai.configure(api_key=api_key)
    # 依然使用最快最免费的 Flash
    model = genai.GenerativeModel("gemini-flash-latest") 
except Exception as e:
    st.error(f"System Error: {e}")

# --- Session State ---
if "topics_list" not in st.session_state:
    st.session_state.topics_list = []
if "current_script" not in st.session_state:
    st.session_state.current_script = ""
if "selected_topic_title" not in st.session_state:
    st.session_state.selected_topic_title = ""

# --- Module 1: Input Stream ---
st.markdown("### 1️⃣ Input Stream / 灵感输入")
user_input = st.text_area(
    "输入原始素材、研报摘要或核心概念：",
    height=100,
    placeholder="Waiting for input data..."
)

if st.button("🚀 Run Analysis / 生成认知选题", type="primary"):
    if not user_input:
        st.error("Input data is empty.")
    else:
        with st.spinner("Analyzing deep psychology patterns..."):
            try:
                full_prompt = f"{TOPIC_PROMPT_TEMPLATE}\n\n【Input Data】：\n{user_input}"
                response = model.generate_content(full_prompt)
                
                raw_text = response.text
                topics = [t.strip() for t in raw_text.split("|||") if t.strip()]
                
                if len(topics) > 0:
                    st.session_state.topics_list = topics
                    st.session_state.current_script = ""
                    st.success(f"Analysis Complete. {len(topics)} topics generated.")
                else:
                    st.error("Format Error. Please retry.")
                    
            except Exception as e:
                st.error(f"Runtime Error: {e}")

# --- Module 2: Selection & Generation ---
if st.session_state.topics_list:
    st.markdown("---")
    st.markdown("### 2️⃣ Select Logic / 选题决策")
    
    for index, topic_content in enumerate(st.session_state.topics_list):
        with st.container():
            st.info(f"**Topic 0{index + 1}**\n\n{topic_content}")
            if st.button(f"⚡ Generate Script (Topic 0{index + 1})", key=f"btn_topic_{index}"):
                st.session_state.selected_topic_title = f"Topic {index + 1}"
                with st.spinner("Synthesizing script with 5-Step Structure..."):
                    try:
                        script_prompt = f"{SCRIPT_PROMPT_TEMPLATE}\n\nSelected Topic:\n{topic_content}"
                        script_response = model.generate_content(script_prompt)
                        st.session_state.current_script = script_response.text
                        st.rerun()
                    except Exception as e:
                        st.error(f"Generation Error: {e}")

# --- Module 3: Output & Teleprompter ---
if st.session_state.current_script:
    st.markdown("---")
    st.markdown("### 3️⃣ Output / 交付与提词")
    
    tab1, tab2 = st.tabs(["📄 Script Preview", "📺 Teleprompter Mode"])
    
    with tab1:
        st.markdown(st.session_state.current_script)
    
    with tab2:
        st.caption("提示：提词器模式已激活 (Dark Mode)")
        teleprompter_html = f"""
        <div style="
            background-color: #0e1117; 
            color: #ffffff; 
            font-size: 38px; 
            line-height: 1.6; 
            padding: 40px; 
            border-radius: 10px; 
            font-family: sans-serif;
            height: 600px;
            overflow-y: scroll;
            border: 1px solid #303030;
        ">
            {st.session_state.current_script.replace(chr(10), '<br>')}
        </div>
        """
        st.components.v1.html(teleprompter_html, height=600, scrolling=True)
