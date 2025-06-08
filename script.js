// Import Leaflet library
const L = window.L

// Konfigurasi peta Bengkulu yang lebih akurat
const BENGKULU_CENTER = [-3.7956, 102.2611] // Pusat kota Bengkulu yang lebih akurat
const BENGKULU_ZOOM = 14 // Zoom level yang lebih dekat untuk detail lebih baik

// Data jalan utama Kota Bengkulu dengan koordinat yang lebih akurat
const BENGKULU_ROADS = {
  sudirman: {
    name: "Jl. Sudirman",
    coordinates: [
      [-3.7901, 102.2601],
      [-3.7925, 102.2612],
      [-3.795, 102.2623],
      [-3.7975, 102.2634],
    ],
    color: "#4CAF50",
    type: "arterial",
    length: 2.3,
    lanes: 4,
  },
  "ahmad-yani": {
    name: "Jl. Ahmad Yani",
    coordinates: [
      [-3.7925, 102.2612],
      [-3.7935, 102.265],
      [-3.7945, 102.269],
      [-3.7955, 102.273],
    ],
    color: "#FF9800",
    type: "arterial",
    length: 1.8,
    lanes: 4,
  },
  suprapto: {
    name: "Jl. Suprapto",
    coordinates: [
      [-3.7925, 102.2612],
      [-3.7945, 102.2592],
      [-3.7965, 102.2572],
      [-3.7985, 102.2552],
    ],
    color: "#F44336",
    type: "collector",
    length: 1.5,
    lanes: 2,
  },
  parman: {
    name: "Jl. S. Parman",
    coordinates: [
      [-3.8025, 102.2552],
      [-3.8045, 102.2572],
      [-3.8065, 102.2592],
      [-3.8085, 102.2612],
    ],
    color: "#2196F3",
    type: "arterial",
    length: 1.7,
    lanes: 4,
  },
  "raya-unib": {
    name: "Jl. WR. Supratman",
    coordinates: [
      [-3.7745, 102.2665],
      [-3.7765, 102.2685],
      [-3.7785, 102.2705],
      [-3.7805, 102.2725],
    ],
    color: "#9C27B0",
    type: "arterial",
    length: 2.5,
    lanes: 4,
  },
  "salak-raya": {
    name: "Jl. Salak",
    coordinates: [
      [-3.7655, 102.2644],
      [-3.7685, 102.2664],
      [-3.7715, 102.2684],
      [-3.7745, 102.2704],
    ],
    color: "#FF5722",
    type: "collector",
    length: 1.2,
    lanes: 2,
  },
  "zainul-arifin": {
    name: "Jl. Zainul Arifin",
    coordinates: [
      [-3.7833, 102.2577],
      [-3.7853, 102.2597],
      [-3.7873, 102.2617],
      [-3.7893, 102.2637],
    ],
    color: "#795548",
    type: "local",
    length: 1.0,
    lanes: 2,
  },
  veteran: {
    name: "Jl. Veteran",
    coordinates: [
      [-3.7944, 102.2622],
      [-3.7964, 102.2642],
      [-3.7984, 102.2662],
      [-3.8004, 102.2682],
    ],
    color: "#607D8B",
    type: "collector",
    length: 1.3,
    lanes: 2,
  },
  "pantai-panjang": {
    name: "Jl. Pantai Panjang",
    coordinates: [
      [-3.8133, 102.2355],
      [-3.8153, 102.2375],
      [-3.8173, 102.2395],
      [-3.8193, 102.2415],
    ],
    color: "#00BCD4",
    type: "arterial",
    length: 7.0,
    lanes: 2,
  },
  "hibrida-raya": {
    name: "Jl. Hibrida",
    coordinates: [
      [-3.7577, 102.2733],
      [-3.7597, 102.2753],
      [-3.7617, 102.2773],
      [-3.7637, 102.2793],
    ],
    color: "#4CAF50",
    type: "collector",
    length: 1.4,
    lanes: 2,
  },
  "basuki-rahmat": {
    name: "Jl. Basuki Rahmat",
    coordinates: [
      [-3.7899, 102.2544],
      [-3.7919, 102.2564],
      [-3.7939, 102.2584],
      [-3.7959, 102.2604],
    ],
    color: "#E91E63",
    type: "local",
    length: 0.9,
    lanes: 2,
  },
  khadijah: {
    name: "Jl. Khadijah",
    coordinates: [
      [-3.7766, 102.2655],
      [-3.7786, 102.2675],
      [-3.7806, 102.2695],
      [-3.7826, 102.2715],
    ],
    color: "#9E9E9E",
    type: "local",
    length: 0.8,
    lanes: 2,
  },
  "padang-harapan": {
    name: "Jl. Padang Harapan",
    coordinates: [
      [-3.7466, 102.2844],
      [-3.7486, 102.2864],
      [-3.7506, 102.2884],
      [-3.7526, 102.2904],
    ],
    color: "#FF9800",
    type: "arterial",
    length: 2.2,
    lanes: 2,
  },
  "lintas-sumatera": {
    name: "Jl. Lintas Sumatera",
    coordinates: [
      [-3.7244, 102.2466],
      [-3.7354, 102.2576],
      [-3.7464, 102.2686],
      [-3.7574, 102.2796],
      [-3.7684, 102.2906],
    ],
    color: "#3F51B5",
    type: "highway",
    length: 8.5,
    lanes: 4,
  },
  "raya-kandang": {
    name: "Jl. Raya Kandang",
    coordinates: [
      [-3.8244, 102.2355],
      [-3.8264, 102.2375],
      [-3.8284, 102.2395],
      [-3.8304, 102.2415],
    ],
    color: "#8BC34A",
    type: "arterial",
    length: 3.1,
    lanes: 2,
  },
  mahoni: {
    name: "Jl. Mahoni",
    coordinates: [
      [-3.7655, 102.2522],
      [-3.7675, 102.2542],
      [-3.7695, 102.2562],
      [-3.7715, 102.2582],
    ],
    color: "#CDDC39",
    type: "local",
    length: 0.7,
    lanes: 2,
  },
  "pagar-dewa": {
    name: "Jl. Pagar Dewa",
    coordinates: [
      [-3.7133, 102.2644],
      [-3.7153, 102.2664],
      [-3.7173, 102.2684],
      [-3.7193, 102.2704],
    ],
    color: "#FFC107",
    type: "arterial",
    length: 2.8,
    lanes: 2,
  },
  bypass: {
    name: "Jl. Bypass",
    coordinates: [
      [-3.7844, 102.2244],
      [-3.7864, 102.2354],
      [-3.7884, 102.2464],
      [-3.7904, 102.2574],
      [-3.7924, 102.2684],
    ],
    color: "#FF5722",
    type: "highway",
    length: 9.2,
    lanes: 4,
  },
  "sawah-lebar": {
    name: "Jl. Sawah Lebar",
    coordinates: [
      [-3.6944, 102.2799],
      [-3.6964, 102.2819],
      [-3.6984, 102.2839],
      [-3.7004, 102.2859],
    ],
    color: "#795548",
    type: "collector",
    length: 1.6,
    lanes: 2,
  },
  "teluk-segara": {
    name: "Jl. Teluk Segara",
    coordinates: [
      [-3.8355, 102.2133],
      [-3.8375, 102.2153],
      [-3.8395, 102.2173],
      [-3.8415, 102.2193],
    ],
    color: "#607D8B",
    type: "arterial",
    length: 2.4,
    lanes: 2,
  },
}

