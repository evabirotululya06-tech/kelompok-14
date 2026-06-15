import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import tkinter as tk
from tkinter import messagebox

# ============================================================
# TIPE BENTUKAN (Record/Struct)
# ============================================================
# Investasi direpresentasikan sebagai dictionary dengan field:
# {
#   "nama": str,
#   "jenis": str,       # Saham / Obligasi / Reksa Dana
#   "dana": float,      # Dana yang diinvestasikan (Rp)
#   "harga_kini": float,# Harga aset terkini (Rp)
#   "jumlah_unit": float# Jumlah unit yang dimiliki
# }

# ============================================================
# ARRAY STATIS (maksimum 100 data)
# ============================================================
MAX_DATA = 100
data_investasi = [None] * MAX_DATA
jumlah_data = 0


# ============================================================
# SUBPROGRAM: CRUD
# ============================================================

def tambah_investasi(nama: str, jenis: str, dana: float,
                     harga_kini: float, jumlah_unit: float) -> bool:
    """
    Menambahkan data investasi baru ke array statis.
    Parameter:
        nama        : nama aset investasi
        jenis       : jenis aset (Saham/Obligasi/Reksa Dana)
        dana        : jumlah dana yang diinvestasikan (Rp)
        harga_kini  : harga aset terkini per unit (Rp)
        jumlah_unit : jumlah unit yang dimiliki
    Return: True jika berhasil, False jika array penuh
    """
    global jumlah_data
    if jumlah_data >= MAX_DATA:
        return False
    data_investasi[jumlah_data] = {
        "nama": nama,
        "jenis": jenis,
        "dana": dana,
        "harga_kini": harga_kini,
        "jumlah_unit": jumlah_unit
    }
    jumlah_data += 1
    return True


def ubah_investasi(indeks: int, nama: str, jenis: str, dana: float,
                   harga_kini: float, jumlah_unit: float) -> bool:
    """
    Mengubah data investasi pada indeks tertentu.
    Parameter:
        indeks      : posisi data di array (0-based)
        nama, jenis, dana, harga_kini, jumlah_unit: data baru
    Return: True jika berhasil, False jika indeks tidak valid
    """
    if indeks < 0 or indeks >= jumlah_data:
        return False
    data_investasi[indeks] = {
        "nama": nama,
        "jenis": jenis,
        "dana": dana,
        "harga_kini": harga_kini,
        "jumlah_unit": jumlah_unit
    }
    return True


def hapus_investasi(indeks: int) -> bool:
    """
    Menghapus data investasi pada indeks tertentu (shift kiri).
    Parameter:
        indeks: posisi data di array (0-based)
    Return: True jika berhasil, False jika indeks tidak valid
    """
    global jumlah_data
    if indeks < 0 or indeks >= jumlah_data:
        return False
    i = indeks
    while i < jumlah_data - 1:
        data_investasi[i] = data_investasi[i + 1]
        i += 1
    data_investasi[jumlah_data - 1] = None
    jumlah_data -= 1
    return True


# ============================================================
# SUBPROGRAM: PERHITUNGAN
# ============================================================

def hitung_nilai_sekarang(investasi: dict) -> float:
    """
    Menghitung nilai investasi saat ini berdasarkan harga terkini.
    Parameter: investasi (dict)
    Return: nilai sekarang (Rp)
    """
    return investasi["harga_kini"] * investasi["jumlah_unit"]


def hitung_keuntungan(investasi: dict) -> float:
    """
    Menghitung keuntungan/kerugian investasi.
    Parameter: investasi (dict)
    Return: selisih nilai sekarang - dana awal (Rp)
    """
    return hitung_nilai_sekarang(investasi) - investasi["dana"]


def hitung_persentase(investasi: dict) -> float:
    """
    Menghitung persentase keuntungan/kerugian.
    Parameter: investasi (dict)
    Return: persentase (float), 0 jika dana = 0
    """
    if investasi["dana"] == 0:
        return 0.0
    return (hitung_keuntungan(investasi) / investasi["dana"]) * 100


def hitung_total_dana() -> float:
    """
    Menghitung total dana yang diinvestasikan.
    Return: total dana (Rp)
    """
    total = 0.0
    i = 0
    while i < jumlah_data:
        total += data_investasi[i]["dana"]
        i += 1
    return total


def hitung_total_nilai_sekarang() -> float:
    """
    Menghitung total nilai portofolio saat ini.
    Return: total nilai sekarang (Rp)
    """
    total = 0.0
    i = 0
    while i < jumlah_data:
        total += hitung_nilai_sekarang(data_investasi[i])
        i += 1
    return total


