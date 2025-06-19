#იმპორტები 
import urllib.parse
import urllib.request
import json
import os
#თარჯიმნის დროისთვის დავამატე datetime მოდული
from datetime import datetime


#ფაილების სახელები
INPUT_FILE = "input.txt"
LANGUAGES_FILE = "lang.txt"
OUTPUT_FILE = "output.txt"
#პლეისჰოლდერი ტექსტი (მონიშნული ტექსტი, რომელიც ჩაწერილია ფაილში)
PLACEHOLDER = "↓↓↓Type your text below to translate...↓↓↓"
#ტერმინალში ენების სია
langs = ["Georgian", "English", "Spanish", "Portuguese", "Russian", "Korean", "Hindi"]


#ფუნქციები

#ეს ფუნქცია ფააილს ქმნის თუ ის არ არსებობს.
def create_file_if_missing(filename, default_content=""):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(default_content)

#ეს ფუნქცია ხსნის ამ ფაილს(input/output ფაილებისთვის)
def open_file(filename):
    os.system(f'start notepad {filename}')

#შემდგობ გამოვიყენებთ ამ ფუნქციას რომ input და lang 
#ტექსტ ფაილები წავშალოთ რადგან აღარ იქნება საჭირო
def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"🗑️ {filename} has been deleted.")
    else:
        print(f"❌ {filename} does not exist.")

#ამ ფუნქციით ვკითხულობთ ტექსტს input ფაილიდან
def read_input(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        
        # პირველ ხაზს აიგნორებს თუ ის placeholder-ის კოპიაა
        #რადგან error არ მოხდეს გადათარგმნისას
        if lines and lines[0] == PLACEHOLDER:
            lines = lines[1:]
            
        return "\n".join(lines) if lines else ""

# lang.txt ფაილიდან ენების ჩამონათვალის წასაკითხად
# რაც ენის ასარჩევად საჭიროა
def load_languages():
    with open(LANGUAGES_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

#ეს ფუნქცია ტერმინალიდან გვაძლევს საშუალებას ავირჩიოთ ენა რომელზეც გადავთარგმნით ტექსტს
def choose_language(languages):
    print("🌐 Choose a language:")
    for i, code in enumerate(languages, start=1):
        print(f"{i}. {langs[i-1]} ({code})")
    try:
        choice = int(input("Enter number: "))
        if 1 <= choice <= len(languages):
            return languages[choice - 1]
    except ValueError:
        pass
    print("❌ Invalid selection. Exiting.")
    exit()

#ფუნქცია რომელიც ტექსტს თარგმნის
def translate(text, target_lang):
    #პარამეტრები URL-ით გადაცემისთვის
    params = urllib.parse.urlencode({
        'client': 'gtx',
        'sl': 'auto',
        'tl': target_lang,
        'dt': 't',
        'q': text
    })

    #Google Translate API-ის ურლ
    url = f"https://translate.googleapis.com/translate_a/single?{params}"

    #URL-ის გახსნა და პასუხის წაკითხვა
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            result = json.loads(response.read())
            # შედეგის დამუშავება
            return "".join([segment[0] for segment in result[0]])
    except Exception as e:
        return f"❌ Error: {e}"

#ეს ფუნქცია პასუხს წერს output ფაილში
def write_all_translations(translations):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for i, (original, translated, lang_code, timestamp) in enumerate(translations):
            if i > 0:
                f.write("\n\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Original: {original}\n")
            f.write(f"Translated ({lang_code}): {translated}")

#ეს ფუნქცია მომხმარებელს ეკითხება თუ უნდა გააგრძელოს პროგრამის გამოყენება
def CONT(translations):
    while True:
        a = input("Continue? (y/n): ").strip().lower()
        if a == 'y':
            # მხოლოდ ვტოვებთ placeholder-ს
            with open(INPUT_FILE, "w", encoding="utf-8") as f:
                f.write(PLACEHOLDER + "\n")
            return True, translations
        elif a == 'n':
            delete_file(INPUT_FILE)
            delete_file(LANGUAGES_FILE)
            print("👋 Exiting...")
            exit()
        else:
            print("❌ Invalid input. Please enter 'y' or 'n'.")

#მთავარი ფუნქცია, სადაც ყველაფერს ვაერთიანებთ ერთი პროგრამის შესაქმნელად
def main():
    #პირველ რიგში ვქმნით საჭირო ფაილებს თუ ისინი არ არსებობენ
    create_file_if_missing(INPUT_FILE, PLACEHOLDER + "\n")
    create_file_if_missing(LANGUAGES_FILE, "ka\nen\nes\npt\nru\nko\nhi")

    # ლისტში ვინახაავთ თარჯიმანს(თუ მომხმარებელი გააგრძელებს პროგრამას რომ ძველი თარჯიმანი შეინახოს)
    translations = []
    
    #while ციკლი რომ პროგრამამ იმუშაოს სანამ ჩვენ გვესაჭიროება
    while True:
        #პირველ რიგში ხსნის input.txt ფაილს
        open_file(INPUT_FILE)
        #ტერმინალში ვეუბნებით user-ს რომ ჩაწეროს ტექსტი და შემდგომ დაააჭიროს Enter-ს
        input("✏️ After editing and saving the input file, press Enter to continue...")

        #დადასტურების შემდეგ ვკითხულობთ დექსტს input ფაილიდან
        text = read_input(INPUT_FILE)
        #თუ ტექსტი ცარიელია ან მხოლოდ placeholer არის დაწერილი, user-ს ვეუბნებით რომ ჩაწეროს ტექსტი
        if not text:
            print("⚠️ No text to translate. Please enter some text.")
            continue
        
        #ვკითხულობთ ენების ჩამონათვალს lang.txt ფაილიდან
        languages = load_languages()
        #ვირჩევთ ენას ტერმინალიდან
        selected_lang = choose_language(languages)
        #ვთარგმნით ტექსტს აირჩეულ ენაზე
        translated = translate(text, selected_lang)
        
        # დააავამატოთ თრჯიმანი ლისტში
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        translations.append((text, translated, selected_lang, timestamp))
        
        # ყველა თარჯიმანი ერთად დააწეროს
        write_all_translations(translations)
        
        #ტერმინალში user-ს ვეუბნებით რომ თარგმნა წარმატებით დასრულდა
        print(f"✅ Translation added to {OUTPUT_FILE}")
        #output ფაილს ვხსნით რომ user-ს შეეძლოს ნახოს შედეგი
        open_file(OUTPUT_FILE)

        #ვკითხულობთ user-ის პასუხს, უნდა გააგრძელოს თუ არა პროგრამის გამოყენება
        should_continue, translations = CONT(translations)
        if not should_continue:
            break

#საბოლოოდ ამ პროგრამას ვიძახებთ
if __name__ == "__main__":
    main()

#ემოჯები დავამატე რომ პროგრამა უფრო კარგად გამოიყურებოდეს