// Inisialisasi variabel global
let map
const roadLayers = {}
let heatmapLayer
const trafficData = {}
const selectedRoads = [] // Untuk menyimpan jalan yang dipilih pengguna
const routePolyline = null // Untuk menyimpan rute yang ditampilkan

// Fungsi untuk memilih jalan untuk rute
function toggleRoadSelection(roadId) {
  const index = selectedRoads.indexOf(roadId)
  if (index === -1) {
    selectedRoads.push(roadId)
  } else {
    selectedRoads.splice(index, 1)
  }
  updateSelectedRoadsUI()
}

// Fungsi untuk menampilkan UI jalan yang dipilih
function updateSelectedRoadsUI() {
  const selectedRoadsDiv = document.getElementById("selected-roads")
  if (selectedRoadsDiv) {
    selectedRoadsDiv.innerHTML = `
      <h4>🛤️ Jalan yang Dipilih</h4>
      <ul>
        ${selectedRoads.map((roadId) => `<li>${BENGKULU_ROADS[roadId].name}</li>`).join("")}
      </ul>
    `
  }
}

// Fungsi untuk menghitung rute kustom berdasarkan jalan yang dipilih
function calculateCustomRoute() {
  // Implementasi logika untuk menghitung rute kustom
  // Ini adalah fungsi placeholder
  alert("Fungsi menghitung rute kustom belum diimplementasi")
}

