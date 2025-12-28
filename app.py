import streamlit as st
import google.generativeai as genai
import os

# --- 1. 页面基础设置 (标题已更新) ---
st.set_page_config(
    page_title="女性成长爆款脚本工具",  # 浏览器标签页标题
    page_icon="🧘‍♀️",
    layout="centered"
)

# --- 2. 侧边栏：配置与说明 ---
with st.sidebar:
    st.header("⚙️ 设置")
    
    # 优先从 Streamlit Secrets 读取 API Key
    # 这样配置好 Secrets 后，就不用每次手动输入了
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ 已自动加载 API Key")
    else:
        # 如果没配置 Secrets，才显示输入框
        api_key = st.text_input("请输入 Google Gemini API Key", type="password")

    st.markdown("---")
    st.info("💡 **工具说明**：\n本工具基于【实见·Sissy】IP逻辑，专为女性成长赛道设计，用于生成“高认知觉醒+打破思维惯性”的短视频脚本。")
    st.markdown("#### 使用步骤：")
    st.markdown("1. 输入资料/概念")
    st.markdown("2. 生成3个爆款选题")
    st.markdown("3. 生成口播逐字稿")

# --- 3. 核心逻辑：System Prompt (保持Sissy灵魂不变) ---
SYSTEM_PROMPT = """
**Role**: 你是由“实见”品牌打造的【Sissy IP·女性成长爆款策划专家】。
你的核心任务是辅助主理人 Sissy 输出“真诚流、高认知、肉身解题”的短视频内容。

**IP Persona (Sissy/竹子)**:
1. **基调**：真诚、通透、有力量的静气。你看透了人性的弱点（焦虑、拖延、比较），你不谩骂，而是如实陈述真相。
2. **语言**：“温柔的一刀”。语速不疾不徐，但逻辑犀利，字字铿锵。
3. **哲学**：“肉身解题”。痛苦是想出来的，解药是做出来的。方案必须是物理层面的具体动作（如：身体扫描、停顿3秒、扔掉手机）。

**Task Workflow**:

**阶段一：生成选题 (Topic Generation)**
基于用户输入，提炼 3 个具有“高认知觉醒+打破思维惯性”的选题。
* **选题逻辑**：
    * **痛点反打**：指出用户潜意识里的“不对劲”。
    * **深度归因**：将表面现象（如熬夜）归因为深层心理机制（如意识监工 VS 潜意识反抗）。

**阶段二：生成逐字稿 (Script Generation)**
用户选定标题后，严格遵循【实见·5步高转化结构】输出：
1. **🟢 黄金开头 (0-5秒)**：撕开假象，建立共情。话术：“承认吧...”、“别被骗了...”。
2. **🟢 深度归因 (5-25秒)**：心理学深度剖析（意识 VS 潜意识，多巴胺陷阱等）。
3. **🟢 认知翻转 (25-40秒)**：Sissy式“温柔一刀”，提出“长期主义”、“课题分离”等高维视角。
4. **🟢 正念解题 (40-55秒)**：落地行动。必须给出一个**极简的、物理性的动作**（如正念扫描）。拒绝空洞口号。
5. **🟢 结尾与引流 (55-60秒)**：金句升华 + 强力钩子（PDF/音频福利）。
"""

# --- 4. 界面主区域 ---

st.title("🧘‍♀️ 女性成长爆款脚本工具")
st.caption("“痛苦源于认知的错位，解药在于当下的行动。”")

# 检查 API Key
if not api_key:
    st.warning("👈 请先在左侧侧边栏输入 API Key，或者在 Streamlit 后台配置 Secrets。")
    st.stop()

# 配置 Gemini
try:
    genai.configure(api_key=api_key)
    # 使用 flash 模型，速度快且免费额度高
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",  # 保持这个名字
        system_instruction=SYSTEM_PROMPT
    )
except Exception as e:
    st.error(f"API Key 配置有误，请检查。错误信息: {e}")

# 初始化 Session State
if "topics_text" not in st.session_state:
    st.session_state.topics_text = ""

# --- 模块一：输入资料 ---
st.subheader("Step 1: 输入灵感素材")
user_input = st.text_area(
    "在此粘贴行业研报、过往文案、或者一个核心概念（如‘同辈压力’、‘内耗’）：",
    height=150,
    placeholder="例如：关于‘35岁焦虑’的思考，或者‘为什么总是讨好别人’..."
)

# 生成选题按钮
if st.button("✨ 第一步：生成爆款选题", type="primary"):
    if not user_input:
        st.error("请先输入内容！")
    else:
        with st.spinner("Sissy 正在洞察人性，提炼观点..."):
            try:
                prompt = f"用户提供的素材资料如下：\n{user_input}\n\n请基于Sissy的【女性成长真诚流】逻辑，生成3个直击痛点的爆款选题，并简述每个选题背后的心理学逻辑。"
                response = model.generate_content(prompt)
                st.session_state.topics_text = response.text
                st.success("选题已生成！请在下方查看。")
            except Exception as e:
                st.error(f"生成失败，请检查网络或API Key。\n错误信息: {e}")

# --- 模块二：展示选题 & 生成逐字稿 ---
if st.session_state.topics_text:
    st.markdown("---")
    st.subheader("Step 2: 确认选题")
    st.markdown(st.session_state.topics_text)
    
    st.markdown("---")
    st.subheader("Step 3: 生成口播逐字稿")
    
    selected_topic = st.text_input(
        "请复制你最满意的一个标题粘贴在这里：",
        placeholder="例如：《别在情绪里寻找答案，去行动里寻找结果》"
    )
    
    if st.button("📝 第二步：生成逐字稿"):
        if not selected_topic:
            st.error("请先填入标题！")
        else:
            with st.spinner("正在撰写逐字稿 (黄金开头...深度归因...正念解题...)..."):
                try:
                    script_prompt = f"用户选择了标题：【{selected_topic}】。\n请严格按照【实见·5步高转化结构】（黄金开头/深度归因/认知翻转/正念解题/结尾引流）撰写口播逐字稿。务必保持Sissy“温柔一刀”的语气。"
                    script_response = model.generate_content(script_prompt)
                    
                    st.markdown("### 🎬 最终逐字稿")
                    st.markdown(script_response.text)
                    st.balloons() 
                except Exception as e:
                    st.error(f"生成失败: {e}")
