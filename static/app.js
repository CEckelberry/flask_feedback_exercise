
current_url = document.URL
console.log(current_url)

$("#delete_btn").click(async function(event) {
    let feed_id = $("#delete_btn").data("id");
    console.log(feed_id);
    const res = await axios.delete(`https://localhost:5000/feedback/${feed_id}/delete`);
    window.location.reload();
});


$("#user_delete_btn").click(async function(event) {
    //event.preventDefault()
    let user_id = $("#user_delete_btn").data("id");
    console.log(user_id);
    const res = await axios.delete(`https://localhost:5000/users/${user_id}/delete`);
    goToRegister();
    
});

function goToRegister() {
    console.log("You made it to goToRegister!")
    window.location.assign("https://localhost:5000/register");
}