// Inisialisasi peta
function initMap() {
  map = L.map("map").setView(BENGKULU_CENTER, BENGKULU_ZOOM)

  // Tambahkan tile layer
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
  }).addTo(map)

  // Tambahkan marker untuk landmark Bengkulu
  addLandmarks()

  // Tambahkan jalan-jalan utama
  // addRoads()  // Comment out atau hapus baris ini

  // Mulai simulasi data real-time
  startRealTimeSimulation()
}

// Tambahkan landmark penting Bengkulu dengan koordinat yang lebih akurat
function addLandmarks() {
  const landmarks = [
    {
      name: "Benteng Marlborough",
      coords: [-3.7856, 102.2589],
      icon: "🏰",
      description: "Benteng bersejarah peninggalan Inggris",
    },
    {
      name: "Pantai Panjang",
      coords: [-3.8123, 102.2456],
      icon: "🏖️",
      description: "Pantai terkenal sepanjang 7 km",
    },
    {
      name: "Universitas Bengkulu",
      coords: [-3.7585, 102.2705],
      icon: "🎓",
      description: "Universitas negeri terbesar di Bengkulu",
    },
    {
      name: "Pasar Panorama",
      coords: [-3.7923, 102.2635],
      icon: "🏪",
      description: "Pasar tradisional terbesar",
    },
    {
      name: "Bandara Fatmawati",
      coords: [-3.8634, 102.3389],
      icon: "✈️",
      description: "Bandara utama Bengkulu",
    },
    {
      name: "Rumah Sakit M. Yunus",
      coords: [-3.7845, 102.2612],
      icon: "🏥",
      description: "Rumah sakit rujukan utama",
    },
    {
      name: "Masjid Jamik",
      coords: [-3.7889, 102.2634],
      icon: "🕌",
      description: "Masjid bersejarah pusat kota",
    },
    {
      name: "Mall Mega Buana",
      coords: [-3.7756, 102.2678],
      icon: "🏬",
      description: "Pusat perbelanjaan modern",
    },
    {
      name: "Stadion Semarak",
      coords: [-3.7612, 102.2723],
      icon: "⚽",
      description: "Stadion utama Bengkulu",
    },
    {
      name: "Pelabuhan Pulau Baai",
      coords: [-3.8456, 102.1234],
      icon: "⚓",
      description: "Pelabuhan utama Bengkulu",
    },
    {
      name: "Kantor Gubernur",
      coords: [-3.7867, 102.2589],
      icon: "🏛️",
      description: "Kantor Pemerintah Provinsi",
    },
    {
      name: "Universitas Dehasen",
      coords: [-3.7456, 102.2834],
      icon: "🎓",
      description: "Universitas swasta terkemuka",
    },
    {
      name: "Tugu Thomas Parr",
      coords: [-3.7823, 102.2567],
      icon: "🗿",
      description: "Monumen bersejarah",
    },
    {
      name: "Pasar Minggu",
      coords: [-3.7645, 102.2512],
      icon: "🛒",
      description: "Pasar tradisional",
    },
    {
      name: "Terminal Panorama",
      coords: [-3.7934, 102.2656],
      icon: "🚌",
      description: "Terminal bus utama",
    },
    {
      name: "Danau Dendam Tak Sudah",
      coords: [-3.7123, 102.2634],
      icon: "🏞️",
      description: "Objek wisata danau",
    },
    {
      name: "Pantai Berkas",
      coords: [-3.8345, 102.2123],
      icon: "🌊",
      description: "Pantai wisata populer",
    },
    {
      name: "Bukit Kaba",
      coords: [-3.5234, 102.6234],
      icon: "⛰️",
      description: "Gunung berapi aktif",
    },
  ]

  landmarks.forEach((landmark) => {
    const marker = L.marker(landmark.coords).addTo(map)
    marker.bindPopup(`
            <div class="popup-content">
                <h4>${landmark.icon} ${landmark.name}</h4>
                <p>${landmark.description}</p>
                <small>Koordinat: ${landmark.coords[0].toFixed(4)}, ${landmark.coords[1].toFixed(4)}</small>
            </div>
        `)
  })
}

