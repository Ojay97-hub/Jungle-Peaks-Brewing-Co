document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    let userEmail = "";

    const newsletterForm = document.getElementById("newsletter-form");
    const interestForm = document.getElementById("interest-form");
    const popup = document.getElementById("newsletter-popup");
    const closePopupBtn = document.getElementById("close-popup");
    const subscriberIdInput = document.getElementById("subscriber_id");

    // Success modal elements
    const successModal = document.getElementById("newsletter-success-modal");
    const successCloseBtn = document.getElementById("close-success-modal");

    function showPopup() {
        popup.style.display = "flex"; 
    }

    function hidePopup() {
        popup.style.display = "none";
    }

    function showSuccessModal() {
        if (successModal) {
            successModal.style.display = "flex";
        }
    }

    function hideSuccessModal() {
        if (successModal) {
            successModal.style.display = "none";
        }
    }

    if (popup) {
        popup.addEventListener("click", function (event) {
            if (event.target === popup) {
                hidePopup();
            }
        });
    }

    if (closePopupBtn) {
        closePopupBtn.addEventListener("click", hidePopup);
    }

    if (successModal) {
        successModal.addEventListener("click", function (event) {
            if (event.target === successModal) {
                hideSuccessModal();
            }
        });
    }

    if (successCloseBtn) {
        successCloseBtn.addEventListener("click", hideSuccessModal);
    }

    // Handle Newsletter Signup
    if (newsletterForm) {
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
    }

    // Handle Interest Submission
    if (interestForm) {
        interestForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const selectedInterests = [];
            document.querySelectorAll("input[name='interest']:checked")
                .forEach((input) => selectedInterests.push(input.value));

            if (selectedInterests.length === 0) {
                alert("Please select at least one interest.");
                return;
            }

            fetch("/set-interests/", {
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
                    showSuccessModal();
                } else {
                    alert("Error saving interests. Try again!");
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("An error occurred. Please try again.");
            });
        });
    }
});