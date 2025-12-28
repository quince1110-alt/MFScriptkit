import streamlit as st
import google.generativeai as genai
import sys

st.set_page_config(page_title="模型自检工具", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ 谷歌 Gemini 模型自检工具")

# 1. 检查 Python 环境里的工具包版本
# 如果这个版本低于 0.7.0，说明 Streamlit 根本没更新成功，gemini-1.5-flash 就肯定用不了。
try:
    import google.generativeai
    version = google.generativeai.__version__
    st.info(f"📦 当前 google-generativeai 库版本: **{version}**")
except Exception as e:
    st.error(f"无法获取库版本: {e}")

# 2. 配置 API Key
with st.sidebar:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ 已加载 Secret Key")
    else:
        api_key = st.text_input("输入 API Key", type="password")

# 3. 列出所有可用模型
if st.button("🔍 开始扫描可用模型", type="primary"):
    if not api_key:
        st.error("请先输入 API Key！")
    else:
        try:
            genai.configure(api_key=api_key)
            
            st.write("正在连接 Google 服务器查询...")
            
            # 获取所有模型列表
            models = list(genai.list_models())
            
            found_flash = False
            found_pro = False
            
            st.markdown("### 📋 您的账号可用的模型列表：")
            
            # 遍历打印
            model_names = []
            for m in models:
                # 只显示支持生成文本的模型
                if 'generateContent' in m.supported_generation_methods:
                    model_names.append(m.name)
                    st.text(f"✅ {m.name}")
                    
                    if "gemini-1.5-flash" in m.name:
                        found_flash = True
                    if "gemini-pro" in m.name:
                        found_pro = True
            
            st.markdown("---")
            st.subheader("诊断结果：")
            
            if found_flash:
                st.success("🎉 太棒了！检测到 `models/gemini-1.5-flash`！\n\n👉 您可以使用 1.5 Flash 模型，请把代码里的 `model_name` 改为 `gemini-1.5-flash`。")
            elif found_pro:
                st.warning("⚠️ 没找到 Flash，但找到了 `models/gemini-pro`。\n\n👉 您的账号或环境可能暂时不支持 Flash，请把代码里的 `model_name` 改为 `gemini-pro`。")
            else:
                st.error("❌ 一个能用的 Gemini 模型都没找到！请检查 API Key 是否开通了权限，或者是否欠费。")
                
        except Exception as e:
            st.error(f"❌ 连接失败，报错信息：\n{e}")
