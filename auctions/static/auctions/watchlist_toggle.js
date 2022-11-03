
fetch("/api_watchlist_count",{method:"GET"})
    .then((response => response.json()))
    .then(data =>{
        document.querySelector('#watchlist_count').innerHTML = "Watchlist [" + data['watchlist_count'] + "]"
    })
    .catch(error =>{
        console.log('**Error**',error)
    })

 document.addEventListener('DOMContentLoaded', ()=> {

        let listing_id = 0;
        document.querySelectorAll('#favorite_button').forEach(button => {
            button.onclick = function () {
                listing_id = button.dataset.id;
                console.log(listing_id);
                fetch(`/api_watchlist_toggle/${listing_id}`,{method:"POST"})
                    .then(response => response.json())
                    .then(data =>{
                    //thank you to https://abcdinamo.com/news/using-variable-fonts-on-the-web
                    document.querySelector(`#heart${listing_id}`).style.fontVariationSettings = "\"FILL\" " + data['isInWatchlist'];
                    document.querySelector('#watchlist_count').innerHTML = "Watchlist [" + data['watchlist_count'] + "]"
                })
                    .catch(error =>{
                    console.log('**Error**',error)
                })
            }
        })

});