import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# অ্যাপের সেটআপ
st.set_page_config(page_title="ব্লাড ডোনেট নেটওয়ার্ক", page_icon="🩸")
st.title("🩸 ব্লাড ডোনেট নেটওয়ার্ক")
st.subheader("রক্ত দিন, জীবন বাঁচান")

# গুগল শিট কানেকশন
conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1X6O8HFWva-bCEgCGRUG8GmjTGUYzZdfjJoFwuqzm9YA/edit?usp=sharing"

# ডাটা পড়ার ফাংশন
def get_data():
    try:
        # worksheet="Form Responses 1" দেওয়া হয়েছে কারণ গুগল ফর্মের ডাটা এখানেই জমা হয়
        df = conn.read(spreadsheet=url, worksheet="Form Responses 1")
        return df
    except Exception as e:
        # যদি কোনো কারণে ফর্মের ট্যাব না পায়, তবে সাধারণ শিট চেক করবে
        try:
            return conn.read(spreadsheet=url)
        except:
            return pd.DataFrame()

# সাইডবারে তোমার ফর্মের লিঙ্ক
st.sidebar.header("ডোনার হতে চান?")
st.sidebar.info("নতুন নাম যোগ করতে চাইলে নিচের বাটনে ক্লিক করে ফরমটি পূরণ করুন।")
st.sidebar.link_button("👉 রেজিস্ট্রেশন ফরম পূরণ করুন", "https://forms.gle/2ZFWEFxrFt58fjRy5")

st.sidebar.markdown("---")
st.sidebar.write("ডেভেলপার: হরশংকর রায়")

# সার্চ সেকশন
st.header("🔍 রক্তের সন্ধান করুন")
search_bg = st.selectbox("কোন গ্রুপের রক্ত খুঁজছেন?", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])

if st.button("সার্চ করুন"):
    df = get_data()
    
    if not df.empty:
        # কলামের নাম যাই হোক না কেন, এটি রক্ত গ্রুপ খুঁজে বের করবে
        # সাধারণত ২য় বা ৩য় কলামে ব্লাড গ্রুপ থাকে, তাই আমরা সব কলামে খুঁজব
        mask = df.apply(lambda row: row.astype(str).str.contains(search_bg, case=False).any(), axis=1)
        results = df[mask]
        
        if not results.empty:
            st.success(f"অভিনন্দন! {search_bg} গ্রুপের ডোনার পাওয়া গেছে:")
            st.dataframe(results) # টেবিল আকারে ডাটা দেখাবে
        else:
            st.warning(f"দুঃখিত, বর্তমানে {search_bg} গ্রুপের কোনো ডোনার আমাদের তালিকায় নেই।")
    else:
        st.error("ডাটাবেসে কোনো তথ্য পাওয়া যায়নি। অনুগ্রহ করে শিটটি চেক করুন।")

st.markdown("---")
st.markdown("---")
st.markdown("### HP ROY ডেভেলপার: হরশংকর রায়")
