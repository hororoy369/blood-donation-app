import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="ব্লাড ডোনেট নেটওয়ার্ক", page_icon="🩸")

st.title("🩸 ব্লাড ডোনেট নেটওয়ার্ক")
st.markdown("### রক্ত দিন, জীবন বাঁচান")

# গুগল শিটের সাথে সহজ কানেকশন
url = "https://docs.google.com/spreadsheets/d/1X6O8HFWva-bCEgCGRUG8GmjTGUYzZdfjJoFwuqzm9YA/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# ডাটা পড়ার ফাংশন
def get_data():
    try:
        return conn.read(spreadsheet=url)
    except:
        return pd.DataFrame(columns=["Name", "Blood Group", "Phone", "Location"])

# সার্চ সেকশন
st.header("রক্তের সন্ধান করুন")
search_bg = st.selectbox("কোন গ্রুপের রক্ত খুঁজছেন?", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])

if st.button("সার্চ করুন"):
    df = get_data()
    if not df.empty:
        results = df[df['Blood Group'].astype(str).str.strip() == search_bg]
        if not results.empty:
            st.success(f"{search_bg} গ্রুপের ডোনার পাওয়া গেছে:")
            st.table(results)
        else:
            st.info(f"দুঃখিত, বর্তমানে {search_bg} গ্রুপের কোনো ডোনার নেই।")
    else:
        st.error("ডাটাবেসে কোনো তথ্য পাওয়া যায়নি।")

st.markdown("---")
st.sidebar.info("নতুন নাম যোগ করতে চাইলে সরাসরি গুগল শিটে গিয়ে লিখে দিন। অ্যাপে সেটা অটোমেটিক চলে আসবে।")
st.markdown("### 👨‍💻 ডেভেলপার: হরশংকর রায়")
