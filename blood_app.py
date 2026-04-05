import streamlit as st
import pandas as pd

# অ্যাপের টাইটেল ও লোগো
st.set_page_config(page_title="ব্লাড ডোনেট নেটওয়ার্ক", page_icon="🩸")
st.title("🩸 ব্লাড ডোনেট নেটওয়ার্ক")

# ডোনার রেজিস্ট্রেশন (Side Bar)
st.sidebar.header("নতুন ডোনার রেজিস্ট্রেশন")
with st.sidebar.form("registration_form"):
    name = st.text_input("আপনার নাম")
    # এখানে key='reg_bg' যোগ করা হয়েছে
    blood_group = st.selectbox("ব্লাড গ্রুপ", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"], key='reg_bg')
    phone = st.text_input("ফোন নম্বর")
    location = st.text_input("আপনার এলাকা")
    submit_button = st.form_submit_button("রেজিস্ট্রেশন সম্পন্ন করুন")

if submit_button:
    st.sidebar.success(f"ধন্যবাদ {name}, আপনার তথ্য নিবন্ধিত হয়েছে!")

# সার্চ সেকশন
st.header("রক্তের সন্ধান করুন")
# এখানে key='search_bg' যোগ করা হয়েছে
search_bg = st.selectbox("কোন গ্রুপের রক্ত খুঁজছেন?", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"], key='search_bg')

# ডেমো ডোনার লিস্ট
data = {
    "নাম": ["রহিম", "করিম", "হরশংকর রায়", "পার্থ"],
    "ব্লাড গ্রুপ": ["A+", "B+", "O+", "AB+"],
    "ফোন": ["018XXXXXXXX", "017XXXXXXXX", "019XXXXXXXX", "015XXXXXXXX"],
    "এলাকা": ["চট্টগ্রাম", "ঢাকা", "কলকাতা", "রাজশাহী"]
}
df = pd.DataFrame(data)

# সার্চ রেজাল্ট দেখানো
result = df[df["ব্লাড গ্রুপ"] == search_bg]

if not result.empty:
    st.success(f"{search_bg} গ্রুপের ডোনার পাওয়া গেছে:")
    st.table(result)
else:
    st.warning("দুঃখিত, এই গ্রুপে এখন কোনো ডোনার নেই।")

# ক্রেডিট সেকশন (তোমার নাম)
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #e63946;'>👨‍💻 ডেভেলপার: হরশংকর রায়</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>'রক্ত দিন, জীবন বাঁচান'</p>", unsafe_allow_html=True)
