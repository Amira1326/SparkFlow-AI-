import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os
import time

# إعداد واجهة المستخدم (Professional & Minimal)
st.set_page_config(page_title="SparkFlow Pro | Kids Gate", page_icon="✨", layout="centered")

# تنسيق بسيط ومريح للعين
st.markdown("""
    <style>
    .stApp { background-color: #F9FBFF; }
    .stButton>button { border-radius: 20px; background: #4A90E2; color: white; border: none; }
    .urgent-task { color: #E74C3C; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# إدارة الحالة (Session State)
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# ترويسة الموقع
st.title("🚀 SparkFlow Pro")
st.write("مساعدكِ الذكي لتنظيم المهام وإصدار تقارير Kids Gate.")

# --- منطقة الإدخال ---
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        task_text = st.text_input("ما هو إنجازك الجديد؟", placeholder="اكتبي هنا...")
    with col2:
        is_urgent = st.toggle("مهمة عاجلة 🔥")
    
    if st.button("إضافة للمفكرة ✨"):
        if task_text:
            st.session_state.tasks.append({
                "task": task_text,
                "urgent": is_urgent,
                "status": "pending",
                "time": datetime.now().strftime("%I:%M %p"),
                "last_notified": time.time()
            })
            st.success("تمت الإضافة!")
            st.rerun()

st.divider()

# --- التنبيهات اللحوحة للمهام العاجلة ---
for t in st.session_state.tasks:
    if t['urgent'] and t['status'] == "pending":
        # تنبيه كل دقيقة إذا لم تنجز
        if time.time() - t['last_notified'] > 60:
            st.toast(f"⚠️ تذكير: هل انتهيتِ من: {t['task']}؟", icon="🔥")
            t['last_notified'] = time.time()

# --- عرض المهام ---
st.subheader("📋 قائمة الإنجازات الحالية")
for i, t in enumerate(st.session_state.tasks):
    if t['status'] == "pending":
        c1, c2 = st.columns([4, 1])
        prefix = "🔥 " if t['urgent'] else "📍 "
        c1.write(f"{prefix} {t['task']}")
        if c2.button("تم ✅", key=f"done_{i}"):
            st.session_state.tasks[i]['status'] = "done"
            st.balloons()
            st.rerun()

# --- وظيفة إصدار الـ PDF فوق صورتك ---
def create_report(done_tasks):
    pdf = FPDF()
    pdf.add_page()
    
    # وضع صورتك كخلفية (يجب أن تكون في GitHub بنفس الاسم)
    img_path = "1000193814.png"
    if os.path.exists(img_path):
        pdf.image(img_path, x=0, y=0, w=210, h=297)
    
    # إعدادات النص (الكتابة فوق المنطقة البيضاء)
    pdf.set_font("Arial", size=14)
    pdf.set_text_color(60, 60, 60)
    
    y_pos = 105 # البدء من منتصف الورقة تقريباً (المنطقة البيضاء)
    for task in done_tasks:
        pdf.set_xy(35, y_pos)
        pdf.cell(0, 10, txt=f"- {task['task']}", ln=True)
        y_pos += 12
        
    return pdf.output()

# --- قسم التحميل ---
st.divider()
if st.button("🪄 توليد تقرير PDF الأسبوعي"):
    completed = [t for t in st.session_state.tasks if t['status'] == "done"]
    if completed:
        try:
            pdf_out = create_report(completed)
            st.download_button(
                label="📥 تحميل التقرير جاهزاً",
                data=bytes(pdf_out),
                file_name=f"Weekly_Report_{datetime.now().strftime('%d_%m')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"تأكدي من رفع الصورة '1000193814.png' لـ GitHub. الخطأ: {e}")
    else:
        st.warning("أنجزي بعض المهام أولاً لتوليد التقرير!")
