// Language Data
const i18n = {
    en: {
        home: "Home",
        detect: "Detect Disease",
        about: "About",
        contact: "Contact",
        login: "Login",
        signup: "Sign Up",
        heroTitle: "Upload Plant Leaf Image",
        tagline: "Smart Vision for Healthy Crops",
        dropText: "Drag and drop leaf image here",
        browse: "Browse Files",
        analyze: "Analyze Leaf",
        resultTitle: "Analysis Result",
        diseaseLabel: "Detected Disease",
        treatmentLabel: "Suggested Treatment",
        another: "Analyze Another Image",
        historyTitle: "Scan History"
    },
    hi: {
        home: "होम",
        detect: "रोग का पता लगाएं",
        about: "हमारे बारे में",
        contact: "संपर्क",
        login: "लॉगिन",
        signup: "साइन अप",
        heroTitle: "पौधे की पत्ती की छवि अपलोड करें",
        tagline: "स्वस्थ फसलों के लिए स्मार्ट विजन",
        dropText: "पत्ती की छवि यहाँ खींचें और छोड़ें",
        browse: "फ़ाइलें ब्राउज़ करें",
        analyze: "पत्ती का विश्लेषण करें",
        resultTitle: "विश्लेषण परिणाम",
        diseaseLabel: "पता चला रोग",
        treatmentLabel: "सुझाया गया उपचार",
        another: "एक और छवि का विश्लेषण करें",
        historyTitle: "स्कैन इतिहास"
    },
    es: {
        home: "Inicio",
        detect: "Detectar enfermedad",
        about: "Acerca de",
        contact: "Contacto",
        login: "Acceso",
        signup: "Inscribirse",
        heroTitle: "Subir imagen de hoja de planta",
        tagline: "Visión inteligente para cultivos sanos",
        dropText: "Arrastre y suelte la imagen de la hoja aquí",
        browse: "Examinar archivos",
        analyze: "Analizar hoja",
        resultTitle: "Resultado del análisis",
        diseaseLabel: "Enfermedad detectada",
        treatmentLabel: "Tratamiento sugerido",
        another: "Analizar otra imagen",
        historyTitle: "Historial de escaneo"
    }
};

// State
let currentLanguage = 'en';
let history = JSON.parse(localStorage.getItem('drishti_history')) || [];

// DOM Elements
const langBtn = document.getElementById('langBtn');
const langDropdown = document.getElementById('langDropdown');
const currentLangText = document.getElementById('currentLang');
const fileInput = document.getElementById('fileInput');
const dropZone = document.getElementById('dropZone');
const previewArea = document.getElementById('previewArea');
const imagePreview = document.getElementById('imagePreview');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultCard = document.getElementById('resultCard');
const diseaseName = document.getElementById('diseaseName');
const treatmentText = document.getElementById('treatmentText');
const confidenceValue = document.getElementById('confidenceValue');
const historySidebar = document.getElementById('historySidebar');
const historyList = document.getElementById('historyList');
const toggleHistoryBtn = document.getElementById('toggleHistory');
const closeHistoryBtn = document.getElementById('closeHistory');
const authModal = document.getElementById('authModal');
const loginForm = document.getElementById('loginForm');
const signupForm = document.getElementById('signupForm');

// --- Language Logic ---
function changeLanguage(lang) {
    currentLanguage = lang;
    const langNames = { en: 'English', hi: 'Hindi', es: 'Spanish' };
    currentLangText.innerText = langNames[lang];
    langDropdown.classList.remove('show');
    
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (i18n[lang][key]) {
            el.innerText = i18n[lang][key];
        }
    });
}

langBtn.addEventListener('click', () => langDropdown.classList.toggle('show'));

// --- Upload Logic ---
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) handleFile(file);
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('active');
});

dropZone.addEventListener('dragleave', () => dropZone.classList.remove('active'));

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('active');
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
});

function handleFile(file) {
    if (!file.type.startsWith('image/')) return;
    
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        dropZone.classList.add('hidden');
        previewArea.classList.remove('hidden');
    };
    reader.readAsDataURL(file);
}

analyzeBtn.addEventListener('click', () => {
    previewArea.classList.add('scanning');
    analyzeBtn.disabled = true;
    analyzeBtn.innerText = "Analyzing...";

    // Mock AI Analysis
    setTimeout(() => {
        const mockResults = [
            { disease: "Tomato Early Blight", confidence: 92, treatment: "Use Mancozeb fungicide and remove infected leaves." },
            { disease: "Healthy Leaf", confidence: 98, treatment: "No treatment needed. Maintain regular watering." },
            { disease: "Potato Late Blight", confidence: 85, treatment: "Apply copper-based fungicides and improve air circulation." },
            { disease: "Apple Scab", confidence: 89, treatment: "Use sulfur-based sprays and prune affected branches." }
        ];
        
        const result = mockResults[Math.floor(Math.random() * mockResults.length)];
        
        showResult(result);
        saveToHistory(result, imagePreview.src);
    }, 2000);
});

function showResult(result) {
    previewArea.classList.add('hidden');
    previewArea.classList.remove('scanning');
    resultCard.classList.remove('hidden');
    
    diseaseName.innerText = result.disease;
    treatmentText.innerText = result.treatment;
    confidenceValue.innerText = result.confidence + "%";
}

function resetUpload() {
    resultCard.classList.add('hidden');
    dropZone.classList.remove('hidden');
    fileInput.value = "";
    analyzeBtn.disabled = false;
    analyzeBtn.innerText = i18n[currentLanguage].analyze;
}

// --- History Logic ---
function saveToHistory(result, img) {
    const historyItem = {
        id: Date.now(),
        disease: result.disease,
        confidence: result.confidence,
        treatment: result.treatment,
        image: img,
        date: new Date().toLocaleString()
    };
    
    history.unshift(historyItem);
    localStorage.setItem('drishti_history', JSON.stringify(history));
    renderHistory();
}

function renderHistory() {
    historyList.innerHTML = "";
    history.forEach(item => {
        const div = document.createElement('div');
        div.className = "history-item";
        div.onclick = () => {
            showResult(item);
            historySidebar.classList.remove('open');
        };
        div.innerHTML = `
            <img src="${item.image}" class="history-img">
            <div class="history-info">
                <span class="history-disease">${item.disease}</span>
                <span class="history-meta">${item.date} • ${item.confidence}%</span>
            </div>
        `;
        historyList.appendChild(div);
    });
}

toggleHistoryBtn.addEventListener('click', () => historySidebar.classList.toggle('open'));
closeHistoryBtn.addEventListener('click', () => historySidebar.classList.remove('open'));

// --- Auth Modal Logic ---
function openModal(type) {
    authModal.classList.remove('hidden');
    toggleAuth(type);
}

function closeModal() {
    authModal.classList.add('hidden');
}

function toggleAuth(type) {
    if (type === 'login') {
        loginForm.classList.remove('hidden');
        signupForm.classList.add('hidden');
    } else {
        loginForm.classList.add('hidden');
        signupForm.classList.remove('hidden');
    }
}

function handleAuth() {
    alert("Authentication feature coming soon!");
    closeModal();
}

// Close dropdown/modal on outside click
window.onclick = (e) => {
    if (!e.target.matches('.lang-btn') && !e.target.closest('.lang-btn')) {
        langDropdown.classList.remove('show');
    }
    if (e.target === authModal) {
        closeModal();
    }
};

// Initial Render
renderHistory();
