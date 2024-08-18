


function submitForm(event) {
    event.preventDefault(); // Prevent form from submitting the traditional way
    document.getElementById('response').textContent = "Listening....";
    
    fetch('/submit', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // Check the status from the response and update the paragraph text accordingly
        document.getElementById('response').textContent = data.status || "I am here to help";
    })
    .catch(error => {
        console.error('Error:', error);
        // In case of an error, update the response text
        document.getElementById('response').textContent = "I am here to help";
    });
}


const mouth = document.querySelector('.mouth');

// Add interactivity if needed
// For instance, toggle animation
mouth.addEventListener('click', () => {
    mouth.classList.toggle('paused');
});
