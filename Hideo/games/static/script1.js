jQuery("document").ready(function(){
    jQuery("#like1").on('click', function(){
        console.log("hello");
            var href = document.getElementById('like1').name;
            jQuery.ajax({
                type: "GET",

                url: "/games/addliketocomment/ajax1/",

                data:{ "addlike" : href,},

                dataType: "text",

                catch: false,

                success: function(data){
                    jQuery("#count_likes1").html(data);
                }
            });
    });
});