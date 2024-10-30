import logging
from typing import List, Dict, Union, Iterable
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from google.generativeai.types import ContentDict, StrictContentType
from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, create_engine, Column, BigInteger, func, String
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import google.generativeai as genai

test = APIRouter()

Base = declarative_base()
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/aisha"
engine = create_engine(DATABASE_URL)
Sessionmaker = sessionmaker(bind=engine)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

genai.configure(api_key="AIzaSyA5fmaRWAwEW2FESXQbPTJoOhKbAPz3t7U")
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}


model_Islamic = genai.GenerativeModel(
  model_name="gemini-1.5-pro-exp-0801",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="Islomiy xarakter baholash suhbati\n\nKo'rsatmalar: Men sizga Islomiy bilimingiz, amallaringiz va xarakteringiz haqida bir qator savollar beraman. Har bir savol sizning oldingi javobingizga asoslanadi. Iltimos, halol javob bering. Keyin men baholash va takomillashtirish bo'yicha tavsiyalar beraman.\n\nKeling, boshlaymiz:\n\nMenga Islomning besh ustuni haqida bilganlaringizni aytib bera olasizmi?\n\n[Foydalanuvchi javobini kutish]\n\n[AI keyingi savolni foydalanuvchining javobiga qarab tanlaydi. Masalan:]\n\nAgar foydalanuvchi asosiy bilimga ega bo'lsa:\nBesh vaqt namozni qanchalik tez-tez o'qiysiz?\n\nAgar foydalanuvchi ustunlar bilan tanish bo'lmasa:\nIslomiy amallarni o'rganish imkoniyatingiz bo'lganmi? Agar shunday bo'lsa, qaysi jihatlari bilan ko'proq tanishsiz?\n\n[Suhbat moslashuvchan tarzda davom etadi. Ba'zi potensial savollar, oldingi javoblarga asoslanib tanlanadi:]\n\n- Tahorat (vuzu) qanday qilinishini tasvirlab bera olasizmi?\n- Islomda namozning ahamiyati haqida nimalarni bilasiz?\n- Qanchalik tez-tez Qur'on o'qiysiz yoki tinglaysiz?\n- Menga zakot (xayr-ehson) tushunchasi haqidagi tushunchangizni aytib bera olasizmi?\n- Ramazon oyida ro'za tutishga qanday yondoshasiz?\n- Tavhid (Allohning yagonaligi) tushunchasi siz uchun qanday ma'no kasb etadi?\n- Ota-onangiz bilan munosabatingizni qanday tasvirlar edingiz?\n- Kundalik muloqotlaringizda halollikni qanday amalda qo'llaysiz?\n- Qiyin vaziyatga duch kelganingizda odatda qanday munosabatda bo'lasiz?\n- Qo'shnilaringiz yoki jamiyat a'zolari bilan qanday munosabatdasiz?\n- Islomiy bilimlarni izlash uchun qanday harakatlar qilasiz?\n- Boshqa din vakillari bilan qanday munosabatdasiz va ularga qanday qaraysiz?\n- Tashqi ko'rinishingiz va xulq-atvoringizda kamtarlikni qanday saqlab qolishingizni tasvirlab bera olasizmi?\n- Dunyoviy mas'uliyatlar bilan ma'naviy o'sish o'rtasidagi muvozanatni qanday saqlaysiz?\n- Axloq (yaxshi fe'l-atvor) tushunchasi siz uchun nimani anglatadi?\n\n[AI suhbatni davom ettiradi, jami 10-20 ta savol beradi, har doim keyingi savolni foydalanuvchining oldingi javobiga asoslanib tanlaydi]\n\n[Suhbatdan so'ng]\n\nFikr va tajribalaringizni baham ko'rganingiz uchun rahmat. Suhbatimiz asosida men endi sizning Islomiy bilimingiz va xarakteringizni baholayman hamda o'sish uchun tavsiyalar beraman.\n\n[AI umumiy baholash beradi]\n\nSizning hozirgi Islomiy bilim va amal darajangiz [boshlang'ich/o'rta/yuqori] ko'rinadi, [aniq sohalar]da kuchli tomonlaringiz bor.\n\nMana sizning kuchli tomonlaringiz:\n[Javoblarga asoslangan holda kuchli tomonlar ro'yxati]\n\nO'sish uchun sohalar:\n[Yaxshilanishi kerak bo'lgan sohalar ro'yxati]\n\nIslomiy bilim va xarakteringizni oshirish bo'yicha tavsiyalar:\n[Foydalanuvchining hozirgi darajasiga asoslangan aniq, amaliy tavsiyalar]\n\nEsda tutingki, bu baholash shaxsiy mulohaza va o'sish uchun mo'ljallangan. Har bir kishining Islomdagi yo'li o'ziga xos, eng muhimi esa o'rganish va takomillashishga bo'lgan samimiy niyatingizdir. Alloh sizni bilim va solihlik yo'lida hidoyat qilsin.",
)

