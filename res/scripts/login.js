const form = document.querySelector('.form-container');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = new FormData(form);

    try {
        const res = await fetch(form.action, {
            method: form.method,
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            },
            body: data
        });

        const json_res = await res.json();

        if (json_res.success) {
            // SPA redirect using softLoad
            if (json_res.redirect) {
                await softLoad(json_res.redirect);
            }
        } else {
            console.error("Login failed:", json_res.message);
        }
    } catch (err) {
        console.error("Error submitting form:", err);
    }
});
