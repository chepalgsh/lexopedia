const links = document.querySelectorAll('.lexopedia__link');
links.forEach((link, index) => {
    const red = 64 + Math.floor(Math.random()*128);
    const green = 64 + Math.floor(Math.random()*128);
    const blue = 64 + Math.floor(Math.random()*128);
    const randomColor = `rgb(${red}, ${green}, ${blue})`;
    link.style.color = randomColor;
});