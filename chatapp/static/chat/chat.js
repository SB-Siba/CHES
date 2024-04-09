$(document).ready(function() {
    // Function to handle click event on sender or recipient's name
    $(".sender-name, .recipient-name").click(function(event) {
        event.preventDefault();  // Prevent default link behavior

        // Remove active class from all links
        $(".recipient-name, .sender-name").removeClass("active");
        $(this).addClass("active"); // Add active class to the clicked link
        
        // Apply CSS styles for the active class
        $(this).css({
            'font-weight': 'bold',
            'color':'green', 
        });

        var recipientFullName = $(this).data("recipient") || $(this).data("sender");
        $("#recipientFullName").val(recipientFullName);
        var fullName = $(this).data("sender") || $(this).data("recipient");   // Get the sender's or recipient's name

        // Determine the URL based on the clicked element's class
        var url = $(this).hasClass('sender-name') ? "http://127.0.0.1:8000/chat/conversation/" : "http://127.0.0.1:8000/chat/conversation_reciver/";
        var $this = $(this);
        console.log(url)
        // AJAX request to fetch messages
        $.ajax({
            url: url + fullName + "/",  // URL to fetch messages
            method: "GET",
            success: function(data) {
                try {
                    // Attempt to append the fetched messages to the messages container
                    var messages = data.messages;
                    var sender = data.sender;
                    console.log(messages)

                    $(".messages-container").empty();

                    
                        $.ajax({
                            url: 'http://127.0.0.1:8000/chat/user-info',  // URL of your Django API endpoint
                            method: 'GET',
                            success: function(response) {
                                for (var i = 0; i < messages.length; i++) {
                                    var message = messages[i];
                                    var timestamp = new Date(message.timestamp);
                                    var timeString = timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                                    if  (message.sender == response.email) {
                                        var messageHTML = "<div>";
                                        messageHTML += "<div class='d-flex justify-content-end"+ " mb-1'>";
                                        messageHTML += "<div>"
                                        messageHTML += message.content + "<br>";
                                        messageHTML += timeString + "<br>";
                                        messageHTML += "</div>";
                                        messageHTML += "<img src='" + response.user_image + "' class='rounded-circle' style='width: 30px; height: 30px;' alt='avatar'>";
                                        messageHTML += "</div>";
                                        messageHTML += "<br>";
                                        // Add more fields as needed
                                        messageHTML += "</div>";
                                        // Append the message HTML to the messages container
                                        $(".messages-container").append(messageHTML);
                                    } else {
                                        var messageHTML = "<div>";
                                        messageHTML += "<div class='d-flex justify-content-start"+ " mb-1'>";
                                        messageHTML += "<img src='" + ($(this).hasClass('sender-name') ? sender.user_image_url : (message.sender_image ? message.sender_image : 'https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-2.webp')) + "' class='rounded-circle' style='width: 30px; height: 30px;' alt='avatar'>";
                                        messageHTML += "<div>"
                                        messageHTML += message.content + "<br>";
                                        messageHTML += timeString + "<br>";
                                        messageHTML += "</div>";
                                        messageHTML += "</div>";
                                        messageHTML += "<br>";
                                        // Add more fields as needed
                                        messageHTML += "</div>";
                                        // Append the message HTML to the messages container
                                        $(".messages-container").append(messageHTML);
                                    }
                                }
                                // You can now access user information in the 'response' object
                            },
                            error: function(xhr, status, error) {
                                // Handle any errors
                                console.error('Error fetching user info:', error);
                            }
                        });                   
                } catch (error) {
                    console.error("Error appending messages:", error);
                }
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);  // Log any errors to the console
            }
        });
    });

    $(".msg_Form").submit(function(event) {
        event.preventDefault();  // Prevent default form submission

        // Extract recipient full name from the hidden input field
        var recipientFullName = $("#recipientFullName").val();
    
        console.log(recipientFullName)

        // Extract message content from the form
        var content = $(this).find("textarea[name='content']").val();
        console.log(content)

        // AJAX POST request to send message
        $.ajax({
            url: "http://127.0.0.1:8000/chat/compose/"+recipientFullName+"/",  // Replace "your_backend_url" with your actual backend URL
            method: "POST",
            data: {
                recipient_full_name: recipientFullName,
                content: content
            },
            success: function(response) {
                // Handle success response
                window.location.reload();
            },
            error: function(xhr, status, error) {
                // Handle error response
                console.error(error);
            }
        });
    });

    
    $(".uuuser:first").trigger("click");
    var $firstRecipient = $(".recipient-name:first");

    
});