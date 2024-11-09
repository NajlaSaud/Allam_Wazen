from openai import OpenAI
import os
import re
from dotenv import load_dotenv

# load OpenAI API key stored in the .env file
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


class GPTDiacritizer:
    def __init__(self, model_name="gpt-3.5-turbo"):
        # Initialize with the model (this can be GPT or any other language model)
        self.model = model_name

    """
    helper function to get completion GPT-3.5 Turbo, 
    sending the prompt as input and receiving the response as output.
    """

    def get_completion(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,  # this is the degree of randomness of the model's output
        )
        return response.choices[0].message.content

    def diacritize_sentence(self, sentence):
        prompt = f"""
        اعمل كخبير في اللغة العربية: قم بتشكيل الجملة المعطاة.
        التشكيل يعني: إضافة الحركات إلى حروف الجملة
        الناتج سيكون عبارة عن الجملة بعد التشكيل فقط.
        
        مثال: إن الرسول لنور يستضاء به
        الجملة بعد التشكيل: إِنَّ الرَّسُولَ لَنُورٌ يُسْتَضَاءُ بِهِ
        
        الجملة: '''{sentence}'''
        """
        diacritized_sentence = self.get_completion(prompt)

        # Remove the standalone diacritics if exist
        standalone_harakat_pattern = re.compile(r'(?<![\u0621-\u064A])[\u0617-\u061A\u064B-\u0652]')
        diacritized_sentence = re.sub(standalone_harakat_pattern, '', diacritized_sentence)

        # Remove "الجملة بعد التشكيل:"
        diacritized_sentence = diacritized_sentence.replace("الجملة بعد التشكيل:", "")
        return diacritized_sentence


def main():
    # create object from the class
    diacritizer = GPTDiacritizer()

    # read sentence from user
    # sentence = input("أدخل الجملة بدون تشكيل: ")
    shatr = "مالي سوى دعوات قلب خاشع"
    diacritized_shatr = diacritizer.diacritize_sentence(shatr.strip())
    # diacritize the sentence
    # diacritized_sentence = diacritizer.diacritize_sentence(sentence)

    # print sentence
    print(diacritized_shatr)


if __name__ == "__main__":
    main()