# ============================================================
# SUBPROGRAM: SEQUENTIAL SEARCH
# ============================================================

def sequential_search_nama(keyword: str) -> list:
    """
    Mencari investasi berdasarkan nama (case-insensitive).
    Parameter: keyword (str)
    Return: list indeks yang cocok
    """
    hasil = []
    i = 0
    while i < jumlah_data:
        if keyword.lower() in data_investasi[i]["nama"].lower():
            hasil.append(i)
        i += 1
    return hasil


def sequential_search_jenis(jenis: str) -> list:
    """
    Mencari investasi berdasarkan jenis aset (case-insensitive).
    Parameter: jenis (str)
    Return: list indeks yang cocok
    """
    hasil = []
    i = 0
    while i < jumlah_data:
        if jenis.lower() in data_investasi[i]["jenis"].lower():
            hasil.append(i)
        i += 1
    return hasil


# ============================================================
# SUBPROGRAM: BINARY SEARCH (berdasarkan nama, array harus sorted)
# ============================================================

def binary_search_nama(arr_sorted: list, keyword: str) -> int:
    """
    Mencari investasi berdasarkan nama exact match (binary search).
    Parameter:
        arr_sorted: list dict yang sudah diurutkan berdasarkan nama
        keyword   : nama yang dicari (exact, case-insensitive)
    Return: indeks di arr_sorted jika ditemukan, -1 jika tidak
    """
    kiri = 0
    kanan = len(arr_sorted) - 1
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        nama_tengah = arr_sorted[tengah]["nama"].lower()
        kw = keyword.lower()
        if nama_tengah == kw:
            return tengah
        elif nama_tengah < kw:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    return -1


# ============================================================
# SUBPROGRAM: SELECTION SORT
# ============================================================

def selection_sort(arr: list, key_func, ascending: bool = True) -> list:
    """
    Mengurutkan list menggunakan Selection Sort.
    Parameter:
        arr       : list data (tidak mengubah array asli)
        key_func  : fungsi untuk mendapatkan nilai kunci
        ascending : True = naik, False = turun
    Return: list baru yang sudah diurutkan
    """
    hasil = arr[:]
    n = len(hasil)
    i = 0
    while i < n - 1:
        idx_ekstrim = i
        j = i + 1
        while j < n:
            if ascending:
                if key_func(hasil[j]) < key_func(hasil[idx_ekstrim]):
                    idx_ekstrim = j
            else:
                if key_func(hasil[j]) > key_func(hasil[idx_ekstrim]):
                    idx_ekstrim = j
            j += 1
        if idx_ekstrim != i:
            hasil[i], hasil[idx_ekstrim] = hasil[idx_ekstrim], hasil[i]
        i += 1
    return hasil


# ============================================================
# SUBPROGRAM: INSERTION SORT
# ============================================================

def insertion_sort(arr: list, key_func, ascending: bool = True) -> list:
    """
    Mengurutkan list menggunakan Insertion Sort.
    Parameter:
        arr       : list data (tidak mengubah array asli)
        key_func  : fungsi untuk mendapatkan nilai kunci
        ascending : True = naik, False = turun
    Return: list baru yang sudah diurutkan
    """
    hasil = arr[:]
    n = len(hasil)
    i = 1
    while i < n:
        kunci = hasil[i]
        j = i - 1
        if ascending:
            while j >= 0 and key_func(hasil[j]) > key_func(kunci):
                hasil[j + 1] = hasil[j]
                j -= 1
        else:
            while j >= 0 and key_func(hasil[j]) < key_func(kunci):
                hasil[j + 1] = hasil[j]
                j -= 1
        hasil[j + 1] = kunci
        i += 1
    return hasil


# ============================================================
# SUBPROGRAM: FORMAT RUPIAH
# ============================================================

def format_rupiah(nilai: float) -> str:
    """
    Memformat angka menjadi format Rupiah Indonesia.
    Parameter: nilai (float)
    Return: string format Rupiah
    """
    if nilai < 0:
        return f"-Rp {abs(nilai):,.0f}"
    return f"Rp {nilai:,.0f}"


# ============================================================
# GUI - APLIKASI MANAJEMEN INVESTASI
# ============================================================

