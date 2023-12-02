// upon search event, request search results from Google Books API
const searchButton = document.getElementById("search-book-button");
searchButton.addEventListener("click", (event) => {
    const searchPath = "https://www.googleapis.com/books/v1/volumes?q=";
    let searchText = encodeURIComponent(document.getElementById("search-book-area").value);

    const request = new XMLHttpRequest();
    request.onload = () => {
        const contentWrapper = document.getElementById("content");
        contentWrapper.appendChild(document.createElement("br"));

        // displays book title, cover, and author(s) if request is good
        if (request.readyState == 4 && request.status == 200) {
            const bookData = JSON.parse(request.response);

            // for book in book search results, display book
            for(let i = 0; i < bookData.items.length; i++) {
                let item = bookData.items[i];
                const bookId = item.id; // returns an id string
                const bookTitle = document.createElement("h4");
                bookTitle.innerHTML = item.volumeInfo.title; // returns a title string
                const bookAuthors  = document.createElement("p");
                bookAuthors.innerHTML = `<b>By:</b> ${item.volumeInfo.authors.join(", ")}`; // returns a list of authors

                // if Google Books has a cover image, display image, else display default image
                const bookCover = document.createElement("img");
                const imgUrl = `https://books.google.com/books/content?id=${bookId}&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api`; // this is a direct path to book cover thumbnail image
                if (imgUrl) {
                    bookCover.src = imgUrl;
                } else {
                    bookCover.src = coverNotFoundImg; // coverNotFoundImg declaration located in book_search template
                }

                // add each book's data to a div and each div to another div
                const bookDiv = document.createElement("div");
                bookDiv.appendChild(bookCover);
                bookDiv.appendChild(bookTitle);
                bookDiv.appendChild(bookAuthors);
                contentWrapper.appendChild(bookDiv);
            }
        // displays error message if request is bad
        } else { 
            const errMsg = document.createElement("h4");
            errMsg.innerHTML = "Something went wrong, try again later.";
            contentWrapper.appendChild(errMsg);
        }
    }

    request.open("GET", searchPath + searchText);
    request.send();
});