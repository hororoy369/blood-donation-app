import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="ব্লাড ডোনেট নেটওয়ার্ক", page_icon="🩸")
st.title("🩸 ব্লাড ডোনেট নেটওয়ার্ক")

# সরাসরি লিঙ্ক এর বদলে Secrets ব্যবহার করছি
conn = st.connection("gsheets", type=GSheetsConnection)
url = st.secrets["connections"]["gsheets"]["spreadsheet"]

# ডাটা পড়ার ফাংশন
def get_data():
    return conn.read(spreadsheet=url, usecols=[0,1,2,3])

# নতুন ডোনার রেজিস্ট্রেশন
st.sidebar.header("নতুন ডোনার রেজিস্ট্রেশন")
with st.sidebar.form(key="registration_form"):
    name = st.text_input("আপনার নাম")
    blood_group = st.selectbox("ব্লাড গ্রুপ", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    phone = st.text_input("ফোন নম্বর")
    location = st.text_input("আপনার এলাকা")
    submit_button = st.form_submit_button(label="রেজিস্ট্রেশন সম্পন্ন করুন")

if submit_button:
    if name and phone and location:
        new_data = pd.DataFrame([{"Name": name, "Blood Group": blood_group, "Phone": phone, "Location": location}])
        df = get_data()
        updated_df = pd.concat([df, new_data], ignore_index=True)
        conn.update(spreadsheet=url, data=updated_df)
        st.sidebar.success(f"ধন্যবাদ {name}, তথ্য সেভ হয়েছে!")
        st.cache_data.clear()
    else:
        st.sidebar.error("সবগুলো ঘর পূরণ করুন জানু!")

# সার্চ সেকশন
st.header("রক্তের সন্ধান করুন")
search_bg = st.selectbox("কোন গ্রুপের রক্ত খুঁজছেন?", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
if st.button("সার্চ করুন"):
    df = get_data()
    results = df[df['Blood Group'].astype(str).str.strip() == search_bg]
    if not results.empty:
        st.table(results)
    else:
        st.info("দুঃখিত, কোনো ডোনার পাওয়া যায়নি।")

st.markdown("---")
st.markdown("### 👨‍💻 ডেভেলপার: হরশংকর রায়")
