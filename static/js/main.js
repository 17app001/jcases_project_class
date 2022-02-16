window.onpageshow = function (event) {
    console.log(event);
    if (event.persisted) {
        window.location.reload()
    }
};