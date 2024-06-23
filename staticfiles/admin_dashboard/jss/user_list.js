function open_wallet_add_modal(element){
    var user_id = element.getAttribute('user_id');
    var email = element.getAttribute('email');
    var myModal = new bootstrap.Modal(document.getElementById('wallet_balance_add_modal'));
    var form = document.getElementById('wallet_balance_add_modal_form');
    form.elements['user_id'].value = user_id;
    form.elements['email'].value = email;
    myModal.show(); //to open a modal
}