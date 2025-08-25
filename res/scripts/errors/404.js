async function main_404() {
  const sacred404Messages = [
    "This page does not exist. Seek His path. (404)",
    "The way is lost. Follow His light. (404)",
    "This page is barren. Trust His plan. (404)",
    "No passage lies ahead. Look above. (404)",
    "The path is hidden. Pray for guidance. (404)",
    "This page is void. Find His truth. (404)",
    "You’ve strayed. Return to His grace. (404)",
    "This road is broken. Hold to His hand. (404)",
    "Here lies nothing. Seek His promise. (404)",
    "This door is empty. Ask, and you shall find. (404)",
    "The path ends here. His mercy does not. (404)",
    "No refuge here. Abide in Him. (404)",
    "This land is dark. Walk in His light. (404)",
    "Lost ground. Stand on His rock. (404)",
    "This path is false. His word is true. (404)",
    "The way is blocked. Let Him lead. (404)",
    "No harbor here. Anchor in Christ. (404)",
    "This page is void. He fills all things. (404)",
    "This road is silent. Hear His call. (404)",
    "No sign of life. Seek the Living Word. (404)"
  ];

  function getRandomMessage() {
    return sacred404Messages[Math.floor(Math.random() * sacred404Messages.length)];
  }

  const msg_container = document.querySelector('.message-container');
  const messageEl = document.querySelector('.error-message');
  const logo = document.querySelector('.message-container img');
  const text = getRandomMessage();

  logo.addEventListener('click', async () => {
    await softLoad('/');
  });

  messageEl.innerHTML = "";
  messageEl.classList.add('cursor-visible');   
  logo.style.transform = "translateX(0)";

  await sleep(900);
  
  msg_container.style.gap = "1rem";

  for (let i = 0; i < text.length; i++) {
    const progress = (i + 1) / text.length;
    const maxShiftLeft = 60;
    logo.style.transform = `translateX(-${maxShiftLeft * progress}%)`;

    const span = document.createElement('span');
    span.textContent = text[i];
    messageEl.appendChild(span);

    await sleep(15 + Math.random() * 100);
    span.classList.add('visible');
  }

  messageEl.classList.remove('cursor-visible');

  await sleep(1000);

  logo.classList.add("highlighted");
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

main_404();
