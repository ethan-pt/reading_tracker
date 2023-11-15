const searchButton = document.getElementById("search-book-button");
searchButton.addEventListener("click", (event) => {
    console.log('button pressed');
    const searchPath = "https://www.googleapis.com/books/v1/volumes?q=";
    let searchText = encodeURIComponent(document.getElementById("search-book-area").value);

    const xhr = new XMLHttpRequest();
    xhr.open("GET", searchPath + searchText);
    console.log('request sent...');
    xhr.onreadystatechange = () => {
        console.log(xhr.status);
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log('success')
            const contentWrapper = document.getElementById("content");
            const data = JSON.parse(xhr.response);

            for(let i = 0; i < data.items.length; i++) {
                let item = data.items[i];
                console.log(item.volumeInfo.title);
                const bookDiv = document.createElement("div");
                bookDiv.innerHTML = `<br><p>${item.volumeInfo.title}</p>`;
                contentWrapper.appendChild(bookDiv);
            }
        } else {
            console.log('failure')
            const errMsg = document.createElement("h4");
            errMsg.innerHTML = "Something went wrong, try again later.";
            contentWrapper.appendChild(errMsg);
        }
    }
});