// Tambahkan jalan-jalan utama ke peta
function addRoads() {
  Object.keys(BENGKULU_ROADS).forEach((roadId) => {
    const road = BENGKULU_ROADS[roadId]
    const polyline = L.polyline(road.coordinates, {
      color: road.color,
      weight: road.type === "highway" ? 8 : road.type === "arterial" ? 6 : 4,
      opacity: 0.8,
    }).addTo(map)

    roadLayers[roadId] = polyline

    // Tambahkan popup untuk setiap jalan
    polyline.bindPopup(`
            <div class="popup-content">
                <h4>🛣️ ${road.name}</h4>
                <p>Tipe: ${getRoadTypeLabel(road.type)}</p>
                <p>Panjang: ${road.length} km</p>
                <p>Jalur: ${road.lanes} lajur</p>
                <p>Status: <span id="status-${roadId}">Loading...</span></p>
                <p>Kecepatan: <span id="speed-${roadId}">-</span> km/h</p>
                <p>Volume: <span id="volume-${roadId}">-</span> kendaraan/jam</p>
                <button onclick="toggleRoadSelection('${roadId}')">Pilih untuk Rute</button>
            </div>
        `)

    // Tambahkan event listener untuk klik pada jalan
    polyline.on("click", function () {
      this.openPopup()
    })
  })
}

// Mendapatkan label tipe jalan
function getRoadTypeLabel(type) {
  switch (type) {
    case "highway":
      return "🛣️ Jalan Tol/Bypass"
    case "arterial":
      return "🚗 Jalan Arteri"
    case "collector":
      return "🚙 Jalan Kolektor"
    case "local":
      return "🏘️ Jalan Lokal"
    default:
      return type
  }
}

// Fungsi untuk mencari rute berdasarkan input lokasi
function findRoute() {
  const startPoint = document.getElementById("start-point").value.trim()
  const endPoint = document.getElementById("end-point").value.trim()

  if (!startPoint || !endPoint) {
    alert("Mohon isi titik awal dan tujuan")
    return
  }

  // Simulasi pencarian rute (dalam implementasi nyata akan menggunakan geocoding)
  const routes = generateRouteRecommendations(startPoint, endPoint)
  displayRouteResults(routes)
}

// Fungsi untuk generate rekomendasi rute
function generateRouteRecommendations(start, end) {
  // Simulasi beberapa rute alternatif
  const routes = [
    {
      name: "Rute Tercepat",
      description: `${start} → Jl. Sudirman → Jl. Ahmad Yani → ${end}`,
      distance: "5.2 km",
      duration: "15 menit",
      traffic: "Lancar",
      color: "#4CAF50",
    },
    {
      name: "Rute Alternatif",
      description: `${start} → Jl. Bypass → Jl. Lintas Sumatera → ${end}`,
      distance: "7.8 km",
      duration: "12 menit",
      traffic: "Lancar",
      color: "#4CAF50",
    },
    {
      name: "Rute Dalam Kota",
      description: `${start} → Jl. Veteran → Jl. Suprapto → ${end}`,
      distance: "4.1 km",
      duration: "18 menit",
      traffic: "Sedang",
      color: "#FF9800",
    },
  ]

  return routes
}

