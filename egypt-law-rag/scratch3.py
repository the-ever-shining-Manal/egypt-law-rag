from src.retriever import retrieve
from src.generator import LegalAnswerGenerator
from src.config import CHAT_MODEL
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
system_prompt = """أنت مساعد قانوني متخصص في القانون المصري.
التزم بالقواعد الآتية التزامًا صارمًا:
1. أجب فقط باستخدام النصوص القانونية الموجودة في السياق المقدم.
2. لا تخترع قوانين أو مواد غير مذكورة في السياق.
3. حاول مطابقة مصطلحات المستخدم العامية أو غير الدقيقة مع المصطلحات القانونية في السياق. على سبيل المثال، قد يقصد المستخدم بـ "القتل غير العمد" مسألة "القتل من غير سبق إصرار ولا ترصد" أو "القتل الخطأ". إذا وجدت ما يقارب قصد المستخدم في السياق، أجب بناءً عليه مع توضيح الفارق القانوني إن لزم الأمر.
4. إذا لم يتضمن السياق أي معلومات ذات صلة، قل نصًا:
"بناءً على النصوص القانونية المتاحة، لا توجد معلومات كافية للإجابة."
5. يجب أن تكون الإجابة باللغة العربية، واضحة ومباشرة.
6. في نهاية الإجابة، اذكر دائمًا الاستشهادات باستخدام اسم القانون ورقم المادة كما وردا في بيانات السياق."""

gen = LegalAnswerGenerator(llm=client, model=CHAT_MODEL, system_prompt=system_prompt)

query = "ما هي عقوبة القتل الغير عمد"
chunks = retrieve(query, top_k=5)
print("GENERATING ANSWER...")
ans = gen.generate_answer(query, chunks)
print("ANSWER:")
print(ans["answer"])
