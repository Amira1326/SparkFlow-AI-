import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الواجهة: Minimal & Clean
st.set_page_config(page_title="SparkFlow Luxury", page_icon="✨", layout="wide")

# تصميم CSS مخصص ليجعله يشبه تطبيقات الـ iOS الهادئة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; }
    
    .main { background-color: #FDFDFD; }
    
    /* ستايل البطاقة */
    .task-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #F1F1F1;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .task-card:hover { transform: translateY(-5px); }
    
    /* الأزرار */
    .stButton>button {
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    /* شريط الأولوية الجانبي */
    .p-urgent { border-left: 6px solid #FF5F5F; }
    .p-important { border-left: 6px solid #FFBD3F; }
    .p-normal { border-left: 6px solid #48BB78; }
    
    </style>
    """, unsafe_allow_html=True)

# العنوان بشكل مودرن
st.markdown("<h2 style='text-align: center; color: #4A4A4A; font-weight: 700;'>✨ SparkFlow Luxury</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #A0A0A0;'>مساحتك الهادئة للإنجاز</p>", unsafe_allow_html=True)

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# منطقة الإدخال بشكل مبسط جداً
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        new_task = st.text_input("", placeholder="ما هو هدفك القادم؟", label_visibility="collapsed")
    with col2:
        priority = st.selectbox("", ["عاجل 🔥", "مخطط له ⭐", "روتيني 🍃"], label_visibility="collapsed")
    
    if st.button("إضافة للمفكرة ✨"):
        if new_task:
            st.session_state.tasks.append({
                "task": new_task, "p": priority, "status": "active", "time": datetime.now().strftime("%I:%M")
            })
            st.rerun()

st.write("---")

# عرض المهام كبطاقات (Cards)
cols = st.columns(2)
for i, t in enumerate(st.session_state.tasks):
    if t['status'] == "active":
        p_class = "p-urgent" if "عاجل" in t['p'] else "p-important" if "مخطط" in t['p'] else "p-normal"
        with cols[i % 2]:
            st.markdown(f"""
            <div class="task-card {p_class}">
                <small style="color: #A0A0A0;">{t['time']}</small>
                <h4 style="color: #2D3748; margin-top: 5px;">{t['task']}</h4>
                <p style="color: #718096; font-size: 0.9em;">الفئة: {t['p']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            if c1.button("إتمام ✅", key=f"d_{i}"):
                st.session_state.tasks[i]['status'] = "done"
                st.rerun()
            if c2.button("حذف 🗑️", key=f"r_{i}"):
                st.session_state.tasks.pop(i)
                st.rerun()

# زر التقرير في الأسفل بشكل أنيق
if st.button("Generate Elegant Report 📄"):
    done_list = [t['task'] for t in st.session_state.tasks if t['status'] == "done"]
    if done_list:
        st.markdown("### 💌 تقريرك جاهز")
        report = "أنجزت اليوم بكل هدوء:\n" + "\n".join([f"• {item}" for item in done_list])
        st.text_area("", report, height=150)
