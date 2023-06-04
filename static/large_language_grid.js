const languageGridWrapper = document.getElementById('language-grid-wrapper');
const languageGridLoading = document.getElementById('language-grid-loading');
const languageGrid = document.getElementById('language-grid');

function getRandomColor() {
  const red = 64 + Math.floor(Math.random()*128);
  const green = 64 + Math.floor(Math.random()*128);
  const blue = 64 + Math.floor(Math.random()*128);
  const randomColor = `rgb(${red}, ${green}, ${blue})`;
  return randomColor;
}

fetch("/static/lexopedia-language-statistics.json")
  .then(response => response.json())
  .then(languages => {
    const maxBlocks = 1000;
    for (let i = 0; i < languages.length && i < maxBlocks; i++) {
      const languageBlock = document.createElement('div');
      languageBlock.classList.add('language-block');
      languageBlock.setAttribute('data-language', languages[i].language);
      
      const languageName = document.createElement('h3');
      languageName.textContent = languages[i].language;
      languageName.style.color = getRandomColor();
      languageBlock.appendChild(languageName);
      
      const wordCount = document.createElement('p');
      wordCount.textContent = `${languages[i].wordsNum} words`;
      wordCount.style.fontStyle = "italic";
      languageBlock.appendChild(wordCount);
      
      languageBlock.addEventListener('click', (event) => {
        const languageName = event.currentTarget.getAttribute('data-language');
        window.location.href = `/dictionary/${languageName}/1`;
      });
      
      languageGrid.appendChild(languageBlock);
    }
    languageGridLoading.style.display = 'none';
    languageGrid.style.display = 'grid';
  })
  .catch(error => {
    languageGridLoading.textContent = 'Error loading language data';
    console.error(error);
  });
