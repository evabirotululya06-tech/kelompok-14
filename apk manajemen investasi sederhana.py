import tkinter as tk
from tkinter import ttk, messagebox

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
    return investasi["harga_kini"] * investasi["jumlah_unit"]


def hitung_keuntungan(investasi: dict) -> float:
    return hitung_nilai_sekarang(investasi) - investasi["dana"]


def hitung_persentase(investasi: dict) -> float:
    if investasi["dana"] == 0:
        return 0.0
    return (hitung_keuntungan(investasi) / investasi["dana"]) * 100


def hitung_total_dana() -> float:
    total = 0.0
    i = 0
    while i < jumlah_data:
        total += data_investasi[i]["dana"]
        i += 1
    return total


def hitung_total_nilai_sekarang() -> float:
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
    hasil = []
    i = 0
    while i < jumlah_data:
        if keyword.lower() in data_investasi[i]["nama"].lower():
            hasil.append(i)
        i += 1
    return hasil


def sequential_search_jenis(jenis: str) -> list:
    hasil = []
    i = 0
    while i < jumlah_data:
        if jenis.lower() in data_investasi[i]["jenis"].lower():
            hasil.append(i)
        i += 1
    return hasil


# ============================================================
# SUBPROGRAM: BINARY SEARCH
# ============================================================

def binary_search_nama(arr_sorted: list, keyword: str) -> int:
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
    if nilai < 0:
        return f"-Rp {abs(nilai):,.0f}"
    return f"Rp {nilai:,.0f}"


# ============================================================
# GUI - APLIKASI MANAJEMEN INVESTASI
# ============================================================

class AplikasiInvestasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Manajemen Investasi Sederhana")
        self.root.geometry("1100x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f4f8")

        # Variabel form
        self.var_nama = tk.StringVar()
        self.var_jenis = tk.StringVar(value="Saham")
        self.var_dana = tk.StringVar()
        self.var_harga = tk.StringVar()
        self.var_unit = tk.StringVar()
        self.var_cari = tk.StringVar()
        self.var_cari_mode = tk.StringVar(value="Nama (Sequential)")
        self.var_sort_key = tk.StringVar(value="Nilai Investasi")
        self.var_sort_algo = tk.StringVar(value="Selection Sort")
        self.var_sort_order = tk.StringVar(value="Descending")

        self.indeks_dipilih = -1

        # Style ttk
        self._setup_style()
        self._bangun_ui()
        self._muat_data_contoh()
        self._refresh_tabel()
        self._update_statistik()

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TNotebook", background="#f0f4f8", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10), padding=[12, 6],
                        background="#dce3ed", foreground="#333")
        style.map("TNotebook.Tab",
                  background=[("selected", "#ffffff")],
                  foreground=[("selected", "#1a73e8")])

        style.configure("TFrame", background="#f0f4f8")
        style.configure("TLabel", background="#f0f4f8", font=("Segoe UI", 9))
        style.configure("TButton", font=("Segoe UI", 9), padding=5)
        style.configure("TEntry", font=("Segoe UI", 9))
        style.configure("TCombobox", font=("Segoe UI", 9))

        style.configure("Treeview",
                        font=("Segoe UI", 9),
                        rowheight=24,
                        background="#ffffff",
                        fieldbackground="#ffffff",
                        foreground="#333333")
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 9, "bold"),
                        background="#e8edf3",
                        foreground="#333333")
        style.map("Treeview", background=[("selected", "#cfe2ff")])

        style.configure("LabelFrame.Label", font=("Segoe UI", 9, "bold"),
                        foreground="#1a73e8", background="#f0f4f8")
        style.configure("TLabelframe", background="#f0f4f8", bordercolor="#c0cfe0")
        style.configure("TLabelframe.Label", background="#f0f4f8",
                        font=("Segoe UI", 9, "bold"), foreground="#1a73e8")

        # Kartu stat styles
        style.configure("Kartu.TFrame", background="#ffffff",
                        relief="solid", borderwidth=1)
        style.configure("KartuJudul.TLabel", background="#ffffff",
                        font=("Segoe UI", 9), foreground="#666666")
        style.configure("KartuNilai.TLabel", background="#ffffff",
                        font=("Segoe UI", 11, "bold"), foreground="#1a73e8")

    def _bangun_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab_dashboard = ttk.Frame(self.notebook)
        self.tab_kelola = ttk.Frame(self.notebook)
        self.tab_cari = ttk.Frame(self.notebook)
        self.tab_urutkan = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_dashboard, text="  Dashboard  ")
        self.notebook.add(self.tab_kelola, text="  Kelola Data  ")
        self.notebook.add(self.tab_cari, text="  Cari Aset  ")
        self.notebook.add(self.tab_urutkan, text="  Urutkan  ")

        self._bangun_tab_dashboard()
        self._bangun_tab_kelola()
        self._bangun_tab_cari()
        self._bangun_tab_urutkan()

    # ------------------------------------------------------------------
    # TAB 1: DASHBOARD
    # ------------------------------------------------------------------
    def _bangun_tab_dashboard(self):
        frame_atas = ttk.Frame(self.tab_dashboard)
        frame_atas.pack(fill=tk.X, padx=15, pady=(15, 5))

        ttk.Label(frame_atas, text="Portofolio Investasi Saya",
                  font=("Segoe UI", 16, "bold"),
                  foreground="#1a73e8").pack(side=tk.LEFT)

        # Kartu statistik
        frame_kartu = ttk.Frame(self.tab_dashboard)
        frame_kartu.pack(fill=tk.X, padx=15, pady=5)

        self.lbl_total_dana = self._kartu_stat(frame_kartu, "Total Dana", "Rp 0", "#1a73e8", 0)
        self.lbl_total_nilai = self._kartu_stat(frame_kartu, "Nilai Sekarang", "Rp 0", "#198754", 1)
        self.lbl_total_untung = self._kartu_stat(frame_kartu, "Keuntungan/Rugi", "Rp 0", "#f59e0b", 2)
        self.lbl_jumlah_aset = self._kartu_stat(frame_kartu, "Jumlah Aset", "0", "#6c757d", 3)

        for i in range(4):
            frame_kartu.columnconfigure(i, weight=1)

        # Tabel portofolio
        frame_tabel = ttk.LabelFrame(self.tab_dashboard,
                                     text="  Daftar Aset Investasi  ")
        frame_tabel.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        kolom = ("No", "Nama Aset", "Jenis", "Dana Awal", "Harga Kini",
                 "Jumlah Unit", "Nilai Sekarang", "Keuntungan/Rugi", "Persentase")
        self.tree_dash = ttk.Treeview(frame_tabel, columns=kolom,
                                      show="headings",
                                      selectmode="browse", height=12)

        lebar = [40, 150, 100, 120, 110, 100, 130, 130, 90]
        for i, (k, l) in enumerate(zip(kolom, lebar)):
            self.tree_dash.heading(k, text=k)
            self.tree_dash.column(k, width=l,
                                  anchor=tk.CENTER if i == 0 else tk.W)

        sb_y = ttk.Scrollbar(frame_tabel, orient=tk.VERTICAL,
                              command=self.tree_dash.yview)
        sb_x = ttk.Scrollbar(frame_tabel, orient=tk.HORIZONTAL,
                              command=self.tree_dash.xview)
        self.tree_dash.configure(yscrollcommand=sb_y.set,
                                 xscrollcommand=sb_x.set)
        sb_y.pack(side=tk.RIGHT, fill=tk.Y)
        sb_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_dash.pack(fill=tk.BOTH, expand=True)

    def _kartu_stat(self, parent, judul, nilai, warna, col):
        # Frame luar untuk border efek kartu
        outer = tk.Frame(parent, bg=warna, bd=0)
        outer.grid(row=0, column=col, padx=5, pady=5, sticky=tk.NSEW)

        inner = tk.Frame(outer, bg="#ffffff", bd=0)
        inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        tk.Label(inner, text=judul, font=("Segoe UI", 9),
                 fg="#666666", bg="#ffffff").pack(pady=(10, 2))
        lbl = tk.Label(inner, text=nilai, font=("Segoe UI", 11, "bold"),
                       fg=warna, bg="#ffffff")
        lbl.pack(pady=(0, 10))
        return lbl

    # ------------------------------------------------------------------
    # TAB 2: KELOLA DATA
    # ------------------------------------------------------------------
    def _bangun_tab_kelola(self):
        frame_form = ttk.LabelFrame(self.tab_kelola,
                                    text="  Form Data Investasi  ")
        frame_form.pack(fill=tk.X, padx=15, pady=(15, 5))

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
                                                  sticky=tk.W, pady=4, padx=5)
            if pilihan:
                w = ttk.Combobox(frame_form, textvariable=var,
                                  values=pilihan, state="readonly", width=28)
            else:
                w = ttk.Entry(frame_form, textvariable=var, width=30)
            w.grid(row=baris, column=1, sticky=tk.W, pady=4, padx=5)

        frame_btn = ttk.Frame(frame_form)
        frame_btn.grid(row=len(fields), column=0, columnspan=2,
                       pady=10, sticky=tk.W)

        ttk.Button(frame_btn, text="Tambah",
                   command=self._tambah, width=12).pack(side=tk.LEFT, padx=4)
        ttk.Button(frame_btn, text="Ubah",
                   command=self._ubah, width=12).pack(side=tk.LEFT, padx=4)
        ttk.Button(frame_btn, text="Hapus",
                   command=self._hapus, width=12).pack(side=tk.LEFT, padx=4)
        ttk.Button(frame_btn, text="Reset Form",
                   command=self._reset_form, width=12).pack(side=tk.LEFT, padx=4)

        frame_list = ttk.LabelFrame(self.tab_kelola,
                                    text="  Data Investasi  ")
        frame_list.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        kolom = ("No", "Nama Aset", "Jenis", "Dana Awal",
                 "Harga Kini", "Jumlah Unit", "Nilai Sekarang", "Untung/Rugi", "%")
        self.tree_kelola = ttk.Treeview(frame_list, columns=kolom,
                                        show="headings",
                                        selectmode="browse", height=8)
        lebar = [40, 150, 100, 120, 110, 100, 130, 120, 80]
        for i, (k, l) in enumerate(zip(kolom, lebar)):
            self.tree_kelola.heading(k, text=k)
            self.tree_kelola.column(k, width=l,
                                    anchor=tk.CENTER if i == 0 else tk.W)

        sb = ttk.Scrollbar(frame_list, orient=tk.VERTICAL,
                            command=self.tree_kelola.yview)
        sb_x = ttk.Scrollbar(frame_list, orient=tk.HORIZONTAL,
                              command=self.tree_kelola.xview)
        self.tree_kelola.configure(yscrollcommand=sb.set,
                                   xscrollcommand=sb_x.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        sb_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_kelola.pack(fill=tk.BOTH, expand=True)
        self.tree_kelola.bind("<<TreeviewSelect>>", self._pilih_baris_kelola)

    # ------------------------------------------------------------------
    # TAB 3: CARI ASET
    # ------------------------------------------------------------------
    def _bangun_tab_cari(self):
        frame_cari = ttk.LabelFrame(self.tab_cari,
                                    text="  Pencarian Aset  ")
        frame_cari.pack(fill=tk.X, padx=15, pady=15)

        ttk.Label(frame_cari, text="Kata Kunci:").grid(row=0, column=0,
                                                        sticky=tk.W, padx=5)
        ttk.Entry(frame_cari, textvariable=self.var_cari,
                  width=35).grid(row=0, column=1, padx=5, pady=4)

        ttk.Label(frame_cari, text="Metode Pencarian:").grid(row=1, column=0,
                                                              sticky=tk.W, padx=5)
        ttk.Combobox(frame_cari, textvariable=self.var_cari_mode,
                     values=["Nama (Sequential)", "Jenis (Sequential)",
                             "Nama (Binary Search - Exact)"],
                     state="readonly", width=33).grid(row=1, column=1,
                                                      padx=5, pady=4)

        frame_btn = ttk.Frame(frame_cari)
        frame_btn.grid(row=2, column=0, columnspan=2, pady=8, sticky=tk.W)
        ttk.Button(frame_btn, text="Cari",
                   command=self._cari, width=12).pack(side=tk.LEFT, padx=4)
        ttk.Button(frame_btn, text="Tampilkan Semua",
                   command=self._tampilkan_semua_cari, width=18).pack(side=tk.LEFT, padx=4)

        self.lbl_info_cari = ttk.Label(frame_cari,
                                        text="Sequential Search: cek setiap elemen satu per satu. "
                                             "Binary Search: butuh data terurut, cari dengan membagi dua.",
                                        wraplength=500, justify=tk.LEFT)
        self.lbl_info_cari.grid(row=3, column=0, columnspan=2,
                                 sticky=tk.W, padx=5, pady=4)

        frame_hasil = ttk.LabelFrame(self.tab_cari,
                                     text="  Hasil Pencarian  ")
        frame_hasil.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.lbl_hasil_cari = ttk.Label(frame_hasil, text="",
                                          font=("Segoe UI", 9))
        self.lbl_hasil_cari.pack(anchor=tk.W, pady=(0, 5))

        kolom = ("No", "Nama Aset", "Jenis", "Dana Awal",
                 "Harga Kini", "Jumlah Unit", "Nilai Sekarang", "Untung/Rugi", "%")
        self.tree_cari = ttk.Treeview(frame_hasil, columns=kolom,
                                       show="headings", height=10)
        lebar = [40, 150, 100, 120, 110, 100, 130, 120, 80]
        for i, (k, l) in enumerate(zip(kolom, lebar)):
            self.tree_cari.heading(k, text=k)
            self.tree_cari.column(k, width=l,
                                  anchor=tk.CENTER if i == 0 else tk.W)
        sb = ttk.Scrollbar(frame_hasil, orient=tk.VERTICAL,
                            command=self.tree_cari.yview)
        sb_x = ttk.Scrollbar(frame_hasil, orient=tk.HORIZONTAL,
                              command=self.tree_cari.xview)
        self.tree_cari.configure(yscrollcommand=sb.set,
                                  xscrollcommand=sb_x.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        sb_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_cari.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------
    # TAB 4: URUTKAN
    # ------------------------------------------------------------------
    def _bangun_tab_urutkan(self):
        frame_opsi = ttk.LabelFrame(self.tab_urutkan,
                                    text="  Opsi Pengurutan  ")
        frame_opsi.pack(fill=tk.X, padx=15, pady=15)

        ttk.Label(frame_opsi, text="Urutkan berdasarkan:").grid(
            row=0, column=0, sticky=tk.W, padx=5)
        ttk.Combobox(frame_opsi, textvariable=self.var_sort_key,
                     values=["Nilai Investasi", "Persentase Keuntungan",
                             "Dana Awal", "Nama Aset"],
                     state="readonly", width=28).grid(row=0, column=1,
                                                      padx=5, pady=4)

        ttk.Label(frame_opsi, text="Algoritma Pengurutan:").grid(
            row=1, column=0, sticky=tk.W, padx=5)
        ttk.Combobox(frame_opsi, textvariable=self.var_sort_algo,
                     values=["Selection Sort", "Insertion Sort"],
                     state="readonly", width=28).grid(row=1, column=1,
                                                      padx=5, pady=4)

        ttk.Label(frame_opsi, text="Urutan:").grid(
            row=2, column=0, sticky=tk.W, padx=5)
        frame_radio = ttk.Frame(frame_opsi)
        frame_radio.grid(row=2, column=1, sticky=tk.W, padx=5)
        ttk.Radiobutton(frame_radio, text="Ascending (Naik)",
                        variable=self.var_sort_order,
                        value="Ascending").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(frame_radio, text="Descending (Turun)",
                        variable=self.var_sort_order,
                        value="Descending").pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_opsi, text="Urutkan Sekarang",
                   command=self._urutkan, width=20).grid(
            row=3, column=0, columnspan=2, pady=10, sticky=tk.W, padx=5)

        self.lbl_info_sort = ttk.Label(frame_opsi, text="",
                                        font=("Segoe UI", 9))
        self.lbl_info_sort.grid(row=4, column=0, columnspan=2,
                                 sticky=tk.W, padx=5)

        frame_hasil = ttk.LabelFrame(self.tab_urutkan,
                                     text="  Hasil Pengurutan  ")
        frame_hasil.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        kolom = ("Rank", "Nama Aset", "Jenis", "Dana Awal",
                 "Harga Kini", "Jumlah Unit", "Nilai Sekarang", "Untung/Rugi", "%")
        self.tree_sort = ttk.Treeview(frame_hasil, columns=kolom,
                                       show="headings", height=12)
        lebar = [50, 150, 100, 120, 110, 100, 130, 120, 80]
        for i, (k, l) in enumerate(zip(kolom, lebar)):
            self.tree_sort.heading(k, text=k)
            self.tree_sort.column(k, width=l,
                                  anchor=tk.CENTER if i == 0 else tk.W)
        sb = ttk.Scrollbar(frame_hasil, orient=tk.VERTICAL,
                            command=self.tree_sort.yview)
        sb_x = ttk.Scrollbar(frame_hasil, orient=tk.HORIZONTAL,
                              command=self.tree_sort.xview)
        self.tree_sort.configure(yscrollcommand=sb.set,
                                  xscrollcommand=sb_x.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        sb_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_sort.pack(fill=tk.BOTH, expand=True)

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
                tree.insert("", tk.END, values=baris, tags=(tag,))
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
        warna = "#198754" if total_untung >= 0 else "#dc3545"
        self.lbl_total_untung.config(text=teks_untung, fg=warna)
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
            messagebox.showerror("Validasi Error", "Semua field wajib diisi!")
            return None
        try:
            dana = float(dana_str.replace(",", ""))
            harga = float(harga_str.replace(",", ""))
            unit = float(unit_str.replace(",", ""))
            if dana <= 0 or harga <= 0 or unit <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validasi Error",
                                 "Dana, Harga, dan Unit harus angka positif!")
            return None
        return nama, jenis, dana, harga, unit

    def _tambah(self):
        hasil = self._validasi_form()
        if hasil is None:
            return
        nama, jenis, dana, harga, unit = hasil
        if not tambah_investasi(nama, jenis, dana, harga, unit):
            messagebox.showerror("Error", "Array penuh! Maksimum 100 data.")
            return
        self._refresh_tabel()
        self._update_statistik()
        self._reset_form()
        messagebox.showinfo("Berhasil", f"Aset '{nama}' berhasil ditambahkan!")

    def _ubah(self):
        if self.indeks_dipilih < 0:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diubah pada tabel!")
            return
        hasil = self._validasi_form()
        if hasil is None:
            return
        nama, jenis, dana, harga, unit = hasil
        if not ubah_investasi(self.indeks_dipilih, nama, jenis, dana, harga, unit):
            messagebox.showerror("Error", "Gagal mengubah data.")
            return
        self._refresh_tabel()
        self._update_statistik()
        self._reset_form()
        messagebox.showinfo("Berhasil", "Data aset berhasil diperbarui!")

    def _hapus(self):
        if self.indeks_dipilih < 0:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus pada tabel!")
            return
        nama = data_investasi[self.indeks_dipilih]["nama"]
        konfirmasi = messagebox.askyesno("Konfirmasi Hapus",
                                          f"Hapus aset '{nama}'?")
        if konfirmasi:
            hapus_investasi(self.indeks_dipilih)
            self._refresh_tabel()
            self._update_statistik()
            self._reset_form()
            messagebox.showinfo("Berhasil", "Data berhasil dihapus!")

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
            messagebox.showwarning("Peringatan", "Masukkan kata kunci pencarian!")
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
            self.tree_cari.insert("", tk.END, values=baris, tags=(tag,))
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
            messagebox.showwarning("Peringatan", "Belum ada data investasi!")
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
            self.tree_sort.insert("", tk.END, values=baris, tags=(tag,))
        self.tree_sort.tag_configure("positif", foreground="#198754")
        self.tree_sort.tag_configure("negatif", foreground="#dc3545")

        self.lbl_info_sort.config(
            text=f"{algo} | Kunci: {key_name} | {order} | {algo_info}")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiInvestasi(root)
    root.mainloop()