document.getElementById("upi-payment-form").addEventListener("submit", function(e) {
    e.preventDefault();

    const upiId = document.getElementById("upi-id").value;
    const name = document.getElementById("name").value;
    const orderId = "ORDER" + Math.floor(Math.random() * 1000000);

    fetch("/verify_payment", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            order_id: orderId,
            upi_id: upiId,
            name: name
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("payment-status").style.display = "block";
        document.getElementById("status").textContent = data.message;
    });
});
