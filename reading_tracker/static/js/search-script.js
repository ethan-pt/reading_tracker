const coverDiv = document.getElementsByClassName('cover-div');
const coverImg = document.getElementsByClassName('cover-img');
// iterates through each cover div and calculates padding needed 
// based on cover image width to square off cover div outline
for (let i = 0; i < coverDiv.length; i++) {
    coverImg[i].onload = (event) => {
        coverDiv[i].style.padding = `0 ${45 - (coverImg[i].width / 2)}px`;
    }
}