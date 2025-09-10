import csv
import uuid
import requests
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import config

API_KEY = config.API_KEY
DEPLOYMENT_URL = config.DEPLOYMENT_URL

def get_prediction(text):
    token_response = requests.post(
        'https://iam.cloud.ibm.com/identity/token',
        data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'}
    )
    mltoken = token_response.json()['access_token']
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    record_id = str(uuid.uuid4())
    payload = {
        "input_data": [
            {
                "fields": ["Conteudo"],
                "values": [[text]],
                "meta": {
                    "record_id": record_id
                }
            }
        ]
    }

    response = requests.post(DEPLOYMENT_URL, json=payload, headers=header)
    result = response.json()
    prediction = int(result['predictions'][0]['values'][0][0])
    probability = result['predictions'][0]['values'][0][1][prediction]
    return prediction, probability


messages = []

base_messages = [
    "Hi Alex, just confirming our lunch at 12 tomorrow.",
    "Dear Team, the server maintenance is scheduled for Saturday night.",
    "Hey Sam, I found that book you were looking for!",
    "Hello, this is a reminder that the yoga class starts at 6 p.m.",
    "Greetings, I hope your conference trip went well.",
    "Just wanted to say thanks for helping with the presentation!",
    "Don't forget the game night at my place on Friday.",
    "The deadline for the report has been extended to next Tuesday.",
    "Please review the attached draft and send feedback.",
    "We’re organizing a potluck lunch in the office kitchen tomorrow.",
    "Can you bring the projector to the meeting room at 3 p.m.?",
    "Let me know if you need a ride to the airport.",
    "Happy birthday! Hope you have a fantastic day.",
    "Thanks again for lending me your umbrella!",
    "Are you still interested in joining the photography club?",
    "I loved the recipe you shared—so delicious!",
    "The weather looks perfect for a hike this weekend.",
    "I'll water your plants while you're on vacation.",
    "Just finished reading that novel you recommended—loved it!",
    "Can we switch our meeting to Thursday afternoon?",
    "Your presentation was really impressive today.",
    "We’re planning a surprise party for Linda—don’t tell her!",
    "Have you tried the new coffee shop on 5th Street?",
    "Thanks for covering my shift last week.",
    "I’ll send you the notes from the lecture later tonight.",
    "Looking forward to our road trip next month!",
    "Your package has arrived at the front desk.",
    "I'm compiling the agenda for Monday's meeting.",
    "Feel free to drop by my office if you have questions.",
    "We’re updating the team calendar with new deadlines.",
    "Just a heads-up: the parking lot will be closed tomorrow.",
    "Thanks for your help with the community cleanup event.",
    "The library is open until 8 p.m. this week.",
    "Don’t forget to submit your reimbursement forms.",
    "I'll be working from home on Friday.",
    "The book club is meeting at 6 p.m. in Room 202.",
    "Lunch was great today—let’s do it again soon!",
    "We’re hosting a trivia night next Wednesday.",
    "Let me know if you need help setting up the projector.",
    "The campus shuttle schedule has been updated.",
    "Your artwork was featured in the newsletter!",
    "We’re collecting donations for the food bank this week.",
    "Thanks for organizing the workshop—it was really helpful.",
    "I'm bringing cookies to the office tomorrow.",
    "The Wi-Fi will be down briefly for maintenance at 9 p.m.",
    "Please RSVP for the holiday party by Friday.",
    "Your feedback on the draft was super helpful—thanks!",
    "We're testing the fire alarm system at noon.",
    "Do you want to join the weekend volunteer event?",
    "The garden club is planting new flowers this weekend.",
    "I’ll send out the meeting minutes later today.",
    "Hope your exam went well!",
    "Can you review this document when you have a chance?",
    "The film screening starts at 7 p.m. in the auditorium.",
    "We’re looking for new members for the debate team.",
    "Your travel itinerary looks great—have a good trip!",
    "I'll pick up the snacks for the meeting.",
    "Please remember to lock the door when you leave.",
    "Your ID card is ready for pickup at the reception.",
    "We’re repainting the hallway on the 3rd floor tomorrow.",
    "The chess club tournament is on Saturday at 10 a.m.",
    "Thanks for the lovely postcard from Paris!",
    "Can you upload your project to the shared folder?",
    "We’re organizing a group lunch on Friday.",
    "I'll send you the Zoom link for the meeting shortly.",
    "Let’s schedule a brainstorming session for next week.",
    "The hiking trail is open again after the storm.",
    "Please fill out the survey about the workshop.",
    "Your login has been updated successfully.",
    "Don’t forget to bring your badge to the event.",
    "The conference call is at 4 p.m. EST.",
    "We’re planning a farewell party for Emily next week.",
    "Your poster design looks fantastic!",
    "Please sign the attendance sheet before you leave.",
    "I’ll be out of the office on Monday.",
    "Let me know if you want to carpool to the seminar.",
    "We’re hosting a bake sale to raise funds.",
    "Thanks for sharing your notes from class.",
    "The printers are being serviced this afternoon.",
    "We’re meeting at the café on Main Street at 10.",
    "The guest lecture was really inspiring.",
    "I'll check with IT about the software update.",
    "Please bring your laptop to the workshop.",
    "Your suggestion was added to the proposal—great idea!",
    "I reserved the conference room from 2 to 4 p.m.",
    "We’re updating the office seating chart this week.",
    "Thanks again for helping with the decorations.",
    "I'll send the finalized slides tomorrow morning.",
    "The bus leaves at 8:15 a.m. sharp.",
    "Let’s grab lunch after the seminar.",
    "The new interns are starting next Monday.",
    "I’ll bring the handouts to the meeting.",
    "Your essay was really well-written!",
    "Let me know if you want to swap shifts.",
    "We’re closing early on Friday for the holiday.",
    "Thanks for the reminder about the meeting.",
    "Please update your contact info in the directory.",
    "The next book club pick is “The Midnight Library.”",
    "I’m happy to proofread your draft—send it over.",
    "Your group project presentation is scheduled for Tuesday.",
    "Let’s plan a study session before the exam.",
    "I found your pen—it was under the couch!",
    "The IT department fixed the network issue.",
    "I'll grab some extra chairs for the workshop.",
    "Please keep the door closed during the performance.",
    "Looking forward to seeing you at the picnic!"
]

