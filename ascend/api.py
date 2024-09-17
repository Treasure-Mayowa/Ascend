API_KEY = settings.API_KEY

STREAM = False

URL = "https://chat.tune.app/api/chat/completions"

HEADERS = {"Authorization": API_KEY, "Content-Type": "application/json"}


# Function for the assessment_api view
def api_assessment(content, number):
    data = {
        "temperature": 0.6,
       "messages": [
        {
           "role": "system",
            "content": "You are an Ascend assessment AI designed to generate assessment questions from topics or notes"
        },
        {
            "role": "user",
            "content": f"Using these topics or notes, generate {number} good assessment questions. Format your response well and do not put an preface text in your response, just the assessment questions: {content}"
        }
        ],
        "model": "mixtral-8x7b-inst-v0-1-32k",
        "stream": STREAM,
        "max_tokens": 1000
        }
    response = requests.post(URL, headers=HEADERS, json=data)
    if stream:
        for line in response.iter_lines():
            if line:
                l = line[6:]
                if l != b'[DONE]':
                    result = json.loads(l)
                    return  result
    else:
        result = response.json()['choices'][0]['message']['content']
        return result

# Function for planner_api view
def api_planner(subject, topic, sub,duration):
    data = {
        "messages": [
            { 
                "role": "system", 
                "content": "You are an Ascend lesson planner AI designed to generate lesson plans for Nigerian teachers" 
            },
            { 
                "role": "user", 
                "content":  f"Generate a lesson plan following the Nigerian curriculum with the the topic, {topic}, sub-topic, {sub}, lesson duration of {duration} minutes under the subject, {subject}. If there is an invalid topic, sub-topic, or subject, just respond 'Invalid input. Try again.' Format your response well and DO NOT put any preface text in your response, just the lesson plan. Also, put 'Key Point' outline in the lessons plan to highlight key points in the subtopic alongside other default outlines."
            }
        ],
        "model": "mixtral-8x7b-inst-v0-1-32k",
        "stream": STREAM,
        "temperature": 0.7,
        "max_tokens": 1000
    }
    response = requests.post(URL, headers=HEADERS, json=data)
    if stream:
        for line in response.iter_lines():
            if line:
                l = line[6:]
                if l != b'[DONE]':
                    result = json.loads(l)
                    return  result
    else:
        result = response.json()['choices'][0]['message']['content']
        return result
    

# Function for pedagogy_api view
def api_pedagogy(pedagogy, subject, topic, subject_class):


    data = {
        "messages": [
            { 
                "role": "system", 
                "content": "You are an Ascend AI bot designed to guide Nigerian teachers to implement various pedagogy in their lesson" 
            },
            { 
                "role": "user", 
                "content":  f"Create a detailed guide for applying {pedagogy} to teach the topic {topic} under the subject {subject} for {subject_class} students"
            }
        ],
        "model": "mixtral-8x7b-inst-v0-1-32k",
        "stream": STREAM,
        "temperature": 0.8,
        "max_tokens": 1000
    }
    response = requests.post(URL, headers=HEADERS, json=data)
    if stream:
        for line in response.iter_lines():
            if line:
                l = line[6:]
                if l != b'[DONE]':
                    result = json.loads(l)
                    return  result
    else:
        result = response.json()['choices'][0]['message']['content']
        return result