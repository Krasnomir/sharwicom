function getCookie(name) {
    let cookieValue = null;

    if(window.document.cookie && window.document.cookie !== '') {
        const cookies = window.document.cookie.split(';');

        // iterate through stored cookies 
        for(let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            
            if(cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function rateAjaxRequest(contentUrlName, rating, ratingPanel) {
    const csrftoken = getCookie('csrftoken')

    const xhr = new XMLHttpRequest();
    xhr.open('POST', `../rate-content/`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    const data = JSON.stringify({
        content_url_name: contentUrlName,
        rating: rating
    });
    xhr.send(data);

    xhr.onload = () => {
        const ratingSuccessfull = JSON.parse(xhr.responseText);  // parse the response as JSON

        if(ratingSuccessfull) {
            ratingPanel.dataset.rating = rating;
        }
    }
}

function checkStars(ratingPanel, starsToCheck) {
    // uncheck all the stars
    for(const star1 of ratingPanel.children) {
        star1.classList.remove('checked');
    }

    const stars = ratingPanel.children;

    // check the correct ammount of stars (passed as an argument)
    for(let i = 0; i < starsToCheck; i++) {
        stars[i].classList.add('checked');
    }
}

const ratingPanels = document.querySelectorAll('.sharwicom-wrapper .rating');

for(const ratingPanel of ratingPanels) {
    checkStars(ratingPanel, ratingPanel.dataset.rating); // automatically check the stars specified in the data attribute so it doesnt have to be added manually

    for(const star of ratingPanel.children) {
        const contentUrlName = ratingPanel.dataset.content_url_name;
        const rating = star.className[1];

        star.addEventListener('click', (event) => {
            rateAjaxRequest(contentUrlName, rating, ratingPanel);
        });
    }

    // hover effect for star ratings
    if(ratingPanel.classList[1] == 'interactable') {
        for(const star of ratingPanel.children) {
            star.addEventListener('mouseover', (event) => {
               checkStars(ratingPanel, star.className[1]);
            });
    
            star.addEventListener('mouseout', (event) => {
                checkStars(ratingPanel, ratingPanel.dataset.rating);
            });
        }
    }
}