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

# --- 3. 核心逻辑：提示词库 ---

# Sissy 的核心人设（公用）
CORE_PERSONA = """
你是由“实见”品牌打造的【Sissy IP·女性成长爆款策划专家】。
**IP Persona**: 真诚、通透、温柔的一刀、肉身解题。
**核心任务**: 辅助主理人 Sissy 输出“真诚流、高认知、肉身解题”的短视频内容。
"""

# 阶段一：选题生成提示词 (增加了格式要求，方便代码切割)
TOPIC_PROMPT_TEMPLATE = f"""
{CORE_PERSONA}
**任务**：基于用户资料，提炼 3 个具有“高认知觉醒+打破思维惯性”的选题。
**格式要求（非常重要）**：
请直接输出 3 个选题，**不要**加任何开场白或结束语。
**务必使用 '|||' 作为三个选题之间的分隔符**。
例如：
选题1标题：xxxx\n逻辑：xxxx
|||
选题2标题：xxxx\n逻辑：xxxx
|||
选题3标题：xxxx\n逻辑：xxxx
"""

# 阶段二：脚本生成提示词
SCRIPT_PROMPT_TEMPLATE = f"""
{CORE_PERSONA}
**任务**：严格遵循【实见·5步高转化结构】撰写口播逐字稿。
**结构要求**：
1. 🟢 黄金开头 (0-5秒)：撕开假象，建立共情。
2. 🟢 深度归因 (5-25秒)：心理学深度剖析。
3. 🟢 认知翻转 (25-40秒)：Sissy式“温柔一刀”，高维视角。
4. 🟢 正念解题 (40-55秒)：落地行动，物理性动作。
5. 🟢 结尾与引流 (55-60秒)：金句升华 + 强力钩子。
"""

# --- 4. 界面主区域 ---
st.title("🧘‍♀️ 女性成长爆款脚本工具")
st.caption("“痛苦源于认知的错位，解药在于当下的行动。”")

if not api_key:
    st.warning("👈 请先在左侧侧边栏输入 API Key")
    st.stop()

# 配置 Gemini
try:
    genai.configure(api_key=api_key)
    # 使用 gemini-flash-latest (免费且快)
    model = genai.GenerativeModel("gemini-flash-latest") 
except Exception as e:
    st.error(f"API Key 配置有误: {e}")

# --- Session State 初始化 ---
if "topics_list" not in st.session_state:
    st.session_state.topics_list = [] # 存储分割好的选题列表
if "current_script" not in st.session_state:
    st.session_state.current_script = "" # 存储生成的逐字稿
if "selected_topic_title" not in st.session_state:
    st.session_state.selected_topic_title = ""

# --- 模块一：输入资料 ---
st.subheader("Step 1: 输入灵感素材")
user_input = st.text_area(
    "在此粘贴资料：",
    height=100,
    placeholder="例如：关于‘35岁焦虑’的思考..."
)

if st.button("✨ 第一步：生成 3 个爆款选题", type="primary"):
    if not user_input:
        st.error("请先输入内容！")
    else:
        with st.spinner("Sissy 正在洞察人性..."):
            try:
                # 拼接提示词
                full_prompt = f"{TOPIC_PROMPT_TEMPLATE}\n\n【用户资料】：\n{user_input}"
                response = model.generate_content(full_prompt)
                
                # 处理返回结果，用 ||| 分割
                raw_text = response.text
                # 简单的清洗和分割
                topics = [t.strip() for t in raw_text.split("|||") if t.strip()]
                
                if len(topics) > 0:
                    st.session_state.topics_list = topics
                    st.session_state.current_script = "" # 清空旧脚本
                    st.success(f"成功生成 {len(topics)} 个选题！请在下方选择。")
                else:
                    st.error("生成格式有误，请重试。")
                    
            except Exception as e:
                st.error(f"生成失败: {e}")

# --- 模块二：点选生成 ---
if st.session_state.topics_list:
    st.markdown("---")
    st.subheader("Step 2: 点击按钮生成逐字稿")
    
    # 遍历显示 3 个选题，每个配一个按钮
    for index, topic_content in enumerate(st.session_state.topics_list):
        with st.container():
            # 使用卡片式布局
            st.info(f"**选题 {index + 1}**\n\n{topic_content}")
            
            # 这里的 key 必须唯一
            if st.button(f"📝 生成【选题 {index + 1}】的逐字稿", key=f"btn_topic_{index}"):
                st.session_state.selected_topic_title = f"选题 {index + 1}"
                with st.spinner(f"正在为【选题 {index + 1}】撰写逐字稿..."):
                    try:
                        script_prompt = f"{SCRIPT_PROMPT_TEMPLATE}\n\n用户选择了以下选题内容：\n{topic_content}"
                        script_response = model.generate_content(script_prompt)
                        st.session_state.current_script = script_response.text
                        st.rerun() # 强制刷新页面以显示结果
                    except Exception as e:
                        st.error(f"生成失败: {e}")

# --- 模块三：结果展示 & 提词器 ---
if st.session_state.current_script:
    st.markdown("---")
    st.subheader("Step 3: 逐字稿 & 提词器")
    
    # 选项卡：普通视图 vs 提词器视图
    tab1, tab2 = st.tabs(["📄 文稿预览", "📺 提词器模式"])
    
    with tab1:
        st.markdown(st.session_state.current_script)
        # 提供复制按钮 (Streamlit 尚无原生复制，用户需手动复制，这里仅展示文本)
    
    with tab2:
        st.warning("💡 提示：提词器模式下，背景为黑色，字体超大，适合录制时直接读取。")
        # 使用 HTML/CSS 实现提词器效果
        teleprompter_html = f"""
        <div style="
            background-color: black; 
            color: white; 
            font-size: 38px; 
            line-height: 1.6; 
            padding: 40px; 
            border-radius: 10px; 
            font-family: sans-serif;
            height: 600px;
            overflow-y: scroll;
        ">
            {st.session_state.current_script.replace(chr(10), '<br>')}
        </div>
        """
        st.components.v1.html(teleprompter_html, height=600, scrolling=True)
