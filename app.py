import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الواجهة الاحترافية
st.set_page_config(
    page_title="SparkFlow Pro | لوحة القيادة الذكية",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص الألوان والتصميم عبر CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #4A90E2; color: white; border: none; }
    .stButton>button:hover { background-color: #357ABD; border: none; }
    .task-card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px; border-right: 5px solid #4A90E2; }
    .priority-high { border-right: 5px solid #FF4B4B !important; }
    .priority-medium { border-right: 5px solid #FFA500 !important; }
    .priority-low { border-right: 5px solid #28A745 !important; }
    </style>
    """, unsafe_allow_html=True)

# إدارة البيانات (Session State)
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3209/3209265.png", width=100)
    st.title("التحكم الذكي")
    st.info("هذا الموقع مخصص لإدارة إنجازاتك وترتيب أولوياتك بذكاء.")
    
    if st.button("🗑️ مسح جميع المهام"):
        st.session_state.tasks = []
        st.rerun()

# --- العنوان الرئيسي ---
st.markdown("<h1 style='text-align: center; color: #2C3E50;'>🚀 SparkFlow Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7F8C8D;'>نظمي يومك، أنجزي بذكاء، واتركي التقرير عليّ</p>", unsafe_allow_html=True)

# --- منطقة الإدخال ---
with st.container():
    st.markdown("### ➕ إضافة مهمة جديدة")
    col1, col2, col3 = st.columns([3, 1.5, 1])
    
    with col1:
        task_input = st.text_input("ماذا ستنجزين الآن؟", placeholder="مثلاً: مراجعة كود قاعدة البيانات...")
    with col2:
        category = st.selectbox("الأولوية والنوع", [
            "🔥 عاجل وهام جداً", 
            "⭐ هام (تخطيط)", 
            "⏳ روتيني (غير عاجل)", 
            "🎈 رفاهية / تعلم"
        ])
    with col3:
        add_btn = st.button("إضافة ✅")

    if add_btn and task_input:
        st.session_state.tasks.append({
            "id": len(st.session_state.tasks),
            "task": task_input,
            "category": category,
            "status": "قيد التنفيذ",
            "time": datetime.now().strftime("%I:%M %p")
        })
        st.success("تمت الإضافة للمفكرة!")

# --- عرض المهام (المصفوفة الذكية) ---
st.divider()
col_active, col_done = st.columns(2)

with col_active:
    st.markdown("### 🎯 مهام قيد العمل")
    if not any(t['status'] == "قيد التنفيذ" for t in st.session_state.tasks):
        st.write("أنتِ مسترخية حالياً.. لا توجد مهام!")
    
    for i, t in enumerate(st.session_state.tasks):
        if t['status'] == "قيد التنفيذ":
            # تحديد لون الكارت حسب الأولوية
            p_class = "priority-high" if "عاجل" in t['category'] else "priority-medium" if "هام" in t['category'] else "priority-low"
            
            with st.container():
                st.markdown(f"""
                <div class='task-card {p_class}'>
                    <small style='color: gray;'>🕒 {t['time']}</small>< boat
                    <h4 style='margin: 5px 0;'>{t['task']}</h4>
                    <p style='font-size: 0.8em; color: #34495E;'>النوع: {t['category']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                if c1.button(f"تم الإنجاز ✨", key=f"done_{i}"):
                    st.session_state.tasks[i]['status'] = "مكتملة"
                    st.rerun()
                if c2.button(f"إزالة 🗑️", key=f"del_{i}"):
                    st.session_state.tasks.pop(i)
                    st.rerun()

with col_done:
    st.markdown("### ✅ الإنجازات المكتملة")
    completed_tasks = [t for t in st.session_state.tasks if t['status'] == "مكتملة"]
    for t in completed_tasks:
        st.markdown(f"📍 **{t['task']}** <span style='color:green'>(تم)</span>", unsafe_allow_html=True)

# --- قسم التقرير النهائي الذكي ---
st.divider()
if st.button("🪄 توليد تقرير الإنجاز الاحترافي"):
    if completed_tasks:
        st.balloons()
        st.markdown("### 📄 التقرير الجاهز للإرسال:")
        
        # صياغة التقرير بذكاء
        report = f"**ملخص الإنجاز اليومي - {datetime.now().strftime('%Y/%m/%d')}**\n\n"
        report += "تحية طيبة، أود إحاطتكم بما تم إنجازه اليوم بكل كفاءة:\n\n"
        
        for t in completed_tasks:
            report += f"* **{t['task']}** (تمت بنجاح)\n"
            
        report += "\n---\n*تم إعداد هذا التقرير عبر SparkFlow Pro الذكي.*"
        
        st.info("يمكنك نسخ التقرير أدناه:")
        st.text_area("", report, height=200)
    else:
        st.warning("لم يتم إكمال أي مهام بعد لصياغة تقرير!")
