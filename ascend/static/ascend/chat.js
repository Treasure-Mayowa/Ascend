// Get chatbot elements
const chatbot = document.getElementById('chatbot');
const conversation = document.getElementById('conversation');
const inputForm = document.getElementById('input-form');
const inputField = document.getElementById('input-field');

inputForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const input = inputField.value;

  // Clear input field
  inputField.value = '';

  // Add user input to conversation
  let message = document.createElement('div');
  message.classList.add('chatbot-message', 'user-message');
  message.innerHTML = `<p class="chatbot-text">${input}</p>`;
  conversation.appendChild(message);

  // Show loading animation
  message = document.createElement('div');
  message.classList.add('chatbot-message', 'chatbot');
  message.innerHTML = `<div class="lds-facebook"><div></div><div></div><div></div></div>`;
  conversation.appendChild(message);
  message.scrollIntoView({ behavior: 'smooth' });


  // Generate chatbot response
  const response = await generateResponse(input);

  // Add chatbot response to conversation
  message.innerHTML = `<p class="chatbot-text">${response.trim()}</p>`;
  message.scrollIntoView({ behavior: 'smooth' });
})

// Generate chatbot response function
async function generateResponse(input) {
  try {
    const response = await fetch('/api/ascendchat/' + input);
    const data = await response.json();
    return data.result;
  } catch (error) {
    console.error('Error fetching data:', error);
    return 'An error occurred while responding.';
  }
}
