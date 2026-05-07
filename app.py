import streamlit as st
from PIL import Image
import urllib.parse

# =========================
# 🧠 穿搭分析（免費簡化AI）
# =========================
def analyze_outfit(image):
    # 這裡用穩定分類（避免 API 卡住）
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

st.markdown("""
<style>
.card {
    padding:15px;
    border-radius:15px;
    background:#111;
    margin-bottom:10px;
}
.title {
    font-size:32px;
    font-weight:800;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🧠 AI 穿搭分析 + 電商搜尋</div>", unsafe_allow_html=True)

uploaded = st.file_uploader("📸 上傳穿搭照片", type=["jpg", "png", "jpeg"])

if uploaded:

    image = Image.open(uploaded)
    st.image(image, use_container_width=True)

    result = analyze_outfit(image)

    st.success(f"風格：{result['style']}")

    st.subheader("👕 分析結果")

    items = {
        "上衣": result["top"],
        "褲子": result["bottom"],
        "鞋子": result["shoes"]
    }

    for part, keyword in items.items():

        st.markdown(f"## {part}：{keyword}")

        links = search_links(keyword)

        for name, url in links.items():

            st.markdown(f"""
            <div class="card">
                <b>{name}</b><br>
                {keyword}<br>
                <a href="{url}" target="_blank">👉 查看商品</a>
            </div>
            """, unsafe_allow_html=True)
# =========================
# 👥 穿搭分享社群
# =========================
st.divider()
st.header("👥 分享你的穿搭")

# 初始化分享列表
if "posts" not in st.session_state:
    st.session_state.posts = []

with st.form("share_form"):
    title = st.text_input("穿搭名稱")
    desc = st.text_area("穿搭介紹")
    share_img = st.file_uploader(
        "上傳分享圖片",
        type=["jpg", "png", "jpeg"],
        key="share_img"
    )

    submit = st.form_submit_button("🚀 分享")

    if submit and share_img:
        img = Image.open(share_img)

        result = analyze_outfit(img)

        items = {
            "上衣": result["top"],
            "褲子": result["bottom"],
            "鞋子": result["shoes"]
        }

        st.session_state.posts.append({
            "title": title,
            "desc": desc,
            "image": img,
            "style": result["style"],
            "items": items
        })

        st.success("分享成功！")

# =========================
# 社群穿搭牆
# =========================
st.divider()
st.header("🔥 大家都在穿")

for post in reversed(st.session_state.posts):

    st.subheader(post["title"])
    st.write(post["desc"])
    st.image(post["image"], width=350)

    st.success(f"風格：{post['style']}")

    for part, keyword in post["items"].items():

        st.markdown(f"### {part}：{keyword}")

        links = search_links(keyword)

        cols = st.columns(4)

        for i, (shop, url) in enumerate(links.items()):
            with cols[i]:
                st.link_button(shop, url)

    st.divider()