class AplikasiInvestasi:
    def __init__(self, root):
        self.root = root
        self.root.title("📈 Aplikasi Manajemen Investasi Sederhana")
        self.root.geometry("1100x700")
        self.root.resizable(True, True)

        # Variabel form
        self.var_nama = ttk.StringVar()
        self.var_jenis = ttk.StringVar(value="Saham")
        self.var_dana = ttk.StringVar()
        self.var_harga = ttk.StringVar()
        self.var_unit = ttk.StringVar()
        self.var_cari = ttk.StringVar()
        self.var_cari_mode = ttk.StringVar(value="Nama (Sequential)")
        self.var_sort_key = ttk.StringVar(value="Nilai Investasi")
        self.var_sort_algo = ttk.StringVar(value="Selection Sort")
        self.var_sort_order = ttk.StringVar(value="Descending")

        self.indeks_dipilih = -1
        self._bangun_ui()
        self._muat_data_contoh()
        self._refresh_tabel()
        self._update_statistik()

    def _bangun_ui(self):
        # ---- Notebook (Tab) ----
        self.notebook = ttk.Notebook(self.root, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.tab_dashboard = ttk.Frame(self.notebook)
        self.tab_kelola = ttk.Frame(self.notebook)
        self.tab_cari = ttk.Frame(self.notebook)
        self.tab_urutkan = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_dashboard, text="  📊 Dashboard  ")
        self.notebook.add(self.tab_kelola, text="  📝 Kelola Data  ")
        self.notebook.add(self.tab_cari, text="  🔍 Cari Aset  ")
        self.notebook.add(self.tab_urutkan, text="  🔃 Urutkan  ")

        self._bangun_tab_dashboard()
        self._bangun_tab_kelola()
        self._bangun_tab_cari()
        self._bangun_tab_urutkan()

    # ------------------------------------------------------------------
    # TAB 1: DASHBOARD
    # ------------------------------------------------------------------
    def _bangun_tab_dashboard(self):
        frame_atas = ttk.Frame(self.tab_dashboard)
        frame_atas.pack(fill=X, padx=15, pady=(15, 5))

        # Judul
        ttk.Label(frame_atas, text="📈 Portofolio Investasi Saya",
                  font=("Segoe UI", 16, "bold"),
                  bootstyle="primary").pack(side=LEFT)

        # Kartu statistik
        frame_kartu = ttk.Frame(self.tab_dashboard)
        frame_kartu.pack(fill=X, padx=15, pady=5)

        self.lbl_total_dana = self._kartu_stat(frame_kartu, "Total Dana", "Rp 0", "info", 0)
        self.lbl_total_nilai = self._kartu_stat(frame_kartu, "Nilai Sekarang", "Rp 0", "success", 1)
        self.lbl_total_untung = self._kartu_stat(frame_kartu, "Keuntungan/Rugi", "Rp 0", "warning", 2)
        self.lbl_jumlah_aset = self._kartu_stat(frame_kartu, "Jumlah Aset", "0", "secondary", 3)

        for i in range(4):
            frame_kartu.columnconfigure(i, weight=1)

        # Tabel portofolio
        frame_tabel = ttk.LabelFrame(self.tab_dashboard,
                                     text="  Daftar Aset Investasi  ",
                                     bootstyle="primary", padding=10)
        frame_tabel.pack(fill=BOTH, expand=True, padx=15, pady=10)

        kolom = ("No", "Nama Aset", "Jenis", "Dana Awal", "Harga Kini",
                 "Jumlah Unit", "Nilai Sekarang", "Keuntungan/Rugi", "Persentase")
        self.tree_dash = ttk.Treeview(frame_tabel, columns=kolom,
                                      show="headings", bootstyle="primary",
                                      selectmode="browse", height=12)

        lebar = [40, 150, 100, 120, 110, 100, 130, 130, 90]
        for i, (k, l) in enumerate(zip(kolom, lebar)):
            self.tree_dash.heading(k, text=k)
            self.tree_dash.column(k, width=l, anchor=CENTER if i == 0 else W)

        sb_y = ttk.Scrollbar(frame_tabel, orient=VERTICAL,
                              command=self.tree_dash.yview)
        sb_x = ttk.Scrollbar(frame_tabel, orient=HORIZONTAL,
                              command=self.tree_dash.xview)
        self.tree_dash.configure(yscrollcommand=sb_y.set,
                                 xscrollcommand=sb_x.set)
        sb_y.pack(side=RIGHT, fill=Y)
        sb_x.pack(side=BOTTOM, fill=X)
        self.tree_dash.pack(fill=BOTH, expand=True)

    def _kartu_stat(self, parent, judul, nilai, style, col):
        frame = ttk.Frame(parent, padding=15)
        frame.grid(row=0, column=col, padx=5, pady=5, sticky=NSEW)
        ttk.Label(frame, text=judul, font=("Segoe UI", 9),
                  bootstyle=f"{style}").pack()
        lbl = ttk.Label(frame, text=nilai, font=("Segoe UI", 12, "bold"),
                        bootstyle=f"{style}")
        lbl.pack(pady=(3, 0))
        # Tambahkan border dengan LabelFrame tipis
        lf = ttk.LabelFrame(parent, bootstyle=style, padding=12)
        lf.grid(row=0, column=col, padx=5, pady=5, sticky=NSEW)
        ttk.Label(lf, text=judul, font=("Segoe UI", 9, "bold")).pack()
        lbl2 = ttk.Label(lf, text=nilai, font=("Segoe UI", 11, "bold"),
                         bootstyle=style)
        lbl2.pack(pady=(2, 0))
        frame.destroy()
        return lbl2

    # ------------------------------------------------------------------
    # TAB 2: KELOLA DATA
    # ------------------------------------------------------------------
    def _bangun_tab_kelola(self):
        # Form input
        frame_form = ttk.LabelFrame(self.tab_kelola,
                                    text="  Form Data Investasi  ",
                                    bootstyle="primary", padding=15)
        frame_form.pack(fill=X, padx=15, pady=(15, 5))

        fields = [
            ("Nama Aset*", self.var_nama, None),
            ("Jenis Aset*", self.var_jenis, ["Saham", "Obligasi", "Reksa Dana"]),
            ("Dana Awal (Rp)*", self.var_dana, None),
            ("Harga Kini/Unit (Rp)*", self.var_harga, None),
            ("Jumlah Unit*", self.var_unit, None),
        ]

        for baris, (label, var, pilihan) in enumerate(fields):
            ttk.Label(frame_form, text=label,
                      font=("Segoe UI", 9)).grid(row=baris, column=0,
                                                  sticky=W, pady=4, padx=5)
            if pilihan:
                w = ttk.Combobox(frame_form, textvariable=var,
                                  values=pilihan, state="readonly", width=28)
            else:
                w = ttk.Entry(frame_form, textvariable=var, width=30)
            w.grid(row=baris, column=1, sticky=W, pady=4, padx=5)

        # Tombol aksi
        frame_btn = ttk.Frame(frame_form)
        frame_btn.grid(row=len(fields), column=0, columnspan=2,
                       pady=10, sticky=W)

        ttk.Button(frame_btn, text="➕ Tambah", bootstyle="success",
                   command=self._tambah, width=12).pack(side=LEFT, padx=4)
        ttk.Button(frame_btn, text="✏️ Ubah", bootstyle="warning",
                   command=self._ubah, width=12).pack(side=LEFT, padx=4)
        ttk.Button(frame_btn, text="🗑️ Hapus", bootstyle="danger",
                   command=self._hapus, width=12).pack(side=LEFT, padx=4)
        ttk.Button(frame_btn, text="🔄 Reset Form", bootstyle="secondary",
                   command=self._reset_form, width=12).pack(side=LEFT, padx=4)

        # Tabel data
        frame_list = ttk.LabelFrame(self.tab_kelola,
                                    text="  Data Investasi  ",
                                    bootstyle="primary", padding=10)
        frame_list.pack(fill=BOTH, expand=True, padx=15, pady=5)

        kolom = ("No", "Nama Aset", "Jenis", "Dana Awal",
                 "Harga Kini", "Jumlah Unit", "Nilai Sekarang", "Untung/Rugi", "%")
        self.tree_kelola = ttk.Treeview(frame_list, columns=kolom,
                                        show="headings", bootstyle="primary",
                                        selectmode="browse", height=8)
        lebar = [40, 150, 100, 120, 110, 100, 130, 120, 80]
        for i, (k, l) in enumerate(zip(kolom, lebar)):
            self.tree_kelola.heading(k, text=k)
            self.tree_kelola.column(k, width=l, anchor=CENTER if i == 0 else W)

        sb = ttk.Scrollbar(frame_list, orient=VERTICAL,
                            command=self.tree_kelola.yview)
        sb_x = ttk.Scrollbar(frame_list, orient=HORIZONTAL,
                              command=self.tree_kelola.xview)
        self.tree_kelola.configure(yscrollcommand=sb.set,
                                   xscrollcommand=sb_x.set)
        sb.pack(side=RIGHT, fill=Y)
        sb_x.pack(side=BOTTOM, fill=X)
        self.tree_kelola.pack(fill=BOTH, expand=True)
        self.tree_kelola.bind("<<TreeviewSelect>>", self._pilih_baris_kelola)

    # ------------------------------------------------------------------
    # TAB 3: CARI ASET
    # ------------------------------------------------------------------
    def _bangun_tab_cari(self):
        frame_cari = ttk.LabelFrame(self.tab_cari,
                                    text="  Pencarian Aset  ",
                                    bootstyle="info", padding=15)
        frame_cari.pack(fill=X, padx=15, pady=15)

        ttk.Label(frame_cari, text="Kata Kunci:").grid(row=0, column=0,
                                                        sticky=W, padx=5)
        ttk.Entry(frame_cari, textvariable=self.var_cari,
                  width=35).grid(row=0, column=1, padx=5, pady=4)

        ttk.Label(frame_cari, text="Metode Pencarian:").grid(row=1, column=0,
                                                              sticky=W, padx=5)
        ttk.Combobox(frame_cari, textvariable=self.var_cari_mode,
                     values=["Nama (Sequential)", "Jenis (Sequential)",
                             "Nama (Binary Search - Exact)"],
                     state="readonly", width=33).grid(row=1, column=1,
                                                      padx=5, pady=4)

        frame_btn = ttk.Frame(frame_cari)
        frame_btn.grid(row=2, column=0, columnspan=2, pady=8, sticky=W)
        ttk.Button(frame_btn, text="🔍 Cari", bootstyle="info",
                   command=self._cari, width=12).pack(side=LEFT, padx=4)
        ttk.Button(frame_btn, text="📋 Tampilkan Semua", bootstyle="secondary",
                   command=self._tampilkan_semua_cari, width=18).pack(side=LEFT, padx=4)

        # Info metode
        self.lbl_info_cari = ttk.Label(frame_cari,
                                        text="ℹ️ Sequential Search: cek setiap elemen satu per satu. "
                                             "Binary Search: butuh data terurut, cari dengan membagi dua.",
                                        bootstyle="secondary", wraplength=500, justify=LEFT)
        self.lbl_info_cari.grid(row=3, column=0, columnspan=2,
                                 sticky=W, padx=5, pady=4)

        # Hasil
        frame_hasil = ttk.LabelFrame(self.tab_cari,
                                     text="  Hasil Pencarian  ",
                                     bootstyle="info", padding=10)
        frame_hasil.pack(fill=BOTH, expand=True, padx=15, pady=5)

        self.lbl_hasil_cari = ttk.Label(frame_hasil, text="",
                                         bootstyle="info", font=("Segoe UI", 9))
        self.lbl_hasil_cari.pack(anchor=W, pady=(0, 5))

        kolom = ("No", "Nama Aset", "Jenis", "Dana Awal",
                 "Harga Kini", "Jumlah Unit", "Nilai Sekarang", "Untung/Rugi", "%")
        self.tree_cari = ttk.Treeview(frame_hasil, columns=kolom,
                                       show="headings", bootstyle="info",
                                       height=10)
        lebar = [40, 150, 100, 120, 110, 100, 130, 120, 80]
        for i, (k, l) in enumerate(zip(kolom, lebar)):
            self.tree_cari.heading(k, text=k)
            self.tree_cari.column(k, width=l, anchor=CENTER if i == 0 else W)
        sb = ttk.Scrollbar(frame_hasil, orient=VERTICAL,
                            command=self.tree_cari.yview)
        sb_x = ttk.Scrollbar(frame_hasil, orient=HORIZONTAL,
                              command=self.tree_cari.xview)
        self.tree_cari.configure(yscrollcommand=sb.set,
                                  xscrollcommand=sb_x.set)
        sb.pack(side=RIGHT, fill=Y)
        sb_x.pack(side=BOTTOM, fill=X)
        self.tree_cari.pack(fill=BOTH, expand=True)

    # ------------------------------------------------------------------
    # TAB 4: URUTKAN
    # ------------------------------------------------------------------
    def _bangun_tab_urutkan(self):
        frame_opsi = ttk.LabelFrame(self.tab_urutkan,
                                    text="  Opsi Pengurutan  ",
                                    bootstyle="warning", padding=15)
        frame_opsi.pack(fill=X, padx=15, pady=15)

        ttk.Label(frame_opsi, text="Urutkan berdasarkan:").grid(
            row=0, column=0, sticky=W, padx=5)
        ttk.Combobox(frame_opsi, textvariable=self.var_sort_key,
                     values=["Nilai Investasi", "Persentase Keuntungan",
                             "Dana Awal", "Nama Aset"],
                     state="readonly", width=28).grid(row=0, column=1,
                                                      padx=5, pady=4)

        ttk.Label(frame_opsi, text="Algoritma Pengurutan:").grid(
            row=1, column=0, sticky=W, padx=5)
        ttk.Combobox(frame_opsi, textvariable=self.var_sort_algo,
                     values=["Selection Sort", "Insertion Sort"],
                     state="readonly", width=28).grid(row=1, column=1,
                                                      padx=5, pady=4)

        ttk.Label(frame_opsi, text="Urutan:").grid(
            row=2, column=0, sticky=W, padx=5)
        frame_radio = ttk.Frame(frame_opsi)
        frame_radio.grid(row=2, column=1, sticky=W, padx=5)
        ttk.Radiobutton(frame_radio, text="Ascending (Naik) ↑",
                        variable=self.var_sort_order,
                        value="Ascending", bootstyle="warning").pack(side=LEFT, padx=5)
        ttk.Radiobutton(frame_radio, text="Descending (Turun) ↓",
                        variable=self.var_sort_order,
                        value="Descending", bootstyle="warning").pack(side=LEFT, padx=5)

        ttk.Button(frame_opsi, text="🔃 Urutkan Sekarang", bootstyle="warning",
                   command=self._urutkan, width=20).grid(
            row=3, column=0, columnspan=2, pady=10, sticky=W, padx=5)

        self.lbl_info_sort = ttk.Label(frame_opsi, text="",
                                        bootstyle="secondary",
                                        font=("Segoe UI", 9))
        self.lbl_info_sort.grid(row=4, column=0, columnspan=2,
                                 sticky=W, padx=5)

        # Hasil urutan
        frame_hasil = ttk.LabelFrame(self.tab_urutkan,
                                     text="  Hasil Pengurutan  ",
                                     bootstyle="warning", padding=10)
        frame_hasil.pack(fill=BOTH, expand=True, padx=15, pady=5)

        kolom = ("Rank", "Nama Aset", "Jenis", "Dana Awal",
                 "Harga Kini", "Jumlah Unit", "Nilai Sekarang", "Untung/Rugi", "%")
        self.tree_sort = ttk.Treeview(frame_hasil, columns=kolom,
                                       show="headings", bootstyle="warning",
                                       height=12)
        lebar = [50, 150, 100, 120, 110, 100, 130, 120, 80]
        for i, (k, l) in enumerate(zip(kolom, lebar)):
            self.tree_sort.heading(k, text=k)
            self.tree_sort.column(k, width=l, anchor=CENTER if i == 0 else W)
        sb = ttk.Scrollbar(frame_hasil, orient=VERTICAL,
                            command=self.tree_sort.yview)
        sb_x = ttk.Scrollbar(frame_hasil, orient=HORIZONTAL,
                              command=self.tree_sort.xview)
        self.tree_sort.configure(yscrollcommand=sb.set,
                                  xscrollcommand=sb_x.set)
        sb.pack(side=RIGHT, fill=Y)
        sb_x.pack(side=BOTTOM, fill=X)
        self.tree_sort.pack(fill=BOTH, expand=True)

    # ------------------------------------------------------------------
    # DATA CONTOH
    # ------------------------------------------------------------------
    def _muat_data_contoh(self):
        contoh = [
            ("BBCA", "Saham", 5000000, 9500, 600),
            ("ORI023", "Obligasi", 3000000, 1010, 2970),
            ("Reksa Dana Syariah", "Reksa Dana", 2000000, 1250, 1600),
            ("TLKM", "Saham", 4000000, 3800, 1100),
            ("SBR012", "Obligasi", 2500000, 1005, 2487),
        ]
        for c in contoh:
            tambah_investasi(*c)

    # ------------------------------------------------------------------
    # REFRESH TABEL & STATISTIK
    # ------------------------------------------------------------------
    def _baris_investasi(self, no, inv):
        nilai = hitung_nilai_sekarang(inv)
        untung = hitung_keuntungan(inv)
        persen = hitung_persentase(inv)
        return (no,
                inv["nama"],
                inv["jenis"],
                format_rupiah(inv["dana"]),
                format_rupiah(inv["harga_kini"]),
                f"{inv['jumlah_unit']:,.2f}",
                format_rupiah(nilai),
                format_rupiah(untung),
                f"{persen:+.2f}%")

    def _refresh_tabel(self, trees=None, data=None):
        if trees is None:
            trees = [self.tree_dash, self.tree_kelola]
        for tree in trees:
            for item in tree.get_children():
                tree.delete(item)
        src = data if data is not None else [data_investasi[i] for i in range(jumlah_data)]
        for idx, inv in enumerate(src):
            baris = self._baris_investasi(idx + 1, inv)
            tag = "positif" if hitung_keuntungan(inv) >= 0 else "negatif"
            for tree in trees:
                tree.insert("", END, values=baris, tags=(tag,))
        for tree in trees:
            tree.tag_configure("positif", foreground="#198754")
            tree.tag_configure("negatif", foreground="#dc3545")

    def _update_statistik(self):
        total_dana = hitung_total_dana()
        total_nilai = hitung_total_nilai_sekarang()
        total_untung = total_nilai - total_dana
        self.lbl_total_dana.config(text=format_rupiah(total_dana))
        self.lbl_total_nilai.config(text=format_rupiah(total_nilai))
        teks_untung = format_rupiah(total_untung)
        style = "success" if total_untung >= 0 else "danger"
        self.lbl_total_untung.config(text=teks_untung, bootstyle=style)
        self.lbl_jumlah_aset.config(text=str(jumlah_data))

    # ------------------------------------------------------------------
    # AKSI FORM KELOLA
    # ------------------------------------------------------------------
    def _validasi_form(self):
        nama = self.var_nama.get().strip()
        jenis = self.var_jenis.get().strip()
        dana_str = self.var_dana.get().strip()
        harga_str = self.var_harga.get().strip()
        unit_str = self.var_unit.get().strip()

        if not nama or not jenis or not dana_str or not harga_str or not unit_str:
            Messagebox.show_error("Semua field wajib diisi!", "Validasi Error")
            return None
        try:
            dana = float(dana_str.replace(",", ""))
            harga = float(harga_str.replace(",", ""))
            unit = float(unit_str.replace(",", ""))
            if dana <= 0 or harga <= 0 or unit <= 0:
                raise ValueError
        except ValueError:
            Messagebox.show_error("Dana, Harga, dan Unit harus angka positif!", "Validasi Error")
            return None
        return nama, jenis, dana, harga, unit

    def _tambah(self):
        hasil = self._validasi_form()
        if hasil is None:
            return
        nama, jenis, dana, harga, unit = hasil
        if not tambah_investasi(nama, jenis, dana, harga, unit):
            Messagebox.show_error("Array penuh! Maksimum 100 data.", "Error")
            return
        self._refresh_tabel()
        self._update_statistik()
        self._reset_form()
        Messagebox.show_info(f"✅ Aset '{nama}' berhasil ditambahkan!", "Berhasil")

    def _ubah(self):
        if self.indeks_dipilih < 0:
            Messagebox.show_warning("Pilih data yang ingin diubah pada tabel!", "Peringatan")
            return
        hasil = self._validasi_form()
        if hasil is None:
            return
        nama, jenis, dana, harga, unit = hasil
        if not ubah_investasi(self.indeks_dipilih, nama, jenis, dana, harga, unit):
            Messagebox.show_error("Gagal mengubah data.", "Error")
            return
        self._refresh_tabel()
        self._update_statistik()
        self._reset_form()
        Messagebox.show_info(f"✅ Data aset berhasil diperbarui!", "Berhasil")

    def _hapus(self):
        if self.indeks_dipilih < 0:
            Messagebox.show_warning("Pilih data yang ingin dihapus pada tabel!", "Peringatan")
            return
        nama = data_investasi[self.indeks_dipilih]["nama"]
        konfirmasi = Messagebox.yesno(
            f"Hapus aset '{nama}'?", "Konfirmasi Hapus")
        if konfirmasi == "Yes":
            hapus_investasi(self.indeks_dipilih)
            self._refresh_tabel()
            self._update_statistik()
            self._reset_form()
            Messagebox.show_info("✅ Data berhasil dihapus!", "Berhasil")

    def _reset_form(self):
        self.var_nama.set("")
        self.var_jenis.set("Saham")
        self.var_dana.set("")
        self.var_harga.set("")
        self.var_unit.set("")
        self.indeks_dipilih = -1

    def _pilih_baris_kelola(self, event):
        sel = self.tree_kelola.selection()
        if not sel:
            return
        idx = self.tree_kelola.index(sel[0])
        if idx >= jumlah_data:
            return
        self.indeks_dipilih = idx
        inv = data_investasi[idx]
        self.var_nama.set(inv["nama"])
        self.var_jenis.set(inv["jenis"])
        self.var_dana.set(str(inv["dana"]))
        self.var_harga.set(str(inv["harga_kini"]))
        self.var_unit.set(str(inv["jumlah_unit"]))

    # ------------------------------------------------------------------
    # AKSI CARI
    # ------------------------------------------------------------------
    def _cari(self):
        keyword = self.var_cari.get().strip()
        mode = self.var_cari_mode.get()

        if not keyword:
            Messagebox.show_warning("Masukkan kata kunci pencarian!", "Peringatan")
            return

        for item in self.tree_cari.get_children():
            self.tree_cari.delete(item)

        if mode == "Nama (Sequential)":
            indeks = sequential_search_nama(keyword)
            metode_info = f"Sequential Search by Nama | Keyword: '{keyword}' | Ditemukan: {len(indeks)} data"
            hasil = [data_investasi[i] for i in indeks]

        elif mode == "Jenis (Sequential)":
            indeks = sequential_search_jenis(keyword)
            metode_info = f"Sequential Search by Jenis | Keyword: '{keyword}' | Ditemukan: {len(indeks)} data"
            hasil = [data_investasi[i] for i in indeks]

        else:  # Binary Search
            arr_sorted = insertion_sort(
                [data_investasi[i] for i in range(jumlah_data)],
                lambda x: x["nama"].lower(), ascending=True)
            idx_bs = binary_search_nama(arr_sorted, keyword)
            if idx_bs >= 0:
                hasil = [arr_sorted[idx_bs]]
                metode_info = (f"Binary Search (Exact) | Keyword: '{keyword}' | "
                               f"Ditemukan pada indeks {idx_bs} (array terurut)")
            else:
                hasil = []
                metode_info = f"Binary Search (Exact) | Keyword: '{keyword}' | Tidak ditemukan"

        self.lbl_hasil_cari.config(text=metode_info)
        for idx, inv in enumerate(hasil):
            baris = self._baris_investasi(idx + 1, inv)
            tag = "positif" if hitung_keuntungan(inv) >= 0 else "negatif"
            self.tree_cari.insert("", END, values=baris, tags=(tag,))
        self.tree_cari.tag_configure("positif", foreground="#198754")
        self.tree_cari.tag_configure("negatif", foreground="#dc3545")

    def _tampilkan_semua_cari(self):
        self.var_cari.set("")
        self.lbl_hasil_cari.config(text=f"Menampilkan semua {jumlah_data} data")
        self._refresh_tabel(trees=[self.tree_cari])

    # ------------------------------------------------------------------
    # AKSI URUTKAN
    # ------------------------------------------------------------------
    def _urutkan(self):
        if jumlah_data == 0:
            Messagebox.show_warning("Belum ada data investasi!", "Peringatan")
            return

        key_name = self.var_sort_key.get()
        algo = self.var_sort_algo.get()
        order = self.var_sort_order.get()
        ascending = (order == "Ascending")

        key_map = {
            "Nilai Investasi": hitung_nilai_sekarang,
            "Persentase Keuntungan": hitung_persentase,
            "Dana Awal": lambda x: x["dana"],
            "Nama Aset": lambda x: x["nama"].lower(),
        }
        key_func = key_map[key_name]
        data_list = [data_investasi[i] for i in range(jumlah_data)]

        if algo == "Selection Sort":
            hasil = selection_sort(data_list, key_func, ascending)
            algo_info = "Selection Sort: cari elemen min/maks, tukar ke posisi yang benar."
        else:
            hasil = insertion_sort(data_list, key_func, ascending)
            algo_info = "Insertion Sort: ambil elemen, sisipkan ke posisi yang tepat di bagian yang sudah terurut."

        for item in self.tree_sort.get_children():
            self.tree_sort.delete(item)
        for idx, inv in enumerate(hasil):
            baris = self._baris_investasi(idx + 1, inv)
            tag = "positif" if hitung_keuntungan(inv) >= 0 else "negatif"
            self.tree_sort.insert("", END, values=baris, tags=(tag,))
        self.tree_sort.tag_configure("positif", foreground="#198754")
        self.tree_sort.tag_configure("negatif", foreground="#dc3545")

        self.lbl_info_sort.config(
            text=f"✅ {algo} | Kunci: {key_name} | {order} | {algo_info}")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    app = ttk.Window(themename="flatly")
    AplikasiInvestasi(app)
    app.mainloop()