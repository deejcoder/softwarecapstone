/**
 * Common util functions used by the entity app
 */
'use strict';


var entity = (function() {

    function init() {
        $(document).ready(function() {});
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

                var $ul = $("<ul style='list-style:none;'></ul>");
                $ul.append('<h6>Owner(s):</h6>')
                for(var i in data.members) {
                    if (data.members[i]['role'] == 'owner') {
                        var $template = $($(template).html());
                        $template.find('.member_username').html(data.members[i]['username']);
                        $template.find('.member_avatar').attr('src', data.members[i]['avatar']);
                        $ul.append($template);
                    }
                }
                $ul.append('<br/><h6>Editors(s):</h6>')
                for(var i in data.members) {
                    if (data.members[i]['role'] == 'editor') {
                        var $template = $($(template).html());
                        $template.find('.member_username').html(data.members[i]['username']);
                        $template.find('.member_avatar').attr('src', data.members[i]['avatar']);
                        $template.find('.delete_button_owner').html('<button class="btn pull-right" type="submit">Delete</button>');
                        $ul.append($template);
                    }
                }
                $ul.append('<br/><h6>Member(s):</h6>')
                for(var i in data.members) {
                    if (data.members[i]['role'] == 'member') {
                        var $template = $($(template).html());
                        $template.find('.member_username').html(data.members[i]['username']);
                        $template.find('.member_avatar').attr('src', data.members[i]['avatar']);
                        $template.find('.delete_button_editor').html('<button class="btn pull-right" type="submit">Delete</button>');
                        $ul.append($template);
                    }
                }
                $ul.append('<button class="btn" type="submit">Add user</button>');
                $(appendto).html($ul);

            }
            else {
                $(appendto).html("There are no members to show");
                $(appendto).append('<br/><button type="submit">Add user</button>');
            }
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
