// (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>
//
// This file is part of Ansible
//
// Ansible is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Ansible is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Ansible.  If not, see <http://www.gnu.org/licenses/>.


$(document).ready(function() {
    prepare_login()
    set_nav_callbacks()
})

function listerController($scope) {
    $scope.items = [
        { name: "alpha", edit_linkage: '1234',  delete_linkage: '12345' },
        { name: "beta",  edit_linkage: '12346', delete_linkage: '12347' }
    ];
}

function api_call(url, method, on_success) {
    username = localStorage.getItem('loginUser')
    password = localStorage.getItem('loginPassword')
    up = username + ":" + password
    up = Base64.encode(up)

    $.ajax({
        url : url,
        crossDomain: true,
        async: false,
        dataType : 'json',
        type: method,
        beforeSend : function(xhr) {
            xhr.setRequestHeader("Authorization", "Basic " + up);
            return true
        },
        error : function(xhr, ajaxOptions, thrownError) {
            alert("failed")
        },
        success : function(data, status, xhr) {
            on_success(data)
        }
    });
}

function login_setup() {
    loginUser = localStorage.getItem("loginUser");
    if ((loginUser == '') || (loginUser == null)) {
        loginUser = 'admin'
    }
    $('#loginUser').val(loginUser)
}

function login_submit() {
    loginUser     = $('#loginUser').val()
    loginPassword = $('#loginPassword').val()
    localStorage.setItem("loginUser", loginUser)
    localStorage.setItem("loginPassword", loginPassword)

    // TODO: test API hit and dismiss only if successful
    api_call('/api/', 'GET', function(data) {
        // alert(data)
        $('#loginModal').modal('hide')
    })
}

function login_clear() {
     localStorage.setItem('loginUser','')
     localStorage.setItem('loginPassword', '')
     $('#loginUser').val('')
     $('#loginPassword').val('')
}

function set_on_enter(id, cb) {
    $(id).keypress(function(event) {
        if ( event.which == 13 ) {
            event.preventDefault();
            cb()
        }
    })
}

function set_nav_callbacks() {

    $('#groupsNav').click(function() {
        load_groups();
    })
    $('#usersNav').click(function() {
        load_users();
    })
    $('#hostsNav').click(function() {
        load_hosts();
    })
    $('#logoutNav').click(function() {
        logout();
    })
}

function load_groups() {
    alert('groups');
}

function load_user() {
    alert('users');
}

function load_hosts() {
    alert('hosts');
}

function logout() {
    login_clear();
    $("#loginModal").modal(keyboard=false);
}

function prepare_login() {
    $("#loginModal").modal(keyboard=false)
    login_setup()
    set_on_enter("#loginUser", login_submit)
    set_on_enter("#loginPassword", login_submit)
    $("#loginSubmit").click(login_submit)
    $("#loginClear").click(login_clear)
}


