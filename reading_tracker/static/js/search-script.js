// upon search event, request search results from Google Books API
const searchForm = document.getElementById("search-form");
searchForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const request = new XMLHttpRequest();
    request.onload = () => {
        const contentWrapper = document.getElementById("content");
        contentWrapper.innerHTML = "";
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
                bookAuthors.innerHTML = `<strong>By:</strong> ${item.volumeInfo.authors.join(", ")}`; // returns a list of authors

                // if Google Books has a cover image, display image, else display default image
                const bookCover = document.createElement("img");
                const imgUrl = `https://books.google.com/books/content?id=${bookId}&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api`; // this is a direct path to book cover thumbnail image
                if (imgUrl) {
                    bookCover.src = imgUrl;
                } else {
                    bookCover.src = coverNotFoundImg; // coverNotFoundImg declaration located in book_search template
                }

                // set image height and allow width to maintain aspect ratio, using new width to calculate padding width to keep a square border
                bookCover.style.height = "80px";
                bookCover.style.width = "auto";
                bookCover.onload = (event) => {
                    coverDiv.style.padding = `0 ${45-(bookCover.width/2)}px`;
                }

                // add each book's data to a div and each div to another div
                const bookSearchDiv = document.createElement("div");
                bookSearchDiv.setAttribute("class", "book-search-div");

                const coverDiv = document.createElement("div");
                coverDiv.setAttribute("class", "cover-div");
                coverDiv.appendChild(bookCover);
                bookSearchDiv.appendChild(coverDiv);

                const infoDiv = document.createElement("div");
                infoDiv.setAttribute("class", "info-div");
                infoDiv.appendChild(bookTitle);
                infoDiv.appendChild(bookAuthors);
                bookSearchDiv.appendChild(infoDiv);

                const anchorWrapper = document.createElement("a");
                anchorWrapper.setAttribute("href", "");
                anchorWrapper.appendChild(bookSearchDiv);

                contentWrapper.appendChild(anchorWrapper);
            }
        // displays error message if request is bad
        } else { 
            const errMsg = document.createElement("h4");
            errMsg.innerHTML = "Something went wrong, try again later.";
            contentWrapper.appendChild(errMsg);
        }
    }

    // get form data
    const formData = new FormData(searchForm);
    const searchText = encodeURIComponent(formData.get("text-area"));

    request.open("GET", "https://www.googleapis.com/books/v1/volumes?q=" + searchText);
    request.send();
});