


function submitForm(event) {
    event.preventDefault(); // Prevent form from submitting the traditional way
    document.getElementById('response').textContent = "Listening....";
    fetch('/submit', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').textContent = "Listening....";
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('response').textContent = "I am here to help";
    });
    document.getElementById('response').textContent = "I am here to help";
}

const mouth = document.querySelector('.mouth');

// Add interactivity if needed
// For instance, toggle animation
mouth.addEventListener('click', () => {
    mouth.classList.toggle('paused');
});