import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ==========================================
# CẤU HÌNH TRANG STREAMLIT
# ==========================================
st.set_page_config(
    page_title="PNJ - Tra Cứu & Hướng Dẫn Thu Đổi",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho phong cách PNJ (Xanh navy #003468 & Vàng kim #C5A059)
st.markdown("""
<style>
    .main-header {
        background-color: #003468;
        padding: 18px 25px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: #F7D070 !important;
        margin: 0;
        font-size: 26px;
        font-weight: 700;
    }
    .main-header p {
        color: #E0E0E0;
        margin: 5px 0 0 0;
        font-size: 14px;
    }
    .card-pa {
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 15px;
        color: white;
        font-weight: bold;
    }
    .pa1-bg { background-color: #28a745; }
    .pa2-bg { background-color: #d39e00; }
    .pa3-bg { background-color: #dc3545; }
    
    .guide-box {
        background-color: #f8f9fa;
        border-left: 5px solid #003468;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    .step-number {
        background-color: #003468;
        color: #F7D070;
        font-weight: bold;
        padding: 4px 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f1f3f5;
        border-radius: 6px 6px 0 0;
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #003468 !important;
        color: #F7D070 !important;
    }
    /* Style nút xóa */
    .del-btn-container {
        margin-top: 28px;
    }
</style>
""", unsafe_allow_html=True)

# Header chung
st.markdown("""
<div class="main-header">
    <h1>💎 PNJ - HỆ THỐNG TRA CỨU & HƯỚNG DẪN THU ĐỔI CHUYỂN ĐỔI</h1>
    <p>Áp dụng theo QĐ 442-2026-TB-P.VHBL-TĐTGTTHML-PNJ & PL A2 (Hiệu lực từ 30/09/2026)</p>
</div>
""", unsafe_allow_html=True)

# Dữ liệu ma trận nhóm hàng & Lộ trình thanh toán
GROUPS_INFO = {
    # --- NHÓM T+2 ---
    "N1": {
        "name": "Vàng miếng, Nhẫn khoen, Vàng Phúc Lộc Tài, Kim Bảo",
        "allowed_to": ["N2", "N3", "N4", "N5", "N6", "N7"],
        "payment": "T+2",
        "schedule": "100% sau 2 ngày làm việc (T+2)"
    },
    
    # --- NHÓM T+7 ---
    "N3": {
        "name": "TS Công nghệ Ý, KGĐ, Dây chuyền, ECZ/CZ",
        "allowed_to": ["N2", "N3", "N5"],
        "payment": "T+7",
        "schedule": "100% sau 7 ngày làm việc (T+7)"
    },
    "N4": {
        "name": "Vàng 21.9K - 24K (91.6% - 99.99%), Quà tặng sưu tầm",
        "allowed_to": ["N2", "N3", "N4", "N5"],
        "payment": "T+7",
        "schedule": "100% sau 7 ngày làm việc (T+7)"
    },
    "N7": {
        "name": "Style by PNJ (KGĐ, CZ/ECZ, Dây chuyền)",
        "allowed_to": ["N6", "N7"],
        "payment": "T+7",
        "schedule": "100% sau 7 ngày làm việc (T+7)"
    },
    "N8": {
        "name": "Danh mục Heart2Heart",
        "allowed_to": ["N8"],
        "payment": "T+7",
        "schedule": "100% sau 7 ngày làm việc (T+7)"
    },
    "N9": {
        "name": "Danh mục Kind Heart",
        "allowed_to": ["N9"],
        "payment": "T+7",
        "schedule": "100% sau 7 ngày làm việc (T+7)"
    },
    "N10": {
        "name": "Charm phong thủy đặc biệt, Bao lì xì phong thủy",
        "allowed_to": ["N10"],
        "payment": "T+7",
        "schedule": "100% sau 7 ngày làm việc (T+7)"
    },

    # --- NHÓM T+120 ---
    "N2": {
        "name": "TS Kim Cương, Đá màu, Ngọc trai, TS Vỏ (Không gồm Style)",
        "allowed_to": ["N2", "N5"],
        "payment": "T+120",
        "schedule": "10% (T/T+1) | 20% (T+30) | 25% (T+60) | 25% (T+90) | 20% (T+120)"
    },
    "N5": {
        "name": "Kim cương rời, Đá màu rời, Ngọc trai rời, Vòng cẩm thạch",
        "allowed_to": ["N2", "N5"],
        "payment": "T+120",
        "schedule": "10% (T/T+1) | 20% (T+30) | 25% (T+60) | 25% (T+90) | 20% (T+120)"
    },
    "N6": {
        "name": "Style by PNJ (TS Kim cương, Đá màu, Ngọc trai)",
        "allowed_to": ["N6"],
        "payment": "T+120",
        "schedule": "10% (T/T+1) | 20% (T+30) | 25% (T+60) | 25% (T+90) | 20% (T+120)"
    }
}

# KHỞI TẠO SESSION STATE CHO DANH SÁCH MÓN
if 'old_items' not in st.session_state:
    st.session_state.old_items = [
        {'id': 1, 'group': None, 'val': 0}
    ]
if 'new_items' not in st.session_state:
    st.session_state.new_items = [
        {'id': 1, 'group': None, 'val': 0}
    ]
if 'next_old_id' not in st.session_state:
    st.session_state.next_old_id = 2
if 'next_new_id' not in st.session_state:
    st.session_state.next_new_id = 2

# ==========================================
# KHỞI TẠO CÁC TAB CHÍNH
# ==========================================
tab_calculator, tab_user_guide, tab_matrix, tab_faq = st.tabs([
    "📋 1. TÍNH TOÁN CẤN TRỪ & PHƯƠNG ÁN THANH TOÁN",
    "📖 2. HƯỚNG DẪN QUY TRÌNH THU ĐỔI (DÀNH CHO KHÁCH & NV)",
    "📊 3. MA TRẬN MAPPING & LỘ TRÌNH THANH TOÁN",
    "❓ 4. HỎI ĐÁP Q&A THƯỜNG GẶP"
])

# ==========================================
# TAB 1: TÍNH TOÁN CẤN TRỪ (PHIẾU KIỂM TRA)
# ==========================================
with tab_calculator:
    st.subheader("📋 Tính Toán Cấn Trừ & Xác Định Phương Án Thanh Toán")
    
    col_input1, col_input2 = st.columns(2)
    
    # ------------------------------------------
    # CỘT 1: HÀNG CỦ (BẢNG KÊ)
    # ------------------------------------------
    with col_input1:
        st.markdown("### 🛍️ 1. Hàng Cũ Thu Đổi / Mua Lại (Bảng kê)")
        
        old_items_processed = []
        total_old_val = 0
        to_delete_old = None

        for idx, item in enumerate(st.session_state.old_items):
            c_group, c_val, c_del = st.columns([5.5, 3.2, 1.3])
            
            # Format hiển thị nhóm hàng
            def format_group_old(x):
                if x is None or x == "":
                    return "❓ -- Chọn nhóm hàng --"
                info = GROUPS_INFO[x]
                return f"[{info['payment']}] N{x[1:]} - {info['name'][:30]}..."

            options_list = [None] + list(GROUPS_INFO.keys())
            curr_index = options_list.index(item['group']) if item['group'] in options_list else 0

            with c_group:
                selected_g = st.selectbox(
                    f"Món BK{idx+1}:",
                    options=options_list,
                    index=curr_index,
                    format_func=format_group_old,
                    key=f"old_g_select_{item['id']}"
                )
                item['group'] = selected_g

            with c_val:
                val = st.number_input(
                    f"Giá trị BK{idx+1} (VNĐ):",
                    min_value=0,
                    value=item['val'],
                    step=1000000,
                    key=f"old_val_input_{item['id']}"
                )
                item['val'] = val

            with c_del:
                st.markdown("<div class='del-btn-container'></div>", unsafe_allow_html=True)
                if st.button("🗑️ Xóa", key=f"del_old_{item['id']}", help="Xóa món này"):
                    to_delete_old = item['id']

            if item['group'] is not None and item['val'] > 0:
                old_items_processed.append({
                    "id": f"BK{idx+1}",
                    "group": item['group'],
                    "name": GROUPS_INFO[item['group']]["name"],
                    "value": item['val'],
                    "payment": GROUPS_INFO[item['group']]["payment"],
                    "schedule": GROUPS_INFO[item['group']]["schedule"]
                })
                total_old_val += item['val']

        # Xử lý xóa món cũ nếu click nút Xóa
        if to_delete_old is not None:
            st.session_state.old_items = [x for x in st.session_state.old_items if x['id'] != to_delete_old]
            st.rerun()

        # Nút Thêm Món Cũ
        if st.button("➕ Thêm món cũ (BK)", key="add_old_btn"):
            st.session_state.old_items.append({
                'id': st.session_state.next_old_id,
                'group': None,
                'val': 0
            })
            st.session_state.next_old_id += 1
            st.rerun()

        st.metric("TỔNG GIÁ TRỊ HÀNG CỦ (BK):", f"{total_old_val:,.0f} VNĐ")

    # ------------------------------------------
    # CỘT 2: HÀNG MỚI (HÓA ĐƠN)
    # ------------------------------------------
    with col_input2:
        st.markdown("### 🛒 2. Hàng Mới Khách Mua (Hóa đơn)")
        
        new_items_processed = []
        total_new_val = 0
        to_delete_new = None

        for idx, item in enumerate(st.session_state.new_items):
            c_group, c_val, c_del = st.columns([5.5, 3.2, 1.3])
            
            def format_group_new(x):
                if x is None or x == "":
                    return "❓ -- Chọn nhóm hàng --"
                info = GROUPS_INFO[x]
                return f"[{info['payment']}] N{x[1:]} - {info['name'][:30]}..."

            options_list_new = [None] + list(GROUPS_INFO.keys())
            curr_index_new = options_list_new.index(item['group']) if item['group'] in options_list_new else 0

            with c_group:
                selected_g_new = st.selectbox(
                    f"Món HĐ{idx+1}:",
                    options=options_list_new,
                    index=curr_index_new,
                    format_func=format_group_new,
                    key=f"new_g_select_{item['id']}"
                )
                item['group'] = selected_g_new

            with c_val:
                val = st.number_input(
                    f"Giá trị HĐ{idx+1} (VNĐ):",
                    min_value=0,
                    value=item['val'],
                    step=1000000,
                    key=f"new_val_input_{item['id']}"
                )
                item['val'] = val

            with c_del:
                st.markdown("<div class='del-btn-container'></div>", unsafe_allow_html=True)
                if st.button("🗑️ Xóa", key=f"del_new_{item['id']}", help="Xóa món này"):
                    to_delete_new = item['id']

            if item['group'] is not None and item['val'] > 0:
                new_items_processed.append({
                    "id": f"HĐ{idx+1}",
                    "group": item['group'],
                    "name": GROUPS_INFO[item['group']]["name"],
                    "value": item['val'],
                    "rem_val": item['val']
                })
                total_new_val += item['val']

        # Xử lý xóa món mới nếu click nút Xóa
        if to_delete_new is not None:
            st.session_state.new_items = [x for x in st.session_state.new_items if x['id'] != to_delete_new]
            st.rerun()

        # Nút Thêm Món Mới
        if st.button("➕ Thêm món mới (HĐ)", key="add_new_btn"):
            st.session_state.new_items.append({
                'id': st.session_state.next_new_id,
                'group': None,
                'val': 0
            })
            st.session_state.next_new_id += 1
            st.rerun()

        st.metric("TỔNG GIÁ TRỊ HÀNG MỚI (HĐ):", f"{total_new_val:,.0f} VNĐ")

    st.markdown("---")
    
    # Điều kiện vận hành
    st.markdown("### ⚙️ Điều Kiện Vận Hành & Tuân Thủ Quầy")
    col_cond1, col_cond2, col_cond3 = st.columns(3)
    with col_cond1:
        is_hub = st.checkbox("Cửa hàng là Điểm Trung Tâm (HUB)?", value=True)
    with col_cond2:
        same_customer = st.checkbox("Hóa đơn cũ & mới CÙNG MÃ KHÁCH HÀNG?", value=True)
    with col_cond3:
        prefer_company = st.checkbox("Ưu tiên cấn trừ tối đa vào hóa đơn mới?", value=True)

    # ------------------------------------------
    # THUẬT TOÁN TÍNH TOÁN CẤN TRỪ
    # ------------------------------------------
    can_tru_list = []
    du_item_list = []
    total_can_tru = 0
    total_chi_sau = 0
    
    # Tạo copy danh sách món mới để trừ dần
    new_pool = [{**item} for item in new_items_processed]
    
    for old in old_items_processed:
        old_val_rem = old["value"]
        
        # Tìm các món mới có ma trận cho phép
        for new in new_pool:
            if old_val_rem <= 0:
                break
            if new["rem_val"] <= 0:
                continue
                
            # Kiểm tra mapping
            allowed_groups = GROUPS_INFO[old["group"]]["allowed_to"]
            if new["group"] in allowed_groups:
                matched_amount = min(old_val_rem, new["rem_val"])
                can_tru_list.append({
                    "old_id": old["id"],
                    "old_group": old["group"],
                    "old_name": old["name"],
                    "new_id": new["id"],
                    "new_group": new["group"],
                    "new_name": new["name"],
                    "amount": matched_amount
                })
                old_val_rem -= matched_amount
                new["rem_val"] -= matched_amount
                total_can_tru += matched_amount
                
        if old_val_rem > 0:
            du_item_list.append({
                "id": old["id"],
                "group": old["group"],
                "name": old["name"],
                "amount": old_val_rem,
                "payment": old["payment"],
                "schedule": old["schedule"]
            })
            total_chi_sau += old_val_rem

    # ------------------------------------------
    # XÁC ĐỊNH PHƯƠNG ÁN
    # ------------------------------------------
    st.markdown("---")
    st.markdown("### 🎯 KẾT QUẢ PHÂN LOẠI PHƯƠNG ÁN THANH TOÁN")
    
    # Cảnh báo nếu chưa chọn nhóm hàng
    has_unselected_old = any(x['group'] is None for x in st.session_state.old_items if x['val'] > 0)
    has_unselected_new = any(x['group'] is None for x in st.session_state.new_items if x['val'] > 0)
    
    if has_unselected_old or has_unselected_new:
        st.warning("⚠️ Vui lòng chọn Nhóm Hàng cho tất cả các món để hệ thống tính toán cấn trừ và phân loại chính xác!")

    if total_old_val == 0 and total_new_val == 0:
        st.info("👋 Hãy chọn Nhóm hàng và nhập giá trị món hàng ở trên để bắt đầu tính toán.")
    elif total_new_val == 0:
        pa_code = "PA3"
        pa_title = "🔴 Phương Án 3: MUA LẠI HOÀN TOÀN"
        pa_bg = "pa3-bg"
        pa_desc = "Khách hàng bán lại sản phẩm và không phát sinh hóa đơn mua mới."
    elif total_chi_sau == 0 and total_can_tru == total_old_val:
        pa_code = "PA1"
        pa_title = "🟢 Phương Án 1: CHUYỂN ĐỔI HOÀN TOÀN"
        pa_bg = "pa1-bg"
        pa_desc = "Toàn bộ giá trị sản phẩm cũ được cấn trừ hết vào hóa đơn mới. Khách hàng đóng thêm tiền chênh lệch (nếu có)."
    else:
        pa_code = "PA2"
        pa_title = "🟡 Phương Án 2: CHUYỂN ĐỔI MỘT PHẦN (Chỉ thực hiện tại Cửa Hàng HUB)"
        pa_bg = "pa2-bg"
        pa_desc = f"Cấn trừ {total_can_tru:,.0f} VNĐ vào hóa đơn mới. Công ty sẽ chi trả lại phần tiền thừa {total_chi_sau:,.0f} VNĐ cho khách theo lộ trình thanh toán."

    if total_old_val > 0 or total_new_val > 0:
        st.markdown(f"""
        <div class="card-pa {pa_bg}">
            <h3 style="margin:0; color:white;">{pa_title}</h3>
            <p style="margin:5px 0 0 0; font-weight:normal;">{pa_desc}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Chi tiết cấn trừ & chi trả
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.success(f"**Tổng tiền cấn trừ ngay:** {total_can_tru:,.0f} VNĐ")
            if can_tru_list:
                st.markdown("**Sơ đồ ghép cấn trừ chi tiết:**")
                for ct in can_tru_list:
                    st.write(f"• **{ct['old_id']}** (N{ct['old_group'][1:]}) ➔ Cấn trừ **{ct['amount']:,.0f} VNĐ** sang **{ct['new_id']}** (N{ct['new_group'][1:]})")
            else:
                st.write("Không có món nào thỏa điều kiện ma trận cấn trừ.")
                
        with res_col2:
            st.warning(f"**Công ty chi trả sau (Theo lộ trình):** {total_chi_sau:,.0f} VNĐ")
            if du_item_list:
                st.markdown("**Chi tiết dư chi trả sau:**")
                for du in du_item_list:
                    st.write(f"• **{du['id']}** (N{du['group'][1:]}): Dư **{du['amount']:,.0f} VNĐ** ➔ Lộ trình **{du['payment']}** ({du['schedule']})")
            else:
                st.write("Không có số tiền thừa chi trả sau.")

        # Kịch bản tư vấn chuẩn
        st.markdown("---")
        st.markdown("### 🗣️ KỊCH BẢN TƯ VẤN MẪU CHO NHÂN VIÊN (ĐỌC CHO KHÁCH HÀNG)")
        
        today_str = datetime.now().strftime("%d/%m/%Y")
        if pa_code == "PA1":
            script_text = f"“Dạ em chào Anh/Chị, tổng giá trị các món cũ của Anh/Chị là {total_old_val:,.0f}đ đã được cấn trừ 100% thẳng vào hóa đơn mua hàng mới trị giá {total_new_val:,.0f}đ. Anh/Chị chỉ cần thanh toán phần chênh lệch còn lại là {max(0, total_new_val - total_old_val):,.0f}đ ạ.”"
        elif pa_code == "PA2":
            max_payment_term = "T+7"
            if any(d['payment'] == 'T+120' for d in du_item_list):
                max_payment_term = "T+120"
            elif any(d['payment'] == 'T+2' for d in du_item_list):
                max_payment_term = "T+2"
                
            script_text = f"“Dạ em chào Anh/Chị, tổng giá trị món cũ của Anh/Chị là {total_old_val:,.0f}đ. Em đã hỗ trợ cấn trừ {total_can_tru:,.0f}đ trực tiếp vào hóa đơn mới. Số tiền dư còn lại là {total_chi_sau:,.0f}đ, PNJ sẽ chuyển khoản chi trả lại cho Anh/Chị theo đúng lộ trình cam kết ({max_payment_term}) tính từ ngày hôm nay {today_str} ạ.”"
        else:
            script_text = f"“Dạ em chào Anh/Chị, giao dịch bán lại sản phẩm của Anh/Chị có tổng trị giá là {total_old_val:,.0f}đ. PNJ tiếp nhận giao dịch và sẽ chuyển khoản thanh toán cho Anh/Chị theo đúng lộ trình quy định của công ty từ 15h00-17h00 hàng ngày ạ.”"
            
        st.info(script_text)

        # Checklist tuân thủ
        st.markdown("### 📝 Checklist Tuân Thủ Vận Hành Quầy")
        c_chk1, c_chk2, c_chk3, c_chk4 = st.columns(4)
        with c_chk1:
            st.checkbox("Đã kiểm tra điều kiện HUB", value=is_hub)
        with c_chk2:
            st.checkbox("Tuân thủ NĐ 232/320/340", value=True)
        with c_chk3:
            st.checkbox("In Phụ lục 01 (Lập 2 bản)", value=(pa_code == "PA2"))
        with c_chk4:
            st.checkbox("Không hứa hẹn chi tiền sớm", value=True)


# ==========================================
# TAB 2: HƯỚNG DẪN QUY TRÌNH THU ĐỔI (DÀNH CHO USER & NV)
# ==========================================
with tab_user_guide:
    st.subheader("📖 Hướng Dẫn Chi Tiết Quy Trình Thu Đổi & Mua Lại Sản Phẩm PNJ")
    st.write("Tài liệu hướng dẫn trực quan dành cho Khách hàng và Nhân viên tư vấn bán hàng toàn hệ thống PNJ.")
    
    st.markdown("---")
    
    # 1. Tóm tắt 3 Phương án
    st.markdown("## 📍 1. Hiểu Rõ 3 Phương Án Thu Đổi & Thanh Toán")
    
    col_pa1, col_pa2, col_pa3 = st.columns(3)
    
    with col_pa1:
        st.markdown("""
        <div style="background-color:#e8f5e9; border:2px solid #28a745; padding:15px; border-radius:8px; height:100%;">
            <h4 style="color:#28a745; margin-top:0;">🟢 PA1: ĐỔI HOÀN TOÀN</h4>
            <p><b>Điều kiện:</b> Món mới ≥ Món cũ & thỏa ma trận mapping nhóm hàng.</p>
            <p><b>Quyền lợi:</b> Cấn trừ 100% giá trị món cũ vào hóa đơn mới.</p>
            <p><b>Nơi thực hiện:</b> Áp dụng tại <b>TẤT CẢ các cửa hàng PNJ</b> toàn quốc.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_pa2:
        st.markdown("""
        <div style="background-color:#fff3cd; border:2px solid #ffc107; padding:15px; border-radius:8px; height:100%;">
            <h4 style="color:#856404; margin-top:0;">🟡 PA2: ĐỔI MỘT PHẦN</h4>
            <p><b>Điều kiện:</b> Món mới < Món cũ (dư tiền thừa).</p>
            <p><b>Quyền lợi:</b> Cấn trừ món mới, phần tiền thừa PNJ chuyển khoản chi trả theo lộ trình.</p>
            <p><b>Nơi thực hiện:</b> <b>BẮT BUỘC thực hiện tại Cửa hàng HUB</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_pa3:
        st.markdown("""
        <div style="background-color:#f8d7da; border:2px solid #dc3545; padding:15px; border-radius:8px; height:100%;">
            <h4 style="color:#721c24; margin-top:0;">🔴 PA3: MUA LẠI HOÀN TOÀN</h4>
            <p><b>Điều kiện:</b> Bán lại sản phẩm, không mua món mới.</p>
            <p><b>Quyền lợi:</b> Nhận 100% tiền mua lại qua tài khoản ngân hàng theo lộ trình.</p>
            <p><b>Nơi thực hiện:</b> <b>BẮT BUỘC tại Cửa hàng HUB</b> (Khung giờ: 15h00 - 17h00).</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 2. Quy trình 4 bước
    st.markdown("## 🔄 2. Quy Trình 4 Bước Tiếp Nhận & Xử Lý Thu Đổi")
    
    st.markdown("""
    <div class="guide-box">
        <h4><span class="step-number">1</span> Bước 1: Kiểm Tra Sản Phẩm & Chứng Từ Pháp Lý</h4>
        <ul>
            <li><b>Kiểm tra hiện trạng:</b> Sản phẩm nguyên hiện trạng (không móp méo, biến dạng, không mất đá chính/phụ, đúng dung sai trọng lượng ±0.006 chỉ).</li>
            <li><b>Chứng từ đi kèm:</b> Hóa đơn mua hàng PNJ (hoặc trích lục hệ thống SAP/mPos), Giấy giám định đá quý GIA/PNJL (nếu có).</li>
            <li><b>Mã khách hàng:</b> Kiểm tra Mã Khách Hàng trên hóa đơn cũ và hóa đơn mới phải <b>CÙNG 1 MÃ KHÁCH HÀNG</b>.</li>
        </ul>
    </div>
    
    <div class="guide-box">
        <h4><span class="step-number">2</span> Bước 2: Phân Loại Nhóm Hàng & Tra Cứu Ma Trận Mapping</h4>
        <ul>
            <li>Xác định mã nhóm hàng cũ (từ N1 đến N10) và mã nhóm hàng mới.</li>
            <li>Tra cứu bảng Ma trận Mapping để kiểm tra nhóm hàng cũ có được phép chuyển đổi sang nhóm hàng mới hay không.</li>
        </ul>
    </div>

    <div class="guide-box">
        <h4><span class="step-number">3</span> Bước 3: Lập Bảng Kê & Phụ Lục Thỏa Thuận (PA2 / PA3)</h4>
        <ul>
            <li>Đối với giao dịch PA2 hoặc PA3 (có phát sinh chi trả tiền): Lập <b>Bảng kê Mẫu 02/TNDN</b> và <b>Phụ lục 01 Thỏa thuận Thu đổi</b>.</li>
            <li>In 2 bản Phụ lục 01: Khách hàng ký tên xác nhận, cửa hàng lưu 1 bản và giao khách hàng 1 bản.</li>
            <li>Kiểm tra Hạn mức Quota chi trả trong ngày của HUB (Khung giờ từ 15h00 đến 17h00).</li>
        </ul>
    </div>

    <div class="guide-box">
        <h4><span class="step-number">4</span> Bước 4: Hoàn Tất Giao Dịch & Thanh Toán Theo Lộ Trình</h4>
        <ul>
            <li><b>PA1:</b> Hoàn tất hóa đơn mới ngay tại quầy.</li>
            <li><b>PA2 & PA3:</b> Tiền chi trả sẽ được PNJ chuyển khoản vào tài khoản ngân hàng của khách theo đúng mốc lịch (T+2, T+7 hoặc T+120).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 3. Phân biệt HUB và CH Thường
    st.markdown("## 🏬 3. Phân Biệt Phân Quyền Cửa Hàng HUB vs Cửa Hàng Thường")
    
    col_hub1, col_hub2 = st.columns(2)
    
    with col_hub1:
        st.info("""
        ### 🏢 CỬA HÀNG THƯỜNG (Standard Store)
        * **Chỉ tiếp nhận:** Giao dịch **Đổi Sản Phẩm Mới (PA1)**.
        * **Điều kiện:** Giá trị món mới $\\ge$ Giá trị món cũ và thỏa ma trận chuyển đổi.
        * **KHÔNG tiếp nhận:** Bất kỳ giao dịch nào phát sinh nghĩa vụ **chi trả lại tiền** cho khách hàng.
        """)
        
    with col_hub2:
        st.success("""
        ### 🏢 CỬA HÀNG DẠNG HUB (Point Central Store)
        * **Tiếp nhận:** **TẤT CẢ** các giao dịch (PA1, PA2, PA3).
        * **Khung giờ tiếp nhận Mua Lại (PA2/PA3):** Từ **15h00 đến 17h00** mỗi ngày.
        * **Quản trị Quota:** Kiểm soát hạn mức tiền mặt/chi trả theo ngày được duyệt bởi Kế toán trưởng Chi nhánh.
        """)


# ==========================================
# TAB 3: MA TRẬN MAPPING & LỘ TRÌNH THANH TOÁN
# ==========================================
with tab_matrix:
    st.subheader("📊 Bảng Ma Trận Mapping Nhóm Hàng & Lộ Trình Thanh Toán PNJ")
    
    st.markdown("### 1. Bảng Tổng Hợp Nhóm Hàng & Lộ Trình Chi Trả")
    
    matrix_data = []
    for code, info in GROUPS_INFO.items():
        matrix_data.append({
            "Mã Nhóm": code,
            "Tên Dòng Sản Phẩm": info["name"],
            "Nhóm Cho Phép Đổi Sang": ", ".join(info["allowed_to"]),
            "Thời Gian Thanh Toán": info["payment"],
            "Chi Tiết Lộ Trình Chi Trả": info["schedule"]
        })
        
    df_matrix = pd.DataFrame(matrix_data)
    st.dataframe(df_matrix, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### 2. Chi Tiết Lộ Trình Thanh Toán T+120 Ngày (Cho Nhóm 2, 5, 6)")
    
    c_lt1, c_lt2, c_lt3, c_lt4, c_lt5 = st.columns(5)
    with c_lt1:
        st.metric("Đợt 1 (T / T+1)", "10%", "Thanh toán ngay/Ngày sau")
    with c_lt2:
        st.metric("Đợt 2 (T + 30)", "20%", "Sau 30 ngày")
    with c_lt3:
        st.metric("Đợt 3 (T + 60)", "25%", "Sau 60 ngày")
    with c_lt4:
        st.metric("Đợt 4 (T + 90)", "25%", "Sau 90 ngày")
    with c_lt5:
        st.metric("Đợt 5 (T + 120)", "20%", "Sau 120 ngày")


# ==========================================
# TAB 4: HỎI ĐÁP Q&A THƯỜNG GẶP
# ==========================================
with tab_faq:
    st.subheader("❓ Các Câu Hỏi Thường Gặp Của Nhân Viên & Khách Hàng (Q&A)")
    
    with st.expander("Q1: Khách hàng muốn bán lại món cũ nhưng cửa hàng không phải HUB thì làm thế nào?"):
        st.write("👉 **Trả lời:** Cửa hàng thường không có chức năng tiếp nhận giao dịch Mua lại (PA3) hoặc Chuyển đổi một phần (PA2). Nhân viên hướng dẫn khách hàng đến Cửa hàng HUB gần nhất trong khung giờ từ 15h00 đến 17h00 để thực hiện.")

    with st.expander("Q2: Hóa đơn cũ và Hóa đơn mới khác tên / khác Mã Khách Hàng có được đổi PA1/PA2 không?"):
        st.write("👉 **Trả lời:** Theo quy định, Hóa đơn cũ và Hóa đơn mới **bắt buộc phải cùng 1 Mã Khách Hàng** thì mới được áp dụng tỷ lệ đổi theo chính sách cam kết.")

    with st.expander("Q3: Sản phẩm bị mất đá tấm hoặc móp méo nhẹ thì tính giá thu đổi như thế nào?"):
        st.write("👉 **Trả lời:** Sản phẩm không nguyên hiện trạng sẽ được xử lý theo Phụ lục A2: Trừ giá trị đá bị mất theo giá niêm yết hiện hành; nếu hao hụt trọng lượng vàng ngoài dung sai ±0.006 chỉ sẽ tính theo giá nguyên liệu thực tế tại thời điểm thu đổi.")

    with st.expander("Q4: Khách hàng chọn Phương án 2 (PA2) thì cần ký những giấy tờ gì?"):
        st.write("👉 **Trả lời:** Cửa hàng cần lập Bảng kê Mẫu 02/TNDN kèm Phụ lục số 01 (Thỏa thuận thu đổi sản phẩm). Phụ lục số 01 in thành 2 bản, khách hàng và cửa hàng ký xác nhận, giao khách giữ 1 bản.")

    with st.expander("Q5: Lộ trình thanh toán T+2, T+7, T+120 được tính bắt đầu từ khi nào?"):
        st.write("👉 **Trả lời:** Ngày T là ngày giao dịch được tiếp nhận và xác lập hoàn tất hồ sơ trên hệ thống tại Cửa hàng HUB.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 13px;">
    © 2026 Phu Nhuan Jewelry Joint Stock Company (PNJ). Bản quyền thuộc về Khối Bán Lẻ & Vận Hành.
</div>
""", unsafe_allow_html=True)
