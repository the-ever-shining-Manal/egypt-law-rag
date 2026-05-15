# المستشار القانوني - Egypt Law RAG ⚖️

نظام ذكاء اصطناعي تفاعلي (RAG) مبني للإجابة على الاستفسارات القانونية بناءً على نصوص القانون المصري (مثل قانون العقوبات المصري). يقوم النظام باستخراج النصوص القانونية، تنظيفها، أرشفتها في قاعدة بيانات متجهة (Vector Database)، ومن ثم استخدام نماذج الذكاء الاصطناعي لاسترجاع المواد ذات الصلة والإجابة على أسئلة المستخدم بدقة مع ذكر المصادر.

## ✨ المميزات (Features)

- **واجهة مستخدم عصرية (Frontend)**: واجهة رسومية بسيطة وجذابة تدعم الوضع المظلم وتتيح التفاعل المباشر مع المساعد القانوني.
- **محرك بحث دلالي (Semantic Search)**: يعتمد على Qdrant و OpenAI Embeddings للبحث الذكي في نصوص المواد القانونية بدلاً من البحث النصي التقليدي.
- **توليد الإجابات (Answer Generation)**: يستخدم نماذج OpenAI (مثل `gpt-4o-mini`) لتقديم إجابة دقيقة مستندة حصراً على النصوص التي تم استرجاعها.
- **إدارة النظام (Pipeline Management)**: واجهة API و UI مخصصة لرفع ملفات PDF قانونية جديدة واستخراج النصوص منها وإعادة بناء الفهرس (Index) تلقائياً.
- **الاستشهادات والمصادر (Citations)**: يتم إرفاق الإجابة دائماً بنص المادة القانونية واسم القانون التي اعتمد عليها النموذج.

## 🛠️ التقنيات المستخدمة (Tech Stack)

- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **Vector Database**: Qdrant (Local Storage)
- **AI / LLM**: OpenAI (Embeddings & Chat Completions)
- **Document Processing**: PyMuPDF (`fitz`), Regular Expressions for structuring Arabic texts.
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6).

## 📂 هيكلة المشروع (Project Structure)

```text
egypt-law-rag/
├── frontend/                # واجهة المستخدم (HTML, CSS, JS)
│   ├── index.html           # الصفحة الرئيسية للمستشار القانوني
│   ├── style.css            # التنسيقات (مظهر عصري داكن)
│   └── script.js            # منطق التواصل مع الـ API
├── src/                     # الكود المصدري للمحرك الخلفي (Backend)
│   ├── api/                 # مسارات FastAPI (Routes)
│   ├── services/            # الخدمات الأساسية (RAG Service)
│   ├── pipeline.py          # خطوات الـ Pipeline (Ingest, Clean, Chunk, Index)
│   ├── retriever.py         # منطق البحث الدلالي في Qdrant
│   ├── generator.py         # منطق توليد الإجابات باستخدام LLM
│   ├── vector_store.py      # إدارة والاتصال بـ Qdrant
│   ├── extractor.py         # استخراج النصوص من الـ PDF
│   └── config.py            # إعدادات المشروع والمتغيرات البيئية
├── data/                    # المجلد الخاص بالبيانات وملفات الـ PDF
├── output/                  # مخرجات النظام المؤقتة (مثل الـ Chunks)
├── qdrant_storage/          # قاعدة البيانات المتجهة المحلية
├── .env                     # مفاتيح الربط (API Keys)
└── requirements.txt         # المكتبات المعتمدة
```

## 🚀 التثبيت والتشغيل (Setup & Installation)

### 1. المتطلبات الأساسية
- تثبيت Python 3.10 أو أحدث.
- حساب في OpenAI للحصول على `OPENAI_API_KEY`.

### 2. تثبيت المكتبات (Dependencies)
قم بإنشاء بيئة افتراضية (Virtual Environment) وتثبيت المكتبات:
```bash
python -m venv .venv
source .venv/bin/activate  # في الويندوز: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. إعداد المتغيرات البيئية (Environment Variables)
قم بإنشاء ملف `.env` في المسار الرئيسي للمشروع وأضف المفتاح الخاص بك:
```env
OPENAI_API_KEY="sk-..."
EMBEDDING_MODEL="text-embedding-3-small"
CHAT_MODEL="gpt-4o-mini"
QDRANT_COLLECTION="legal_articles"
```

### 4. تشغيل الخادم (Running the Backend)
لتشغيل الـ API محلياً باستخدام `uvicorn`:
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```
الخادم سيعمل الآن على الرابط: `http://localhost:8000`

### 5. تشغيل واجهة المستخدم (Running the Frontend)
نظراً لأن الواجهة تعتمد على ملفات HTML و JS نقية، يمكنك فتح ملف `frontend/index.html` مباشرةً في المتصفح الخاص بك.
للحصول على أفضل تجربة، يمكنك تشغيله باستخدام أي خادم محلي مثل Live Server في VS Code.

## 🔌 مسارات الـ API (Endpoints)

- `GET /health` : فحص حالة الخادم، إعدادات OpenAI، ومعلومات Qdrant.
- `POST /query` : إرسال سؤال قانوني واستلام الإجابة بالإضافة للمصادر (Sources).
- `POST /documents/upload` : رفع ملف قانوني PDF لمعالجته في الخلفية.
- `POST /pipeline/ingest` : استخراج وتنظيف نصوص الـ PDF الحالية.
- `POST /pipeline/index` : تحويل النصوص إلى Vectors وحفظها في Qdrant.
- `POST /pipeline/full` : تشغيل الدورة الكاملة (استخراج، تنظيف، أرشفة).

## ⚠️ ملاحظات هامة (Important Notes)

- النظام الحالي معتمد على قوانين محددة تم أرشفتها مسبقاً (مثل قانون العقوبات).
- تم ضبط النموذج (LLM Prompt) للإجابة حصراً باستخدام النصوص التي يسترجعها من قاعدة البيانات لمنع "الهلوسة" (Hallucinations) واختراع معلومات قانونية خاطئة.
- إذا قام المستخدم باستخدام مصطلحات شائعة أو غير دقيقة، يقوم النظام بذكاء بمحاولة ربطها بالمصطلحات القانونية الصحيحة وإجابتها، وإذا لم يجد ما يخصها يعتذر عن الإجابة لعدم توفر سياق قانوني موثوق.
