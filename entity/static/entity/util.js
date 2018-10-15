/**
 * Common util functions used by the entity app
 */
'use strict';


var entity = (function() {

    function init() {
        $(document).ready(function() {

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
    function get_members(appendto, template) {

        /* When the server returns a list of members... */
        function process_members(data) {

            if(data.members.length !== 0) {

                var $ul = $("<ul class='list-group list-group-flush'></ul>");

                for(var i in data.members) {
                    var $template = $($(template).html());
                    $template.find('.member_avatar').attr('src', data.members[i]['avatar']);
                    $template.find('.member_username').html(data.members[i]['username']);
                    $template.find('.member_username').attr('href', "/user/" + data.members[i]['username'])
                    $template.find('.member_role').html(upper(data.members[i]['role']));

                    if(data.members[i]['role'] != "owner") {
                        $template.find('.delete_button_editor').html('<a href="#" class="pull-right">Remove</a>');
                    }
                    $ul.append($template);
                }
                $(appendto).html($ul);

            }
            else {
                $(appendto).html("There are no members to show");
            }
        }
        // Send an AJAX request
        $.ajax({
            url: './members',
            success: process_members
        });
    };

    // These functions are `public`
    return {
        init: init(),
        get_members: get_members,
    };
}());
