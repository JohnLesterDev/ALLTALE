const loaderBar = document.querySelector('.soft-loader-bar');

document.addEventListener('DOMContentLoaded', () => {

    // Injects all anchors chu chu
    document.addEventListener('click', async (e) => {
        const link = e.target.closest('a');
        if (!link) return;

        if (link.origin !== location.origin) return;

        e.preventDefault();
        await softLoad(link.href); 
    })
})

function setLoaderWidth(percent) {
    if (loaderBar) loaderBar.style.width = percent + "%";
}

async function softLoad(url) {
    try {
        if (loaderBar) {
            loaderBar.style.width = "0%";
            loaderBar.style.display = "block";
        }

        if (loaderBar) setLoaderWidth(20);

        const res = await fetch(url, {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        });

        if (loaderBar) setLoaderWidth(50);

        if (res.redirected) {
            window.location.href = res.url;
            return;
        }

        const html = await res.text();

        if (loaderBar) setLoaderWidth(80);

        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");

        const newRoot = doc.querySelector("#root-content");
        const curRoot = document.querySelector("#root-content");

        if (newRoot && curRoot) {
            curRoot.replaceWith(newRoot);
            history.pushState(null, "", url);
        }

        if (loaderBar) setLoaderWidth(100);
    
    } catch (err) {
        console.error("SPA loading failed: ", err);
        window.location.href = url;
    
    } finally {
        if (loaderBar) {
            setTimeout(() => {
                loaderBar.style.display = "none";
                loaderBar.style.width = "0%";
            }, 300);
        }
    }
}