// Fungsi untuk menampilkan hasil rute
function displayRouteResults(routes) {
  const routeResultDiv = document.getElementById("route-result")

  let html = "<h4>🛣️ Rekomendasi Rute</h4>"

  routes.forEach((route, index) => {
    html += `
      <div class="route-option" style="margin-bottom: 15px; padding: 12px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid ${route.color};">
        <h5 style="margin-bottom: 8px; color: #333;">${route.name}</h5>
        <p style="font-size: 0.9rem; margin-bottom: 5px;">${route.description}</p>
        <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #666;">
          <span>📏 ${route.distance}</span>
          <span>⏱️ ${route.duration}</span>
          <span style="color: ${route.color};">🚦 ${route.traffic}</span>
        </div>
      </div>
    `
  })

  routeResultDiv.innerHTML = html
}

// Simulasi data traffic real-time
function startRealTimeSimulation() {
  setInterval(() => {
    updateTrafficData()
    updateUI()
  }, 5000) // Update setiap 5 detik

  // Update pertama kali
  updateTrafficData()
  updateUI()
}

// Generate data traffic random untuk simulasi
function updateTrafficData() {
  Object.keys(BENGKULU_ROADS).forEach((roadId) => {
    const road = BENGKULU_ROADS[roadId]

    // Faktor kemacetan berdasarkan tipe jalan
    let congestionFactor = Math.random()

    // Jalan tol/highway cenderung lebih lancar
    if (road.type === "highway") {
      congestionFactor *= 0.6
    }
    // Jalan lokal cenderung lebih macet
    else if (road.type === "local") {
      congestionFactor *= 1.3
    }

    // Jam sibuk (7-9 pagi dan 17-19 sore)
    const hour = new Date().getHours()
    if ((hour >= 7 && hour <= 9) || (hour >= 17 && hour <= 19)) {
      congestionFactor += 0.2
    }

    // Pastikan nilai tetap dalam rentang 0-1
    congestionFactor = Math.min(1, Math.max(0, congestionFactor))

    // Base speed berdasarkan tipe jalan
    const baseSpeed = road.type === "highway" ? 80 : road.type === "arterial" ? 60 : road.type === "collector" ? 40 : 30

    // Volume berdasarkan tipe jalan
    const baseVolume =
      road.type === "highway" ? 800 : road.type === "arterial" ? 600 : road.type === "collector" ? 400 : 200

    let status, color, speed

    if (congestionFactor < 0.4) {
      status = "Lancar"
      color = "#4CAF50"
      speed = baseSpeed * (0.9 + Math.random() * 0.2) // 90-110% dari base speed
    } else if (congestionFactor < 0.7) {
      status = "Sedang"
      color = "#FF9800"
      speed = baseSpeed * (0.6 + Math.random() * 0.2) // 60-80% dari base speed
    } else {
      status = "Macet"
      color = "#F44336"
      speed = baseSpeed * (0.3 + Math.random() * 0.2) // 30-50% dari base speed
    }

    // Volume kendaraan berdasarkan congestion factor
    const volume = Math.floor(baseVolume * (0.8 + congestionFactor * 0.4))

    trafficData[roadId] = {
      status,
      speed: Math.round(speed),
      volume,
      color,
      congestionLevel: congestionFactor,
    }

    // Update warna jalan di peta
    if (roadLayers[roadId]) {
      roadLayers[roadId].setStyle({ color: color })
    }

    // Update popup content
    const statusElement = document.getElementById(`status-${roadId}`)
    const speedElement = document.getElementById(`speed-${roadId}`)
    const volumeElement = document.getElementById(`volume-${roadId}`)

    if (statusElement) {
      statusElement.textContent = status
      statusElement.className = `traffic-level ${status.toLowerCase()}`
    }
    if (speedElement) speedElement.textContent = speed
    if (volumeElement) volumeElement.textContent = volume
  })
}

