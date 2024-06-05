$(document).ready(function () {
    // Get the first friend drawer with the 'active' class
    var firstFriendDrawer = $('.friend-drawer.active').first();

    // Trigger a click event on the first friend drawer
    firstFriendDrawer.click();
});
function loadMessages(receiverId) {
    document.getElementById('receiverIdInput').value = receiverId;
    
    // Fetch receiver details to get the name
    $.ajax({
        url: 'http://127.0.0.1:8000/chat/fetch_user_details/',
        method: 'GET',
        data: { user_id: receiverId },
        success: function (userResponse) {
            var receiverName = userResponse.name; // Assuming the response contains the name of the receiver
            var userImage = userResponse.user_image;
            console.log(userResponse);
            // Fetch messages for the selected receiver using AJAX
            $.ajax({
                url: 'http://127.0.0.1:8000/chat/fetch_messages/',
                method: 'GET',
                data: { receiver_id: receiverId },
                success: function (response) {
                    var chatPanelHTML = ''; // Initialize an empty string to store the HTML content
                    var senderId = response.senderId;
                    allMessages = response.messages;
                    $('#chatpartner_name').text(receiverName);
                    $('#chatpartner-profile-image').attr('src', userImage);
                 
                    // Iterate through each message and create a new row in the table
                    for (var i=0; i < allMessages.length; i++) { 
                        
                        var bubbleClass = (allMessages[i].sender === senderId) ? 'chat-bubble chat-bubble--right' : 'chat-bubble chat-bubble--left';
                        var bubbleHTML = '<div class="row no-gutters">' +
                                '<div class="col-md-5' + ((allMessages[i].sender === senderId) ? ' offset-md-7' : '') + '">' +
                                '<div class="' + bubbleClass + '">' +
                                allMessages[i].message + // Assuming message contains the actual message content
                                '</div>' +
                                '</div>' +
                                '</div>';
        
                            // Append the bubble HTML to the chat panel HTML
                            chatPanelHTML += bubbleHTML;
                    };
                    $('.chat-panel').html(chatPanelHTML); // Add the complete chat panel HTML to the page
                    scrollChatToBottom();
                },
                error: function (xhr, status, error) {
                    console.error(error);
                }
            });
        },
        error: function (xhr, status, error) {
            console.error(error);
        }
    });
}
document.getElementById("submitMessage").addEventListener("click", function () {
    var receiverId = document.getElementById('receiverIdInput').value;
    console.log(receiverId);

    // Check if receiver ID is provided
    if (receiverId) {
        // Submit the form
        document.getElementById('messageForm').submit();
    } else {
        // If receiver ID is not provided, show an error or handle accordingly
        console.error('Receiver ID is not provided.');
        // You can show an alert or any other error handling mechanism here
    }
});
function refreshPage() {
    location.reload();
}
function scrollChatToBottom() {
    var chatPanel = document.getElementById('chat-panel');
    chatPanel.scrollTop = chatPanel.scrollHeight;
}