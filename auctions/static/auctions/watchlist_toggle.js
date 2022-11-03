document.addEventListener('DOMContentLoaded', function() {
    //let url = window.location.href;
    //let listing_id = url.charAt(url.length-2);// to get listing_id
    if(document.querySelector('#ident') != undefined) {
        let listing_id = document.querySelector('#ident').innerHTML;
        console.log(listing_id);
    }
    else{
        return true;
    }
    if(document.querySelector('#watchlist_remove') != null){
    document.querySelector('#watchlist_remove').onsubmit = ()=> {
        fetch(`/api_watchlist_toggle/${listing_id}`,{method: "POST",data: 'csrfmiddlewaretoken={{csrf_token}}'})
            .then(response => response.json())
            .then(data =>{
                //thank you to https://abcdinamo.com/news/using-variable-fonts-on-the-web
                document.querySelector('.material-symbols-outlined').style.fontVariationSettings = "\"FILL\" " + 0;
            })
            .catch(error =>{
                console.log('**Error**',error)
            })
    }}
    if(document.querySelector('#watchlist_add') != null){
    document.querySelector('#watchlist_add').onsubmit = ()=> {
        fetch(`/api_watchlist_toggle/${listing_id}`,{method: "POST"})
            .then(response => response.json())
            .then(data =>{
                //thank you to https://abcdinamo.com/news/using-variable-fonts-on-the-web
                document.querySelector('.material-symbols-outlined').style.fontVariationSettings = "\"FILL\" " + 1
            })
            .catch(error =>{
                console.log('**Error**',error)
            });
    }}
});