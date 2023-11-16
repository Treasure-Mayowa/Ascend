const inputForm = document.getElementById('planner-form')
const topicInput = document.getElementById('topic')
const subInput = document.getElementById('sub-topic')
const durationInput = document.getElementById('duration')
const subjectInput = document.getElementById('subject')
const resultdiv = document.getElementById('result')

inputForm.addEventListener('submit', async (event)=> {
    event.preventDefault()

    const subject = subjectInput.value
    const topic = topicInput.value
    const sub = subInput.value
    const duration = durationInput.value

    // Clear input field
    subjectInput.value = ''
    topicInput.value = ''
    subInput.value = ''
    durationInput.value = ''
    resultdiv.innerHTML = ''

    // Show loading animation
    let message = document.createElement('div')
    message.innerHTML = `<div class="lds-facebook"><div class="tools"></div><div class="tools"></div><div class="tools"></div></div>`
    resultdiv.appendChild(message)
    message.scrollIntoView({ behavior: 'smooth' })

    const response = await getPlan(subject, topic, sub, duration)

    // Add chatbot response to conversation
    message.innerText = `${response}`
    message.scrollIntoView({ behavior: 'smooth' })
})


async function getPlan(subject, topic, sub, duration) {
    try {
        const response = await fetch(`/api/planner?subject=${subject}&topic=${topic}&sub=${sub}&duration=${duration}`)
        const data = await response.json()
        const adaptedResult = data.result.replace(/\\n/g, '<br>')
        return adaptedResult
      } catch (error) {
        console.error('Error fetching data:', error)
        return 'An error occurred. Try again';
      }
}