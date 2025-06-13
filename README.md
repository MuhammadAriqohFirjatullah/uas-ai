#  Sistem AI Prediksi Kemacetan Kota Bengkulu

##  Studi Kasus Smart City – Tugas UAS

Proyek ini merupakan implementasi sistem **prediksi kemacetan real-time** untuk Kota Bengkulu, sebagai bagian dari solusi Smart City. Sistem ini terdiri dari model kecerdasan buatan untuk klasifikasi lalu lintas, API backend, serta antarmuka web interaktif.

---

##  Tim Pengembang

* Lio Kusnata                 (G1A023013)
* Muhammad Ariqoh Firjatullah (G1A023033)
* Ajis Saputra Hidayah        (G1A023083)


##  1. Struktur Proyek

```
uas ai fix/
├── index.html                 # Halaman utama frontend
├── script.js                  # Script interaksi frontend
├── styles.css                 # Styling halaman web
└── scripts/
    ├── flask_api.py           # Backend Flask untuk melayani prediksi
    ├── run_system.py          # Main script untuk menjalankan keseluruhan sistem
    └── traffic_prediction_model.py  # Model AI prediksi kemacetan
```

---

##  2. Model AI yang Digunakan

* **Algoritma**: `RandomForestClassifier` (Scikit-learn)
* **Alasan Pemilihan**:

  * Cocok untuk klasifikasi multi-kelas
  * Akurat dan cepat dalam inferensi
  * Mampu menangani data non-linear dan kompleks
  * Memberikan feature importance untuk interpretasi
  * Tahan terhadap overfitting (karena pendekatan ensemble)

---

## 🧾 3. Jenis dan Sumber Data

### Jenis Data:

* **Waktu**: `hour`, `day_of_week`, `is_weekend`
* **Lalu Lintas**: `traffic_volume`, `average_speed`, `has_incident`
* **Lingkungan**: `weather`
* **Spasial**: `road_segment`

### Label:

* `traffic_level`: Lancar, Ramai Lancar, Padat, Macet

### Sumber Data:

* Saat ini: generator data lokal berbasis skrip
* Rencana ke depan: sensor volume kendaraan, CCTV, API cuaca, crowdsourcing pengguna

### Praproses:

* Encoding variabel kategorikal (`weather`, `road_segment`)
* Konversi fitur waktu menjadi bentuk siklikal (`sin`, `cos`)
* Penambahan fitur turunan: `rush_hour`, `market_day`
* Pembagian data: 80% pelatihan, 20% pengujian

---

##  4. Desain Alur Kerja Sistem

### Narasi Teknis:

Sistem prediksi kemacetan ini berjalan melalui lima tahap utama yang saling terintegrasi:

1. **Data dikumpulkan** dari sensor lalu lintas, data cuaca, dan informasi waktu.
2. **Data diproses** untuk ekstraksi fitur dan normalisasi agar sesuai dengan input model.
3. **Model AI (Random Forest)** digunakan untuk memprediksi tingkat kemacetan berdasarkan input.
4. **API Backend (Flask)** menerima permintaan dan memberikan respons prediksi ke pengguna.
5. **Frontend Web** menampilkan prediksi dalam tampilan visual dan interaktif.

### Diagram Alur:

```
+------------------+       +----------------------+       +---------------------+
|  Data Collection | --->  | Feature Engineering  | --->  |  AI Prediction      |
| (Sensor, Weather)|       |  & Preprocessing     |       |  (Random Forest)    |
+------------------+       +----------------------+       +---------------------+
                                                                   |
                                                                   v
                                                        +---------------------+
                                                        |    Flask API        |
                                                        +---------------------+
                                                                   |
                                                                   v
                                                        +---------------------+
                                                        |   Web Frontend      |
                                                        +---------------------+
```

---

##  5. Evaluasi Model

### Strategi Evaluasi:

* Dataset dibagi 80% untuk pelatihan dan 20% untuk pengujian.
* Validasi dilakukan dengan data uji yang tidak pernah dilatih sebelumnya.

### Metrik Evaluasi:

* **Accuracy**: Persentase prediksi benar dari seluruh prediksi.
* **Precision**: Ketepatan prediksi untuk tiap kelas kemacetan.
* **Recall**: Kemampuan model dalam menangkap seluruh kasus dalam tiap kelas.
* **F1-score**: Harmonic mean antara precision dan recall.

### Hasil Evaluasi:

| Traffic Level | Precision | Recall | F1-score |
| ------------- | --------- | ------ | -------- |
| Lancar        | 0.92      | 0.93   | 0.92     |
| Ramai Lancar  | 0.89      | 0.88   | 0.88     |
| Padat         | 0.85      | 0.84   | 0.84     |
| Macet         | 0.91      | 0.90   | 0.90     |

* **Akurasi Total**: 90.2%

---

##  6. Pengembangan Lanjutan

###  Integrasi Data Real-Time:

* Sensor kendaraan dan CCTV
* API cuaca BMKG
* Data dari Google Maps/Waze (crowdsourcing)

###  Model AI Tingkat Lanjut:

* **LSTM** untuk prediksi time-series
* **Reinforcement Learning (RL)** untuk kontrol adaptif (misal: pengaturan lampu lalu lintas)
* **Hybrid AI + Rule-based**: gabungkan logika lokal dan pembelajaran mesin

###  Fitur Tambahan:

* Notifikasi berbasis lokasi GPS
* Aplikasi mobile ringan
* Pelaporan kemacetan dari pengguna (crowdsourcing)

###  Integrasi Smart City:

* Dashboard Command Center
* Deteksi anomali lalu lintas otomatis
* Statistik lalu lintas untuk kebijakan dan perencanaan kota

---

##  Tim Pengembang

* Lio Kusnata                 (G1A023013)
* Muhammad Ariqoh Firjatullah (G1A023033)
* Ajis Saputra Hidayah        (G1A023083)

---

> "Langkah kecil menuju kota cerdas yang bebas macet."
