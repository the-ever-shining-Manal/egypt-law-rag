const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const chatContainer = document.getElementById('chat-container');
const queryForm = document.getElementById('query-form');
const questionInput = document.getElementById('question-input');
const sendBtn = document.getElementById('send-btn');
const btnClearChat = document.getElementById('btn-clear-chat');
const suggestionBtns = document.querySelectorAll('.suggestion-btn');

const uploadForm = document.getElementById('upload-form');
const pdfFileInput = document.getElementById('pdf-file');
const fileNameDisplay = document.getElementById('file-name');
const uploadBtn = document.getElementById('upload-btn');
const uploadSpinner = document.getElementById('upload-spinner');

const btnIngest = document.getElementById('btn-ingest');
const btnIndex = document.getElementById('btn-index');
const btnFullPipeline = document.getElementById('btn-full-pipeline');

// Helper to show toasts
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = 'fa-info-circle';
    if (type === 'success') icon = 'fa-check-circle';
    if (type === 'error') icon = 'fa-exclamation-circle';
    
    toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
    
    container.appendChild(toast);
    
    // Remove after 4 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-in forwards';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Check health on load
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            const data = await response.json();
            console.log('Health Check:', data);
        } else {
            showToast('الخادم لا يستجيب', 'error');
            document.querySelector('.status-indicator').classList.remove('online');
            document.querySelector('.status-indicator').textContent = 'غير متصل';
        }
    } catch (err) {
        showToast('تعذر الاتصال بالخادم. يرجى التأكد من تشغيله.', 'error');
        document.querySelector('.status-indicator').classList.remove('online');
        document.querySelector('.status-indicator').textContent = 'غير متصل';
    }
}

// Chat UI helpers
function appendUserMessage(text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message user-message';
    msgDiv.innerHTML = `
        <div class="avatar"><i class="fa-solid fa-user"></i></div>
        <div class="message-content"><p>${text}</p></div>
    `;
    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showTypingIndicator() {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message bot-message typing-id';
    msgDiv.id = 'typing-indicator';
    msgDiv.innerHTML = `
        <div class="avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="message-content">
            <div class="typing-indicator">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>
    `;
    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) indicator.remove();
}

function formatSourcesList(sources) {
    if (!sources || sources.length === 0) return '';
    
    let html = '<div class="citations">';
    html += '<div class="citations-title"><i class="fa-solid fa-book-open"></i> المصادر:</div>';
    html += '<ul class="citation-list">';
    
    const uniqueSources = [];
    const seen = new Set();
    sources.forEach(src => {
        const key = `${src.law}-${src.article}`;
        if (!seen.has(key)) {
            seen.add(key);
            uniqueSources.push(src);
        }
    });

    uniqueSources.forEach(src => {
        html += `<li class="citation-item">`;
        html += `<strong>${src.law} - المادة ${src.article}</strong>`;
        html += `<p style="margin-top: 0.5rem; font-size: 0.85em; color: var(--text-secondary); line-height: 1.4;">${src.text_preview}...</p>`;
        html += `</li>`;
    });
    
    html += '</ul></div>';
    return html;
}

function appendBotMessage(text, sources = []) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message bot-message';
    
    // Parse markdown-like text to basic HTML (bolding)
    let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formattedText = formattedText.replace(/\n/g, '<br>');

    let contentHTML = `<p>${formattedText}</p>`;
    contentHTML += formatSourcesList(sources);

    msgDiv.innerHTML = `
        <div class="avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="message-content">${contentHTML}</div>
    `;
    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Chat interactions
queryForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const question = questionInput.value.trim();
    if (!question) return;

    // UI Updates
    questionInput.value = '';
    sendBtn.disabled = true;
    appendUserMessage(question);
    showTypingIndicator();

    // API Call
    try {
        const response = await fetch(`${API_BASE_URL}/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question, top_k: 5 })
        });

        const data = await response.json();
        removeTypingIndicator();

        if (response.ok) {
            appendBotMessage(data.answer, data.sources);
        } else {
            appendBotMessage("عذراً، حدث خطأ أثناء معالجة سؤالك: " + (data.detail || "خطأ غير معروف"));
        }
    } catch (err) {
        removeTypingIndicator();
        appendBotMessage("عذراً، تعذر الاتصال بالخادم. تأكد من أن الـ API يعمل.");
        console.error(err);
    } finally {
        sendBtn.disabled = false;
        questionInput.focus();
    }
});

suggestionBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        questionInput.value = btn.textContent;
        queryForm.dispatchEvent(new Event('submit'));
    });
});

btnClearChat.addEventListener('click', () => {
    // Keep only the first welcome message
    const firstMsg = chatContainer.firstElementChild;
    chatContainer.innerHTML = '';
    chatContainer.appendChild(firstMsg);
});

// File Upload
pdfFileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        fileNameDisplay.textContent = e.target.files[0].name;
    } else {
        fileNameDisplay.textContent = 'لم يتم اختيار ملف';
    }
});

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const file = pdfFileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('law_name', 'مستند مخصص'); // Default custom law name
    // The backend endpoint defaults to background=True

    uploadBtn.disabled = true;
    uploadSpinner.classList.remove('hidden');

    try {
        const response = await fetch(`${API_BASE_URL}/documents/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (response.ok) {
            showToast('تم بدء معالجة الملف في الخلفية', 'success');
            pdfFileInput.value = '';
            fileNameDisplay.textContent = 'لم يتم اختيار ملف';
        } else {
            showToast(data.detail || 'حدث خطأ أثناء الرفع', 'error');
        }
    } catch (err) {
        showToast('فشل الاتصال بالخادم', 'error');
        console.error(err);
    } finally {
        uploadBtn.disabled = false;
        uploadSpinner.classList.add('hidden');
    }
});

// Pipeline Management
async function triggerPipeline(endpoint, buttonId) {
    const btn = document.getElementById(buttonId);
    const originalContent = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> جاري المعالجة...';
    btn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/pipeline/${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        if (response.ok) {
            showToast(`تم بدء: ${data.message || 'العملية بنجاح'}`, 'success');
        } else {
            showToast(data.detail || 'حدث خطأ', 'error');
        }
    } catch (err) {
        showToast('فشل الاتصال بالخادم', 'error');
        console.error(err);
    } finally {
        btn.innerHTML = originalContent;
        btn.disabled = false;
    }
}

btnIngest.addEventListener('click', () => triggerPipeline('ingest', 'btn-ingest'));
btnIndex.addEventListener('click', () => triggerPipeline('index', 'btn-index'));
btnFullPipeline.addEventListener('click', () => triggerPipeline('full', 'btn-full-pipeline'));

// Initialize
window.addEventListener('DOMContentLoaded', () => {
    checkHealth();
    questionInput.focus();
});
