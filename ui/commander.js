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
})

function login_setup() {
    loginUser = localStorage.getItem("loginUser");
    if ((loginUser == '') || (loginUser == null)) {
        loginUser = 'admin'
    }
    loginEndpoint = localStorage.getItem("loginEndpoint");
    if ((loginEndpoint == '') || (loginEndpoint == null)) {
        loginEndpoint = 'http://commander:5000/';
    }
    $('#loginUser').val(loginUser)
    $('#loginEndpoint').val(loginEndpoint)
}

function login_submit() {
    loginUser     = $('#loginUser').val()
    loginPassword = $('#loginPassword').val()
    loginEndpoint = $('#loginEndpoint').val()
    localStorage.setItem("loginUser", loginUser)
    localStorage.setItem("loginPassword", loginPassword)
    localStorage.setItem("loginEndpoint", loginEndpoint)
    window.alert("Handler for .click() called.");
}

function login_clear() {
     localStorage.setItem('loginUser','')
     localStorage.setItem('loginPassword', '')
     $('#loginUser').val('')
     $('#loginPassword').val('')
}

function prepare_login() {
    login_setup()
    $("#loginButton").click(login_submit)
    $("#loginClear").click(login_clear)
}


