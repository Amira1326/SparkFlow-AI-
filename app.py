import streamlit as st
from fpdf import FPDF
import os
import time
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# إعداد واجهة المستخدم
st.set_page_config(page_title="SparkFlow Pro | Kids Gate", page_icon="✨")

# إدارة حالة المهام
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# دالة معالجة النصوص العربية
def process_arabic(text):
    if not text: return ""
    return get_display(reshape(text))

st.title("🚀 SparkFlow Pro")

# --- منطقة الإدخال ---
with st.container():
    col1, col2 = st.columns([3, 1])
    task_text = col1.text_input("ما هو إنجازك الجديد؟")
    is_urgent = col2.toggle("عاجلة 🔥")
    
    if st.button("إضافة للمفكرة ✨"):
        if task_text:
            st.session_state.tasks.append({
                "task": task_text,
                "urgent": is_urgent,
                "status": "pending",
                "time": time.time()
            })
            st.success("تم الحفظ!")
            st.rerun()

# --- عرض المهام وتحويلها لـ "تم" ---
st.subheader("📋 المهام المنجزة لهذا الأسبوع")
for i, t in enumerate(st.session_state.tasks):
    if t['status'] == "pending":
        c1, c2 = st.columns([4, 1])
        c1.write(f"{'🔥' if t['urgent'] else '📍'} {t['task']}")
        if c2.button("إتمام ✅", key=f"btn_{i}"):
            st.session_state.tasks[i]['status'] = "done"
            st.rerun()

# --- وظيفة صناعة الـ PDF بالخط العربي ---
def create_report(done_tasks):
    pdf = FPDF()
    pdf.add_page()
    
    # 1. وضع صورة الخلفية
    img_path = "1000193814.png"
    if os.path.exists(img_path):
        pdf.image(img_path, x=0, y=0, w=210, h=297)
    
    # 2. تفعيل الخط العربي الذي رفعتِه
    # تأكدي أن الاسم هنا "Amiri-Regular.ttf" يطابق تماماً ما رفعتِه لـ GitHub
    font_path = "Amiri-Regular.ttf" 
    if os.path.exists(font_path):
        pdf.add_font('Amiri', '', font_path)
        pdf.set_font('Amiri', size=18)
    else:
        pdf.set_font("Arial", size=14) # احتياطي

    # 3. كتابة المهام في المنطقة البيضاء
    y_pos = 110 
    for t in done_tasks:
        safe_text = process_arabic(t['task'])
        pdf.set_xy(30, y_pos)
        pdf.cell(150, 10, txt=safe_text, ln=True, align='R')
        y_pos += 12
        
    return pdf.output()

# --- زر التحميل النهائي ---
st.divider()
if st.button("🪄 إصدار تقرير Kids Gate (PDF)"):
    completed = [t for t in st.session_state.tasks if t['status'] == "done"]
    if completed:
        try:
            pdf_out = create_report(completed)
            st.download_button(
                label="📥 تحميل ملف التقرير الآن",
                data=bytes(pdf_out),
                file_name=f"Report_{time.strftime('%Y-%m-%d')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"خطأ في التصدير: {e}")
    else:
        st.warning("لم يتم تحديد أي مهام كـ 'تم' حتى الآن!")
