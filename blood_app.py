import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# অ্যাপের কনফিগারেশন
st.set_page_config(page_title="ব্লাড ডোনেট নেটওয়ার্ক", page_icon="🩸")
st.title("🩸 ব্লাড ডোনেট নেটওয়ার্ক")
st.subheader("রক্ত দিন, জীবন বাঁচান")

# গুগল শিট কানেকশন
conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1X6O8HFWva-bCEgCGRUG8GmjTGUYzZdfjJoFwuqzm9YA/edit?usp=sharing"

# ডাটা পড়ার ফাংশন (Indentation ঠিক করা হয়েছে)
def get_data():
    try:
        # গুগল ফর্মের ডাটা সাধারণত "Form Responses 1" ট্যাবে জমা হয়
        return conn.read(spreadsheet=url, worksheet="Form Responses 1", usecols=[0,1,2,3,4])
    except:
        # যদি কোনো কারণে এরর হয়, তবে অন্তত খালি ডাটাফ্রেম দেখাবে
        return pd.DataFrame(columns=["Timestamp", "Name", "Blood Group", "Phone", "Location"])

# সাইডবারে রেজিস্ট্রেশন ফর্মের লিঙ্ক
st.sidebar.header("ডোনার হতে চান?")
st.sidebar.info("নতুন নাম যোগ করতে চাইলে নিচের বাটনে ক্লিক করে ফরমটি পূরণ করুন।")
st.sidebar.link_button("👉 রেজিস্ট্রেশন ফরম পূরণ করুন", "https://forms.gle/2ZFWEFxrFt58fjRy5")

st.sidebar.markdown("---")
st.sidebar.write("গুগল ফর্মে তথ্য দেওয়ার ১-২ মিনিট পর অ্যাপটি রিফ্রেশ করলে আপনার নাম তালিকায় দেখা যাবে।")

# রক্তের সন্ধান করার সেকশন
st.header("🔍 রক্তের সন্ধান করুন")
search_bg = st.selectbox("কোন গ্রুপের রক্ত খুঁজছেন?", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])

if st.button("সার্চ করুন"):
    df = get_data()
    if not df.empty:
        # ব্লাড গ্রুপ দিয়ে ফিল্টার করা (গুগল ফর্মে সাধারণত ৩ নম্বর কলামে ব্লাড গ্রুপ থাকে)
        # এখানে iloc[:, 2] ব্যবহার করা হয়েছে কারণ প্রথম কলামটি Timestamp
        results = df[df.iloc[:, 2].astype(str).str.strip() == search_bg]
        
        if not results.empty:
            st.success(f"অভিনন্দন! {search_bg} গ্রুপের ডোনার পাওয়া গেছে:")
            st.table(results)
        else:
            st.warning(f"দুঃখিত, বর্তমানে {search_bg} গ্রুপের কোনো ডোনার আমাদের তালিকায় নেই।")
    else:
        st.error("ডাটাবেসে কোনো তথ্য পাওয়া যায়নি।")

# ফুটার
st.markdown("---")
st.markdown("### 👨‍💻 ডেভেলপার: হরশংকর রায়")
