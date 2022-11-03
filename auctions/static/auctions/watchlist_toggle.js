if(document.querySelector('#watchlist_count') != null) {
    //grabs watchlist count
    fetch("/api_watchlist_count", {method: "GET"})
        .then((response => response.json()))
        .then(data => {
            document.querySelector('#watchlist_count').innerHTML = "Watchlist [" + data['watchlist_count'] + "]"
        })
        .catch(error => {
            console.log('**Error**', error)
        })

    document.addEventListener('DOMContentLoaded', () => {
        //waits for a favorite button to be pressed
        let listing_id = 0;
        document.querySelectorAll('#favorite_button').forEach(button => {
            button.onclick = function () {
                //set a data-id field for each button to then grab the listing_id
                listing_id = button.dataset.id;
                console.log(listing_id);

                //allows each favorite button to be individually addressable
                fetch(`/api_watchlist_toggle/${listing_id}`, {method: "POST"})
                    .then(response => response.json())
                    .then(data => {
                        //thank you to https://abcdinamo.com/news/using-variable-fonts-on-the-web
                        //isInWatchlist is a boolean value, as the name suggests, it is true if the listing is in favorites, and false if not.
                        document.querySelector(`#heart${listing_id}`).style.fontVariationSettings = "\"FILL\" " + data['isInWatchlist'];

                        //format for showing count on watchlist
                        document.querySelector('#watchlist_count').innerHTML = "Watchlist [" + data['watchlist_count'] + "]";

                    })
                    .catch(error => {
                        console.log('**Error**', error)
                    })
            }
        })

    })
};