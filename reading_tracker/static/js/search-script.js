const searchButton = document.getElementById("search-book-button");
searchButton.addEventListener("click", (event) => {
    const searchPath = "https://www.googleapis.com/books/v1/volumes?q=";
    let searchText = encodeURIComponent(document.getElementById("search-book-area").value);

    const xhr = new XMLHttpRequest();
    xhr.onload = () => {
        const contentWrapper = document.getElementById("content");

        if (xhr.readyState == 4 && xhr.status == 200) {
            const data = JSON.parse(xhr.response);

            for(let i = 0; i < data.items.length; i++) {
                let item = data.items[i];
                const bookDiv = document.createElement("div");
                bookDiv.innerHTML = `<br><h4>${item.volumeInfo.title}</h4>`;
                contentWrapper.appendChild(bookDiv);
            }
        } else {
            const errMsg = document.createElement("h4");
            errMsg.innerHTML = "Something went wrong, try again later.";
            contentWrapper.appendChild(errMsg);
        }
    }

    xhr.open("GET", searchPath + searchText);
    xhr.send();
});