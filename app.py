import streamlit as st
from PIL import Image
import urllib.parse
from supabase import create_client
import uuid

# =========================
# 🔐 Supabase 連線
# =========================
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# =========================
# 📸 上傳圖片到 Storage
# =========================
def upload_image(file):
    file_name = f"{uuid.uuid4()}.jpg"

    supabase.storage.from_("images").upload(
        file_name,
        file.getvalue(),
        {"content-type": "image/jpeg"}
    )

    return supabase.storage.from_("images").get_public_url(file_name)

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
        "淘寶": f"https://world.taobao.com/search/search.htm?_ksTS=1&q={q}",
        "SHEIN": f"https://www.shein.com/search?keyword={q}",
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
# 👥 分享穿搭（Supabase + Storage）
# =========================
st.divider()
st.header("👥 分享你的穿搭")

with st.form("share_form"):
    title = st.text_input("穿搭名稱")
    desc = st.text_area("穿搭介紹")
    share_img = st.file_uploader("上傳分享圖片", type=["jpg", "png", "jpeg"], key="share")

    submit = st.form_submit_button("🚀 分享")

    if submit and share_img:

        img = Image.open(share_img)
        result = analyze_outfit(img)

        # 🚀 上傳圖片到 Supabase Storage
        image_url = upload_image(share_img)

        supabase.table("posts").insert({
            "title": title,
            "description": desc,
            "image_url": image_url,
            "style": result["style"],
            "top": result["top"],
            "bottom": result["bottom"],
            "shoes": result["shoes"]
        }).execute()

        st.success("分享成功（已上傳雲端圖片）！")

# =========================
# 🔥 社群牆
# =========================
st.divider()
st.header("🔥 大家都在穿")

data = supabase.table("posts").select("*").execute()

if data.data:

    posts = sorted(data.data, key=lambda x: x["id"], reverse=True)

    for post in posts:

        st.subheader(post["title"])

        # 📸 顯示圖片（重點）
        if post.get("image_url"):
            st.image(post["image_url"], width=300)

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
