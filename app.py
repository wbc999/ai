import streamlit as st
from PIL import Image
import urllib.parse
from supabase import create_client

# =========================
# 🔐 Supabase 連線
# =========================
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# =========================
# 🧠 穿搭分析（簡化AI）
# =========================
def analyze_outfit(image):
    return {
        "style": "streetwear casual outfit",
        "top": "oversized t shirt",
        "bottom": "loose jeans pants",
        "shoes": "sneakers shoes"
    }

# =========================
# 🔎 電商搜尋
# =========================
def search_links(query):
    q = urllib.parse.quote(query)

    return {
        "Shopee": f"https://shopee.tw/search?keyword={q}",
        "momo": f"https://www.momoshop.com.tw/search/searchShop.jsp?keyword={q}",
        "PChome": f"https://ecshweb.pchome.com.tw/search/v3.3/?q={q}",
        "Google": f"https://www.google.com/search?tbm=shop&q={q}",
    }

# =========================
# 🌐 UI
# =========================
st.set_page_config(page_title="AI 穿搭分析商城", layout="wide")

st.title("🧠 AI 穿搭分析 + 電商搜尋 + 社群")

uploaded = st.file_uploader("📸 上傳穿搭照片", type=["jpg", "png", "jpeg"])

# =========================
# 🔍 穿搭分析區
# =========================
if uploaded:

    image = Image.open(uploaded)
    st.image(image, use_container_width=True)

    result = analyze_outfit(image)

    st.success(f"風格：{result['style']}")

    items = {
        "上衣": result["top"],
        "褲子": result["bottom"],
        "鞋子": result["shoes"]
    }

    st.subheader("👕 分析結果")

    for part, keyword in items.items():

        st.markdown(f"## {part}：{keyword}")

        links = search_links(keyword)

        for name, url in links.items():
            st.markdown(f"- [{name}]({url})")

# =========================
# 👥 分享穿搭（Supabase）
# =========================
st.divider()
st.header("👥 分享你的穿搭")

with st.form("share_form"):
    title = st.text_input("穿搭名稱")
    desc = st.text_area("穿搭介紹")
    share_img = st.file_uploader("上傳分享圖片", type=["jpg", "png", "jpeg"])

    submit = st.form_submit_button("🚀 分享")

    if submit and share_img:

        img = Image.open(share_img)
        result = analyze_outfit(img)

        # 👉 存到 Supabase
        supabase.table("posts").insert({
            "title": title,
            "description": desc,
            "style": result["style"],
            "top": result["top"],
            "bottom": result["bottom"],
            "shoes": result["shoes"]
        }).execute()

        st.success("分享成功（已存到雲端）！")

# =========================
# 🔥 社群牆（Supabase讀取）
# =========================
st.divider()
st.header("🔥 大家都在穿")

data = supabase.table("posts").select("*").order("id", desc=True).execute()

if data.data:

    for post in data.data:

        st.subheader(post["title"])
        st.write(post["description"])

        st.success(f"風格：{post['style']}")

        items = {
            "上衣": post["top"],
            "褲子": post["bottom"],
            "鞋子": post["shoes"]
        }

        for part, keyword in items.items():
            st.markdown(f"### {part}：{keyword}")

            links = search_links(keyword)

            cols = st.columns(4)

            for i, (shop, url) in enumerate(links.items()):
                with cols[i]:
                    st.link_button(shop, url)

        st.divider()

else:
    st.info("還沒有任何分享，快來當第一個穿搭達人🔥")
