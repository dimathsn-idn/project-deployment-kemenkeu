# 01. Import library
import streamlit as st
import pandas as pd
import requests
from ui.widgets import banner

# 02. Definisi endpoint API
ENDPOINT = ('https://training.ekos.my.id/api/tax-revenue-dashboard')

# 03. Buat fungsi loader data: memanggil API, membaca payload JSON, normalisasi ke `DataFrame`, parsing kolom tanggal, casting kolom numerik.
@st.cache_data
def load_data():
    response = requests.get(ENDPOINT, timeout=10)
    response.raise_for_status()
    js = response.json()
    if "data" in js:
        data = pd.json_normalize(js["data"])
    else:
        data = pd.json_normalize(js)
    return data

# Membuat fungsi tombol aksi awal
def click_button():
    st.session_state.button_clicked = True

# Fungsi untuk mereset form
def reset_form():
    st.session_state['hasil_analisis'] = ""

# 04. Buat fungsi render() untuk menampilkan banner, tujuan mini project, dan tombol aksi awal
def render() -> None:
    banner("Mini Project Kelompok 01", "Belajar membangun aplikasi dengan Streamlit")
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False
    st.button("Tujuan Mini Project", on_click=click_button)
    if st.session_state.button_clicked:
        st.write("Sebagai salah satu tugas kelompok PJJ Data Analytics")

    # 05. Tampilkan data mentah menggunakan st.expander
    with st.expander("Tampilkan Raw Data"):
        st.title("Tabel Raw Data Tax Revenue")
        data = load_data()
        df = data.copy()
        st.dataframe(df)
        st.write(df.dtypes)
     
        # 06. Widget filter: provinsi, jenis pajak, rentang tahun, dan threshold penerimaan neto.
        col1, col2, col3, col4 = st.columns(4)
        kolom_propinsi = df['provinsi'].sort_values().unique()
        kolom_jenis_pajak = df['jenis_pajak'].sort_values().unique()
        kolom_rentang_tahun = df['tahun_pajak'].sort_values().unique()
        kolom_threshold_neto = ['kurang dari Rp 4,8 Miliar', 'Rp 4,8 Miliar atau lebih']
        with col1:
            propinsi = st.multiselect("Provinsi", kolom_propinsi)
        with col2:
            jenis_pajak = st.multiselect("Jenis Pajak", kolom_jenis_pajak)
        with col3:
            rentang_tahun = st.multiselect("Tahun Pajak", kolom_rentang_tahun)
        with col4:
            threshold_neto = st.multiselect("Threshold Penerimaan Neto", kolom_threshold_neto)
        filtered_data = df.copy()
        if propinsi:
            filtered_data = filtered_data[filtered_data['provinsi'].isin(propinsi)]
        if jenis_pajak:
            filtered_data = filtered_data[filtered_data['jenis_pajak'].isin(jenis_pajak)]
        if rentang_tahun:
            filtered_data = filtered_data[filtered_data['tahun_pajak'].isin(rentang_tahun)]
        if threshold_neto:
            if 'kurang dari Rp 4,8 Miliar' in threshold_neto:
                filtered_data = filtered_data[filtered_data['penerimaan_neto_idr'] < 4800000000]
            if 'Rp 4,8 Miliar atau lebih' in threshold_neto:
                filtered_data = filtered_data[filtered_data['penerimaan_neto_idr'] >= 4800000000]

        # 07. Hitung KPI Utama: total bruto, restitusi, neto, jumlah wajib pajak, dan rasio restitusi
        st.write("KPI Utama")
        col1, col2, col3 = st.columns(3)
        col4, col5 = st.columns(2)
        kolom_total_bruto = df['penerimaan_bruto_idr'].sum()
        kolom_restitusi_idr = df['restitusi_idr'].sum()
        kolom_neto = df['penerimaan_neto_idr'].sum()
        kolom_jumlah_wajib_pajak = df['jumlah_wp'].sum()
        kolom_rasio_restitusi = kolom_restitusi_idr / kolom_total_bruto
        col1.metric("Total Bruto", kolom_total_bruto, border=True, format="accounting")
        col2.metric("Restitusi", kolom_restitusi_idr, border=True, format="accounting")
        col3.metric("Neto", kolom_neto, border=True, format="accounting")
        col4.metric("Jumlah Wajib Pajak", kolom_jumlah_wajib_pajak, border=True, format="localized")
        col5.metric("Rasio Restitusi", kolom_rasio_restitusi, border=True, format="percent")

        # 08. Bangun visualisasi dengan tab: tabel data, tren waktu, dan breakdown sektor.
        st.write("Tabel Filter Tax Revenue")
        st.dataframe(filtered_data)
        st.write("Grafik Tren Waktu")
        st.line_chart(df, x='tahun_pajak', y='penerimaan_neto_idr')
        st.write("Grafik Breakdown per Sektor")
        st.bar_chart(df, x='sektor', y='penerimaan_neto_idr')

        # 09. Form Insight Analis
        st.title("Form Insight Analis")
        with st.form(key='reset_form', clear_on_submit=True):
            st.text_input("Hasil Analisis", key='hasil_analisis')
            submit_button = st.form_submit_button(label='Validasi dan Kirim', on_click=reset_form)
            if submit_button:
                st.success("Hasil Analisis berhasil dikirim!")

        # 10. Export hasil filter ke file CSV
        csv = filtered_data.to_csv().encode("utf-8")
        st.download_button(label="Download CSV", data=csv, file_name="data.csv", mime="text/csv", icon=":material/download:")



