const inputForm = document.getElementById('assessment-form')
const contentInput = document.getElementById('content')
const numberInput = document.getElementById('number')
const resultdiv = document.getElementById('result')


inputForm.addEventListener('submit', async (event)=> {
    event.preventDefault()

    const content = contentInput.value
    const number = numberInput.value

    // Clear input field
    contentInput.value = ''
    numberInput.value = ''
    resultdiv.innerHTML = ''

    // Show loading animation
    let message = document.createElement('div')
    message.innerHTML = `<div class="lds-facebook"><div class="tools"></div><div class="tools"></div><div class="tools"></div></div>`
    resultdiv.appendChild(message)
    message.scrollIntoView({ behavior: 'smooth' })

    const response = await getAssessment(content, number)

    // Add chatbot response to conversation
    message.innerText = `${response}`
    message.scrollIntoView({ behavior: 'smooth' })
})


async function getAssessment(content, number) {
    try {
        const response = await fetch(`/api/assessment?content=${content}&number=${number}`)
        const data = await response.json()
        console.log(data)
        const adaptedResult = data.result.replace(/\\n/g, '<br>')
        console.log(adaptedResult)
        return adaptedResult
      } catch (error) {
        console.error('Error fetching data:', error)
        return 'An error occurred. Try again';
      }
}