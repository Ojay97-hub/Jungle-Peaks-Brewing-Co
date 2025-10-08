document.addEventListener("DOMContentLoaded", () => {
    const steppers = document.querySelectorAll("[data-quantity-stepper]");

    steppers.forEach((stepper) => {
        const input = stepper.querySelector("input[type='number']");
        if (!input) {
            return;
        }
        const min = parseInt(input.min || "1", 10);
        const max = parseInt(input.max || "99", 10);

        stepper.addEventListener("click", (event) => {
            const button = event.target.closest("button[data-step]");
            if (!button) {
                return;
            }

            event.preventDefault();
            let currentValue = parseInt(input.value || String(min), 10);

            if (Number.isNaN(currentValue)) {
                currentValue = min;
            }

            if (button.dataset.step === "increase" && currentValue < max) {
                currentValue += 1;
            }

            if (button.dataset.step === "decrease" && currentValue > min) {
                currentValue -= 1;
            }

            input.value = currentValue;
        });
    });
});
