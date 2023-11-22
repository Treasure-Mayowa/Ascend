const inputForm = document.getElementById('pedagogy-form')
const topicInput = document.getElementById('topic')
const classInput = document.getElementById('class')
const pedagogyInput = document.getElementById('pedagogy')
const subjectInput = document.getElementById('subject')
const resultdiv = document.getElementById('result')

inputForm.addEventListener('submit', async (event)=> {
    event.preventDefault()

    const subject = subjectInput.value
    const topic = topicInput.value
    const subject_class = classInput.value
    const pedagogy = pedagogyInput.value

    // Clear input field
    subjectInput.value = ''
    topicInput.value = ''
    resultdiv.innerHTML = ''

    // Show loading animation
    let message = document.createElement('div')
    message.innerHTML = `<div class="lds-facebook"><div class="tools"></div><div class="tools"></div><div class="tools"></div></div>`
    resultdiv.appendChild(message)
    message.scrollIntoView({ behavior: 'smooth' })

    const response = await getGuide(subject, topic, subject_class, pedagogy)

    // Add chatbot response to conversation
    message.innerText = `${response}`
    message.scrollIntoView({ behavior: 'smooth' })
})


async function getGuide(subject, topic, subject_class, pedagogy) {
    try {
        const response = await fetch(`/api/pedagogy-guide?subject=${subject}&topic=${topic}&class=${subject_class}&pedagogy=${pedagogy}`)
        const data = await response.json()
        const adaptedResult = data.result.replace(/\\n/g, '<br>')
        return adaptedResult
      } catch (error) {
        console.error('Error fetching data:', error)
        return 'An error occurred. Try again';
      }
}