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

    // send request to the server containing the content's name and the rating value
    const xhr = new XMLHttpRequest();
    xhr.open('POST', `../rate-content/`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    const data = JSON.stringify({
        content_url_name: contentUrlName,
        rating: rating
    });
    xhr.send(data);

    // update the rating panels once the client recieves the server's response
    xhr.onload = () => {
        const response = JSON.parse(xhr.responseText);  // parse the response as JSON

        if(response.success) {
            ratingPanel.dataset.rating = rating;

            checkStars(ratingPanel, rating, false);

            const community_rating_panel = document.querySelector('.sharwicom-wrapper .rating.community');
            checkStars(community_rating_panel, response.community_rating, true);
        }
    }
}

function checkStars(ratingPanel, starsToCheck, isPartiallyFillable) {
    ratingPanel.dataset.rating = starsToCheck;

    if(isPartiallyFillable) {
        // unfill all stars
        for (const star of ratingPanel.children) {
            star.style.setProperty('--fill', '0%');
        }
    
        let rating = ratingPanel.dataset.rating;
    
        for (const star of ratingPanel.children) {
            if (rating < 1) {
                star.style.setProperty('--fill', rating * 100 + "%")
                break;
            } else {
                star.style.setProperty('--fill', '100%');
            }
            rating -= 1;
        }
    }
    else {
        // uncheck all the stars
        for(const star of ratingPanel.children) {
            star.classList.remove('checked');
        }

        const stars = ratingPanel.children;

        // check the correct ammount of stars (passed as an argument)
        for(let i = 0; i < starsToCheck; i++) {
            stars[i].classList.add('checked');
        }   
    }
}

const ratingPanels = document.querySelectorAll('.sharwicom-wrapper .rating');

for(const ratingPanel of ratingPanels) {
    for(const star of ratingPanel.children) {
        const contentUrlName = ratingPanel.dataset.content_url_name;
        const rating = star.className[1];

        star.addEventListener('click', (event) => {
            rateAjaxRequest(contentUrlName, rating, ratingPanel);
        });
    }

    // hover effect for star ratings
    if(ratingPanel.classList[1] == 'interactable') {
        checkStars(ratingPanel, ratingPanel.dataset.rating, false); // automatically check the stars specified in the data attribute so it doesnt have to be added manually

        for(const star of ratingPanel.children) {
            star.addEventListener('mouseover', (event) => {
               checkStars(ratingPanel, star.className[1]);
            });
    
            star.addEventListener('mouseout', (event) => {
                checkStars(ratingPanel, ratingPanel.dataset.rating);
            });
        }
    }
    else {
        // for those rating panels that may contain stars which are partially filled
        checkStars(ratingPanel, ratingPanel.dataset.rating, true); // automatically check the stars specified in the data attribute so it doesnt have to be added manually
    }
}