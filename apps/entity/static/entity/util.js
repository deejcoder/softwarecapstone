/**
 * Common util functions used by the entity app
 */
'use strict';


var entity = (function() {

    var global = {}
    function init() {
        $(document).ready(function() {
            global.config = {
                appendto: null,
                template: null,
                url: null,
            }
        });
    }

    /**
     * Takes a word and capitalizes the first letter
     * @param {string} word 
     */
    function upper(word) {
        return word.charAt(0).toUpperCase() + word.slice(1);
    }

    /**
     * Gets all members assiocated with an entity and
     * attaches a list of members to the given HTML element
     * NOTE a template must define .member_username & .member_avatar classes
     * @param {string} appendto The element to attach the member list to
     * @param {string} template The template to use for each member
     */
    function get_members(appendto, template, url) {
        global.config.appendto = appendto;
        global.config.template = template;
        global.config.url = url;

        /* When the server returns a list of members... */
        function process_members(data) {

            if(data.members.length !== 0) {

                var $ul = $("<ul class='list-group list-group-flush'></ul>");

                for(var i in data.members) {
                    var $template = $($(template).html());
                    $template.find('.member_avatar').attr('src', data.members[i]['avatar']);
                    $template.find('.member_username').html(data.members[i]['username']);

                    if(data.members[i]['is_consultant'] == true) {
                        $template.find('.member_username').attr('href', "/user/" + data.members[i]['username'])
                    }
                    else {
                        $template.find('.member_username').attr('href', "#")
                    }

                    $template.find('.member_role').html(upper(data.members[i]['role']));
                    $template.find('.delete_button_editor').html('<a href="#" onclick="entity.remove_member(this,\'' + data.members[i]['username'] + '\');" class="pull-right no-decoration text-danger">Remove</a>');

                    $ul.append($template);
                }

                $(appendto).html($ul);

            }
            else {
                $(appendto).html("<p class='text-green'>There are no members to show</p>");
            }
        }
        // Send an AJAX request
        $.ajax({
            url: url,
            success: process_members
        });
    };

    /**
     * Removes a member from an entity
     * @param {*} elem the element that was clicked
     * @param {string} username the username of the user to remove
     */
    function remove_member(elem, username) {

        function remove_response(data) {
            if(data['error'] === "200") {
                $(elem).parents('li').remove()
            }
        }
        $.ajax({
            url: 'members/remove/' + username,
            success: remove_response
        });
    }

    /**
     * Adds a new member based on what is contained in the text field.
     * Then refreshes the members list.
     * @param {string} username_text_field the text field containing a username
     */
    function add_member(username_text_field) {

        function add_response(data) {
            if(data['error'] == "200") {
                get_members(global.config.appendto, global.config.template, global.config.url);
                $(username_text_field).val("");
            }
        }

        var username = $(username_text_field).val();
        $.ajax({
            url: 'members/add/' + username,
            success: add_response,
        });
    }

    // These functions are `public`
    return {
        init: init(),
        get_members: get_members,
        remove_member: remove_member,
        add_member: add_member,
    };
}());