#from ui.widgets import banner
#import streamlit as st


#def render() -> None:
#    banner(
#        "Mini Project",
#        "Praktik langsung dengan membangun aplikasi dengan Streamlit.",
#    )

#    with st.expander("Instruksi Aktivitas"):
#        st.subheader("Instruksi From Scratch (untuk peserta)")
#        st.info(
#            "Ikuti urutan langkah berikut saat live coding agar file mini project bisa dibangun dari nol secara bertahap."
#        )
#        st.markdown(
#            """
#    Urutan kerja yang disarankan:
#    1. **Buat file halaman** `page/mini_project.py` lalu tambahkan import dasar: `streamlit`, `pandas`, `requests`, dan `banner` dari `ui.widgets`.
#    2. **Definisikan endpoint API** ke variabel `ENDPOINT` dengan nilai default adalah: https://training.ekos.my.id/api/tax-revenue-dashboard.
#    3. **Buat fungsi loader data** (gunakan `@st.cache_data`) untuk:
#    - memanggil API,
#    - membaca payload JSON,
#    - normalisasi ke `DataFrame`,
#    - parsing kolom tanggal,
#    - casting kolom numerik.
#    4. **Buat fungsi `render()`** lalu tampilkan banner, tujuan mini project, dan tombol aksi awal.
#    5. **Tampilkan data mentah** dalam `st.expander` agar peserta bisa validasi hasil ambil data.
#    6. **Tambahkan widget filter**: provinsi, jenis pajak, rentang tahun, dan threshold penerimaan neto.
#    7. **Hitung KPI utama**: total bruto, restitusi, neto, jumlah wajib pajak, dan rasio restitusi.
#    8. **Bangun visualisasi** dengan tab: tabel data, tren waktu, dan breakdown sektor.
#    9. **Tambahkan form insight analis** + validasi sederhana sebelum simpan ringkasan.
#    10. **Tambahkan export** hasil filter ke CSV via `st.download_button`.

#    Checklist selesai:
#    - Data API berhasil ditarik.
#    - Filter bekerja sesuai input.
#    - KPI dan chart tampil benar.
#    - Ringkasan insight bisa disimpan.
#    - Hasil analisis bisa diunduh.
#    """
#        )