results = []

for msg_text in base_messages:
    try:
        prediction, probability = get_prediction(msg_text)
        print(f"Mensagem: {msg_text}\nPredição: {prediction}, Probabilidade: {probability}\n")
        results.append({
            "message": msg_text,
            "prediction": prediction,
            "probability": probability
        })
    except Exception as e:
        print(f"Erro na mensagem: {msg_text}\nErro: {e}")
        results.append({
            "message": msg_text,
            "prediction": None,
            "probability": None,
            "error": str(e)
        })

# Salvando resultados no CSV
with open("./testing/testing_messages_results.csv", mode="w", newline="", encoding="utf-8") as file:
    fieldnames = ["message", "prediction", "probability", "error"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        if "error" not in row:
            row["error"] = ""
        writer.writerow(row)

print("Processamento finalizado. Resultados salvos em ./testing/testing_messages_results.csv")

# Contagem de predições
total_msgs = len(results)
eng_social = sum(1 for r in results if r["prediction"] == 1)
nao_eng_social = sum(1 for r in results if r["prediction"] == 0)

percent_eng_social = (eng_social / total_msgs) * 100
percent_nao_eng_social = (nao_eng_social / total_msgs) * 100

print("\n=== Resumo Geral ===")
print(f"Total de mensagens processadas: {total_msgs}")
print(f"Engenharia Social: {eng_social} ({percent_eng_social:.2f}%)")
print(f"Não Engenharia Social: {nao_eng_social} ({percent_nao_eng_social:.2f}%)")