/*******Alerts***********/
function displayAlert(message, alertType, containerId = "alerts") {
    const container = document.getElementById(containerId);

    // Create the alert div
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${alertType} bg-${alertType}  text-light border-0  alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;

    // Append the alert div to the container
    container.appendChild(alertDiv);

    // Automatically remove the alert after a certain time (e.g., 5 seconds)
    setTimeout(() => {
        container.removeChild(alertDiv);
    }, 5000);
}

/*******Alerts***********/



// const scriptURL = 'https://script.google.com/macros/s/AKfycbxpErz8oIYDNRCuth4lkoqRHMquLrEeLoDaApf-PHK0xBnqvUSRpboqDI6VzLady1EP/exec'


const scriptURL = 'https://script.google.com/macros/s/AKfycbw0oyogsTKl49Gis17Yr3KIaXdUphoqeU9NT6fqkhcVZ05tJw6W7-hlHXBE4Zup2ok/exec'



const form = document.forms['submit-to-google-sheet']



form.addEventListener('submit', e => {
    const currentTime = new Date().toLocaleString();

    // Append current time to form data
    const formData = new FormData(form);
    formData.append('Datetime', currentTime);

    e.preventDefault();

    fetch(scriptURL, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // console.log('Success!', response);
                displayAlert("Your response was submitted successfully.", "success");
              
              
                setTimeout(() => {
                    location.reload();
                }, 2500);

                
           
            } else {
                // console.error('Error!', response.statusText);
                displayAlert("Failed to submit response. Please try again later.", "danger");
          
            }
        })
        .catch(error => {
            // console.error('Error!', error.message);
            displayAlert("Failed to submit response. Please try again later.", "danger");
        });
});