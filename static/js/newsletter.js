document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    // Store the user's email from the first form for later use in the second form
    let userEmail = "";

    const newsletterForm = document.getElementById("newsletter-form");
    const interestForm = document.getElementById("interest-form");
    const popup = document.getElementById("newsletter-popup");
    const closePopupBtn = document.getElementById("close-popup");
    const subscriberIdInput = document.getElementById("subscriber_id");

    // Show the pop-up
    function showPopup() {
        popup.style.display = "flex"; // Show the modal with flexbox centering
    }

    // Hide the pop-up
    function hidePopup() {
        popup.style.display = "none";
    }

    // Close pop-up when clicking outside the card
    popup.addEventListener("click", function (event) {
        if (event.target === popup) {
            hidePopup();
        }
    });

    // Close pop-up when clicking the close button
    closePopupBtn.addEventListener("click", hidePopup);

    // Handle Newsletter Form Submission
    newsletterForm.addEventListener("submit", function (e) {
        e.preventDefault();

        // Capture the email in a global-scope variable
        userEmail = document.getElementById("email").value;

        fetch("/newsletter-signup/", {
            body: JSON.stringify({ email: userEmail }),
            headers: { "Content-Type": "application/json" },
            method: "POST"
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                subscriberIdInput.value = data.subscriber_id;
                showPopup();  // Show the pop-up questionnaire
            } else {
                alert("Email already subscribed!");
            }
        });
    });

    // Handle Interest Form Submission
    interestForm.addEventListener("submit", function (e) {
        e.preventDefault();

        // Collect selected interests
        const selectedInterests = [];
        document.querySelectorAll("input[name=\"interest\"]:checked")
            .forEach((input) => {
                selectedInterests.push(input.value);
            });

        // Submit interests along with the stored userEmail
        fetch("/newsletter-signup/", {
            body: JSON.stringify({ email: userEmail, interests: selectedInterests }),
            headers: { "Content-Type": "application/json" },
            method: "POST"
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                hidePopup();  // Hide the pop-up
                alert("Thanks for subscribing!");
            } else {
                alert("Error saving interests. Try again!");
            }
        });
    });
});
