
current_url = document.URL
console.log(current_url)

$("#feedback").on("click", "i", async function(event) {
    console.log(event.target);
    
    let feed_id = $("#delete_btn").data("id");
    console.log(feed_id);
    const res = await axios.delete(`/feedback/${feed_id}/delete`);
    location.reload();
});


$("#user_delete_btn").click(async function(event) {
    //event.preventDefault()
    let user_id = $("#user_delete_btn").data("id");
    console.log(user_id);
    const res = await axios.delete(`/users/${user_id}/delete`);
    goToRegister();
    
});

function goToRegister() {
    console.log("You made it to goToRegister!")
    window.location.assign("/register");
}