// Update UI dashboard
function updateUI() {
  let smoothCount = 0,
    mediumCount = 0,
    heavyCount = 0
  let totalSpeed = 0,
    totalVolume = 0

  Object.values(trafficData).forEach((data) => {
    if (data.status === "Lancar") smoothCount++
    else if (data.status === "Sedang") mediumCount++
    else heavyCount++

    totalSpeed += data.speed
    totalVolume += data.volume
  })

  // Update status counts
  document.getElementById("smooth-count").textContent = smoothCount
  document.getElementById("medium-count").textContent = mediumCount
  document.getElementById("heavy-count").textContent = heavyCount

  // Update real-time data
  const avgSpeed = Object.keys(trafficData).length > 0 ? Math.round(totalSpeed / Object.keys(trafficData).length) : 0
  document.getElementById("avg-speed").textContent = avgSpeed
  document.getElementById("vehicle-count").textContent = totalVolume
  document.getElementById("last-update").textContent = new Date().toLocaleTimeString("id-ID")

  // Update selected roads UI jika ada
  updateSelectedRoadsUI()
}

// Toggle heatmap
function toggleHeatmap() {
  if (heatmapLayer) {
    map.removeLayer(heatmapLayer)
    heatmapLayer = null
  } else {
    // Generate heatmap data berdasarkan traffic data
    const heatData = []
    Object.keys(BENGKULU_ROADS).forEach((roadId) => {
      const road = BENGKULU_ROADS[roadId]
      const traffic = trafficData[roadId]

      if (traffic) {
        road.coordinates.forEach((coord) => {
          heatData.push([coord[0], coord[1], traffic.congestionLevel])
        })
      }
    })

    heatmapLayer = L.heatLayer(heatData, {
      radius: 25,
      blur: 15,
      maxZoom: 17,
    }).addTo(map)
  }
}

// Tambahkan fungsi untuk menampilkan statistik jalan
function updateRoadStatistics() {
  const roadStats = {
    total: Object.keys(BENGKULU_ROADS).length,
    highway: 0,
    arterial: 0,
    collector: 0,
    local: 0,
  }

  // Klasifikasi jalan berdasarkan tipe
  Object.keys(BENGKULU_ROADS).forEach((roadId) => {
    const roadType = BENGKULU_ROADS[roadId].type
    roadStats[roadType]++
  })

  // Update UI jika ada elemen statistik
  const statsElement = document.getElementById("road-statistics")
  if (statsElement) {
    statsElement.innerHTML = `
      <h4>📊 Statistik Jaringan Jalan</h4>
      <p>Total Jalan: <strong>${roadStats.total}</strong></p>
      <p>🛣️ Jalan Tol/Bypass: ${roadStats.highway}</p>
      <p>🚗 Jalan Arteri: ${roadStats.arterial}</p>
      <p>🚙 Jalan Kolektor: ${roadStats.collector}</p>
      <p>🏘️ Jalan Lokal: ${roadStats.local}</p>
    `
  }
}

// Event listeners
document.addEventListener("DOMContentLoaded", () => {
  initMap()
  updateRoadStatistics()

  // Map control buttons
  document.getElementById("refresh-btn").addEventListener("click", () => {
    updateTrafficData()
    updateUI()
  })

  document.getElementById("toggle-heatmap").addEventListener("click", toggleHeatmap)

  // Ganti event listener untuk route finding
  document.getElementById("find-route-btn").addEventListener("click", findRoute)

  // Hapus semua event listener yang terkait dengan road selection
})

// Fungsi untuk memanggil API Python (akan diimplementasi dengan backend)
async function callPredictionAPI(roadData) {
  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(roadData),
    })

    const result = await response.json()
    return result
  } catch (error) {
    console.error("Error calling prediction API:", error)
    return null
  }
}

// Export functions untuk testing
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    updateTrafficData,
    toggleRoadSelection,
    calculateCustomRoute,
  }
}
