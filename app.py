import streamlit as st
from fpdf import FPDF
import os
import time
import requests
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# إعدادات الصفحة
st.set_page_config(page_title="SparkFlow Pro | Smart Reminders", page_icon="🔔")

# رابط الـ Webhook الخاص بكِ في n8n (تم تحديثه بناءً على صورتك)
N8N_WEBHOOK_URL = "https://amira-all1.app.n8n.cloud/webhook-test/9f4684c0-2c05-4657-bdb5-b0a5fe7c2747"

# إدارة حالة المهام
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# دالة معالجة النصوص العربية للـ PDF
def process_arabic(text):
    if not text: return ""
    return get_display(reshape(text))

st.title("🚀 SparkFlow Smart System")

# --- منطقة الإدخال الذكية ---
with st.expander("➕ إضافة مهمة جديدة وتفعيل التنبيهات", expanded=True):
    task_text = st.text_input("المهمة:")
    requester = st.text_input("من صاحب الطلب؟ (مثل: Najwa، المدير)")
    is_urgent = st.toggle("عاجلة جداً (تنبيه للجوال) 🔥")
    
    if st.button("حفظ وإرسال تنبيه ✨"):
        if task_text and requester:
            new_task = {
                "task": task_text,
                "requester": requester,
                "urgent": is_urgent,
                "status": "pending",
                "time_added": time.strftime("%H:%M")
            }
            st.session_state.tasks.append(new_task)
            
            # إرسال البيانات لـ n8n إذا كانت المهمة عاجلة
            if is_urgent:
                try:
                    # نرسل البيانات لـ n8n ليقوم بمعالجتها وإرسالها للتليجرام
                    response = requests.post(N8N_WEBHOOK_URL, json=new_task)
                    if response.status_code == 200:
                        st.toast(f"تم إرسال تنبيه لـ n8n لمتابعة مهمة {requester}!", icon="📲")
                    else:
                        st.error("وصلت الإشارة لـ n8n ولكن حدث خطأ في الاستلام")
                except Exception as e:
                    st.error(f"فشل الاتصال بـ n8n: {e}")
            
            st.success("تم الحفظ بنجاح!")
            st.rerun()

# --- عرض المهام الحالية ---
st.subheader("📋 المهام الحالية")
for i, t in enumerate(st.session_state.tasks):
    if t['status'] == "pending":
        col1, col2 = st.columns([4, 1])
        with col1:
            urgent_mark = "🔥" if t['urgent'] else "📍"
            st.markdown(f"{urgent_mark} **{t['task']}**")
            st.caption(f"بطلب من: {t['requester']} | الوقت: {t['time_added']}")
        if col2.button("تم ✅", key=f"done_{i}"):
            st.session_state.tasks[i]['status'] = "done"
            st.rerun()

# --- وظيفة صناعة تقرير PDF ---
def create_report(done_tasks):
    pdf = FPDF()
    pdf.add_page()
    
    # خلفية التقرير (تأكدي من وجود الصورة في GitHub)
    img_path = "1000193814.png"
    if os.path.exists(img_path):
        pdf.image(img_path, x=0, y=0, w=210, h=297)
    
    # إعداد الخط العربي (تأكدي من وجود الملف في GitHub)
    font_path = "Amiri-Regular.ttf"
    if os.path.exists(font_path):
        pdf.add_font('Amiri', '', font_path)
        pdf.set_font('Amiri', size=16)
    else:
        pdf.set_font("Arial", size=14)

    y_pos = 110 # نقطة البداية فوق التصميم
    for t in done_tasks:
        # دمج اسم المهمة مع صاحب الطلب في سطر واحد
        full_text = f"{t['task']} (بطلب من: {t['requester']})"
        display_text = process_arabic(full_text)
        
        pdf.set_xy(30, y_pos)
        pdf.cell(150, 10, txt=display_text, ln=True, align='R')
        y_pos += 12
        
    return pdf.output()

# --- تصدير التقرير ---
st.divider()
if st.button("🪄 إصدار تقرير PDF"):
    completed = [t for t in st.session_state.tasks if t['status'] == "done"]
    if completed:
        try:
            pdf_out = create_report(completed)
            st.download_button(
                label="📥 تحميل التقرير النهائي",
                data=bytes(pdf_out),
                file_name=f"Report_{time.strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"حدث خطأ أثناء إصدار الملف: {e}")
    else:
        st.warning("أتمي بعض المهام أولاً لتتمكني من إصدار التقرير!")
