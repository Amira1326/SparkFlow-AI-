import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os
import time
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# إعداد الواجهة
st.set_page_config(page_title="SparkFlow Pro", layout="centered")

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# وظيفة لتنسيق النص العربي ليظهر بشكل صحيح في الـ PDF
def format_arabic(text):
    reshaped_text = reshape(text)
    return get_display(reshaped_text)

st.title("🚀 SparkFlow Pro")

# --- منطقة الإدخال ---
with st.container():
    col1, col2 = st.columns([3, 1])
    task_text = col1.text_input("ما هو إنجازك الجديد؟")
    is_urgent = col2.toggle("عاجلة 🔥")
    if st.button("إضافة للمفكرة ✨"):
        if task_text:
            st.session_state.tasks.append({"task": task_text, "urgent": is_urgent, "status": "pending"})
            st.rerun()

# --- عرض المهام الحالية ---
st.subheader("📋 قائمة الإنجازات")
for i, t in enumerate(st.session_state.tasks):
    if t['status'] == "pending":
        c1, c2 = st.columns([4, 1])
        c1.write(f"{'🔥' if t['urgent'] else '📍'} {t['task']}")
        if c2.button("تم ✅", key=f"d_{i}"):
            st.session_state.tasks[i]['status'] = "done"
            st.rerun()

# --- وظيفة صنع الـ PDF الاحترافية ---
def create_report(done_tasks):
    pdf = FPDF()
    pdf.add_page()
    
    # إضافة صورة الخلفية
    img_path = "1000193814.png"
    if os.path.exists(img_path):
        pdf.image(img_path, x=0, y=0, w=210, h=297)
    
    # استخدام خط يدعم العربية (سيحاول البرنامج استخدام الخط المتاح في النظام)
    # ملاحظة: إذا كنتِ تملكين ملف خط (.ttf) ارفعيه لـ GitHub وسأعدل الكود ليستخدمه
    pdf.set_font("Arial", size=14) 
    
    y_pos = 105
    for task in done_tasks:
        # تحويل النص العربي ليظهر صحيحاً
        display_text = format_arabic(f"- {task['task']}")
        pdf.set_xy(35, y_pos)
        # الكتابة من اليمين لليسار
        pdf.multi_cell(140, 10, txt=display_text, align='R')
        y_pos += 12
        
    return pdf.output()

# --- زر التحميل ---
if st.button("🪄 توليد تقرير PDF"):
    completed = [t for t in st.session_state.tasks if t['status'] == "done"]
    if completed:
        try:
            pdf_out = create_report(completed)
            st.download_button(
                label="📥 تحميل التقرير",
                data=bytes(pdf_out),
                file_name="Weekly_Report.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"حدث خطأ في الخطوط. حاولي كتابة المهام بالإنجليزية مؤقتاً أو ارفعي ملف خط عربي .ttf للمستودع. الخطأ: {e}")