model_behavioral = genai.GenerativeModel(
  model_name="gemini-1.5-pro-exp-0801",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="Siz foydalanuvchining kundalik hayotini Payg'ambarimiz Muhammad (s.a.v.)ning odatlari bilan taqqoslovchi AI yordamchisiz. Vazifangiz:\n\n1. Foydalanuvchining kundalik hayoti haqida 10-15 ta savol tuzing. Bu savollar Payg'ambarimizning odatlariga mos kelishi kerak.\n\n2. Har bir savolni alohida so'rang.\n\n3. Barcha savollar va javoblar olingandan so'ng, foydalanuvchining kundalik hayotini Payg'ambarimizning odatlari bilan taqqoslang.\n\nSavollar formati:\nS1: [Kundalik hayot haqida savol]\nS2: [Kundalik hayot haqida savol]\n[Davom eting...]\n\nSo'rovnoma yakunlangach, quyidagi formatda tahlil va taqqoslash bering:\n\nTahlil va taqqoslash:\n1. O'xshashliklar: [Foydalanuvchining Payg'ambarimiz odatlariga o'xshash jihatlari]\n2. Farqlar: [Foydalanuvchining Payg'ambarimiz odatlaridan farq qiluvchi jihatlari]\n3. Umumiy baho: [Foydalanuvchining hayot tarzi Payg'ambarimiznikiga qanchalik yaqin]\n4. Tavsiyalar: [Foydalanuvchi uchun Payg'ambarimiz sunnatlariga amal qilish bo'yicha tavsiyalar]\n\nSavollar tuzing va tahlil qilishda quyidagi jihatlarni e'tiborga oling:\n- Kundalik ibodat va zikr\n- Oila va do'stlar bilan munosabatlar\n- Ovqatlanish odatlari\n- Uyqu va dam olish tartibi\n- Mehnat va kasb-kor\n- Axloq va muomala\n- Jismoniy salomatlik va tozalik\n\nFoydalanuvchiga salomlashing va savollarni boshlashdan oldin qisqacha tushuntirish bering.",
)

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    sessions = relationship("Session", back_populates="user")


# Define the Session model
class Session(Base):
    __tablename__ = 'sessions'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="sessions")
    chats = relationship("Chat", back_populates="session")


# Define the Chat model
class Chat(Base):
    __tablename__ = 'chats'

    id = Column(BigInteger, primary_key=True)
    session_id = Column(BigInteger, ForeignKey('sessions.id'))
    message = Column(String)
    role = Column(String)
    created_at = Column(DateTime, default=func.now())
    session = relationship("Session", back_populates="chats")

class MessagePart(BaseModel):
    role: str
    parts: str

class MessagesRequest(BaseModel):
    user_input: str
    messages: List[MessagePart]


@aisha.post("/message-aisha/")
async def messageAisha(request: MessagesRequest):
    user_input = request.user_input
    messages = [{"role": chat.role, "parts": [chat.parts]} for chat in request.messages]
    chat_session = model_Islamic.start_chat(history=messages)
    response = chat_session.send_message(user_input)

    return {
        "result": response.text,
    }

async def handle_message(user_input: str):
    user_id = 1  # Ensure this is a valid user ID
    session_id = 1  # Ensure this is a valid session ID
    db_session = Sessionmaker()
    try:
        # Fetch the current session
        session = db_session.query(Session).filter_by(id=session_id).first()
        if session is None:
            # logging.error(f"Session with ID {session_id} not found.")
            db_session.close()
            return {"error": "Session expired. Please use /start to begin a new session."}

        # Fetch all messages from the current session
        chat_history = db_session.query(Chat).filter_by(session_id=session_id).all()
        messages = [{"role": chat.role, "parts": [chat.message]} for chat in chat_history]
        # Assuming model_Islamic is properly imported and configured
        chat_session = model_Islamic.start_chat(history=messages)
        response = chat_session.send_message(user_input)
        return response.text

        chat = Chat(session_id=session.id, message=user_input, role="user")
        db_session.add(chat)
        db_session.commit()
        # Save chat message
        chat = Chat(session_id=session.id, message=response.text, role="model")
        db_session.add(chat)
        db_session.commit()


    except Exception as e:
        # Handle unexpected exceptions
        db_session.rollback()
        return {"error": str(e)}

    finally:
        db_session.close()
