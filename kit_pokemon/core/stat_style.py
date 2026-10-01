def get_stat_color(value: int) -> str:
    if value < 60:
        return "#FF4D4D"
    elif value < 90:
        return "#FFCC00"
    elif value < 120:
        return "#4CAF50"
    else:
        return "#2E7D32"


def get_stat_color_name(value: int) -> str:
    if value < 60:
        return "red"
    elif value < 90:
        return "orange"
    elif value < 120:
        return "green"
    else:
        return "darkgreen"


def calc_hp_min_max(base: int) -> tuple[int, int]:
    min_val = (2 * base) + 110
    max_val = (2 * base) + 204
    return min_val, max_val


def calc_other_min_max(base: int) -> tuple[int, int]:
    min_val = int(((2 * base) + 5) * 0.9)
    max_val = int(((2 * base) + 99) * 1.1)
    return min_val, max_val


def render_stat_row(base: int, label: str, is_hp: bool = False, bar_width: int = 180) -> str:
    if is_hp:
        min_val, max_val = calc_hp_min_max(base)
    else:
        min_val, max_val = calc_other_min_max(base)

    pct = min(base / 180, 1.0)
    color = get_stat_color(base)
    filled_width = int(bar_width * pct)

    return f'''
    <div style="margin: 4px 0;">
        <div style="display: flex; align-items: center; gap: 8px; font-family: 'Segoe UI', sans-serif;">
            <span style="width: 70px; font-weight: 600; font-size: 13px; color: #333;">{label}</span>
            <span style="width: 40px; text-align: right; font-weight: bold; font-size: 13px; color: {color};">{base}</span>
            <div style="flex: 1; max-width: {bar_width}px; height: 18px; background: #e8e8e8; border-radius: 9px; overflow: hidden;">
                <div style="width: {filled_width}px; height: 100%; background: {color}; border-radius: 9px; transition: width 0.3s;"></div>
            </div>
            <span style="width: 55px; text-align: right; font-size: 12px; color: #666; font-family: monospace;">{min_val}</span>
            <span style="width: 55px; text-align: right; font-size: 12px; color: #666; font-family: monospace;">{max_val}</span>
        </div>
    </div>
    '''


def render_stat_bar_html(base: int, label: str = "", max_val: int = 180, is_hp: bool = False, width: int = 180) -> str:
    return render_stat_row(base, label, is_hp, width)


def inject_stat_css():
    import streamlit as st
    st.markdown("""
    <style>
    .stat-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 4px 0;
        font-family: 'Segoe UI', sans-serif;
    }
    .stat-label {
        width: 70px;
        font-weight: 600;
        font-size: 13px;
        color: #333;
    }
    .stat-base {
        width: 40px;
        text-align: right;
        font-weight: bold;
        font-size: 13px;
    }
    .stat-bar-track {
        flex: 1;
        max-width: 180px;
        height: 18px;
        background: #e8e8e8;
        border-radius: 9px;
        overflow: hidden;
    }
    .stat-bar-fill {
        height: 100%;
        border-radius: 9px;
        transition: width 0.3s;
    }
    .stat-minmax {
        width: 55px;
        text-align: right;
        font-size: 12px;
        color: #666;
        font-family: monospace;
    }
    </style>
    """, unsafe_allow_html=True)