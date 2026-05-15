
# المستشار القانوني - Egypt Law RAG ⚖️

نظام ذكاء اصطناعي تفاعلي (RAG) مبني للإجابة على الاستفسارات القانونية بناءً على نصوص القانون المصري (مثل قانون العقوبات المصري). يقوم النظام باستخراج النصوص القانونية، تنظيفها، أرشفتها في قاعدة بيانات متجهة (Vector Database)، ومن ثم استخدام نماذج الذكاء الاصطناعي لاسترجاع المواد ذات الصلة والإجابة على أسئلة المستخدم بدقة مع ذكر المصادر.

<img width="1440" height="681" alt="593313951-8d4e8f4f-f37b-47d7-a542-c4b3b0deaf27" src="https://github.com/user-attachments/assets/f043e7ff-bc31-4e09-873d-35a34e78e140" />

## ✨ Features

- **واجهة مستخدم عصرية (Frontend)**: واجهة رسومية بسيطة وجذابة تدعم الوضع المظلم وتتيح التفاعل المباشر مع المساعد القانوني.
- **محرك بحث دلالي (Semantic Search)**: يعتمد على Qdrant و OpenAI Embeddings للبحث الذكي في نصوص المواد القانونية بدلاً من البحث النصي التقليدي.
- **توليد الإجابات (Answer Generation)**: يستخدم نماذج OpenAI (مثل `gpt-4o-mini`) لتقديم إجابة دقيقة مستندة حصراً على النصوص التي تم استرجاعها.
- **إدارة النظام (Pipeline Management)**: واجهة API و UI مخصصة لرفع ملفات PDF قانونية جديدة واستخراج النصوص منها وإعادة بناء الفهرس (Index) تلقائياً.
- **الاستشهادات والمصادر (Citations)**: يتم إرفاق الإجابة دائماً بنص المادة القانونية واسم القانون التي اعتمد عليها النموذج.
- **Docker Support**: يمكن تشغيل النظام بالكامل (Backend + Frontend + Qdrant) بأمر واحد باستخدام Docker Compose.

## 🛠️ Tech Stack

- **Backend**: Python 3.12, FastAPI, Uvicorn
- **Vector Database**: Qdrant (Docker Container)
- **AI / LLM**: OpenAI (Embeddings & Chat Completions)
- **Document Processing**: PyMuPDF (`fitz`), Regular Expressions for structuring Arabic texts
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6), served via Nginx
- **Infrastructure**: Docker, Docker Compose

## 📂  Project Structure

```text
egypt-law-rag/
├── frontend/                # واجهة المستخدم (HTML, CSS, JS)
│   ├── Dockerfile           # Nginx container for the frontend
│   ├── index.html           # الصفحة الرئيسية للمستشار القانوني
│   ├── style.css            # التنسيقات (مظهر عصري داكن)
│   └── script.js            # منطق التواصل مع الـ API
├── src/                     # الكود المصدري للمحرك الخلفي (Backend)
│   ├── api/                 # مسارات FastAPI (Routes)
│   ├── data/                # معالجة النصوص (Extract, Clean, Chunk)
│   ├── services/            # الخدمات الأساسية (RAG Service)
│   ├── pipeline.py          # خطوات الـ Pipeline (Ingest, Clean, Chunk, Index)
│   ├── retriever.py         # منطق البحث الدلالي في Qdrant
│   ├── generator.py         # منطق توليد الإجابات باستخدام LLM
│   ├── vector_store.py      # إدارة والاتصال بـ Qdrant
│   └── config.py            # إعدادات المشروع والمتغيرات البيئية
├── data/                    # المجلد الخاص بالبيانات وملفات الـ PDF
├── output/                  # مخرجات النظام المؤقتة (مثل الـ Chunks)
├── Dockerfile               # Backend container definition
├── docker-compose.yml       # Orchestrates all 3 services
├── .env                     # مفاتيح الربط (API Keys) - لا يُرفع على GitHub
└── requirements.txt         # المكتبات المعتمدة
```

## 🚀 التشغيل باستخدام Docker (Recommended)

### 1. requirements
- تثبيت [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- حساب في OpenAI للحصول على `OPENAI_API_KEY`

### 2. enviroment
قم بإنشاء ملف `.env` في مجلد `egypt-law-rag/`:
```env
OPENAI_API_KEY="sk-..."
EMBEDDING_MODEL="text-embedding-3-small"
CHAT_MODEL="gpt-4o-mini"
QDRANT_COLLECTION="legal_articles"
```

### 3. إضافة ملف الـ PDF
ضع ملف القانون في مجلد `data/`:
