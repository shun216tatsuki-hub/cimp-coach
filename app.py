import streamlit as st
import google.generativeai as genai

# 設定は一番上
st.set_page_config(page_title="CIMP AI Coach", layout="centered")

# CSSをここに集約
st.markdown("""
    <style>
    /* 1. 全ての邪魔な要素をクラス名の一部指定で抹殺 */
    [class*="viewerBadge"],
    [class*="profileContainer"],
    [class*="profilePreview"],
    [class*="StyledFooter"],
    a[href*="streamlit.io/cloud"] {
        display: none !important;
        opacity: 0 !important;
        visibility: hidden !important;
        height: 0 !important;
        pointer-events: none !important;
    }

    /* 2. フッター（Made with Streamlit）を完全に消す */
    footer {
        display: none !important;
    }

    /* 3. ヘッダー（右上の三本線とか）を消す */
    header {
        visibility: hidden;
        height: 0;
    }
    
    /* 4. アプリ下の余白を詰める */
    .main .block-container {
        padding-bottom: 0rem !important;
    }
    </style>
    """, unsafe_allow_html=True)　
st.title("🎓 CIMP AI Marking")
st.write("Grade your work and gives you advice to achieve higher grade!")

# 【変更点】サイトの裏側（Secrets）から、君のAPIキーをこっそり読み込む
# 友達にはキーの入力欄は見えない！
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.subheader("1. Upload your Rubic")
rubric_file = st.file_uploader("File or Image", type=['pdf', 'png', 'jpg'])

st.subheader("2. Upload your Work")
assignment_text = st.text_area("Paste your work here", height=200)

if st.button("Submit"):
    if rubric_file and assignment_text:
        with st.spinner("Marking"):
            prompt = f"""
            You are a strict CIMP (Canadian International Matriculation Programme) grader.
            1. Read the attached Rubric.
            2. Analyze this student's assignment: {assignment_text}
            3. Grade it based on K (Knowledge), I (Inquiry), C (Communication), A (Application).
            4. Tell the student exactly what to fix to get Level 4 (80%+). Be strict but constructive.
            """
            response = model.generate_content([prompt, rubric_file])
            st.markdown("### 📝Feedback")
            st.write(response.text)
    else:
        st.warning("Submit Both Rubic and your Works!")
