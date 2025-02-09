const ratingPanels = document.querySelectorAll('.sharwicom-wrapper .rating');

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

for(const ratingPanel of ratingPanels) {
    checkStars(ratingPanel, ratingPanel.dataset.rating); // automatically check the stars specified in the data attribute so it doesnt have to be added manually

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