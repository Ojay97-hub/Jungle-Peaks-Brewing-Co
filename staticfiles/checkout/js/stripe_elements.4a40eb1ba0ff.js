// Boutique Ado
/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

const stripePublicKeyElement = document.getElementById('id_stripe_public_key');
const clientSecretElement = document.getElementById('id_client_secret');

if (!stripePublicKeyElement || !clientSecretElement) {
    console.error('Stripe public key or client secret not found in the DOM.');
    // Exit early to prevent ReferenceErrors
    throw new Error('Required Stripe elements not found');
}

let stripePublicKey, clientSecret, stripe;

// Safely parse JSON with error handling
try {
    stripePublicKey = JSON.parse(stripePublicKeyElement.textContent);
    clientSecret = JSON.parse(clientSecretElement.textContent);
} catch (error) {
    console.error('Failed to parse Stripe configuration from DOM:', error);
    throw new Error('Invalid Stripe configuration in DOM');
}

// Validate required values
if (!stripePublicKey || !clientSecret) {
    console.error('Stripe public key or client secret is missing or invalid');
    throw new Error('Invalid Stripe credentials');
}

// Initialize Stripe
try {
    stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();
    const style = {
        base: {
            color: '#000',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#dc3545',
            iconColor: '#dc3545'
        }
    };
    const card = elements.create('card', { style });
    card.mount('#card-element');

    const form = document.getElementById('payment-form');
    const submitButton = document.getElementById('submit-button');
    const overlay = document.getElementById('loading-overlay');
    const paymentCard = form ? form.closest('.payment-card') : null;
    const errorContainer = document.getElementById('card-errors');

    const setProcessingState = (isProcessing) => {
        card.update({ disabled: isProcessing });
        if (submitButton) {
            submitButton.disabled = isProcessing;
        }
        if (overlay) {
            overlay.classList.toggle('active', isProcessing);
        }
        if (paymentCard) {
            paymentCard.classList.toggle('is-processing', isProcessing);
        }
    };

    const renderError = (message) => {
        if (!errorContainer) {
            return;
        }

        if (!message) {
            errorContainer.textContent = '';
            errorContainer.innerHTML = '';
            return;
        }

        errorContainer.innerHTML = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${message}</span>
        `;
    };

    card.addEventListener('change', (event) => {
        if (event.error) {
            renderError(event.error.message);
        } else {
            renderError('');
        }
    });

    if (form) {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            setProcessingState(true);

            const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
            const saveInfoCheckbox = document.getElementById('id-save-info');
            const postData = new URLSearchParams();

            if (!csrfInput) {
                renderError('Missing CSRF token. Please refresh and try again.');
                setProcessingState(false);
                return;
            }

            postData.append('csrfmiddlewaretoken', csrfInput.value);
            postData.append('client_secret', clientSecret);
            postData.append('save_info', saveInfoCheckbox && saveInfoCheckbox.checked ? 'true' : 'false');

            const getTrimmedValue = (fieldName) => {
                const field = form.elements.namedItem(fieldName);
                return field ? field.value.trim() : '';
            };

            try {
                const response = await fetch('/checkout/cache_checkout_data/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: postData.toString()
                });

                if (!response.ok) {
                    throw new Error('Failed to cache checkout data.');
                }

                const billingDetails = {
                    name: getTrimmedValue('full_name'),
                    phone: getTrimmedValue('phone_number'),
                    email: getTrimmedValue('email'),
                    address: {
                        line1: getTrimmedValue('street_address1'),
                        line2: getTrimmedValue('street_address2'),
                        city: getTrimmedValue('town_or_city'),
                        country: getTrimmedValue('country'),
                        state: getTrimmedValue('county')
                    }
                };

                const shippingDetails = {
                    name: billingDetails.name,
                    phone: billingDetails.phone,
                    address: {
                        line1: billingDetails.address.line1,
                        line2: billingDetails.address.line2,
                        city: billingDetails.address.city,
                        country: billingDetails.address.country,
                        postal_code: getTrimmedValue('postcode'),
                        state: billingDetails.address.state
                    }
                };

                const result = await stripe.confirmCardPayment(clientSecret, {
                    payment_method: {
                        card,
                        billing_details: billingDetails
                    },
                    shipping: shippingDetails
                });

                if (result.error) {
                    renderError(result.error.message);
                    setProcessingState(false);
                } else if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            } catch (error) {
                window.location.reload();
            }
        });
    }
} catch (error) {
    console.error('Failed to initialize Stripe:', error);
    // Show error to user
    const errorContainer = document.getElementById('card-errors');
    if (errorContainer) {
        errorContainer.innerHTML = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>Payment system unavailable. Please refresh the page or try again later.</span>
        `;
    }
    // Disable the form
    const form = document.getElementById('payment-form');
    const submitButton = document.getElementById('submit-button');
    if (form) form.style.display = 'none';
    if (submitButton) submitButton.disabled = true;
}
