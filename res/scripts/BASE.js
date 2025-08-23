const loaderBar = document.querySelector('.soft-loader-bar');

document.addEventListener('DOMContentLoaded', () => {

    document.addEventListener('click', async (e) => {
        const link = e.target.closest('a');
        if (!link) return;
        if (link.origin !== location.origin) return;

        e.preventDefault();

        loaderBar.style.display = "block";
        loaderBar.style.width = "0%";
        loaderBar.style.opacity = "1";
        requestAnimationFrame(async () => {
            await softLoad(link.href);
        });
    })
})

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function setLoaderWidth(percent) {
    console.log(percent);
    if (loaderBar) loaderBar.style.width = percent + "%";
}

async function softLoad(url) {
    try {
        if (loaderBar) {
            loaderBar.style.width = "0%";
            loaderBar.style.display = "block";
        }

        await setLoaderWidth(10);

        const res = await fetch(url, {
            method: "GET",
            headers: { "X-Requested-With": "XMLHttpRequest" }
        });

        if (res.redirected) return window.location.href = res.url;

        await setLoaderWidth(20);

        const html = await res.text();
        await setLoaderWidth(35);

        const curRoot = document.querySelector("#root-content");
        if (!curRoot) return;

        curRoot.style.transition = "opacity 0.15s ease-in, transform 0.3s ease-out";
        curRoot.style.transformOrigin = "bottom center"; 
        curRoot.style.opacity = "0";
        curRoot.style.transform = "scaleY(0)";

        await new Promise(r => setTimeout(r, 300)); 

        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");

        const newTitle = doc.querySelector("title")?.textContent;
        if (newTitle) document.title = newTitle;

        await setLoaderWidth(55);

        const oldLinks = Array.from(document.querySelectorAll('link[rel="stylesheet"]'));

        const alwaysKeep = oldLinks.filter(l => 
            l.href.includes('BASE.css') || l.href.includes('fonts.googleapis.com')
        );

        oldLinks.forEach(l => {
            if (!alwaysKeep.includes(l)) l.remove();
        });

        const newLinks = Array.from(doc.querySelectorAll('link[rel="stylesheet"]'));
        const cssPromises = [];
        newLinks.forEach(link => {
            if (!document.querySelector(`link[href="${link.href}"]`) && 
                !link.href.includes('BASE.css') && 
                !link.href.includes('fonts.googleapis.com')) 
            {
                const newLink = document.createElement('link');
                newLink.rel = "stylesheet";
                newLink.href = link.href;
                document.head.appendChild(newLink);
                cssPromises.push(new Promise(r => { newLink.onload = r; newLink.onerror = r; }));
            }
        });

        await Promise.all(cssPromises);
        await setLoaderWidth(75);

        const newRoot = doc.querySelector("#root-content");
        if (newRoot) {
            curRoot.replaceWith(newRoot);

            newRoot.style.opacity = "0";
            newRoot.style.transform = "scaleY(0)";
            newRoot.style.transition = "opacity 0.3s ease, transform 0.3s ease";
            requestAnimationFrame(() => {
                newRoot.style.opacity = "1";
                newRoot.style.transform = "scaleY(1)";
            });
        }

        await setLoaderWidth(85);

        Array.from(document.querySelectorAll('script')).forEach(s => {
            if (s.src && !s.src.includes("BASE.js")) s.remove();
        });

        const newScripts = Array.from(doc.querySelectorAll('script'));
        for (let script of newScripts) {
            if (script.src && !script.src.includes("BASE.js")) {
                await new Promise(r => {
                    const s = document.createElement('script');
                    s.src = script.src;
                    s.async = false;
                    s.onload = r;
                    document.body.appendChild(s);
                });
            } else if (!script.src && script.textContent.trim()) {
                const s = document.createElement('script');
                s.textContent = script.textContent;
                document.body.appendChild(s);
            }
        }

        await setLoaderWidth(90);

        history.pushState(null, "", url);
        await setLoaderWidth(100);

    } catch (err) {
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
