import streamlit as st
import random
import operator

# Daftar semua operasi matematika
operations = [
    ('+', operator.add),
    ('-', operator.sub),
    ('*', operator.mul),
    ('/', operator.truediv)
]

suits = ['h', 's', 'w', 'k']  # hati, sekop, wajik, keriting
values = [
    *(f"{i}" for i in range(1, 11)),  # kartu 1 sampai 10
    'j', 'q', 'k'  # jack, queen, king
]
all_cards = [f"kartu-{suit}{value}" for suit in suits for value in values]

# Fungsi untuk mendapatkan nilai kartu
def get_card_value(card_name):
    try:
        value_part = card_name.split('-')[1][1:]  # Ambil bagian nilainya (setelah suit)
        return 10 if value_part in ['j', 'q', 'k'] else int(value_part)
    except (IndexError, ValueError):
        return None

# Fungsi untuk menghasilkan semua kombinasi ekspresi
def generate_combinations(numbers, ops, target):
    expressions = []
    n = len(numbers)
    for i in range(n):
        for j in range(n):
            if i != j:
                for k in range(n):
                    if k != i and k != j:
                        for l in range(n):
                            if l != i and l != j and l != k:
                                for op1 in ops:
                                    for op2 in ops:
                                        for op3 in ops:
                                            patterns = [
                                                f"(({numbers[i]} {op1[0]} {numbers[j]}) {op2[0]} {numbers[k]}) {op3[0]} {numbers[l]}",
                                                f"({numbers[i]} {op1[0]} ({numbers[j]} {op2[0]} {numbers[k]})) {op3[0]} {numbers[l]}",
                                                f"{numbers[i]} {op1[0]} (({numbers[j]} {op2[0]} {numbers[k]}) {op3[0]} {numbers[l]})",
                                                f"{numbers[i]} {op1[0]} ({numbers[j]} {op2[0]} ({numbers[k]} {op3[0]} {numbers[l]}))",
                                                f"({numbers[i]} {op1[0]} {numbers[j]}) {op2[0]} ({numbers[k]} {op3[0]} {numbers[l]})"
                                            ]
                                            try:
                                                for pattern in patterns:
                                                    if abs(eval(pattern) - target) < 1e-6:
                                                        expressions.append(pattern)
                                            except ZeroDivisionError:
                                                continue
    return expressions

# Inisialisasi session state jika pertama kali
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'mode': 'original',
        'cards': [],
        'target': 24,
        'solutions': [],
        'result_shown': False,
        'game_started': False
    }

def start_game(target=None):
    if st.session_state.game_state['mode'] == 'original':
        st.session_state.game_state['target'] = 24
    elif st.session_state.game_state['mode'] == 'random':
        st.session_state.game_state['target'] = random.randint(10, 50)

    st.session_state.game_state['cards'] = random.sample(all_cards, 4)
    card_values = [get_card_value(card) for card in st.session_state.game_state['cards']]
    st.session_state.game_state['solutions'] = generate_combinations(card_values, operations, st.session_state.game_state['target'])
    st.session_state.game_state['result_shown'] = False
    st.session_state.game_state['game_started'] = True

def start_custom_game(cards, target):
    try:
        card_values = [int(card) for card in cards]
        st.session_state.game_state['cards'] = cards
        st.session_state.game_state['target'] = int(target)
        st.session_state.game_state['solutions'] = generate_combinations(card_values, operations, st.session_state.game_state['target'])
        st.session_state.game_state['result_shown'] = False
        st.session_state.game_state['game_started'] = True
    except ValueError:
        st.error("Input kartu dan target harus berupa angka yang valid.")

st.sidebar.title("Pilih Mode")
st.session_state.game_state['mode'] = st.sidebar.radio("Mode Permainan", ["original", "random", "custom"])

st.title("Remi 24")

# Tombol utama untuk memulai atau mengambil kartu lagi
if st.session_state.game_state['mode'] == "custom":
    with st.form("custom_game_form", clear_on_submit=True):
        target = st.text_input("Masukkan target:", "24")
        cards = st.text_input("Masukkan 4 angka kartu (pisahkan dengan spasi):", "1 2 3 4")
        submitted = st.form_submit_button("Mulai Permainan")
        if submitted:
            start_custom_game(cards.split(), target)
else:
    if st.button("Mulai / Ambil Kartu Lagi"):
        start_game()

if st.session_state.game_state['game_started']:
    st.header(f"Kartu yang diambil (Target: {st.session_state.game_state['target']}):")
    cards = st.session_state.game_state['cards']

    rows = [cards[:2], cards[2:]]
    for row in rows:
        cols = st.columns(len(row))
        for idx, card in enumerate(row):
            card_value = card if st.session_state.game_state['mode'] == "custom" else get_card_value(card)
            with cols[idx]:
                if st.session_state.game_state['mode'] == "custom":
                    st.write(f"Kartu: {card}")
                else:
                    try:
                        st.image(f"kartu/{card}.png", caption=f"({card_value})" if card_value else card, width=100)
                    except Exception:
                        st.write(f"Kartu: {card} ({card_value})")

    st.subheader("Apakah kartu tersebut bisa menjadi target?")
    col1, col2 = st.columns(2)
    if col1.button("Bisa"):
        st.session_state.game_state['result_shown'] = True
        if st.session_state.game_state['solutions']:
            st.success("Benar! Kartu tersebut bisa mencapai target.")
            st.markdown("### Solusi yang memungkinkan:")
            for solution in st.session_state.game_state['solutions']:
                st.markdown(f"- {solution}")
        else:
            st.error("Salah! Kartu tersebut tidak bisa mencapai target.")

    if col2.button("Tidak Bisa"):
        st.session_state.game_state['result_shown'] = True
        if not st.session_state.game_state['solutions']:
            st.success("Benar! Kartu tersebut tidak bisa mencapai target.")
        else:
            st.error("Salah! Kartu tersebut bisa mencapai target.")
            st.markdown("### Solusi yang memungkinkan:")
            for solution in st.session_state.game_state['solutions']:
                st.markdown(f"- {solution}")
