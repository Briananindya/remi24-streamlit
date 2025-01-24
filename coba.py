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

# Fungsi untuk menghasilkan semua kombinasi ekspresi
def generate_combinations(numbers, ops):
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
                                                # Evaluasi semua pola
                                                for pattern in patterns:
                                                    value = eval(pattern)
                                                    if value != float('inf') and value != float('-inf') and abs(value - 24) < 1e-6:
                                                        expressions.append(pattern)
                                            except ZeroDivisionError:
                                                continue
    return expressions

# Inisialisasi session state jika pertama kali
if 'cards' not in st.session_state:
    st.session_state.cards = []
    st.session_state.solutions = []
    st.session_state.result_shown = False
    st.session_state.game_started = False
    st.session_state.bisa_pressed = False
    st.session_state.tidak_bisa_pressed = False

# Fungsi untuk mereset kartu dan solusi
def reset_game():
    st.session_state.cards = [random.randint(1, 10) for _ in range(4)]
    st.session_state.solutions = generate_combinations(st.session_state.cards, operations)
    st.session_state.result_shown = False
    st.session_state.game_started = True
    st.session_state.bisa_pressed = False
    st.session_state.tidak_bisa_pressed = False

# Judul aplikasi
st.title("REMI 24")

# Tombol untuk memulai permainan
if not st.session_state.game_started:
    if st.button("Mulai Ambil Kartu"):
        reset_game()

# Jika permainan dimulai, tampilkan kartu dan tombol permainan
if st.session_state.game_started:
    cards = st.session_state.cards
    st.header(f"Kartu yang diambil: {cards[0]}, {cards[1]}, {cards[2]}, {cards[3]}")
    st.subheader("Apakah kartu tersebut bisa menjadi 24?")

    # Tombol "bisa" dan "tidak bisa"
    if not st.session_state.result_shown:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Bisa"):
                st.session_state.bisa_pressed = True
                if st.session_state.solutions:
                    st.success("Benar! Kartu tersebut bisa menjadi 24.")
                    st.markdown("### Solusi yang memungkinkan:")
                    for solution in st.session_state.solutions:
                        st.markdown(f"- {solution}")
                else:
                    st.error("Salah! Kartu tersebut tidak bisa menjadi 24.")
                st.session_state.result_shown = True

        with col2:
            if st.button("Tidak Bisa"):
                st.session_state.tidak_bisa_pressed = True
                if not st.session_state.solutions:
                    st.success("Benar! Kartu tersebut tidak bisa menjadi 24.")
                else:
                    st.error("Salah! Kartu tersebut bisa menjadi 24.")
                    st.markdown("### Solusi yang memungkinkan:")
                    for solution in st.session_state.solutions:
                        st.markdown(f"- {solution}")
                st.session_state.result_shown = True

    # Tombol untuk memulai ulang permainan
    if st.button("Main Lagi"):
        reset_game()