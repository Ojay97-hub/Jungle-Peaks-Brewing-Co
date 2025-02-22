document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    let userEmail = "";

    const newsletterForm = document.getElementById("newsletter-form");
    const interestForm = document.getElementById("interest-form");
    const popup = document.getElementById("newsletter-popup");
    const closePopupBtn = document.getElementById("close-popup");
    const subscriberIdInput = document.getElementById("subscriber_id");

    function showPopup() {
        popup.style.display = "flex"; 
    }

    function hidePopup() {
        popup.style.display = "none";
    }

    popup.addEventListener("click", function (event) {
        if (event.target === popup) {
            hidePopup();
        }
    });

    closePopupBtn.addEventListener("click", hidePopup);

    // Handle Newsletter Signup
    newsletterForm.addEventListener("submit", function (e) {
        e.preventDefault();

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
                showPopup();
            } else {
                alert("Email already subscribed!");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });
    });

    // Handle Interest Submission
    interestForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const selectedInterests = [];
        document.querySelectorAll("input[name='interest']:checked")
            .forEach((input) => selectedInterests.push(input.value));

        if (selectedInterests.length === 0) {
            alert("Please select at least one interest.");
            return;
        }

        fetch("/set-interests/", {  // ✅ Fix the endpoint URL
            body: JSON.stringify({
                subscriber_id: subscriberIdInput.value,
                interests: selectedInterests
            }),
            headers: { "Content-Type": "application/json" },
            method: "POST"
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                hidePopup();
                alert("Thanks for subscribing!");
            } else {
                alert("Error saving interests. Try again!");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });
    });
});