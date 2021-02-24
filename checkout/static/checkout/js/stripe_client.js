/* Custom payment flow logic is from:
 * https://stripe.com/docs/payments/integration-builder
 * I have left the variable declarations as var, as that is how it came from Stripe
 */ 

    // A reference to Stripe.js initialized with your real test publishable API key.
    var stripe = Stripe("pk_test_51I94JSGCTK7uumSDLZ5aH00plz6tDGrlJgDLvut5RBKPFwbdHoGOQcttdS4DFhKemJOukLbDUsnIahNbXoqpOTZQ00Nc1A8S6l");

    var form = document.getElementById("id-orderform");
    
    // Disable the button until we have Stripe set up on the page
    document.querySelector("button").disabled = true;
    fetch("/checkout/create-payment-intent/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    })
    .then(function(result) {
        if (result.status != 200) {
            return;
        } else {
            return result.json();
        }
    })
    .then(function(data) {
        if (data === undefined) {
            window.location.href = '/cart/';
        }
        var elements = stripe.elements();

        var style = {
        base: {
            color: "#32325d",
            fontFamily: 'Arial, sans-serif',
            fontSmoothing: "antialiased",
            fontSize: "16px",
            "::placeholder": {
            color: "#32325d"
            }
        },
        invalid: {
            fontFamily: 'Arial, sans-serif',
            color: "#fa755a",
            iconColor: "#fa755a"
        }
        };

        var card = elements.create("card", { style: style });
        // Stripe injects an iframe into the DOM
        card.mount("#card-element");

        card.on("change", function (event) {
        // Disable the Pay button if there are no card details in the Element
        document.querySelector("button").disabled = event.empty;
        document.querySelector("#card-error").textContent = event.error ? event.error.message : "";
        });

        form.addEventListener('submit', function(event) {
            event.preventDefault();
            // Complete payment when the submit button is clicked
            payWithCard(stripe, card, data.clientSecret);
        });
    });

    // Calls stripe.confirmCardPayment
    // If the card requires authentication Stripe shows a pop-up modal to
    // prompt the user to enter authentication details without leaving your page.
    var payWithCard = function(stripe, card, clientSecret) {
    loading(true);
    stripe
        .confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    email: $.trim(form.email.value),
                    phone: $.trim(form.phone_number.value),
                    address:{
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        state: $.trim(form.county.value),
                        country: $.trim(form.country.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    state: $.trim(form.county.value),
                    postal_code: $.trim(form.postcode.value),
                }
            },
        })
        .then(function(result) {
        if (result.error) {
            // Show error to your customer
            showError(result.error.message);
        } else {
            // The payment succeeded!
            $('#id_stripe_pid').val(result.paymentIntent.id);
            orderComplete(result.paymentIntent.id);
            form.submit();
        }
        });
    };

    /* ------- UI helpers ------- */

    // Shows a success message when the payment is complete
    var orderComplete = function(paymentIntentId) {
        loading(false);
        console.log({paymentIntentId})
        document.querySelector(".result-message").classList.remove("hidden");
        document.querySelector("button").disabled = true;
    };

    // Show the customer the error from Stripe if their card fails to charge
    var showError = function(errorMsgText) {
    loading(false);
    var errorMsg = document.querySelector("#card-error");
    errorMsg.textContent = errorMsgText;
    setTimeout(function() {
        errorMsg.textContent = "";
    }, 4000);
    };

    // Show a spinner on payment submission
    var loading = function(isLoading) {
    if (isLoading) {
        // Disable the button and show a spinner
        document.querySelector("button").disabled = true;
        document.querySelector("#spinner").classList.remove("hidden");
        document.querySelector("#button-text").classList.add("hidden");
    } else {
        document.querySelector("button").disabled = false;
        document.querySelector("#spinner").classList.add("hidden");
        document.querySelector("#button-text").classList.remove("hidden");
    }
    };
