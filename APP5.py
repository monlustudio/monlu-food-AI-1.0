import streamlit as st
import google.generativeai as genai
import PIL.Image
import io

# --- 1. 密碼驗證邏輯 ---
def check_password():
    """驗證密碼，成功回傳 True"""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # 登入介面樣式
    st.markdown("""
        <style>
        .login-box {
            background-color: #1E2B24; padding: 40px; border-radius: 15px;
            border: 1px solid #C5A47E; text-align: center; color: #F1F3F2;
        }
        .stApp { background-color: #2D4035; }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color:#F1F3F2;">🏯 夢廬系統登入</h3>', unsafe_allow_html=True)
        pwd = st.text_input("請輸入授權密碼", type="password")
        if st.button("驗證登入"):
            if pwd == "11090801":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("密碼錯誤，請聯繫管理員。")
        st.markdown('</div>', unsafe_allow_html=True)
    return False

# 執行驗證
if not check_password():
    st.stop()

# --- 2. 核心設定 ---
try:
    # 優先從 Secrets 讀取，若無則報錯
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("❌ 未偵測到 API 金鑰。請在 Secrets 中設定 GEMINI_API_KEY")
    st.stop()

# 頁面標題與佈局設定
st.set_page_config(page_title="夢廬 | AI 美食攝影生成助手", layout="wide", page_icon="🍽️")

# --- 3. 品牌色彩注入 (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #2D4035; color: #F1F3F2; }
    h1, h2, h3, h4, h5, h6, p, span, label { color: #F1F3F2 !important; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #1E2B24 !important;
        color: #FFFFFF !important;
        border: 1px solid #C5A47E !important;
    }
    ::placeholder { color: #A0B0A6 !important; opacity: 1; }
    div.stButton > button:first-child {
        background-color: #C5A47E !important;
        color: #2D4035 !important;
        border-radius: 5px;
        font-weight: bold; border: none; width: 100%; height: 3.5em; font-size: 1.1rem;
    }
    [data-testid="stSidebar"] { background-color: #1A261F !important; }
    .image-card {
        border: 2px solid #C5A47E; border-radius: 10px; padding: 15px;
        background-color: #1E2B24; margin-top: 20px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 側邊欄
st.sidebar.markdown("# 🏯 夢廬攝影工作室")
st.sidebar.markdown("### 專業 AI 視覺生成系統")
st.sidebar.success("🔑 系統已授權登入")

st.title("🍽️ 夢廬：專業美食攝影生成助手")
st.caption("品牌專屬視覺生成系統 | 用美學邏輯驅動 AI 直接生成影像")
st.markdown("---")

# 1-3 基礎品牌與餐點
st.header("🏢 階段一：品牌與產品基礎")
col_base1, col_base2 = st.columns(2)
with col_base1:
    brand_name = st.text_input("1. 品牌名稱", placeholder="例如：夢廬食堂...")
    restaurant_type = st.text_input("2. 餐廳類型", placeholder="例如：私廚、餐酒館...")
    
    # 擴展多元品牌特性
    brand_style_list = [
        "中式 (港式/台式/川菜)", "日式 (和食/居酒屋/壽司)", "西式 (義式/美式/法式)", 
        "東南亞 (泰式/越式/印尼)", "韓式料理", "地中海/歐式", "南美/墨西哥", 
        "中東料理", "北歐風", "印度料理", "甜點/下午茶", "精品咖啡/茶飲", "其他"
    ]
    brand_style = st.selectbox("3. 品牌特性", brand_style_list)
    
    other_style = ""
    if "其他" in brand_style:
        other_style = st.text_input("🔍 請輸入其他料理類型", placeholder="例如：分子料理、融合菜...")

with col_base2:
    food_detail = st.text_area("✨ 生成的餐點內容 (詳細描述)", placeholder="例如：白醬義大利麵，醬油拉麵，玉米濃湯...")

st.markdown("---")

# 尺寸與類型選擇
st.header("📐 階段二：照片規格與類型")
col_spec1, col_spec2 = st.columns(2)
with col_spec1:
    aspect_ratio = st.radio("選擇照片比例", ["直式 (3:5)", "橫式 (16:9)", "正方形 (1:1)"], horizontal=True)
with col_spec2:
    photo_type = st.radio("照片構圖類型", ["單品情境 (聚焦主體)", "組合情境 (豐富擺盤)", "職人作畫 (帶入動作感)", "品牌形象 (帶入空間與質感)"], horizontal=True)

st.markdown("---")

# 人物設定
st.header("🤝 階段三：人物設定")
col_human1, col_human2 = st.columns(2)
with col_human1:
    human_presence = st.selectbox("人物出現程度", ["不要人物", "僅手部動作", "模糊背景人物", "側身互動 (職人擺盤)", "雙手奉上", "用餐中的模特兒"])

human_action = "無特定動作"
if human_presence == "僅手部動作":
    with col_human2:
        human_action = st.selectbox("👉 請選擇手部具體動作", ["正在淋醬汁 / 擠檸檬", "正在用叉子/筷子夾起食物", "正在撒下調味料 / 糖粉", "手持餐具準備開動", "拿著食物", "正在用刀切開食物", "手指輕觸盤緣 (微調位置)"])
else:
    with col_human2:
        st.write("ℹ️ 此模式下將由 AI 自動分配人物姿態。")

st.markdown("---")

# 風格、氛圍與配色
st.header("🎨 階段四：風格與配色定位")
col_vibe1, col_vibe2 = st.columns(2)
with col_vibe1:
    color_style = st.radio("選擇色彩風格", ["暗色系 (Moody)", "亮色系 (Bright)", "中色系 (Neutral)"], horizontal=True)
    overall_color = st.text_input("🎨 整體配色要求", placeholder="例如：深灰色、深綠色、低彩度莫蘭迪色...")
with col_vibe2:
    vibes = st.multiselect("選擇氛圍 (可複選)", ["鮮明、色彩豐富", "低調", "靜謐感", "簡約", "時尚", "文藝氣息", "人情味", "傳統", "現代", "熱鬧", "古樸", "高級", "親民", "奢華", "浮誇", "手作感", "鄉村風"])

st.markdown("---")

# 💡 階段五：光影與構圖設定
st.header("💡 階段五：光影與構圖設定")
col_l1, col_l2, col_l3 = st.columns([1, 1, 2])
with col_l1:
    light_quality = st.radio("A. 光線質地", ["柔光 (Soft)", "硬光 (Hard)"], horizontal=True)
with col_l2:
    light_pos = st.selectbox("B. 光線位置", ["側頂光 🔥", "逆頂光 🔥", "側逆頂光 ⭐", "側光", "逆光", "側逆光", "頂光", "側順光"])
with col_l3:
    angle = st.select_slider("C. 拍攝角度", options=["水平", "30度", "45度", "60度", "俯拍"])

st.markdown("---")

# 環境與器皿材質
st.header("🧱 階段六：環境與器皿材質")
col_env1, col_env2, col_env3 = st.columns(3)

# 邏輯判斷：如果是俯拍，背景預設為無
wall_options = ["木頭", "大理石", "布 (掛布)", "窗簾", "窗戶 (帶自然光)", "石膏", "金屬","塑膠","粉刷", "磁磚", "植物", "無"]
default_wall = "無" if angle == "俯拍" else "粉刷"

with col_env1:
    table_mat = st.selectbox("桌面材質", ["木頭", "大理石", "布 (桌巾/襯布)", "石膏", "粉刷", "岩石", "金屬","塑膠", "玻璃", "磁磚", "陶瓷", "水泥"])
    # 新增顏色選擇器
    table_color_hex = st.color_picker("桌面主色調", "#4A3728") 
    table_color_desc = st.text_input("桌面顏色詳細描述", placeholder="例如：胡桃木、深厚紋理...")
    # 組合顏色資訊供後續提詞使用
    table_color = f"{table_color_hex} ({table_color_desc})" if table_color_desc else table_color_hex

with col_env2:
    wall_mat = st.selectbox("背景材質 (俯拍時自動設為無)", wall_options, index=wall_options.index(default_wall))
    # 新增顏色選擇器
    wall_color_hex = st.color_picker("背景主色調", "#00416b")
    wall_color_desc = st.text_input("背景顏色詳細描述", placeholder="例如：米白色or紋理強烈...")
    # 組合顏色資訊
    wall_color = f"{wall_color_hex} ({wall_color_desc})" if wall_color_desc else wall_color_hex

with col_env3:
    ware_mat = st.selectbox("器皿材質", ["陶器 (手作質感)", "瓷器 (精緻亮面)", "玻璃 (通透反射)", "金屬 (冷冽感)", "木質 (自然感)", "塑膠", "琺瑯", "無"])
    wall_color_hex = st.color_picker("器皿色調", "#63676d")
    ware_detail = st.text_input("器皿細節描述", placeholder="例如：霧面 方形盤...")

st.markdown("---")






# 備註
st.header("📝 階段七：額外敘事備註")
extra_note = st.text_area("補充畫面細節", placeholder="例如：桌上有凌亂的餐巾、光線營造出孤獨感...")

st.divider()

# --- 5. 生成邏輯 ---
if st.button("🚀 開始夢廬影像生成", type="primary", use_container_width=True):
    if not brand_name or not food_detail:
        st.error("❌ 請填寫品牌名稱與餐點內容！")
    else:
        # 構建 夢廬專業格式提詞
        clean_light_pos = light_pos.replace(" 🔥", "").replace(" ⭐", "")
        vibe_tags = "、".join(vibes)
        final_style = other_style if brand_style == "其他" else brand_style
        ratio_dict = {"直式 (3:5)": "3:5", "橫式 (16:9)": "16:9", "正方形 (1:1)": "1:1"}
        ratio = ratio_dict[aspect_ratio]
        
        # 組合提詞
        full_prompt = (
            f"專業美食攝影提案（由夢廬攝影師定義）：\n"
            f"品牌：{brand_name} | 料理類型：{final_style}\n"
            f"【視覺參數】：比例 {ratio} | 視角 {angle} | 光學：{clean_light_pos}的{light_quality}\n"
            f"【場景構建】：{food_detail}。背景為{wall_color}{wall_mat}，桌面為{table_color}{table_mat}。\n"
            f"【質感細節】：使用{ware_detail}{ware_mat}。氛圍強調「{vibe_tags}」，配色為「{overall_color}」。\n"
            f"【動態與人】：{human_presence}，執行「{human_action}」。\n"
            f"【敘事備註】：{extra_note}。\n"
            f"請根據以上專業規格，生成一張 8k 超寫實、具備商業大片畫質的作品。\n"
            f"⚠️ 重要指令：請直接輸出影像 Blob 數據，嚴禁輸出任何文字、描述或解釋。"
        )

        try:
            with st.spinner("🎨 夢廬 AI 正根據您的提案渲染影像，請稍候..."):
                # 初始化模型
                model = genai.GenerativeModel('gemini-3.1-flash-image-preview')
                
                # 發送請求
                response = model.generate_content(full_prompt)
                
                # 過濾並搜尋影像數據
                found_image = False
                if response.candidates:
                    for part in response.candidates[0].content.parts:
                        # 檢查是否為 inline_data 且 mime_type 是圖片
                        if hasattr(part, 'inline_data') and part.inline_data:
                            img_data = part.inline_data.data
                            image = PIL.Image.open(io.BytesIO(img_data))
                            
                            st.markdown('<div class="image-card">', unsafe_allow_html=True)
                            st.subheader("📸 夢廬提案渲染結果")
                            st.image(image, caption=f"【{brand_name}】專屬視覺提案", use_container_width=True)
                            
                            # 提供下載
                            buf = io.BytesIO()
                            image.save(buf, format="PNG")
                            st.download_button("💾 下載 PNG 影像", buf.getvalue(), f"{brand_name}_proposal.png", "image/png")
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            found_image = True
                            st.success("✅ 影像渲染成功！")
                            break
                
                if not found_image:
                    st.warning("⚠️ 模型回傳了非影像內容。")
                    with st.expander("查看 AI 回饋 (可能為安全過濾或文字回覆)"):
                        st.write(response.text)

        except Exception as e:
            st.error(f"❌ 渲染過程發生錯誤: {e}")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 夢廬工作室 | 版權所有")
