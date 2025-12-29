import streamlit as st
import time
import sys

# Menghilangkan batas konversi integer besar (aman karena hasil tidak ditampilkan penuh)
sys.set_int_max_str_digits(0)

# FUNGSI ALGORITMA

# Iteratif O(n)
def pangkat_iteratif(basis, eksponen):
    hasil = 1
    for _ in range(eksponen):
        hasil *= basis
    return hasil


# Rekursif O(n)
def pangkat_rekursif(basis, eksponen):
    if eksponen == 0:
        return 1
    return basis * pangkat_rekursif(basis, eksponen - 1)



# FUNGSI UKUR WAKTU (UNTUK GRAFIK)

def waktu_iteratif(basis, n):
    start = time.perf_counter()
    temp = 1
    for _ in range(n):
        temp *= basis
    return time.perf_counter() - start


def waktu_rekursif(basis, n):
    def helper(b, e):
        if e == 0:
            return 1
        return b * helper(b, e - 1)

    start = time.perf_counter()
    helper(basis, n)
    return time.perf_counter() - start



# UI STREAMLIT


st.set_page_config(
    page_title="Analisis Kompleksitas Algoritma Pangkat",
    layout="wide"
)

st.title("📊 Analisis Kompleksitas Algoritma Pangkat")
st.write(
    "Perbandingan **Algoritma Iteratif** dan **Algoritma Rekursif** "
    "berdasarkan waktu eksekusi dan kompleksitas algoritma."
)


# INPUT USER

with st.sidebar:
    st.header("🔢 Input Data")

    basis = st.number_input(
        "Masukkan Basis (x)",
        min_value=0,
        max_value=1000,
        value=1
    )

    eksponen = st.number_input(
        "Masukkan Eksponen (n)",
        min_value=0,
        max_value=10000,
        value=1
    )

    st.divider()

    n_grafik = st.slider(
        "Eksponen Maksimum untuk Grafik",
        min_value=1,
        max_value=500,
        value=min(eksponen, 500),
        step=10
    )

tombol_hitung = st.button("🚀 Bandingkan Algoritma")


# PROSES & OUTPUT


if tombol_hitung:

    col1, col2 = st.columns(2)

    # --- Iteratif ---
    start = time.perf_counter()
    hasil_i = pangkat_iteratif(basis, eksponen)
    waktu_i = time.perf_counter() - start

    # --- Rekursif ---
    start = time.perf_counter()
    hasil_r = pangkat_rekursif(basis, eksponen)
    waktu_r = time.perf_counter() - start

    with col1:
        st.subheader("🔄 Algoritma Iteratif")
        st.write(
            f"Hasil {basis} pangkat {eksponen}: {pangkat_iteratif(basis, eksponen)}")
        st.write(f"Jumlah digit hasil: **{len(str(hasil_i))} digit**")
        st.metric("Waktu Eksekusi", f"{waktu_i:.8f} detik")
        st.info(
            "Kompleksitas Waktu: **O(n)**\n\n"
            "Kompleksitas Ruang: **O(1)**"
        )

    with col2:
        st.subheader("🪞 Algoritma Rekursif")
        st.write(
            f"Hasil {basis} pangkat {eksponen}: {pangkat_rekursif(basis, eksponen)}")
        st.write(f"Jumlah digit hasil: **{len(str(hasil_r))} digit**")
        st.metric("Waktu Eksekusi", f"{waktu_r:.8f} detik")
        st.info(
            "Kompleksitas Waktu: **O(n)**\n\n"
            "Kompleksitas Ruang: **O(n)** (Stack Rekursi)"
        )

    st.divider()

    
    # GRAFIK KOMPLEKSITAS

    st.subheader("📈 Grafik Kompleksitas Berdasarkan Input x dan n")

    eksponen_list = list(range(1, n_grafik + 1))
    waktu_iter = []
    waktu_rek = []

    for n in eksponen_list:
        waktu_iter.append(waktu_iteratif(basis, n))
        waktu_rek.append(waktu_rekursif(basis, n))

    data_chart = {
        "Eksponen (n)": eksponen_list,
        "Iteratif (O(n))": waktu_iter,
        "Rekursif (O(n))": waktu_rek
    }

    st.line_chart(data_chart, x="Eksponen (n)")

    
    # ANALISIS OTOMATIS

    st.subheader("🧠 Analisis Hasil")

    if waktu_i < waktu_r:
        st.success(
            "Algoritma **Iteratif** lebih cepat dibandingkan Rekursif "
            "karena tidak memiliki overhead pemanggilan fungsi."
        )
    else:
        st.success(
            "Algoritma **Rekursif** memiliki performa setara atau sedikit lebih cepat "
            "pada nilai n kecil."
        )

    st.warning(
        "Catatan: Algoritma rekursif berisiko mengalami **stack overflow** "
        "untuk nilai n besar, sedangkan algoritma iteratif lebih stabil "
        "dalam penggunaan memori."
    )
