import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# =============================================================================
# 1. CẤU HÌNH TRANG WEB STREAMLIT & CUSTOM CSS
# =============================================================================
st.set_page_config(
    page_title="PNJ - Tra Cứu Chuyển Đổi Thanh Toán",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS tạo giao diện chuẩn như Phiếu Kiểm Tra PNJ
st.markdown("""
<style>
    .main-title {
        color: #003468;
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 2px;
    }
    .sub-title {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 20px;
    }
    .card-pa2 {
        background-color: #d97706;
        color: white;
        padding: 16px 20px;
        border-radius: 8px;
        font-size: 22px;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    .card-pa1 {
        background-color: #15803d;
        color: white;
        padding: 16px 20px;
        border-radius: 8px;
        font-size: 22px;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    .card-pa3 {
        background-color: #b91c1c;
        color: white;
        padding: 16px 20px;
        border-radius: 8px;
        font-size: 22px;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    .hub-badge {
        background-color: rgba(255, 255, 255, 0.25);
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: normal;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .quote-box {
        background-color: #0f172a;
        color: #f8fafc;
        padding: 20px;
        border-radius: 8px;
        font-size: 15px;
        line-height: 1.6;
        margin-top: 10px;
        margin-bottom: 15px;
        border-left: 5px solid #3b82f6;
    }
    .mapping-row {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 10px 15px;
        font-size: 14px;
        margin-bottom: 8px;
    }
    .timeline-card {
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;
        padding: 16px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 2. DỮ LIỆU CHÍNH SÁCH MAPPING & LỘ TRÌNH THANH TOÁN (PNJ 2026)
# =============================================================================
GROUPS = {
    "N1": {"name": "Vàng miếng / Nhẫn khoen / PLT / Kim Bảo", "timeline": "T+2", "days": 2, "roadmap": "100% T+2"},
    "N2": {"name": "TS Kim cương / Đá màu / Ngọc trai / Vỏ", "timeline": "T+120", "days": 120, "roadmap": "10% T+1, 20% T+30, 25% T+60, 25% T+90, 20% T+120"},
    "N3": {"name": "TS Công nghệ Ý / Không gắn đá / CZ / Dây chuyền", "timeline": "T+7", "days": 7, "roadmap": "100% T+7"},
    "N4": {"name": "Vàng 22K-24K (91,6% - 99,99%) / Quà tặng sưu tầm", "timeline": "T+7", "days": 7, "roadmap": "100% T+7"},
    "N5": {"name": "Kim cương rời / Đá màu rời / Ngọc trai rời / Cẩm thạch", "timeline": "T+120", "days": 120, "roadmap": "10% T+1, 20% T+30, 25% T+60, 25% T+90, 20% T+120"},
    "N6": {"name": "Style by PNJ (TS Kim cương / Đá màu / Ngọc trai)", "timeline": "T+120", "days": 120, "roadmap": "10% T+1, 20% T+30, 25% T+60, 25% T+90, 20% T+120"},
    "N7": {"name": "Style by PNJ (TS KGĐ / CZ / Dây chuyền)", "timeline": "T+7", "days": 7, "roadmap": "100% T+7"},
    "N8": {"name": "Danh mục Heart2Heart", "timeline": "T+7", "days": 7, "roadmap": "100% T+7"},
    "N9": {"name": "Danh mục Kind Heart / Phong thủy đặc biệt", "timeline": "T+7", "days": 7, "roadmap": "100% T+7"},
    "N10": {"name": "Vòng lắc charm phong thủy / Bao lì xì", "timeline": "T+7", "days": 7, "roadmap": "100% T+7"}
}

# Bảng ma trận Mapping cho phép cấn trừ chuyển đổi (Món cũ -> Món mới)
MAPPING_MATRIX = {
    "N1": ["N2", "N3", "N4", "N5", "N6", "N7"],
    "N2": ["N2", "N4"],
    "N3": ["N1", "N2", "N3", "N4"],
    "N4": ["N1", "N2", "N3", "N4"],
    "N5": ["N2", "N5"],
    "N6": ["N6"],
    "N7": ["N6", "N7"],
    "N8": ["N8"],
    "N9": ["N9"],
    "N10": ["N10"]
}

# =============================================================================
# 3. HEADER & THANH ĐIỀU HUỚNG SIDEBAR
# =============================================================================
head_left, head_right = st.columns([3, 1])
with head_left:
    st.markdown("<div class='main-title'>Chuyển đổi thanh toán – Hỏi nhanh</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Công cụ cấn trừ tự động & xuất lịch thanh toán theo quy định PNJ hiệu lực từ 30/09/2026</div>", unsafe_allow_html=True)
with head_right:
    today_str = datetime.now().strftime("%d/%m/%Y")
    st.markdown(f"<div style='text-align: right; color: #003468; font-weight: bold; font-size: 16px;'>Ngày: {today_str}</div>", unsafe_allow_html=True)

st.divider()

# Sidebar Setup
st.sidebar.markdown("## ⚙️ Bối Cảnh Vận Hành")
is_hub = st.sidebar.checkbox("Cửa hàng HUB (Trung tâm)", value=True, help="Các điểm HUB mới được quyền tiếp nhận mua lại và chi trả tiền.")
is_paid_new = st.sidebar.radio("Trạng thái HĐ mới", ["Chưa thanh toán", "Đã thanh toán"], index=0)
priority_policy = st.sidebar.selectbox("Tiêu chí cấn trừ", ["Ưu tiên giữ tiền công ty", "Thứ tự nhập"])

st.sidebar.divider()
st.sidebar.markdown("### 📋 Checklist Điều Kiện Tuân Thủ")
chk_hub = st.sidebar.checkbox("Tiếp nhận tại HUB", value=is_hub)
chk_nd232 = st.sidebar.checkbox("Tuân thủ NĐ 232/320/340", value=True)
chk_cust = st.sidebar.checkbox("Cùng Mã Khách Hàng", value=True)
chk_agree = st.sidebar.checkbox("Có Thỏa thuận PA2", value=True)
chk_no_early = st.sidebar.checkbox("Không hứa chi tiền sớm", value=True)

# =============================================================================
# 4. NHẬP LIỆU TÌNH HUỐNG GIAO DỊCH (BẢNG KÊ & HÓA ĐƠN)
# =============================================================================
col_left, col_right = st.columns(2)

# Khách bán / đổi (Bảng kê)
with col_left:
    st.subheader("📦 Khách bán / đổi (Bảng kê)")
    if "bk_list" not in st.session_state:
        # Mock dữ liệu mặc định đúng theo hình phieu_kiem_tra.jpg
        st.session_state.bk_list = [
            {"grp": "N1", "desc": "Vàng miếng / nhẫn khoen / PLT / Kim Bảo (T+2)", "val": 120000000},
            {"grp": "N4", "desc": "Vàng 22K–24K (91,6–99,99%) / Quà tặng sưu tầm (T+7)", "val": 140000000}
        ]

    bk_items = []
    total_bk = 0
    for idx, item in enumerate(st.session_state.bk_list):
        c1, c2, c3, c4 = st.columns([2, 4, 3, 1])
        with c1:
            grp = st.selectbox(f"Mã BK{idx+1}", list(GROUPS.keys()), index=list(GROUPS.keys()).index(item["grp"]), key=f"bk_g_{idx}")
        with c2:
            desc = st.text_input(f"Mô tả BK{idx+1}", value=item["desc"], key=f"bk_d_{idx}")
        with c3:
            val = st.number_input(f"Giá trị BK{idx+1} (đ)", value=int(item["val"]), step=1000000, key=f"bk_v_{idx}")
        with c4:
            if st.button("❌", key=f"del_bk_{idx}"):
                st.session_state.bk_list.pop(idx)
                st.rerun()
        bk_items.append({"id": f"BK{idx+1}", "grp": grp, "desc": desc, "val": val, "rem": val})
        total_bk += val

    if st.button("➕ Thêm món Bảng Kê (BK)"):
        st.session_state.bk_list.append({"grp": "N1", "desc": "Sản phẩm thu đổi cũ", "val": 10000000})
        st.rerun()

    st.markdown(f"<div style='text-align: right; font-weight: bold; font-size: 18px; color: #003468;'>Tổng: {total_bk:,.0f}đ</div>", unsafe_allow_html=True)

# Khách mua mới (Hóa đơn)
with col_right:
    st.subheader("🛒 Khách mua mới (Hóa đơn)")
    if "hd_list" not in st.session_state:
        # Mock dữ liệu mặc định đúng theo hình phieu_kiem_tra.jpg
        st.session_state.hd_list = [
            {"grp": "N2", "desc": "TS KC / đá màu / ngọc trai / vỏ", "val": 130000000},
            {"grp": "N4", "desc": "Vàng 22K–24K (91,6–99,99%) / Quà tặng sưu tầm", "val": 1000000}
        ]

    hd_items = []
    total_hd = 0
    for idx, item in enumerate(st.session_state.hd_list):
        c1, c2, c3, c4 = st.columns([2, 4, 3, 1])
        with c1:
            grp = st.selectbox(f"Mã HĐ{idx+1}", list(GROUPS.keys()), index=list(GROUPS.keys()).index(item["grp"]), key=f"hd_g_{idx}")
        with c2:
            desc = st.text_input(f"Mô tả HĐ{idx+1}", value=item["desc"], key=f"hd_d_{idx}")
        with c3:
            val = st.number_input(f"Giá trị HĐ{idx+1} (đ)", value=int(item["val"]), step=1000000, key=f"hd_v_{idx}")
        with c4:
            if st.button("❌", key=f"del_hd_{idx}"):
                st.session_state.hd_list.pop(idx)
                st.rerun()
        hd_items.append({"id": f"HĐ{idx+1}", "grp": grp, "desc": desc, "val": val, "need": val})
        total_hd += val

    if st.button("➕ Thêm món Hóa Đơn (HĐ)"):
        st.session_state.hd_list.append({"grp": "N2", "desc": "Sản phẩm mua mới", "val": 10000000})
        st.rerun()

    st.markdown(f"<div style='text-align: right; font-weight: bold; font-size: 18px; color: #003468;'>Tổng: {total_hd:,.0f}đ</div>", unsafe_allow_html=True)

st.divider()

# =============================================================================
# 5. XỬ LÝ LOGIC CẤN TRỪ & PHÂN LOẠI PHƯƠNG ÁN
# =============================================================================
offset_logs = []
total_offset = 0

bks = [dict(b) for b in bk_items]
hds = [dict(h) for h in hd_items]

# Thuật toán ghép món theo ma trận mapping
for h in hds:
    for b in bks:
        if b["rem"] <= 0:
            continue
        if h["need"] <= 0:
            break
        
        allowed_targets = MAPPING_MATRIX.get(b["grp"], [])
        if h["grp"] in allowed_targets:
            amount = min(b["rem"], h["need"])
            b["rem"] -= amount
            h["need"] -= amount
            total_offset += amount
            offset_logs.append({
                "bk_id": b["id"], "bk_grp": b["grp"], "bk_desc": b["desc"],
                "hd_id": h["id"], "hd_grp": h["grp"], "hd_desc": h["desc"],
                "amount": amount
            })

remaining_cash = total_bk - total_offset

# Phân loại phương án (PA1, PA2, PA3)
if total_bk <= total_hd and total_offset == total_bk:
    pa_code = "PA1"
    pa_label = "🟢 Chuyển đổi hoàn toàn · PA1"
    pa_css = "card-pa1"
elif remaining_cash > 0:
    if is_hub:
        pa_code = "PA2"
        pa_label = "🟠 Chuyển đổi một phần · PA2"
        pa_css = "card-pa2"
    else:
        pa_code = "PA3"
        pa_label = "🔴 Bắt buộc chuyển Cửa hàng HUB (Không thuộc thẩm quyền quầy thường)"
        pa_css = "card-pa3"
else:
    pa_code = "PA3"
    pa_label = "🔴 Mua lại hoàn toàn · PA3"
    pa_css = "card-pa3"

# =============================================================================
# 6. HIỂN THỊ KẾT QUẢ KHOẢN CẤN TRỪ & SƠ ĐỒ GHÉP MÓN
# =============================================================================
st.markdown("### KẾT QUẢ CẤN TRỪ & PHƯƠNG ÁN XỬ LÝ")

badge_txt = "Chỉ HUB" if is_hub else "Cửa Hàng Thường"
st.markdown(f"""
<div class='{pa_css}'>
    <span>{pa_label}</span>
    <span class='hub-badge'>{badge_txt}</span>
</div>
""", unsafe_allow_html=True)

col_m1, col_m2 = st.columns(2)
with col_m1:
    st.markdown(f"""
    <div class='metric-card'>
        <div style='color: #64748b; font-size: 14px; font-weight: 500;'>Cấn trừ Hóa đơn mới</div>
        <div style='color: #15803d; font-size: 28px; font-weight: bold; margin-top: 4px;'>{total_offset:,.0f}đ</div>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
    <div class='metric-card'>
        <div style='color: #64748b; font-size: 14px; font-weight: 500;'>Công ty chi trả sau theo lộ trình</div>
        <div style='color: #d97706; font-size: 28px; font-weight: bold; margin-top: 4px;'>{remaining_cash:,.0f}đ</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("#### 🔄 Chi tiết Sơ đồ ghép món cấn trừ (CÁCH GHÉP)")
if offset_logs:
    for log in offset_logs:
        st.markdown(f"""
        <div class='mapping-row'>
            🟢 <b>{log['bk_id']} · {log['bk_desc']}</b> ─── [cấn trừ: <span style='color: #15803d; font-weight: bold;'>{log['amount']:,.0f}đ</span>] ─── 🎯 <b>{log['hd_id']} · {log['hd_desc']}</b>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Không có món nào đáp ứng Ma trận Mapping để thực hiện cấn trừ.")

# Danh mục dư chi trả
unmatched_bks = [b for b in bks if b["rem"] > 0]
if unmatched_bks:
    st.markdown("##### ⏳ Danh mục món dư chuyển sang chi trả lộ trình:")
    for b in unmatched_bks:
        ginfo = GROUPS.get(b["grp"], {})
        st.markdown(f"• **{b['id']} · {b['desc']}**: dư **{b['rem']:,.0f}đ** ➔ Lộ trình **{ginfo.get('timeline', 'T+7')}** ({ginfo.get('roadmap', '')})")

st.divider()

# =============================================================================
# 7. KỊCH BẢN TƯ VẤN KHÁCH HÀNG & LỊCH NHẬN TIỀN
# =============================================================================
c_say, c_sched = st.columns([3, 2])

# Tìm ngày nhận tiền dự kiến
max_d = 7
for b in unmatched_bks:
    d = GROUPS.get(b["grp"], {}).get("days", 7)
    if d > max_d:
        max_d = d
target_date = (datetime.now() + timedelta(days=max_d)).strftime("%d/%m")

with c_say:
    st.markdown("#### 🗣️ TRẢ LỜI KHÁCH (Kịch bản tư vấn chuẩn)")
    if remaining_cash > 0:
        speech = f"“{total_offset:,.0f}đ giá trị món cũ được trừ thẳng vào hóa đơn mới. Phần còn lại {remaining_cash:,.0f}đ công ty chuyển khoản theo lộ trình: {remaining_cash:,.0f}đ ngày {target_date}.”"
    else:
        speech = f"“Toàn bộ {total_offset:,.0f}đ giá trị món cũ của quý khách đã được cấn trừ 100% vào hóa đơn mới hôm nay.”"

    st.markdown(f"""
    <div class='quote-box'>
        💬 {speech}
    </div>
    """, unsafe_allow_html=True)

with c_sched:
    st.markdown("#### 🗓️ LỊCH NHẬN TIỀN")
    if remaining_cash > 0:
        st.markdown(f"""
        <div class='timeline-card'>
            <div style='background-color: #2563eb; color: white; display: inline-block; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 13px;'>
                {GROUPS.get(unmatched_bks[0]['grp'], {}).get('timeline', 'T+7')} · {target_date}
            </div>
            <div style='color: #1e3a8a; font-size: 22px; font-weight: bold; margin-top: 8px;'>{remaining_cash:,.0f}đ</div>
            <div style='color: #64748b; font-size: 12px; margin-top: 2px;'>Chuyển khoản trực tiếp vào TK ngân hàng KH</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("Không phát sinh tiền mặt chi trả sau.")

st.caption("Căn cứ: TB 442-2026 · HĐ 355-2026. Kết quả là đề xuất tự động; KTT khu vực quyết định trường hợp đặc biệt.")
