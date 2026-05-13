import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# إعداد واجهة البرنامج
st.set_page_config(page_title="SparkFlow | تقارير Kids Gate", page_icon="📝")

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

st.title("📝 صانع التقرير الأسبوعي الذكي")
st.info("سيتم طباعة مهامك مباشرة فوق تصميم Kids Gate الخاص بكِ.")

# --- منطقة إدخال المهام ---
with st.form("task_form"):
    task = st.text_input("المهمة المنجزة:")
    submitted = st.form_submit_button("إضافة للمسودة")
    if submitted and task:
        st.session_state.tasks.append(task)

# عرض المهام الحالية
if st.session_state.tasks:
    st.write("### إنجازاتك لهذا الأسبوع:")
    for i, t in enumerate(st.session_state.tasks):
        st.write(f"{i+1}. {t}")

# --- وظيفة صناعة الـ PDF فوق الخلفية ---
def export_to_pdf(tasks):
    pdf = FPDF()
    pdf.add_page()
    
    # 1. وضع صورة الخلفية (التصميم الخاص بكِ)
    # تأكدي أن اسم الملف في GitHub مطابق تماماً لهذا الاسم
    bg_path = "1000193814.png"
    if os.path.exists(bg_path):
        pdf.image(bg_path, x=0, y=0, w=210, h=297) # مقاس A4 كامل
    
    # 2. إعدادات النص (الإحداثيات للبدء بالكتابة في المنطقة البيضاء)
    pdf.set_font("Arial", size=14)
    pdf.set_text_color(50, 50, 50)
    
    # البدء بالكتابة من ارتفاع مناسب (بعد ترويسة التصميم)
    y_position = 100 
    
    for i, t in enumerate(tasks):
        pdf.set_xy(30, y_position) # ترك مسافة من اليسار 30
        pdf.multi_cell(150, 10, txt=f"- {t}", align='L')
        y_position += 10 # ترك مسافة بين الأسطر
        
    return pdf.output(dest='S').encode('latin-1')

# --- زر التحميل ---
st.divider()
if st.button("✨ إصدار التقرير النهائي (PDF)"):
    if st.session_state.tasks:
        try:
            pdf_bytes = export_to_pdf(st.session_state.tasks)
            st.download_button(
                label="📥 تحميل الملف الآن",
                data=pdf_bytes,
                file_name=f"Weekly_Report_{datetime.now().strftime('%Y_%m_%d')}.pdf",
                mime="application/pdf"
            )
            st.success("تم دمج تقريرك مع التصميم بنجاح!")
        except Exception as e:
            st.error(f"تأكدي من رفع صورة التصميم لـ GitHub بنفس الاسم. الخطأ: {e}")
    else:
        st.warning("أضيفي بعض المهام أولاً!")
