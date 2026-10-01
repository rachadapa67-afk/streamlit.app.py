import streamlit as st

# ตั้งค่าหน้าเว็บแบบกว้างและใส่ธีม
st.set_page_config(
    page_title="วิเคราะห์เลขทะเบียนรถมงคล",
    page_icon="🚘",
    layout="centered"
)

# --- พจนานุกรมแปลงตัวอักษรเป็นตัวเลขตามตาราง ---
CHAR_TO_NUM = {
    'ก': 1, 'ด': 1, 'ถ': 1, 'ท': 1, 'ภ': 1, 'ฤ': 1,
    'ข': 2, 'บ': 2, 'ป': 2, 'ง': 2, 'ช': 2,
    'ต': 3, 'ท': 3, 'ฒ': 3, 'ฆ': 3,
    'ค': 4, 'ธ': 4, 'ร': 4, 'ญ': 4, 'ษ': 4,
    'ฉ': 5, 'ณ': 5, 'ฌ': 5, 'น': 5, 'ม': 5, 'ห': 5, 'ฮ': 5, 'ฎ': 5, 'ฬ': 5,
    'จ': 6, 'ล': 6, 'ว': 6, 'อ': 6,
    'ซ': 7, 'ศ': 7, 'ส': 7,
    'ย': 8, 'ผ': 8, 'ฝ': 8, 'พ': 8, 'ฟ': 8,
    'ฏ': 9, 'ฐ': 9
}

# --- ชุดข้อมูลผลรวมและคำทำนายตามตาราง ---
GOOD_NUMS = {4, 5, 6, 9, 14, 15, 19, 23, 24, 32, 36, 40, 41, 42, 44, 45, 46, 50, 51, 54}
MODERATE_NUMS = {8, 10, 13, 16, 18, 22, 25, 26, 28, 31, 35, 38, 39, 47, 49, 52, 53}
BAD_NUMS = {3, 7, 11, 12, 17, 20, 21, 27, 29, 30, 33, 34, 37, 43, 48}

# --- Sidebar: ข้อมูลกลุ่ม Nova ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/car--v1.png")
    st.header("📌 เกี่ยวกับโปรเจกต์")
    st.write("**กลุ่ม Nova หมายเลข 2**")
    st.markdown("---")
    st.subheader("👥 รายชื่อสมาชิกกลุ่ม")
    st.markdown("""
    1. น.ส.รชดา ปัททุม
    2. น.ส.บุศรกร สุดโต
    3. นายอนันต์โชค ไพฑูรย์ ยืนยง
    4. นายเนศ เฉลียวยิ่ง
    5. น.ส.ฐิตินันท์ ไชยอง
    """)
    st.markdown("---")
    st.caption("พัฒนาด้วย Streamlit 🎈")

# --- Header ส่วนหัวแอปพลิเคชัน ---
st.title("🚗 วิเคราะห์เลขทะเบียนรถมงคล")
st.caption("✨ ระบบเช็กผลรวมทะเบียนรถและแปลความหมายตัวอักษรตามศาสตร์ตัวเลข")

st.write("")

# --- ส่วนที่ 1: รับค่าอินพุต ---
with st.container(border=True):
    st.subheader("1️⃣ กรอกข้อมูลทะเบียนรถ")
    
    col1, col2 = st.columns(2)
    with col1:
        letters = st.text_input("🔤 หมวดตัวอักษร", value="ผอ", max_chars=3, help="เช่น ผอ, 1กข, กท")
    with col2:
        digits = st.text_input("🔢 ตัวเลข 4 ตัวท้าย", value="8930", max_chars=4, help="เช่น 8930, 1234")
    
    analyze_btn = st.button("🔮 วิเคราะห์ทะเบียนรถ", type="primary", use_container_width=True)

if analyze_btn:
    clean_letters = letters.strip()
    clean_digits = "".join(filter(str.isdigit, digits))

    if not clean_letters or not clean_digits:
        st.error("⚠️ กรุณากรอกข้อมูลตัวอักษรและตัวเลขให้ถูกต้องครบถ้วน")
    else:
        # คำนวณตัวเลข
        digit_sum = sum(int(d) for d in clean_digits)
        letter_sum = 0
        letter_details = []
        for char in clean_letters:
            val = CHAR_TO_NUM.get(char, 0)
            letter_sum += val
            letter_details.append(f"**{char}** = {val}")

        total_sum = digit_sum + letter_sum

        st.write("")

        # --- ส่วนที่ 2: ขั้นตอนการคำนวณ ---
        with st.container(border=True):
            st.subheader("2️⃣ ขั้นตอนการคำนวณ")
            
            digit_str_list = [d for d in clean_digits]
            
            m1, m2, m3 = st.columns(3)
            m1.metric("ผลรวมเลข 4 ตัวท้าย", f"{digit_sum}", " + ".join(digit_str_list))
            m2.metric("ผลรวมตัวอักษร", f"{letter_sum}", ", ".join(letter_details))
            m3.metric("ผลรวมทั้งหมด", f"{total_sum}", f"{digit_sum} + {letter_sum}")

        st.write("")

        # --- ส่วนที่ 3: ผลการทำนาย ---
        with st.container(border=True):
            st.subheader("3️⃣ ผลการทำนายและระดับมงคล")
            
            if total_sum in GOOD_NUMS:
                st.success(f"🌟 **ผลรวมได้ {total_sum} : ระดับดีมาก (มงคลยิ่ง)**")
                st.markdown("""
                > **ความหมาย:**  
                > ส่งเสริมให้ชีวิตก้าวหน้า นำไปสู่ความสำเร็จที่ยิ่งใหญ่ ให้ผลดีในด้าน **การเงิน การงาน ความรัก** ไม่ว่าจะทำอะไรก็จะมีคนสนับสนุนค้ำชูเสมอ
                """)
            elif total_sum in MODERATE_NUMS:
                st.info(f"⚖️ **ผลรวมได้ {total_sum} : ระดับปานกลาง**")
                st.markdown("""
                > **ความหมาย:**  
                > มีอุปสรรคเข้ามาบ้าง แต่ผ่านพ้นไปได้เสมอ ไม่อับจน กำลังใจดี มีเพื่อนฝูงอุปถัมภ์ค้ำชู หากทำบุญและคิดดีทำดีจะช่วยส่งเสริมให้ดียิ่งขึ้น
                """)
            elif total_sum in BAD_NUMS:
                st.warning(f"⚠️ **ผลรวมได้ {total_sum} : ระดับควรระวัง (ไม่ดี)**")
                st.markdown("""
                > **ความหมาย:**  
                > อุปสรรคเยอะ ต้องเหนื่อยกว่าคนอื่นหลายเท่า ปัญหาเก่าหาย ปัญหาใหม่มักเข้ามา มักมีปัญหาเรื่องเงินไม่รู้จบ และมีโอกาสเกิดอุบัติเหตุบ่อย ควรมีสติไม่ประมาท
                """)
            else:
                st.write(f"📊 **ผลรวมได้ {total_sum}** : ไม่อยู่ในกลุ่มเกณฑ์มาตรฐานทำนายทั่วไป")

# --- Footer ด้านล่าง ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Group Nova No. 2 — License Plate Analysis Project</p>", unsafe_html=True)
