import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# إعدادات الواجهة
st.set_page_config(page_title="SparkFlow Pro", layout="centered")

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# دالة معالجة النص العربي (مهمة جداً لظهور الحروف متصلة)
def process_arabic(text):
    if not text: return ""
    reshaped = reshape(text) # تصحيح شكل الحروف
    bidi_text = get_display(reshaped) # عكس اتجاه النص للعربية
    return bidi_text

st.title("🚀 SparkFlow Pro")

# --- إضافة مهمة ---
with st.expander("➕ إضافة مهمة جديدة", expanded=True):
    task_text = st.text_input("ما هو إنجازك الجديد؟")
    is_urgent = st.toggle("عاجلة 🔥")
    if st.button("إضافة للمفكرة ✨"):
        if task_text:
            st.session_state.tasks.append({"task": task_text, "urgent": is_urgent, "status": "pending"})
            st.rerun()

# --- قائمة المهام ---
st.subheader("📋 قائمة الإنجازات")
for i, t in enumerate(st.session_state.tasks):
    if t['status'] == "pending":
        c1, c2 = st.columns([4, 1])
        c1.write(f"{'🔥' if t['urgent'] else '📍'} {t['task']}")
        if c2.button("تم ✅", key=f"done_{i}"):
            st.session_state.tasks[i]['status'] = "done"
            st.rerun()

# --- وظيفة صنع الـ PDF ---
def create_report(done_tasks):
    # استخدام fpdf تدعم Unicode
    pdf = FPDF()
    pdf.add_page()
    
    # التأكد من وجود الصورة
    img_path = "1000193814.png"
    if os.path.exists(img_path):
        pdf.image(img_path, x=0, y=0, w=210, h=297)
    
    # اختيار خط يدعم الـ Unicode (نستخدم Arial كخط افتراضي يدعم العربية في أغلب الأنظمة)
    pdf.set_font("Arial", size=16)
    
    y_pos = 110 # الإحداثيات لتناسب تصميمك
    for task in done_tasks:
        # معالجة النص العربي قبل الكتابة
        arabic_task = process_arabic(task['task'])
        pdf.set_xy(30, y_pos)
        # الكتابة من اليمين (Align='R')
        pdf.cell(150, 10, txt=arabic_task, ln=True, align='R')
        y_pos += 12
        
    return pdf.output()

# --- زر توليد التقرير ---
if st.button("🪄 توليد تقرير PDF"):
    completed = [t for t in st.session_state.tasks if t['status'] == "done"]
    if completed:
        try:
            pdf_bytes = create_report(completed)
            st.download_button(
                label="📥 تحميل التقرير الأسبوعي",
                data=bytes(pdf_bytes),
                file_name="KidsGate_Report.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")
            st.info("نصيحة: إذا استمر الخطأ، جربي رفع ملف خط باسم 'arial.ttf' للمستودع")
    else:
        st.warning("لم يتم إنجاز أي مهام بعد!")
