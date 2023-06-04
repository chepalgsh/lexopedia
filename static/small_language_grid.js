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

const specificLanguages = ['English', 'Latin', 'Ancient Greek', 'Proto-Indo-European', 'Proto-Germanic', 'Proto-Italic', 'Egyptian', ];

fetch("/static/lexopedia-language-statistics.json")
  .then(response => response.json())
  .then(languages => {
    const maxBlocks = 8;
    let displayedLanguages = 0;
    for (let i = 0; i < languages.length && displayedLanguages < maxBlocks; i++) {
      const language = languages[i];
      if (specificLanguages.includes(language.language)) {
        const languageBlock = document.createElement('div');
        languageBlock.classList.add('language-block');
        languageBlock.setAttribute('data-language', language.language);

        const languageName = document.createElement('h3');
        languageName.textContent = language.language;
        languageName.style.color = getRandomColor();
        languageBlock.appendChild(languageName);

        const wordCount = document.createElement('p');
        wordCount.textContent = `${language.wordsNum} words`;
        wordCount.style.fontStyle = "italic";
        languageBlock.appendChild(wordCount);

        languageBlock.addEventListener('click', (event) => {
          const languageName = event.currentTarget.getAttribute('data-language');
          window.location.href = `/dictionary/${languageName}/1`;
        });

        languageGrid.appendChild(languageBlock);
        displayedLanguages++;
      }
    }
    languageGridLoading.style.display = 'none';
    languageGrid.style.display = 'grid';

    if (displayedLanguages < specificLanguages.length) {

      const linkBlock = document.createElement('div');
      linkBlock.classList.add('link-block');

      const linkText = document.createElement('h3');
      linkText.textContent = "Show All Languages";
      linkText.style.color = "#800000";
      linkBlock.appendChild(linkText);

      linkBlock.addEventListener('click', (event) => {
        window.location.href = `/dictionaries`;
      });

      languageGrid.appendChild(linkBlock);
    }
  })
  .catch(error => {
    languageGridLoading.textContent = 'Error loading language data';
    console.error(error);
  });

