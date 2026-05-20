import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# .env ဖိုင်ထဲက API Key ကို ဖတ်ရန်
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Groq Client ကို ချိတ်ဆက်ခြင်း
client = Groq(api_key=api_key)

# Web Page ရဲ့ Layout ကို သတ်မှတ်ခြင်း
st.set_page_config(page_title="GreyHat AI Code Fixer", layout="centered")

st.title("👨‍💻 GreyHat AI Code Fixer")
st.subheader("သင့်ရဲ့ Python ကုဒ်မှားတွေကို AI နဲ့ ပြင်ကြမယ်")
st.write("---")

# User ဆီကနေ ကုဒ်လက်ခံမည့်နေရာ
user_code = st.text_area("ဒီမှာ ကုဒ်ကို Paste လုပ်ပါ (Python):", height=250, placeholder="ဥပမာ- print('Hello World")

# Fix လုပ်မည့် Button
if st.button("ကုဒ်ကို ပြင်ပေးပါ"):
    if not api_key:
        st.error("Error: API Key မရှိသေးပါ။ ကျေးဇူးပြု၍ .env ဖိုင်မှာ အရင်ထည့်ပါ။")
    elif user_code.strip() == "":
        st.warning("ကျေးဇူးပြု၍ ကုဒ်တစ်ခုခု အရင်ထည့်ပေးပါဦး။")
    else:
        with st.spinner("AI က သင့်ကုဒ်ကို စစ်ဆေးပြီး ပြင်ပေးနေပါပြီ..."):
            try:
                # Groq AI (Llama 3) ဆီသို့ မေးခွန်းပို့ခြင်း
                completion = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a Python expert. Fix the user's code, explain the error in Burmese language, and provide the clean corrected code."
                        },
                        {
                            "role": "user", 
                            "content": f"Fix this Python code and explain in Burmese: \n\n{user_code}"
                        }
                    ],
                    temperature=0.5,
                    max_tokens=2048
                )
                
                # ရလာတဲ့ အဖြေကို ပြသခြင်း
                st.success("ပြင်ဆင်ပြီးပါပြီ!")
                st.write("### 💡 AI ရဲ့ အကြံပြုချက်နှင့် ရှင်းပြချက်:")
                st.info(completion.choices[0].message.content)
                
            except Exception as e:
                st.error(f"တစ်ခုခု မှားယွင်းနေပါတယ်: {e}")

st.write("---")
st.caption("Developed by GreyHat | Powered by Groq AI")
